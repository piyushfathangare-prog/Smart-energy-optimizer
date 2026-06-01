"""
Test script for image recognition module
"""

from image_recognizer import get_recognizer
import sys

def test_recognizer():
    """Test the image recognizer"""
    print("=" * 50)
    print("Testing Image Recognition Module")
    print("=" * 50)
    print()
    
    # Get recognizer
    recognizer = get_recognizer()
    print(f"✓ Recognizer loaded: {type(recognizer).__name__}")
    print()
    
    # Test with sample filenames (fallback method)
    test_files = [
        "my_refrigerator.jpg",
        "living_room_ac.png",
        "kitchen_microwave.jpg",
        "bedroom_tv.jpg",
        "washing_machine_photo.jpg"
    ]
    
    print("Testing with sample filenames:")
    print("-" * 50)
    
    for filename in test_files:
        # Create a mock file object
        class MockFile:
            def __init__(self, name):
                self.name = name
        
        mock_file = MockFile(filename)
        result = recognizer.recognize_appliance(mock_file)
        
        if result['success']:
            print(f"✓ {filename}")
            print(f"  → Detected: {result['appliance']}")
            print(f"  → Confidence: {result['confidence']:.1f}%")
        else:
            print(f"✗ {filename}")
            print(f"  → {result['message']}")
        print()
    
    print("=" * 50)
    print("Test Complete!")
    print("=" * 50)
    print()
    print("To use with real images:")
    print("1. Run: python -m streamlit run smart_ai_app.py")
    print("2. Upload appliance photos in the sidebar")
    print("3. Click 'Detect Appliances from Images'")
    print()

if __name__ == "__main__":
    test_recognizer()
