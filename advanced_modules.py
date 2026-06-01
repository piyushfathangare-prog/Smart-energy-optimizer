"""
Advanced Modules:
1. Weather-Integrated Forecasting
2. Appliance Degradation Alert
3. Battery/ESS + Time-of-Use Optimization
4. NILM Virtual Smart Meter
5. Eco-Score Algorithm
6. PDF Report Generator
"""

import numpy as np
import requests
from datetime import datetime, timedelta


# ─────────────────────────────────────────────
# 1. WEATHER FORECASTING
# ─────────────────────────────────────────────

CITY_COORDS = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Bangalore": (12.9716, 77.5946),
    "Pune": (18.5204, 73.8567),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Ahmedabad": (23.0225, 72.5714),
}

# Simulated monthly avg temps (°C) for Mumbai if API unavailable
MUMBAI_MONTHLY_TEMPS = [24, 25, 28, 31, 33, 31, 29, 29, 29, 30, 28, 25]

def get_weather_forecast(city="Mumbai", api_key=None):
    """Fetch weather or fall back to simulated data."""
    month = datetime.now().month
    next_month = (month % 12) + 1

    if api_key:
        try:
            lat, lon = CITY_COORDS.get(city, (19.0760, 72.8777))
            url = (
                f"https://api.openweathermap.org/data/2.5/forecast"
                f"?lat={lat}&lon={lon}&appid={api_key}&units=metric&cnt=40"
            )
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                temps = [item["main"]["temp"] for item in data["list"]]
                avg_temp = np.mean(temps)
                max_temp = max(temps)
                return {
                    "source": "live",
                    "city": city,
                    "avg_temp": avg_temp,
                    "max_temp": max_temp,
                    "next_month_temp": avg_temp,
                }
        except Exception:
            pass

    # Simulated fallback
    current_temp = MUMBAI_MONTHLY_TEMPS[month - 1]
    next_temp = MUMBAI_MONTHLY_TEMPS[next_month - 1]
    return {
        "source": "simulated",
        "city": city,
        "avg_temp": current_temp,
        "max_temp": current_temp + 4,
        "next_month_temp": next_temp,
    }


def predict_bill_with_weather(monthly_kwh, weather_data, appliance_data):
    """Predict next month's bill using weather + regression logic."""
    base_kwh = monthly_kwh
    temp_diff = weather_data["next_month_temp"] - weather_data["avg_temp"]

    # AC sensitivity: each +1°C → ~3% more AC usage
    ac_keys = [k for k in appliance_data if "AC" in k.upper() or "AIR" in k.upper()]
    ac_kwh = sum(
        appliance_data[k]["power_watts"] * appliance_data[k]["hours_per_day"] / 1000 * 30
        for k in ac_keys
    )
    ac_adjustment = ac_kwh * (temp_diff * 0.03)

    predicted_kwh = base_kwh + ac_adjustment
    confidence = 88 if weather_data["source"] == "live" else 75

    from smart_ai_app import calculate_slab_based_bill
    bill = calculate_slab_based_bill(predicted_kwh)

    return {
        "predicted_kwh": predicted_kwh,
        "predicted_bill": bill["total_bill"],
        "temp_diff": temp_diff,
        "ac_adjustment_kwh": ac_adjustment,
        "confidence": confidence,
        "weather_source": weather_data["source"],
    }


# ─────────────────────────────────────────────
# 2. APPLIANCE DEGRADATION ALERT
# ─────────────────────────────────────────────

# Expected wattage ranges per appliance type
EXPECTED_WATTAGE = {
    "AC": {"1_ton": (900, 1100), "1.5_ton": (1300, 1600), "2_ton": (1700, 2100)},
    "REFRIGERATOR": {"standard": (80, 150)},
    "WASHING MACHINE": {"standard": (400, 600)},
    "WATER HEATER": {"standard": (1500, 2200)},
    "MICROWAVE": {"standard": (700, 1200)},
    "TV": {"standard": (50, 200)},
}


