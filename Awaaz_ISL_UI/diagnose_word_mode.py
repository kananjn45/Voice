"""
Simple diagnostic to test if word mode is actually being triggered
"""
import sys
sys.path.insert(0, '.')

from gesture_simulator import GestureSimulator
from word_library import ISL_WORDS
import time

print("=" * 60)
print("WORD MODE DIAGNOSTIC TEST")
print("=" * 60)

# Initialize simulator
sim = GestureSimulator()

print("\n1. Testing simulator initialization...")
print(f"   Model loaded: {sim.model is not None}")
print(f"   Letter sequence: {sim.letter_sequence}")
print(f"   Word timeout: {sim.word_timeout} seconds")

print("\n2. Available words in library:")
for word, data in ISL_WORDS.items():
    print(f"   {word:12} -> {data['pattern']}")

print("\n3. Simulating letter sequence for 'YES'...")
print("   (This simulates what happens when you sign Y, then E, then S)")

# Create mock hand data
class MockHand:
    def __init__(self):
        self.hand_landmarks = []

# We can't actually test without real hand data, but we can check the flow
print("\n4. Testing word matching directly...")
from word_library import get_word_by_pattern

test_cases = [
    (['Y', 'E', 'S'], 'YES'),
    (['N', 'O'], 'NO'),
    (['H', 'E', 'L', 'P'], 'HELP'),
]

all_passed = True
for sequence, expected in test_cases:
    result = get_word_by_pattern(sequence)
    passed = result == expected
    all_passed = all_passed and passed
    status = "✓" if passed else "✗"
    print(f"   {status} {sequence} -> {result} (expected: {expected})")

print("\n" + "=" * 60)
if all_passed:
    print("✓ ALL TESTS PASSED - Word matching logic is working!")
    print("\nIf words still don't work in the app, the issue is likely:")
    print("  1. Letters not being detected correctly by the model")
    print("  2. Sequence timing out before completion")
    print("  3. UI not updating properly")
    print("\nTo debug further:")
    print("  - Run the app and switch to WORD mode")
    print("  - Watch the console for [WORD MODE] messages")
    print("  - Try signing Y-E-S slowly")
    print("  - Share the console output with me")
else:
    print("✗ TESTS FAILED - Word matching has issues!")

print("=" * 60)
