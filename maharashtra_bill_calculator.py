"""
Maharashtra Electricity Bill Calculator
MSEDCL (Maharashtra State Electricity Distribution Co. Ltd.) Tariff Rates
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Maharashtra Bill Calculator",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: #f8fafc;
    }
    
    .header-section {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .tariff-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 4px solid #2563eb;
        margin-bottom: 1rem;
    }
    
    .bill-summary {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #2563eb 0%, #1e40af 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Maharashtra MSEDCL Tariff Rates (LT-I Residential)
# Updated rates as per MSEDCL tariff structure
MAHARASHTRA_TARIFF = {
    "LT-I(B) Residential": {
        "slabs": [
            {"min": 0, "max": 100, "rate": 3.61, "fixed": 25},
            {"min": 101, "max": 300, "rate": 7.82, "fixed": 55},
            {"min": 301, "max": 500, "rate": 9.07, "fixed": 110},
            {"min": 501, "max": float('inf'), "rate": 10.64, "fixed": 140}
        ],
        "description": "Residential connections for domestic use"
    },
    "LT-I(A) Residential (BPL)": {
        "slabs": [
            {"min": 0, "max": 30, "rate": 1.90, "fixed": 10},
            {"min": 31, "max": 100, "rate": 3.61, "fixed": 25},
            {"min": 101, "max": 300, "rate": 7.82, "fixed": 55},
            {"min": 301, "max": float('inf'), "rate": 9.07, "fixed": 110}
        ],
        "description": "Below Poverty Line (BPL) residential connections"
    },
    "LT-II Commercial": {
        "slabs": [
            {"min": 0, "max": float('inf'), "rate": 11.50, "fixed": 200}
        ],
        "description": "Commercial establishments, shops, offices"
    }
}

# Additional charges
FUEL_ADJUSTMENT_CHARGE = 0.50  # Per unit (approximate)
ELECTRICITY_DUTY = 0.16  # 16% on energy charges
METER_RENT = 15  # Monthly meter rent

# Appliance database with typical power ratings
APPLIANCES = {
    "Air Conditioner (1.5 Ton)": 1500,
    "Air Conditioner (1 Ton)": 1000,
    "Refrigerator (Single Door)": 150,
    "Refrigerator (Double Door)": 250,
    "Washing Machine": 500,
    "TV (LED 32 inch)": 60,
    "TV (LED 55 inch)": 100,
    "Computer/Laptop": 200,
    "Water Heater (Geyser)": 2000,
    "Microwave Oven": 1200,
    "Induction Cooktop": 1500,
    "Electric Iron": 1000,
    "Ceiling Fan": 75,
    "Table Fan": 50,
    "LED Bulb (9W)": 9,
    "LED Bulb (15W)": 15,
    "Tube Light": 40,
    "Water Pump": 750,
    "Mixer Grinder": 500,
    "Electric Kettle": 1500,
    "Room Heater": 2000,
    "Dishwasher": 1800
}

def calculate_bill(units, tariff_type):
    """Calculate electricity bill based on MSEDCL tariff"""
    tariff = MAHARASHTRA_TARIFF[tariff_type]
    slabs = tariff["slabs"]
    
    energy_charges = 0
    fixed_charges = 0
    slab_breakdown = []
    
    remaining_units = units
    
    for slab in slabs:
        if remaining_units <= 0:
            break
        
        slab_min = slab["min"]
        slab_max = slab["max"]
        slab_rate = slab["rate"]
        
        # Calculate units in this slab
        if slab_max == float('inf'):
            units_in_slab = remaining_units
        else:
            slab_size = slab_max - slab_min + 1
            units_in_slab = min(remaining_units, slab_size)
        
        # Calculate charges for this slab
        slab_charges = units_in_slab * slab_rate
        energy_charges += slab_charges
        
        # Fixed charges (use the highest slab's fixed charge)
        fixed_charges = slab["fixed"]
        
        slab_breakdown.append({
            "slab": f"{slab_min}-{slab_max if slab_max != float('inf') else '∞'} units",
            "units": units_in_slab,
            "rate": slab_rate,
            "amount": slab_charges
        })
        
        remaining_units -= units_in_slab
    
    # Calculate additional charges
    fuel_charges = units * FUEL_ADJUSTMENT_CHARGE
    electricity_duty = energy_charges * ELECTRICITY_DUTY
    meter_rent = METER_RENT
    
    # Total bill
    total_bill = energy_charges + fixed_charges + fuel_charges + electricity_duty + meter_rent
    
    return {
        "energy_charges": energy_charges,
        "fixed_charges": fixed_charges,
        "fuel_charges": fuel_charges,
        "electricity_duty": electricity_duty,
        "meter_rent": meter_rent,
        "total_bill": total_bill,
        "slab_breakdown": slab_breakdown
    }

def calculate_consumption_from_appliances(appliances_data):
    """Calculate total monthly consumption from appliances"""
    total_kwh = 0
    breakdown = []
    
    for appliance in appliances_data:
        power_watts = appliance["power"]
        hours_per_day = appliance["hours"]
        quantity = appliance["quantity"]
        days_per_month = 30
        
        # Calculate monthly consumption
        daily_kwh = (power_watts * hours_per_day * quantity) / 1000
        monthly_kwh = daily_kwh * days_per_month
        total_kwh += monthly_kwh
        
        breakdown.append({
            "appliance": appliance["name"],
            "power": power_watts,
            "hours": hours_per_day,
            "quantity": quantity,
            "monthly_kwh": monthly_kwh
        })
    
    return total_kwh, breakdown

# Header
st.markdown("""
<div class="header-section">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">⚡ Maharashtra Electricity Bill Calculator</h1>
    <p style="font-size: 1.1rem; opacity: 0.95;">
        MSEDCL Tariff-based Bill Estimation | Accurate & Up-to-date
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🔧 Configuration")
    
    # Tariff selection
    st.markdown("### 📋 Select Tariff Type")
    tariff_type = st.selectbox(
        "Choose your connection type:",
        list(MAHARASHTRA_TARIFF.keys()),
        help="Select the tariff category applicable to your connection"
    )
    
    st.info(f"ℹ️ {MAHARASHTRA_TARIFF[tariff_type]['description']}")
    
    st.markdown("---")
    
    # Calculation method
    st.markdown("### 🧮 Calculation Method")
    calc_method = st.radio(
        "Choose method:",
        ["Enter Units Directly", "Calculate from Appliances"]
    )
    
    st.markdown("---")
    
    if calc_method == "Enter Units Directly":
        st.markdown("### 📊 Enter Consumption")
        units = st.number_input(
            "Monthly Units (kWh):",
            min_value=0.0,
            value=300.0,
            step=10.0,
            help="Enter your monthly electricity consumption in units (kWh)"
        )
        
        if st.button("🔍 Calculate Bill", use_container_width=True):
            st.session_state.calculate = True
            st.session_state.units = units
            st.session_state.tariff_type = tariff_type
            st.session_state.calc_method = calc_method
    
    else:
        st.markdown("### 🔌 Add Appliances")
        
        if "appliances_list" not in st.session_state:
            st.session_state.appliances_list = []
        
        # Appliance selection
        selected_appliance = st.selectbox(
            "Select Appliance:",
            list(APPLIANCES.keys())
        )
        
        col1, col2 = st.columns(2)
        with col1:
            hours = st.number_input("Hours/day", 1.0, 24.0, 8.0, 0.5)
        with col2:
            quantity = st.number_input("Quantity", 1, 20, 1)
        
        if st.button("➕ Add Appliance", use_container_width=True):
            st.session_state.appliances_list.append({
                "name": selected_appliance,
                "power": APPLIANCES[selected_appliance],
                "hours": hours,
                "quantity": quantity
            })
            st.rerun()
        
        # Show added appliances
        if st.session_state.appliances_list:
            st.markdown("#### Added Appliances:")
            for idx, app in enumerate(st.session_state.appliances_list):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(f"{app['name']} ({app['quantity']}x)")
                with col2:
                    if st.button("🗑️", key=f"del_{idx}"):
                        st.session_state.appliances_list.pop(idx)
                        st.rerun()
            
            if st.button("🔍 Calculate Bill", use_container_width=True):
                total_units, breakdown = calculate_consumption_from_appliances(
                    st.session_state.appliances_list
                )
                st.session_state.calculate = True
                st.session_state.units = total_units
                st.session_state.tariff_type = tariff_type
                st.session_state.calc_method = calc_method
                st.session_state.appliance_breakdown = breakdown
                st.rerun()

