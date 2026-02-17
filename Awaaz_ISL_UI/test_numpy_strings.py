"""
Test to simulate actual word mode behavior
"""
import pickle

# Load model
with open('model.p', 'rb') as f:
    model_data = pickle.load(f)
    model = model_data['model']

print("Model classes (first 10):", model.classes_[:10])
print("Model class type:", type(model.classes_[0]))

# Simulate a prediction
import numpy as np
dummy_features = np.random.rand(1, 42)  # 42 features for hand landmarks
prediction = model.predict(dummy_features)
print(f"\nSample prediction: {prediction[0]}")
print(f"Prediction type: {type(prediction[0])}")

# Test word matching
from word_library import get_word_by_pattern

# Simulate detecting Y, E, S in sequence
test_sequence = ['Y', 'E', 'S']
print(f"\nTest sequence: {test_sequence}")
result = get_word_by_pattern(test_sequence)
print(f"Match result: {result}")

# Check if numpy string vs regular string matters
import numpy as np
numpy_seq = [np.str_('Y'), np.str_('E'), np.str_('S')]
print(f"\nNumpy string sequence: {numpy_seq}")
result2 = get_word_by_pattern(numpy_seq)
print(f"Match result with numpy strings: {result2}")

# Test comparison
print(f"\nDoes 'Y' == np.str_('Y')? {('Y' == np.str_('Y'))}")
print(f"Does ['Y'] == [np.str_('Y')]? {(['Y'] == [np.str_('Y')])}")
