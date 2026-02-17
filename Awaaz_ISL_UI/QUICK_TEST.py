"""
QUICK TEST FOR WORD MODE
========================

This script will help you verify word mode is working.

BEFORE RUNNING THE APP:
1. Make sure you've restarted the app to load the latest code
2. The app must be closed before running it again

TO TEST WORD MODE:
1. Run: python main.py
2. Click "Start Camera"
3. Click "Switch to WORD Mode"
4. Try signing: Y -> E -> S (for "YES")

WHAT YOU SHOULD SEE:
- CURRENT WORD field shows: "Y" then "YE" then "YES"
- When complete, "YES" appears in SENTENCE OUTPUT
- Console shows: [WORD MODE] messages

CONSOLE OUTPUT TO LOOK FOR:
[WORD MODE] Added 'Y' (type: <class 'numpy.str_'>) -> Sequence: ['Y']
[WORD MODE] Checking sequence ['Y'] against word patterns...
[WORD MODE] No match found for ['Y']
[WORD MODE] Added 'E' (type: <class 'numpy.str_'>) -> Sequence: ['Y', 'E']
[WORD MODE] Checking sequence ['Y', 'E'] against word patterns...
[WORD MODE] No match found for ['Y', 'E']
[WORD MODE] Added 'S' (type: <class 'numpy.str_'>) -> Sequence: ['Y', 'E', 'S']
[WORD MODE] Checking sequence ['Y', 'E', 'S'] against word patterns...
[WORD MODE] ✓ MATCHED WORD: YES

IF YOU DON'T SEE CONSOLE MESSAGES:
- The model might not be detecting letters correctly
- Try LETTER mode first to verify letters are being detected
- Check camera is working and hand is visible

AVAILABLE WORDS TO TEST:
- YES (Y-E-S) - easiest to test
- NO (N-O) - very short
- HELP (H-E-L-P)
- GOOD (G-O-O-D)
- BAD (B-A-D)
- LOVE (L-O-V-E)
- HELLO (H-E-L-L-O)
- SORRY (S-O-R-R-Y)
- PLEASE (P-L-E-A-S-E)
- THANK YOU (T-H-A-N-K)

TIPS:
- Hold each letter for 1-2 seconds
- Don't wait more than 5 seconds between letters
- Watch the CURRENT WORD field - it shows your progress!
"""

print(__doc__)

# Quick verification
print("\n" + "="*60)
print("QUICK VERIFICATION")
print("="*60)

try:
    from word_library import ISL_WORDS
    from gesture_simulator import GestureSimulator
    
    print(f"✓ Word library loaded: {len(ISL_WORDS)} words available")
    
    sim = GestureSimulator()
    print(f"✓ Gesture simulator initialized")
    print(f"  - Model loaded: {sim.model is not None}")
    print(f"  - Word timeout: {sim.word_timeout} seconds")
    
    print("\n✓ ALL COMPONENTS READY!")
    print("\nYou can now run: python main.py")
    print("Then switch to WORD mode and try signing YES (Y-E-S)")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("Please make sure all files are in place")