# Main content
if "calculate" in st.session_state and st.session_state.calculate:
    units = st.session_state.units
    tariff_type = st.session_state.tariff_type
    
    # Calculate bill
    bill_details = calculate_bill(units, tariff_type)
    
    # Bill Summary
    st.markdown(f"""
    <div class="bill-summary">
        <h2 style="margin-bottom: 1rem;">💰 Your Estimated Bill</h2>
        <h1 style="font-size: 3rem; margin: 1rem 0;">₹{bill_details['total_bill']:.2f}</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">for {units:.2f} units consumption</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bill Breakdown
    st.markdown("### 📊 Bill Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Energy Charges", f"₹{bill_details['energy_charges']:.2f}")
        st.metric("Fixed Charges", f"₹{bill_details['fixed_charges']:.2f}")
    
    with col2:
        st.metric("Fuel Adjustment", f"₹{bill_details['fuel_charges']:.2f}")
        st.metric("Electricity Duty (16%)", f"₹{bill_details['electricity_duty']:.2f}")
    
    with col3:
        st.metric("Meter Rent", f"₹{bill_details['meter_rent']:.2f}")
        st.metric("Total Amount", f"₹{bill_details['total_bill']:.2f}", 
                 delta=None, delta_color="off")
    
    st.markdown("---")
    
    # Slab-wise Breakdown
    st.markdown("### 📈 Slab-wise Consumption Breakdown")
    
    slab_df = pd.DataFrame(bill_details['slab_breakdown'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Slab breakdown table
        st.dataframe(
            slab_df.style.format({
                "units": "{:.2f}",
                "rate": "₹{:.2f}",
                "amount": "₹{:.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        # Pie chart
        fig = go.Figure(data=[go.Pie(
            labels=slab_df['slab'],
            values=slab_df['amount'],
            hole=0.4,
            marker_colors=['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
        )])
        fig.update_layout(
            title='Cost Distribution by Slab',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Appliance breakdown (if calculated from appliances)
    if st.session_state.calc_method == "Calculate from Appliances" and "appliance_breakdown" in st.session_state:
        st.markdown("### 🔌 Appliance-wise Consumption")
        
        app_df = pd.DataFrame(st.session_state.appliance_breakdown)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart
            fig = px.bar(
                app_df,
                x='appliance',
                y='monthly_kwh',
                color='monthly_kwh',
                color_continuous_scale='Blues',
                title='Monthly Consumption by Appliance'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Pie chart
            fig = go.Figure(data=[go.Pie(
                labels=app_df['appliance'],
                values=app_df['monthly_kwh'],
                hole=0.4
            )])
            fig.update_layout(
                title='Consumption Distribution',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.dataframe(
            app_df.style.format({
                "power": "{:.0f}W",
                "hours": "{:.1f}h",
                "monthly_kwh": "{:.2f} kWh"
            }),
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
    
    # Detailed Bill Summary
    st.markdown("### 📄 Detailed Bill Summary")
    
    summary_data = {
        "Description": [
            "Energy Charges",
            "Fixed Charges",
            "Fuel Adjustment Charges",
            "Electricity Duty (16%)",
            "Meter Rent",
            "Total Bill Amount"
        ],
        "Amount (₹)": [
            f"₹{bill_details['energy_charges']:.2f}",
            f"₹{bill_details['fixed_charges']:.2f}",
            f"₹{bill_details['fuel_charges']:.2f}",
            f"₹{bill_details['electricity_duty']:.2f}",
            f"₹{bill_details['meter_rent']:.2f}",
            f"₹{bill_details['total_bill']:.2f}"
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Comparison with other slabs
    st.markdown("### 📊 Cost Comparison Across Consumption Levels")
    
    comparison_units = [100, 200, 300, 400, 500, 600]
    comparison_bills = []
    
    for u in comparison_units:
        bill = calculate_bill(u, tariff_type)
        comparison_bills.append({
            "Units": u,
            "Bill Amount": bill['total_bill'],
            "Per Unit Cost": bill['total_bill'] / u
        })
    
    comp_df = pd.DataFrame(comparison_bills)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(
            comp_df,
            x='Units',
            y='Bill Amount',
            markers=True,
            title='Bill Amount vs Consumption'
        )
        fig.add_vline(x=units, line_dash="dash", line_color="red", 
                     annotation_text="Your Usage")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(
            comp_df,
            x='Units',
            y='Per Unit Cost',
            markers=True,
            title='Average Cost per Unit'
        )
        fig.add_vline(x=units, line_dash="dash", line_color="red",
                     annotation_text="Your Usage")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Export options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Calculate Again", use_container_width=True):
            st.session_state.calculate = False
            st.rerun()
    
    with col2:
        # Download bill summary
        bill_summary = f"""
MAHARASHTRA ELECTRICITY BILL SUMMARY
=====================================
Date: {datetime.now().strftime('%d-%m-%Y')}
Tariff: {tariff_type}
Consumption: {units:.2f} units

CHARGES BREAKDOWN:
------------------
Energy Charges:        ₹{bill_details['energy_charges']:.2f}
Fixed Charges:         ₹{bill_details['fixed_charges']:.2f}
Fuel Adjustment:       ₹{bill_details['fuel_charges']:.2f}
Electricity Duty:      ₹{bill_details['electricity_duty']:.2f}
Meter Rent:            ₹{bill_details['meter_rent']:.2f}
------------------
TOTAL AMOUNT:          ₹{bill_details['total_bill']:.2f}
=====================================
        """
        st.download_button(
            "📄 Download Summary",
            bill_summary,
            f"bill_summary_{datetime.now().strftime('%Y%m%d')}.txt",
            "text/plain",
            use_container_width=True
        )
    
    with col3:
        # Download CSV
        if st.session_state.calc_method == "Calculate from Appliances" and "appliance_breakdown" in st.session_state:
            csv = app_df.to_csv(index=False)
            st.download_button(
                "📊 Download CSV",
                csv,
                f"appliance_data_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                use_container_width=True
            )

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: white; border-radius: 16px; margin: 2rem 0;">
        <h2 style="color: #2563eb; margin-bottom: 1rem;">Welcome to Maharashtra Bill Calculator</h2>
        <p style="font-size: 1.1rem; color: #64748b; margin-bottom: 1.5rem;">
            Calculate your electricity bill based on MSEDCL tariff rates
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📋</div>
                <div style="font-weight: 600;">MSEDCL Tariff</div>
                <div style="font-size: 0.875rem; color: #64748b;">Official Rates</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧮</div>
                <div style="font-weight: 600;">Accurate Calculation</div>
                <div style="font-size: 0.875rem; color: #64748b;">Slab-wise Breakdown</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-weight: 600;">Detailed Analysis</div>
                <div style="font-size: 0.875rem; color: #64748b;">Charts & Reports</div>
            </div>
        </div>
        <p style="margin-top: 2rem; color: #64748b;">
            👈 Configure your settings in the sidebar to get started
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tariff information
    st.markdown("### 📋 Maharashtra MSEDCL Tariff Rates")
    
    for tariff_name, tariff_info in MAHARASHTRA_TARIFF.items():
        with st.expander(f"📌 {tariff_name}"):
            st.write(f"**Description:** {tariff_info['description']}")
            st.write("**Rate Slabs:**")
            
            slab_data = []
            for slab in tariff_info['slabs']:
                slab_data.append({
                    "Units Range": f"{slab['min']}-{slab['max'] if slab['max'] != float('inf') else '∞'}",
                    "Rate (₹/unit)": f"₹{slab['rate']:.2f}",
                    "Fixed Charges": f"₹{slab['fixed']:.2f}"
                })
            
            st.table(pd.DataFrame(slab_data))

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 1rem;">
    <p style="font-size: 0.875rem;">
        ⚡ Maharashtra Electricity Bill Calculator | MSEDCL Tariff-based | Accurate Estimation
    </p>
    <p style="font-size: 0.75rem; margin-top: 0.5rem;">
        Note: Rates are approximate and may vary. Please refer to official MSEDCL website for exact tariffs.
    </p>
</div>
""", unsafe_allow_html=True)
