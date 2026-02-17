from word_library import get_word_by_pattern, ISL_WORDS

print("=== WORD LIBRARY DEBUG ===\n")

# Show all word patterns
print("Available word patterns:")
for word, data in ISL_WORDS.items():
    pattern = data["pattern"]
    print(f"  {word}: {pattern} (types: {[type(x).__name__ for x in pattern]})")

print("\n=== TESTING PATTERN MATCHING ===\n")

# Test cases
test_cases = [
    (["Y", "E", "S"], "YES"),
    (["H", "E", "L", "L", "O"], "HELLO"),
    (["N", "O"], "NO"),
    (["H", "E", "L", "P"], "HELP"),
]

for pattern, expected in test_cases:
    result = get_word_by_pattern(pattern)
    status = "✓ PASS" if result == expected else "✗ FAIL"
    print(f"{status}: Pattern {pattern} -> Result: {result} (Expected: {expected})")
    
    # Debug: Check if pattern exists in library
    if result != expected:
        print(f"  DEBUG: Checking exact match...")
        for word, data in ISL_WORDS.items():
            if data["pattern"] == pattern:
                print(f"    Found exact match: {word}")
            elif len(data["pattern"]) == len(pattern):
                print(f"    Same length as {word}: {data['pattern']}")
                for i, (a, b) in enumerate(zip(pattern, data["pattern"])):
                    if a != b:
                        print(f"      Mismatch at index {i}: '{a}' ({type(a)}) != '{b}' ({type(b)})")
