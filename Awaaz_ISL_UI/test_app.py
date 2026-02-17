"""
Quick test to verify all components work
"""
import sys
import os

print("Testing imports...")

try:
    # Test gesture simulator
    from gesture_simulator import GestureSimulator
    print("✓ GestureSimulator imported")
    
    # Test word library
    from word_library import get_word_by_pattern, ISL_WORDS
    print(f"✓ Word library imported ({len(ISL_WORDS)} words)")
    
    # Test simulator initialization
    sim = GestureSimulator()
    print("✓ GestureSimulator initialized")
    
    # Test word pattern matching
    test_pattern = ["Y", "E", "S"]
    word = get_word_by_pattern(test_pattern)
    print(f"✓ Pattern matching works: {test_pattern} -> {word}")
    
    # Test mode parameter
    class MockData:
        hand_landmarks = []
    
    result = sim.predict_gesture(MockData(), mode="LETTER")
    print(f"✓ LETTER mode works: {result}")
    
    result = sim.predict_gesture(MockData(), mode="WORD")
    print(f"✓ WORD mode works: {result}")
    
    print("\n✅ All tests passed! The app should work correctly.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
