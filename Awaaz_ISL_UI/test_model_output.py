"""
Test to check what type of data the model returns
"""
import pickle
import numpy as np

print("=== MODEL OUTPUT TYPE TEST ===\n")

# Load model
try:
    with open('model.p', 'rb') as f:
        model_dict = pickle.load(f)
        model = model_dict['model']
    print("✓ Model loaded successfully\n")
    
    # Create dummy input (42 features for normalized x,y coordinates of 21 landmarks)
    dummy_input = np.random.rand(1, 42).tolist()
    
    # Get prediction
    prediction = model.predict(dummy_input)
    letter = prediction[0]
    
    print(f"Prediction result: {letter}")
    print(f"Type: {type(letter)}")
    print(f"Type name: {type(letter).__name__}")
    
    # Check if it's a numpy type
    if hasattr(letter, 'item'):
        print(f"Has .item() method (numpy type)")
        print(f"Converted: {letter.item()} (type: {type(letter.item())})")
    
    # Test comparison
    test_str = "A"
    print(f"\nComparison test:")
    print(f"  letter == '{test_str}': {letter == test_str}")
    print(f"  str(letter) == '{test_str}': {str(letter) == test_str}")
    
    # Test in list
    test_list = [letter, letter, letter]
    print(f"\nList test:")
    print(f"  List: {test_list}")
    print(f"  Types in list: {[type(x).__name__ for x in test_list]}")
    
    # Test pattern matching
    from word_library import get_word_by_pattern
    
    # Create a test sequence with model output type
    test_sequence = [letter, letter, letter]
    result = get_word_by_pattern(test_sequence)
    print(f"\nPattern matching test:")
    print(f"  Sequence: {test_sequence}")
    print(f"  Result: {result}")
    
    # Try with string conversion
    test_sequence_str = [str(x) for x in test_sequence]
    result_str = get_word_by_pattern(test_sequence_str)
    print(f"  Sequence (converted): {test_sequence_str}")
    print(f"  Result (converted): {result_str}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
