"""
Advanced Energy Features
- Peak Load Alerts
- Energy Waste Detection
- City Comparison
- Gamification System
"""

import numpy as np
from datetime import datetime

class AdvancedEnergyFeatures:
    
    # City average consumption data (kWh/month)
    CITY_AVERAGES = {
        "Mumbai": 240,
        "Delhi": 280,
        "Bangalore": 220,
        "Pune": 210,
        "Hyderabad": 230,
        "Chennai": 250,
        "Kolkata": 200,
        "Ahmedabad": 260
    }
    
    def __init__(self):
        self.user_level = 1
        self.user_points = 0
        self.badges = []
    
    def check_peak_load_alert(self, daily_kwh, historical_avg=None):
        """Check if current usage is abnormally high"""
        if historical_avg is None:
            historical_avg = daily_kwh * 0.85  # Simulate 15% lower baseline
        
        increase_pct = ((daily_kwh - historical_avg) / historical_avg * 100) if historical_avg > 0 else 0
        
        if increase_pct > 20:
            return {
                "alert": True,
                "severity": "high",
                "message": f"⚠️ Peak Consumption Alert",
                "details": f"Your usage is {increase_pct:.0f}% higher than normal today.",
                "suggestions": [
                    "Turn off unused appliances",
                    "Reduce AC temperature by 2°C",
                    "Switch to LED bulbs",
                    "Unplug devices on standby"
                ],
                "increase_pct": increase_pct
            }
        elif increase_pct > 10:
            return {
                "alert": True,
                "severity": "medium",
                "message": f"⚡ Usage Increase Detected",
                "details": f"Your usage is {increase_pct:.0f}% higher than usual.",
                "suggestions": [
                    "Check for appliances left on",
                    "Optimize AC usage"
                ],
                "increase_pct": increase_pct
            }
        else:
            return {
                "alert": False,
                "message": "✅ Usage is normal",
                "increase_pct": increase_pct
            }
    
    def detect_energy_waste(self, appliance_data):
        """Detect appliances wasting electricity"""
        waste_detected = []
        
        for appliance, data in appliance_data.items():
            power_w = data['power_watts']
            hours = data['hours_per_day']
            daily_kwh = power_w * hours / 1000
            
            # Check for excessive usage
            if 'AC' in appliance.upper() or 'AIR CONDITIONER' in appliance.upper():
                if hours > 10:
                    monthly_waste = (hours - 8) * power_w * 30 / 1000
                    savings = monthly_waste * 12  # ₹12/kWh avg
                    waste_detected.append({
                        "appliance": appliance,
                        "issue": f"Running for {hours:.1f} hours daily",
                        "recommendation": "Reduce to 8 hours or use timer",
                        "potential_savings": savings,
                        "severity": "high"
                    })
            
            elif 'HEATER' in appliance.upper() or 'GEYSER' in appliance.upper():
                if hours > 3:
                    monthly_waste = (hours - 2) * power_w * 30 / 1000
                    savings = monthly_waste * 12
                    waste_detected.append({
                        "appliance": appliance,
                        "issue": f"Running for {hours:.1f} hours daily",
                        "recommendation": "Use timer, reduce to 2 hours",
                        "potential_savings": savings,
                        "severity": "medium"
                    })
            
            elif 'REFRIGERATOR' in appliance.upper() or 'FRIDGE' in appliance.upper():
                if power_w > 150:
                    savings = (power_w - 100) * 24 * 30 / 1000 * 12
                    waste_detected.append({
                        "appliance": appliance,
                        "issue": f"High power consumption ({power_w}W)",
                        "recommendation": "Replace with 5-Star rated model",
                        "potential_savings": savings,
                        "severity": "medium"
                    })
            
            # Check for old/inefficient appliances (high power)
            if power_w > 2000 and hours > 5:
                savings = power_w * hours * 0.3 * 30 / 1000 * 12
                waste_detected.append({
                    "appliance": appliance,
                    "issue": f"High power appliance ({power_w}W) used extensively",
                    "recommendation": "Upgrade to energy-efficient model",
                    "potential_savings": savings,
                    "severity": "high"
                })
        
        return waste_detected
    
    def compare_with_city(self, monthly_kwh, city="Mumbai"):
        """Compare user's consumption with city average"""
        city_avg = self.CITY_AVERAGES.get(city, 240)
        difference = monthly_kwh - city_avg
        difference_pct = (difference / city_avg * 100) if city_avg > 0 else 0
        
        if difference_pct > 20:
            status = "🔴 Much Higher"
            message = f"You consume {difference_pct:.0f}% more than average {city} household"
        elif difference_pct > 0:
            status = "🟡 Slightly Higher"
            message = f"You consume {difference_pct:.0f}% more than average {city} household"
        elif difference_pct > -20:
            status = "🟢 Below Average"
            message = f"You consume {abs(difference_pct):.0f}% less than average {city} household"
        else:
            status = "🟢 Excellent"
            message = f"You consume {abs(difference_pct):.0f}% less than average {city} household"
        
        return {
            "city": city,
            "city_average": city_avg,
            "your_usage": monthly_kwh,
            "difference": difference,
            "difference_pct": difference_pct,
            "status": status,
            "message": message
        }
    
    def calculate_gamification_score(self, monthly_kwh, previous_month_kwh=None):
        """Calculate points, level, and badges"""
        # Base points (lower consumption = more points)
        if monthly_kwh < 150:
            base_points = 100
        elif monthly_kwh < 250:
            base_points = 75
        elif monthly_kwh < 350:
            base_points = 50
        else:
            base_points = 25
        
        # Bonus for reduction
        reduction_bonus = 0
        if previous_month_kwh:
            reduction_pct = ((previous_month_kwh - monthly_kwh) / previous_month_kwh * 100) if previous_month_kwh > 0 else 0
            if reduction_pct > 20:
                reduction_bonus = 50
            elif reduction_pct > 10:
                reduction_bonus = 30
            elif reduction_pct > 5:
                reduction_bonus = 15
        
        total_points = base_points + reduction_bonus
        self.user_points += total_points
        
        # Calculate level (every 200 points = 1 level)
        self.user_level = (self.user_points // 200) + 1
        
        # Award badges
        new_badges = []
        if monthly_kwh < 150 and "🌟 Eco Warrior" not in self.badges:
            self.badges.append("🌟 Eco Warrior")
            new_badges.append("🌟 Eco Warrior")
        
        if reduction_bonus >= 50 and "🏆 Super Saver" not in self.badges:
            self.badges.append("🏆 Super Saver")
            new_badges.append("🏆 Super Saver")
        
        if self.user_level >= 3 and "⚡ Energy Master" not in self.badges:
            self.badges.append("⚡ Energy Master")
            new_badges.append("⚡ Energy Master")
        
        if monthly_kwh < 200 and "🌱 Green Champion" not in self.badges:
            self.badges.append("🌱 Green Champion")
            new_badges.append("🌱 Green Champion")
        
        return {
            "points_earned": total_points,
            "total_points": self.user_points,
            "level": self.user_level,
            "badges": self.badges,
            "new_badges": new_badges,
            "next_level_points": (self.user_level * 200) - self.user_points
        }
    
    def get_smart_schedule_recommendation(self, appliance_name):
        """Suggest best time to run appliances"""
        recommendations = {
            "WASHING MACHINE": {
                "best_time": "11 AM - 3 PM",
                "reason": "Lower grid load, solar power available",
                "avoid": "6 PM - 10 PM (peak hours)"
            },
            "DISHWASHER": {
                "best_time": "10 AM - 2 PM or after 11 PM",
                "reason": "Off-peak hours, lower rates",
                "avoid": "6 PM - 10 PM (peak hours)"
            },
            "EV CHARGER": {
                "best_time": "12 AM - 6 AM",
                "reason": "Lowest grid load, cheapest rates",
                "avoid": "6 PM - 10 PM (peak hours)"
            },
            "WATER HEATER": {
                "best_time": "6 AM - 8 AM",
                "reason": "Just before use, minimal standby loss",
                "avoid": "Leaving on all day"
            }
        }
        
        for key in recommendations:
            if key in appliance_name.upper():
                return recommendations[key]
        
        return {
            "best_time": "11 AM - 4 PM",
            "reason": "Lower grid load during midday",
            "avoid": "6 PM - 10 PM (peak hours)"
        }