def check_appliance_degradation(appliance_data):
    """Flag appliances drawing more power than expected."""
    alerts = []
    for name, data in appliance_data.items():
        power = data["power_watts"]
        name_upper = name.upper()

        expected = None
        if "AC" in name_upper or "AIR CONDITIONER" in name_upper:
            if "2 TON" in name_upper or "2TON" in name_upper:
                expected = EXPECTED_WATTAGE["AC"]["2_ton"]
            elif "1.5" in name_upper:
                expected = EXPECTED_WATTAGE["AC"]["1.5_ton"]
            else:
                expected = EXPECTED_WATTAGE["AC"]["1_ton"]
        elif "REFRIGERATOR" in name_upper or "FRIDGE" in name_upper:
            expected = EXPECTED_WATTAGE["REFRIGERATOR"]["standard"]
        elif "WASHING" in name_upper:
            expected = EXPECTED_WATTAGE["WASHING MACHINE"]["standard"]
        elif "HEATER" in name_upper or "GEYSER" in name_upper:
            expected = EXPECTED_WATTAGE["WATER HEATER"]["standard"]

        if expected:
            low, high = expected
            if power > high * 1.15:
                excess_pct = ((power - high) / high) * 100
                monthly_extra_kwh = (power - high) * data["hours_per_day"] * 30 / 1000
                monthly_savings = monthly_extra_kwh * 12  # ₹12/kWh avg
                alerts.append({
                    "appliance": name,
                    "current_power": power,
                    "expected_max": high,
                    "excess_pct": excess_pct,
                    "monthly_extra_cost": monthly_savings,
                    "message": (
                        f"Your {name} power draw is {excess_pct:.0f}% higher than normal. "
                        f"It may require servicing."
                    ),
                    "savings_message": f"Servicing could save ₹{monthly_savings:.0f}/month",
                })
    return alerts


# ─────────────────────────────────────────────
# 3. BATTERY / ESS + TIME-OF-USE OPTIMIZATION
# ─────────────────────────────────────────────

# Maharashtra ToU rates (₹/kWh)
TOU_RATES = {
    "peak":     {"hours": list(range(18, 23)), "rate": 17.68},   # 6 PM – 11 PM
    "standard": {"hours": list(range(7, 18)),  "rate": 11.10},   # 7 AM – 6 PM
    "offpeak":  {"hours": list(range(23, 24)) + list(range(0, 7)), "rate": 4.28},  # 11 PM – 7 AM
}


def optimize_battery_schedule(daily_kwh, battery_capacity_kwh=5.0, solar_kwh=0.0):
    """
    Recommend when to charge battery from grid vs run on battery.
    Returns hourly schedule and financial savings.
    """
    hourly_load = []
    for h in range(24):
        if 6 <= h < 9:    # Morning
            hourly_load.append(daily_kwh * 0.08)
        elif 9 <= h < 18:  # Daytime
            hourly_load.append(daily_kwh * 0.04)
        elif 18 <= h < 23: # Evening peak
            hourly_load.append(daily_kwh * 0.10)
        else:              # Night
            hourly_load.append(daily_kwh * 0.02)

    schedule = []
    battery_soc = battery_capacity_kwh * 0.2  # Start at 20%
    cost_without_battery = 0
    cost_with_battery = 0

    for h in range(24):
        load = hourly_load[h]
        solar_gen = 0

        # Solar generation 8 AM – 5 PM
        if 8 <= h < 17:
            solar_gen = solar_kwh / 9

        # Determine rate
        if h in TOU_RATES["peak"]["hours"]:
            rate = TOU_RATES["peak"]["rate"]
            period = "peak"
        elif h in TOU_RATES["offpeak"]["hours"]:
            rate = TOU_RATES["offpeak"]["rate"]
            period = "offpeak"
        else:
            rate = TOU_RATES["standard"]["rate"]
            period = "standard"

        cost_without_battery += load * rate

        # Battery logic
        net_load = load - solar_gen
        action = "grid"

        if period == "offpeak" and battery_soc < battery_capacity_kwh * 0.9:
            # Charge battery during cheap hours
            charge = min(battery_capacity_kwh * 0.2, battery_capacity_kwh - battery_soc)
            battery_soc += charge
            cost_with_battery += (net_load + charge) * rate
            action = "charging"
        elif period == "peak" and battery_soc > battery_capacity_kwh * 0.2:
            # Discharge during expensive hours
            discharge = min(net_load, battery_soc - battery_capacity_kwh * 0.1)
            battery_soc -= discharge
            grid_needed = max(0, net_load - discharge)
            cost_with_battery += grid_needed * rate
            action = "discharging"
        else:
            cost_with_battery += max(0, net_load) * rate

        schedule.append({
            "hour": h,
            "load_kwh": round(load, 3),
            "solar_kwh": round(solar_gen, 3),
            "battery_soc": round(battery_soc, 2),
            "action": action,
            "rate": rate,
            "period": period,
        })

    monthly_savings = (cost_without_battery - cost_with_battery) * 30
    return {
        "schedule": schedule,
        "daily_cost_without": cost_without_battery,
        "daily_cost_with": cost_with_battery,
        "daily_savings": cost_without_battery - cost_with_battery,
        "monthly_savings": monthly_savings,
        "yearly_savings": monthly_savings * 12,
    }


