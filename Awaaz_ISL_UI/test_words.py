"""
Test word mode functionality
"""
from word_library import get_word_by_pattern, ISL_WORDS

print("Testing word library...")
print(f"Total words: {len(ISL_WORDS)}\n")

# Test patterns
test_cases = [
    (["Y", "E", "S"], "YES"),
    (["H", "E", "L", "L", "O"], "HELLO"),
    (["N", "O"], "NO"),
    (["H", "E", "L", "P"], "HELP"),
    (["A", "B", "C"], None),  # Should not match
]

print("Testing pattern matching:")
for pattern, expected in test_cases:
    result = get_word_by_pattern(pattern)
    status = "✓" if result == expected else "✗"
    print(f"{status} Pattern {pattern} -> {result} (expected: {expected})")

print("\nAll word patterns:")
for word, data in ISL_WORDS.items():
    print(f"  {word}: {data['pattern']}")
