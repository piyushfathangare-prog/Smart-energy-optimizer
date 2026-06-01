"""
🖼️ Image Recognition Module for Appliance Detection
----------------------------------------------------
Uses pre-trained MobileNet model to identify appliances from images
"""

try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    tf = None

try:
    import numpy as np
except ImportError:
    np = None

from PIL import Image
import io

class ApplianceRecognizer:
    def __init__(self):
        """Initialize the image recognition model"""
        # Load pre-trained MobileNetV2 model
        if not TENSORFLOW_AVAILABLE:
            print("TensorFlow not available. Using fallback recognizer.")
            self.model_loaded = False
            return
            
        try:
            self.model = tf.keras.applications.MobileNetV2(
                weights='imagenet',
                include_top=True
            )
            self.model_loaded = True
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model_loaded = False
        
        # Mapping of ImageNet classes to our appliances
        self.appliance_mapping = {
            # Cooling
            'refrigerator': 'Refrigerator',
            'fridge': 'Refrigerator',
            'air conditioner': 'Air Conditioner',
            'fan': 'Fan',
            'electric fan': 'Fan',
            
            # Cleaning
            'washer': 'Washing Machine',
            'washing machine': 'Washing Machine',
            'dishwasher': 'Dishwasher',
            'vacuum': 'Vacuum Cleaner',
            
            # Entertainment
            'television': 'TV',
            'tv': 'TV',
            'monitor': 'TV',
            'screen': 'TV',
            
            # Electronics
            'computer': 'Computer',
            'laptop': 'Computer',
            'desktop computer': 'Computer',
            'notebook': 'Computer',
            
            # Heating
            'heater': 'Heater',
            'space heater': 'Heater',
            'radiator': 'Heater',
            
            # Cooking
            'microwave': 'Microwave',
            'oven': 'Oven',
            'toaster': 'Microwave',
            'stove': 'Oven',
            
            # Lighting
            'lamp': 'Lights',
            'light': 'Lights',
            'bulb': 'Lights'
        }
    
    def preprocess_image(self, image_file):
        """Preprocess image for model input"""
        if not TENSORFLOW_AVAILABLE:
            return None, None
            
        try:
            # Read image
            image = Image.open(image_file)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to model input size
            image = image.resize((224, 224))
            
            # Convert to array
            img_array = tf.keras.preprocessing.image.img_to_array(image)
            img_array = np.expand_dims(img_array, axis=0)
            
            # Preprocess for MobileNetV2
            img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
            
            return img_array, image
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None, None
    
    def recognize_appliance(self, image_file):
        """
        Recognize appliance from uploaded image
        
        Returns:
            dict: {
                'appliance': str,
                'confidence': float,
                'all_predictions': list,
                'success': bool,
                'message': str
            }
        """
        if not self.model_loaded:
            return {
                'success': False,
                'message': 'TensorFlow not available. Using fallback mode - please name your files like "refrigerator.jpg" or "ac.jpg"',
                'appliance': None,
                'confidence': 0,
                'all_predictions': []
            }
        
        # Preprocess image
        img_array, original_image = self.preprocess_image(image_file)
        
        if img_array is None:
            return {
                'success': False,
                'message': 'Failed to process image',
                'appliance': None,
                'confidence': 0,
                'all_predictions': []
            }
        
        try:
            # Make prediction
            predictions = self.model.predict(img_array, verbose=0)
            
            # Decode predictions
            decoded = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=10)[0]
            
            # Find matching appliance
            detected_appliance = None
            confidence = 0
            all_predictions = []
            
            for pred in decoded:
                class_name = pred[1].lower()
                class_confidence = float(pred[2])
                
                all_predictions.append({
                    'class': pred[1],
                    'confidence': class_confidence * 100
                })
                
                # Check if this class matches any appliance
                for key, appliance in self.appliance_mapping.items():
                    if key in class_name:
                        if class_confidence > confidence:
                            detected_appliance = appliance
                            confidence = class_confidence
            
            if detected_appliance:
                return {
                    'success': True,
                    'appliance': detected_appliance,
                    'confidence': confidence * 100,
                    'all_predictions': all_predictions,
                    'message': f'Detected {detected_appliance} with {confidence*100:.1f}% confidence'
                }
            else:
                return {
                    'success': False,
                    'appliance': None,
                    'confidence': 0,
                    'all_predictions': all_predictions,
                    'message': 'Could not identify appliance. Top predictions: ' + 
                              ', '.join([f"{p['class']} ({p['confidence']:.1f}%)" for p in all_predictions[:3]])
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error during recognition: {str(e)}',
                'appliance': None,
                'confidence': 0,
                'all_predictions': []
            }
    
    def batch_recognize(self, image_files):
        """Recognize multiple appliances from multiple images"""
        results = []
        for image_file in image_files:
            result = self.recognize_appliance(image_file)
            results.append(result)
        return results


# Simple fallback using basic pattern matching (if TensorFlow not available)
class SimpleApplianceRecognizer:
    """Fallback recognizer using filename patterns"""
    
    def __init__(self):
        self.patterns = {
            'ac': 'Air Conditioner',
            'air_conditioner': 'Air Conditioner',
            'aircon': 'Air Conditioner',
            'fridge': 'Refrigerator',
            'refrigerator': 'Refrigerator',
            'washing': 'Washing Machine',
            'washer': 'Washing Machine',
            'tv': 'TV',
            'television': 'TV',
            'computer': 'Computer',
            'laptop': 'Computer',
            'pc': 'Computer',
            'heater': 'Heater',
            'dishwasher': 'Dishwasher',
            'microwave': 'Microwave',
            'oven': 'Oven',
            'fan': 'Fan',
            'light': 'Lights',
            'lamp': 'Lights'
        }
    
    def recognize_appliance(self, image_file):
        """Simple recognition based on filename"""
        filename = image_file.name.lower() if hasattr(image_file, 'name') else str(image_file).lower()
        
        for pattern, appliance in self.patterns.items():
            if pattern in filename:
                return {
                    'success': True,
                    'appliance': appliance,
                    'confidence': 80.0,
                    'message': f'Detected {appliance} from filename',
                    'all_predictions': []
                }
        
        return {
            'success': False,
            'appliance': None,
            'confidence': 0,
            'message': 'Could not identify appliance from filename. Please select manually.',
            'all_predictions': []
        }


# Factory function to get appropriate recognizer
def get_recognizer():
    """Get the best available recognizer"""
    if TENSORFLOW_AVAILABLE:
        try:
            recognizer = ApplianceRecognizer()
            if recognizer.model_loaded:
                return recognizer
        except Exception as e:
            print(f"Failed to load TensorFlow recognizer: {e}")
    
    # Fallback to simple recognizer
    print("Using simple filename-based recognizer")
    return SimpleApplianceRecognizer()