# ─────────────────────────────────────────────
# 4. NILM – VIRTUAL SMART METER
# ─────────────────────────────────────────────

APPLIANCE_SIGNATURES = [
    {"name": "1.5-Ton AC",        "min": 1300, "max": 1700, "prob": 0.7},
    {"name": "Water Heater/Geyser","min": 1500, "max": 2200, "prob": 0.5},
    {"name": "Washing Machine",    "min": 400,  "max": 700,  "prob": 0.4},
    {"name": "Microwave",          "min": 700,  "max": 1200, "prob": 0.3},
    {"name": "Refrigerator",       "min": 80,   "max": 200,  "prob": 0.95},
    {"name": "LED TV",             "min": 50,   "max": 150,  "prob": 0.6},
    {"name": "Ceiling Fan (×4)",   "min": 200,  "max": 320,  "prob": 0.8},
    {"name": "LED Lights",         "min": 50,   "max": 200,  "prob": 0.9},
    {"name": "Laptop/Computer",    "min": 50,   "max": 200,  "prob": 0.5},
    {"name": "Induction Cooktop",  "min": 1000, "max": 2000, "prob": 0.3},
]


def nilm_detect(total_watts):
    """Guess which appliances are running given total wattage."""
    detected = []
    remaining = total_watts

    # Sort by power descending for greedy matching
    sigs = sorted(APPLIANCE_SIGNATURES, key=lambda x: -x["max"])

    for sig in sigs:
        mid = (sig["min"] + sig["max"]) / 2
        if remaining >= sig["min"] * 0.8 and np.random.random() < sig["prob"]:
            detected.append({
                "name": sig["name"],
                "estimated_watts": int(mid),
                "confidence": int(sig["prob"] * 100),
            })
            remaining -= mid
            if remaining < 50:
                break

    # Unaccounted
    unaccounted = max(0, remaining)
    return {
        "total_input": total_watts,
        "detected": detected,
        "accounted_watts": int(total_watts - unaccounted),
        "unaccounted_watts": int(unaccounted),
    }


# ─────────────────────────────────────────────
# 5. ECO-SCORE (0 – 1000)
# ─────────────────────────────────────────────

def calculate_eco_score(monthly_kwh, city_avg_kwh, renewable_pct, appliance_efficiency_avg):
    """
    Eco-Score = weighted sum of:
      - Consumption vs city avg  (40%)
      - Renewable energy mix     (30%)
      - Appliance efficiency     (30%)
    """
    # Consumption score (lower = better)
    ratio = monthly_kwh / max(city_avg_kwh, 1)
    if ratio <= 0.5:
        consumption_score = 400
    elif ratio <= 0.75:
        consumption_score = 350
    elif ratio <= 1.0:
        consumption_score = 280
    elif ratio <= 1.25:
        consumption_score = 180
    else:
        consumption_score = 80

    # Renewable score
    renewable_score = int((renewable_pct / 100) * 300)

    # Efficiency score (appliance_efficiency_avg is 1-5 stars)
    efficiency_score = int((appliance_efficiency_avg / 5) * 300)

    total = consumption_score + renewable_score + efficiency_score

    if total >= 800:
        grade, label = "A+", "Platinum"
    elif total >= 650:
        grade, label = "A", "Gold"
    elif total >= 500:
        grade, label = "B", "Silver"
    elif total >= 350:
        grade, label = "C", "Bronze"
    else:
        grade, label = "D", "Needs Improvement"

    return {
        "score": total,
        "grade": grade,
        "label": label,
        "consumption_score": consumption_score,
        "renewable_score": renewable_score,
        "efficiency_score": efficiency_score,
    }


# ─────────────────────────────────────────────
# 6. PDF REPORT GENERATOR
# ─────────────────────────────────────────────

