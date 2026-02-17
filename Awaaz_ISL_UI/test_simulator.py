"""
Test gesture simulator word mode
"""
from gesture_simulator import GestureSimulator

print("Testing GestureSimulator...")

# Create simulator
sim = GestureSimulator()
print(f"✓ Simulator created")
print(f"  Model loaded: {sim.model is not None}")

# Test with mock data
class MockData:
    hand_landmarks = []

# Test LETTER mode
print("\n--- Testing LETTER mode ---")
result = sim.predict_gesture(MockData(), mode="LETTER")
print(f"Result: {result}")
print(f"Type: {type(result)}")

# Test WORD mode
print("\n--- Testing WORD mode ---")
result = sim.predict_gesture(MockData(), mode="WORD")
print(f"Result: {result}")
print(f"Type: {type(result)}")

# Check if result is dict
if isinstance(result, dict):
    print(f"✓ Returns dictionary")
    print(f"  Keys: {result.keys()}")
    print(f"  Type: {result.get('type')}")
    print(f"  Value: {result.get('value')}")
else:
    print(f"✗ Does not return dictionary!")
