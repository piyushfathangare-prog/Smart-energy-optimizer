"""
ML Predictor Module - Linear Regression for Energy Consumption
---------------------------------------------------------------
Industry-level ML integration for consumption prediction
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import os

class EnergyPredictor:
    """ML model for predicting energy consumption"""
    
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False
        self.r2_score = 0
        self.mse = 0
        self.training_samples = 0
    
    def prepare_training_data(self, appliance_data, historical_days=30):
        """
        Prepare training data from appliance usage
        
        Args:
            appliance_data: Dict of appliances with power and usage
            historical_days: Number of days to simulate
        
        Returns:
            X: Features (power, hours, quantity)
            y: Target (daily consumption in kWh)
        """
        X = []
        y = []
        
        # Simulate historical data with some variance
        for day in range(historical_days):
            for appliance, data in appliance_data.items():
                power = data['power_watts']
                hours = data['hours_per_day']
                quantity = data['quantity']
                
                # Add realistic variance (±10%)
                variance = np.random.uniform(0.9, 1.1)
                actual_consumption = (power * hours * quantity * variance) / 1000
                
                X.append([power, hours, quantity])
                y.append(actual_consumption)
        
        return np.array(X), np.array(y)
    
    def train_from_excel(self, file_path):
        """
        Train model from Excel file
        
        Expected columns: appliance, power_watts, hours_per_day, quantity, daily_kwh
        
        Args:
            file_path: Path to Excel file
        
        Returns:
            dict: Training metrics
        """
        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Check required columns
            required_cols = ['power_watts', 'hours_per_day', 'quantity', 'daily_kwh']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                return {
                    "success": False,
                    "error": f"Missing columns: {', '.join(missing_cols)}"
                }
            
            # Prepare data
            X = df[['power_watts', 'hours_per_day', 'quantity']].values
            y = df['daily_kwh'].values
            
            # Train model
            self.model.fit(X, y)
            self.is_trained = True
            self.training_samples = len(X)
            
            # Calculate metrics
            y_pred = self.model.predict(X)
            self.r2_score = r2_score(y, y_pred)
            self.mse = mean_squared_error(y, y_pred)
            
            return {
                "success": True,
                "r2_score": self.r2_score,
                "mse": self.mse,
                "samples": len(X),
                "message": f"Model trained successfully with {len(X)} samples"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def train(self, appliance_data):
        """
        Train the ML model
        
        Args:
            appliance_data: Dict of appliances with power and usage
        
        Returns:
            dict: Training metrics
        """
        if not appliance_data:
            return {"success": False, "error": "No data provided"}
        
        # Prepare data
        X, y = self.prepare_training_data(appliance_data)
        
        # Train model
        self.model.fit(X, y)
        self.is_trained = True
        
        # Calculate metrics
        y_pred = self.model.predict(X)
        self.r2_score = r2_score(y, y_pred)
        self.mse = mean_squared_error(y, y_pred)
        
        return {
            "success": True,
            "r2_score": self.r2_score,
            "mse": self.mse,
            "samples": len(X)
        }
    
    def predict_consumption(self, power, hours, quantity):
        """
        Predict energy consumption for given parameters
        
        Args:
            power: Power rating in watts
            hours: Usage hours per day
            quantity: Number of appliances
        
        Returns:
            float: Predicted daily consumption in kWh
        """
        if not self.is_trained:
            # Fallback to simple calculation
            return (power * hours * quantity) / 1000
        
        X = np.array([[power, hours, quantity]])
        prediction = self.model.predict(X)[0]
        
        return max(0, prediction)  # Ensure non-negative
    
    def predict_monthly_consumption(self, appliance_data):
        """
        Predict total monthly consumption
        
        Args:
            appliance_data: Dict of appliances
        
        Returns:
            dict: Predictions and breakdown
        """
        daily_predictions = {}
        total_daily = 0
        
        for appliance, data in appliance_data.items():
            daily_kwh = self.predict_consumption(
                data['power_watts'],
                data['hours_per_day'],
                data['quantity']
            )
            daily_predictions[appliance] = daily_kwh
            total_daily += daily_kwh
        
        return {
            "daily_total": total_daily,
            "monthly_total": total_daily * 30,
            "yearly_total": total_daily * 365,
            "breakdown": daily_predictions,
            "confidence": self.r2_score if self.is_trained else 0.95
        }
    
    def get_model_info(self):
        """Get model information"""
        if not self.is_trained:
            return {"trained": False}
        
        return {
            "trained": True,
            "r2_score": round(self.r2_score, 4),
            "mse": round(self.mse, 4),
            "accuracy": round(self.r2_score * 100, 2),
            "coefficients": self.model.coef_.tolist(),
            "intercept": float(self.model.intercept_)
        }


def calculate_peak_offpeak_cost(daily_kwh, rate_peak, rate_offpeak, peak_hours=4):
    """
    Calculate cost split between peak and off-peak hours
    
    Args:
        daily_kwh: Total daily consumption
        rate_peak: Peak rate per kWh
        rate_offpeak: Off-peak rate per kWh
        peak_hours: Number of peak hours per day
    
    Returns:
        dict: Cost breakdown
    """
    # Assume consumption is distributed across 24 hours
    peak_consumption = daily_kwh * (peak_hours / 24)
    offpeak_consumption = daily_kwh * ((24 - peak_hours) / 24)
    
    peak_cost = peak_consumption * rate_peak
    offpeak_cost = offpeak_consumption * rate_offpeak
    
    return {
        "peak_kwh": round(peak_consumption, 2),
        "offpeak_kwh": round(offpeak_consumption, 2),
        "peak_cost": round(peak_cost, 2),
        "offpeak_cost": round(offpeak_cost, 2),
        "total_cost": round(peak_cost + offpeak_cost, 2)
    }


def optimize_usage_schedule(appliance_data, rate_peak, rate_offpeak):
    """
    Suggest optimal usage schedule to minimize costs
    
    Args:
        appliance_data: Dict of appliances
        rate_peak: Peak rate
        rate_offpeak: Off-peak rate
    
    Returns:
        dict: Optimization suggestions
    """
    suggestions = []
    total_savings = 0
    
    # Appliances that can be shifted to off-peak
    shiftable = ["Washing Machine", "Dishwasher", "Heater"]
    
    for appliance, data in appliance_data.items():
        if appliance in shiftable:
            daily_kwh = (data['power_watts'] * data['hours_per_day'] * data['quantity']) / 1000
            
            # Current cost (assume peak usage)
            current_cost = daily_kwh * rate_peak
            
            # Optimized cost (off-peak usage)
            optimized_cost = daily_kwh * rate_offpeak
            
            savings = current_cost - optimized_cost
            total_savings += savings
            
            suggestions.append({
                "appliance": appliance,
                "recommendation": f"Shift usage to off-peak hours (after 10 PM)",
                "current_cost": round(current_cost, 2),
                "optimized_cost": round(optimized_cost, 2),
                "daily_savings": round(savings, 2),
                "monthly_savings": round(savings * 30, 2)
            })
    
    return {
        "suggestions": suggestions,
        "total_daily_savings": round(total_savings, 2),
        "total_monthly_savings": round(total_savings * 30, 2),
        "total_yearly_savings": round(total_savings * 365, 2)
    }


if __name__ == "__main__":
    # Test the predictor
    test_data = {
        "AC": {"power_watts": 1500, "hours_per_day": 8, "quantity": 1},
        "Fridge": {"power_watts": 150, "hours_per_day": 24, "quantity": 1}
    }
    
    predictor = EnergyPredictor()
    result = predictor.train(test_data)
    print("Training Result:", result)
    
    prediction = predictor.predict_monthly_consumption(test_data)
    print("Prediction:", prediction)
    
    print("Model Info:", predictor.get_model_info())
