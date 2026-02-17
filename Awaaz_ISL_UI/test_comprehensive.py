"""
Comprehensive test of word matching with numpy strings from model
"""
import pickle
import numpy as np
from word_library import get_word_by_pattern, ISL_WORDS

# Load actual model
with open('model.p', 'rb') as f:
    model = pickle.load(f)['model']

print("=" * 60)
print("WORD LIBRARY PATTERNS:")
print("=" * 60)
for word, data in ISL_WORDS.items():
    pattern = data['pattern']
    print(f"{word:12} -> {pattern}")

print("\n" + "=" * 60)
print("TESTING WITH NUMPY STRINGS (as model outputs):")
print("=" * 60)

# Simulate model predictions for YES
yes_sequence_numpy = [np.str_('Y'), np.str_('E'), np.str_('S')]
print(f"\nSequence (numpy): {yes_sequence_numpy}")
print(f"Type check: {[type(x) for x in yes_sequence_numpy]}")
result = get_word_by_pattern(yes_sequence_numpy)
print(f"Match result: {result}")
print(f"Expected: YES")
print(f"SUCCESS: {result == 'YES'}")

# Test HELLO
hello_sequence = [np.str_('H'), np.str_('E'), np.str_('L'), np.str_('L'), np.str_('O')]
print(f"\nSequence (numpy): {hello_sequence}")
result = get_word_by_pattern(hello_sequence)
print(f"Match result: {result}")
print(f"Expected: HELLO")
print(f"SUCCESS: {result == 'HELLO'}")

# Test NO
no_sequence = [np.str_('N'), np.str_('O')]
print(f"\nSequence (numpy): {no_sequence}")
result = get_word_by_pattern(no_sequence)
print(f"Match result: {result}")
print(f"Expected: NO")
print(f"SUCCESS: {result == 'NO'}")

print("\n" + "=" * 60)
print("TESTING LIST EQUALITY:")
print("=" * 60)
pattern_from_lib = ISL_WORDS['YES']['pattern']
print(f"Library pattern: {pattern_from_lib} (type: {type(pattern_from_lib[0])})")
print(f"Numpy sequence:  {yes_sequence_numpy} (type: {type(yes_sequence_numpy[0])})")
print(f"Are they equal? {pattern_from_lib == yes_sequence_numpy}")

# Element by element
print("\nElement-by-element comparison:")
for i, (lib, test) in enumerate(zip(pattern_from_lib, yes_sequence_numpy)):
    print(f"  [{i}] '{lib}' == '{test}' ? {lib == test} (types: {type(lib)} vs {type(test)})")