def generate_pdf_report(appliance_data, prediction, bill_details, carbon_impact, eco_score_data, city):
    """Generate a PDF energy audit report. Returns bytes."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        )
        from reportlab.lib.units import cm
        import io

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("title", parent=styles["Title"],
                                     fontSize=22, textColor=colors.HexColor("#10b981"),
                                     spaceAfter=6)
        h2_style = ParagraphStyle("h2", parent=styles["Heading2"],
                                  fontSize=14, textColor=colors.HexColor("#3b82f6"),
                                  spaceBefore=12, spaceAfter=4)
        body_style = styles["BodyText"]
        body_style.fontSize = 10

        story = []

        # Header
        story.append(Paragraph("⚡ Smart Energy Optimizer – Energy Audit Report", title_style))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')} | City: {city}",
            body_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#10b981")))
        story.append(Spacer(1, 0.4*cm))

        # Eco Score
        story.append(Paragraph("🏆 Eco-Score", h2_style))
        story.append(Paragraph(
            f"Score: <b>{eco_score_data['score']}/1000</b> | "
            f"Grade: <b>{eco_score_data['grade']}</b> | "
            f"Rating: <b>{eco_score_data['label']}</b>",
            body_style))
        story.append(Spacer(1, 0.3*cm))

        # Summary
        story.append(Paragraph("📊 Consumption Summary", h2_style))
        summary_data = [
            ["Metric", "Value"],
            ["Daily Consumption", f"{prediction['daily_total']:.2f} kWh"],
            ["Monthly Consumption", f"{prediction['monthly_total']:.2f} kWh"],
            ["Monthly Bill (Maharashtra Tariff)", f"₹{bill_details['total_bill']:.2f}"],
            ["Monthly CO₂ Emissions", f"{carbon_impact['monthly_co2']:.1f} kg"],
            ["Trees Required to Offset (yearly)", f"{carbon_impact['trees_equivalent']:.0f} trees"],
        ]
        t = Table(summary_data, colWidths=[9*cm, 7*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#10b981")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f0fdf4"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1fae5")),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.4*cm))

        # Appliance Breakdown
        story.append(Paragraph("🔌 Appliance Breakdown", h2_style))
        app_data = [["Appliance", "Power (W)", "Hours/Day", "Monthly kWh", "Monthly Cost (₹)"]]
        rate_avg = 12
        for app, data in appliance_data.items():
            daily_kwh = data["power_watts"] * data["hours_per_day"] / 1000
            monthly_kwh = daily_kwh * 30
            monthly_cost = monthly_kwh * rate_avg
            app_data.append([
                app[:30],
                str(data["power_watts"]),
                f"{data['hours_per_day']:.1f}",
                f"{monthly_kwh:.2f}",
                f"₹{monthly_cost:.0f}",
            ])
        t2 = Table(app_data, colWidths=[6*cm, 2.5*cm, 2.5*cm, 3*cm, 3*cm])
        t2.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3b82f6")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#eff6ff"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bfdbfe")),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("PADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(t2)
        story.append(Spacer(1, 0.4*cm))

        # Bill Breakdown
        story.append(Paragraph("💰 Bill Breakdown (Maharashtra Tariff)", h2_style))
        bill_data = [
            ["Component", "Amount"],
            ["Energy Charges", f"₹{bill_details['energy_charges']:.2f}"],
            ["Fixed Charges", f"₹{bill_details['fixed_charges']:.2f}"],
            ["Electricity Duty (16%)", f"₹{bill_details['electricity_duty']:.2f}"],
            ["Total Bill", f"₹{bill_details['total_bill']:.2f}"],
        ]
        t3 = Table(bill_data, colWidths=[9*cm, 7*cm])
        t3.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f59e0b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#fffbeb"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#fde68a")),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t3)
        story.append(Spacer(1, 0.4*cm))

        # Footer
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#10b981")))
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(
            "⚡ Smart Energy Optimizer | Professional Energy Intelligence Platform | "
            "This report is auto-generated and for informational purposes only.",
            ParagraphStyle("footer", parent=body_style, fontSize=8,
                           textColor=colors.HexColor("#94a3b8"))))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue(), None

    except ImportError:
        return None, "reportlab not installed. Run: pip install reportlab"
    except Exception as e:
        return None, str(e)
