"""
Quick test to verify word matching with actual model output format
"""
from word_library import get_word_by_pattern, ISL_WORDS

print("Testing with string letters (as model outputs):")
print("-" * 50)

# Test with actual string format from model
test_sequences = [
    ['Y', 'E', 'S'],
    ['N', 'O'],
    ['H', 'E', 'L', 'L', 'O'],
    ['H', 'E', 'L', 'P'],
    ['G', 'O', 'O', 'D'],
]

for seq in test_sequences:
    result = get_word_by_pattern(seq)
    print(f"Sequence: {seq} -> Match: {result}")

print("\n" + "=" * 50)
print("Available word patterns in library:")
print("=" * 50)
for word, data in ISL_WORDS.items():
    pattern = data['pattern']
    print(f"{word:12} -> {pattern}")
    # Check type of first element
    if pattern:
        print(f"             (pattern[0] type: {type(pattern[0])})")
