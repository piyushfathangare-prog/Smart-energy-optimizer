"""
🎯 Goal-Based Energy Tracker
Set consumption targets and track progress with alerts
"""

import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class EnergyGoalTracker:
    """Track energy consumption goals and provide progress updates"""
    
    def __init__(self):
        self.goal_types = {
            'daily': 'Daily Consumption Goal',
            'monthly': 'Monthly Consumption Goal',
            'bill': 'Monthly Bill Goal',
            'carbon': 'Carbon Reduction Goal'
        }
    
    def calculate_progress(self, current_value, target_value):
        """Calculate progress percentage towards goal"""
        if target_value == 0:
            return 0
        
        progress = (current_value / target_value) * 100
        return min(progress, 100)  # Cap at 100%
    
    def get_status(self, current_value, target_value):
        """Get goal status with color coding"""
        progress = self.calculate_progress(current_value, target_value)
        
        if progress <= 70:
            return {
                'status': '🟢 On Track',
                'color': '#10b981',
                'message': 'Great! You\'re well within your target.',
                'icon': '✅'
            }
        elif progress <= 90:
            return {
                'status': '🟡 Warning',
                'color': '#f59e0b',
                'message': 'Approaching your limit. Consider reducing usage.',
                'icon': '⚠️'
            }
        elif progress <= 100:
            return {
                'status': '🟠 Critical',
                'color': '#f97316',
                'message': 'Very close to exceeding your goal!',
                'icon': '🚨'
            }
        else:
            return {
                'status': '🔴 Exceeded',
                'color': '#ef4444',
                'message': 'Goal exceeded! Take immediate action.',
                'icon': '❌'
            }
    
    def calculate_daily_target(self, monthly_target, days_in_month=30):
        """Calculate daily target from monthly goal"""
        return monthly_target / days_in_month
    
    def calculate_remaining(self, current_value, target_value):
        """Calculate remaining allowance"""
        remaining = target_value - current_value
        return max(remaining, 0)
    
    def estimate_month_end(self, current_daily_avg, days_elapsed, days_in_month=30):
        """Estimate end-of-month consumption based on current trend"""
        if days_elapsed == 0:
            return 0
        
        projected_total = (current_daily_avg * days_in_month)
        return projected_total
    
    def get_recommendations(self, current_value, target_value, goal_type='daily'):
        """Get personalized recommendations based on progress"""
        progress = self.calculate_progress(current_value, target_value)
        recommendations = []
        
        if progress > 100:
            recommendations = [
                "🔴 Immediate action needed - goal exceeded",
                "Turn off unnecessary appliances",
                "Shift heavy usage to off-peak hours",
                "Check for appliances left on standby",
                "Consider upgrading to energy-efficient devices"
            ]
        elif progress > 90:
            recommendations = [
                "⚠️ Approaching limit - reduce usage now",
                "Minimize AC/heater usage",
                "Use natural lighting when possible",
                "Postpone heavy appliance usage",
                "Monitor real-time consumption closely"
            ]
        elif progress > 70:
            recommendations = [
                "🟡 On track but monitor closely",
                "Maintain current usage patterns",
                "Plan heavy usage carefully",
                "Continue energy-saving practices"
            ]
        else:
            recommendations = [
                "✅ Excellent progress!",
                "Keep up the good work",
                "You're well within your target",
                "Consider setting a more ambitious goal"
            ]
        
        return recommendations
    
    def calculate_savings_potential(self, current_value, target_value, cost_per_unit):
        """Calculate potential savings if goal is met"""
        if current_value <= target_value:
            return 0
        
        excess_units = current_value - target_value
        potential_savings = excess_units * cost_per_unit
        return potential_savings
    
    def generate_goal_summary(self, goals_data):
        """Generate comprehensive goal summary"""
        summary = {
            'total_goals': len(goals_data),
            'achieved': 0,
            'in_progress': 0,
            'exceeded': 0,
            'overall_performance': 0
        }
        
        for goal in goals_data:
            progress = self.calculate_progress(goal['current'], goal['target'])
            
            if progress <= 100:
                summary['achieved'] += 1
            elif progress <= 110:
                summary['in_progress'] += 1
            else:
                summary['exceeded'] += 1
            
            summary['overall_performance'] += min(progress, 100)
        
        if summary['total_goals'] > 0:
            summary['overall_performance'] /= summary['total_goals']
        
        return summary
    
    def create_milestone_tracker(self, target_value, num_milestones=4):
        """Create milestone checkpoints for goal"""
        milestones = []
        step = target_value / num_milestones
        
        for i in range(1, num_milestones + 1):
            milestones.append({
                'milestone': i,
                'value': step * i,
                'percentage': (i / num_milestones) * 100,
                'label': f"{(i / num_milestones) * 100:.0f}% Complete"
            })
        
        return milestones
    
    def check_milestone_reached(self, current_value, milestones):
        """Check which milestones have been reached"""
        reached = []
        
        for milestone in milestones:
            if current_value >= milestone['value']:
                reached.append(milestone)
        
        return reached
    
    def calculate_daily_budget(self, monthly_target, days_remaining):
        """Calculate daily budget for remaining days"""
        if days_remaining <= 0:
            return 0
        
        return monthly_target / days_remaining
    
    def get_alert_message(self, progress, goal_type='consumption'):
        """Generate alert message based on progress"""
        if progress > 100:
            return f"🚨 ALERT: {goal_type.title()} goal exceeded by {progress - 100:.1f}%!"
        elif progress > 90:
            return f"⚠️ WARNING: {goal_type.title()} at {progress:.1f}% of target!"
        elif progress > 70:
            return f"📊 UPDATE: {goal_type.title()} at {progress:.1f}% of target"
        else:
            return f"✅ GOOD: {goal_type.title()} well within target ({progress:.1f}%)"
    
    def compare_with_previous(self, current_value, previous_value):
        """Compare current performance with previous period"""
        if previous_value == 0:
            return {
                'change': 0,
                'percentage': 0,
                'trend': 'neutral',
                'message': 'No previous data available'
            }
        
        change = current_value - previous_value
        percentage = (change / previous_value) * 100
        
        if change < 0:
            trend = 'improving'
            message = f"📉 Reduced by {abs(percentage):.1f}% from last period"
        elif change > 0:
            trend = 'worsening'
            message = f"📈 Increased by {percentage:.1f}% from last period"
        else:
            trend = 'stable'
            message = "➡️ Same as last period"
        
        return {
            'change': change,
            'percentage': percentage,
            'trend': trend,
            'message': message
        }
