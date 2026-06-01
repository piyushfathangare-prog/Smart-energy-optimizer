"""
☀️ Solar Energy ROI & Cost Recovery Calculator
Professional solar panel investment analysis with ROI calculations
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

class SolarROICalculator:
    """Calculate solar panel ROI and investment recovery"""
    
    def __init__(self):
        self.co2_per_kwh = 0.82  # kg CO2 per kWh in India
        
    def calculate_system_size(self, monthly_units, sunlight_hours=5):
        """Calculate required solar system size in kW"""
        # 1 kW system generates approximately: sunlight_hours × 30 days per month
        units_per_kw = sunlight_hours * 30
        system_size = monthly_units / units_per_kw
        return round(system_size, 2)
    
    def calculate_installation_cost(self, system_size, cost_per_kw=55000, subsidy_percent=0):
        """Calculate total installation cost with subsidy"""
        total_cost = system_size * cost_per_kw
        subsidy_amount = (total_cost * subsidy_percent) / 100
        final_cost = total_cost - subsidy_amount
        
        return {
            'total_cost': total_cost,
            'subsidy_amount': subsidy_amount,
            'final_cost': final_cost
        }
    
    def calculate_monthly_generation(self, system_size, sunlight_hours=5):
        """Calculate monthly solar generation in kWh"""
        return system_size * sunlight_hours * 30
    
    def calculate_savings(self, monthly_solar_units, cost_per_unit, maintenance_yearly=0):
        """Calculate monthly and yearly savings"""
        monthly_savings = monthly_solar_units * cost_per_unit
        yearly_savings = (monthly_savings * 12) - maintenance_yearly
        
        return {
            'monthly_savings': monthly_savings,
            'yearly_savings': yearly_savings
        }
    
    def calculate_payback_period(self, final_cost, yearly_savings):
        """Calculate payback period in years"""
        if yearly_savings <= 0:
            return float('inf')
        return final_cost / yearly_savings
    
    def calculate_roi(self, final_cost, yearly_savings, years=25, tariff_increase=0):
        """Calculate ROI over specified years with optional tariff increase"""
        total_savings = 0
        
        for year in range(1, years + 1):
            if tariff_increase > 0:
                # Apply compound tariff increase
                year_savings = yearly_savings * ((1 + tariff_increase/100) ** year)
            else:
                year_savings = yearly_savings
            total_savings += year_savings
        
        net_profit = total_savings - final_cost
        roi_percent = (net_profit / final_cost) * 100 if final_cost > 0 else 0
        
        return {
            'total_savings': total_savings,
            'net_profit': net_profit,
            'roi_percent': roi_percent
        }
    
    def calculate_carbon_reduction(self, monthly_solar_units, years=25):
        """Calculate carbon emission reduction"""
        yearly_units = monthly_solar_units * 12
        total_units = yearly_units * years
        
        co2_reduced = total_units * self.co2_per_kwh
        trees_equivalent = co2_reduced / 21  # 1 tree absorbs ~21 kg CO2/year
        
        return {
            'yearly_co2_reduced': yearly_units * self.co2_per_kwh,
            'total_co2_reduced': co2_reduced,
            'trees_equivalent': trees_equivalent
        }
    
    def get_recommendation(self, payback_period):
        """Get investment recommendation based on payback period"""
        if payback_period < 5:
            return {
                'rating': '🔥 Excellent',
                'message': 'Excellent Investment Opportunity! Quick payback with high returns.',
                'color': '#10b981'
            }
        elif payback_period <= 8:
            return {
                'rating': '✅ Good',
                'message': 'Good Long-Term Investment with steady returns.',
                'color': '#3b82f6'
            }
        else:
            return {
                'rating': '⚠️ Consider',
                'message': 'Consider subsidy options or cost optimization for better ROI.',
                'color': '#f59e0b'
            }
    
    def generate_cumulative_savings_data(self, final_cost, yearly_savings, years=25, tariff_increase=0):
        """Generate cumulative savings data for visualization"""
        years_list = list(range(0, years + 1))
        cumulative_savings = [0]  # Start at 0
        
        for year in range(1, years + 1):
            if tariff_increase > 0:
                year_savings = yearly_savings * ((1 + tariff_increase/100) ** year)
            else:
                year_savings = yearly_savings
            
            cumulative_savings.append(cumulative_savings[-1] + year_savings)
        
        # Subtract initial investment
        net_cumulative = [savings - final_cost for savings in cumulative_savings]
        
        return years_list, net_cumulative, cumulative_savings
    
    def calculate_without_solar_cost(self, monthly_bill, years=25, tariff_increase=0):
        """Calculate total electricity cost without solar over years"""
        total_cost = 0
        yearly_bill = monthly_bill * 12
        
        for year in range(1, years + 1):
            if tariff_increase > 0:
                year_cost = yearly_bill * ((1 + tariff_increase/100) ** year)
            else:
                year_cost = yearly_bill
            total_cost += year_cost
        
        return total_cost
    
    def calculate_with_solar_cost(self, final_cost, maintenance_yearly, years=25):
        """Calculate total cost with solar (installation + maintenance)"""
        return final_cost + (maintenance_yearly * years)
    
    def suggest_optimal_system(self, monthly_units, rooftop_area, sunlight_hours=5):
        """Suggest optimal system size based on consumption and space"""
        # Calculate based on consumption
        consumption_based = self.calculate_system_size(monthly_units, sunlight_hours)
        
        # Calculate based on rooftop area
        # Assume: 1 kW requires ~100 sq ft
        space_based = rooftop_area / 100
        
        # Recommend the smaller of the two
        optimal_size = min(consumption_based, space_based)
        
        return {
            'optimal_size': round(optimal_size, 2),
            'consumption_based': round(consumption_based, 2),
            'space_based': round(space_based, 2),
            'space_sufficient': space_based >= consumption_based
        }
    
    def suggest_battery(self, system_size):
        """Suggest battery capacity for backup"""
        # Typical recommendation: 2-3 hours of backup
        # Battery capacity in kWh = System size × backup hours
        recommended_capacity = system_size * 2.5
        
        return {
            'recommended_capacity': round(recommended_capacity, 2),
            'estimated_cost': round(recommended_capacity * 15000, 0),  # ~₹15,000 per kWh
            'backup_hours': 2.5
        }
    
    def generate_report_data(self, inputs, results):
        """Generate comprehensive report data for export"""
        report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'inputs': inputs,
            'results': results
        }
        return report
