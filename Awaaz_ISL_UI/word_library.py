"""
ISL Word Library
Contains common Indian Sign Language words with their gesture patterns.
This library is used for word-level recognition in WORD mode.
"""

# Common ISL words with their characteristic patterns
ISL_WORDS = {
    "HELLO": {
        "description": "Wave gesture with open palm",
        "pattern": ["H", "E", "L", "L", "O"],
        "gesture_type": "dynamic"
    },
    "THANK YOU": {
        "description": "Hand moves from chin forward",
        "pattern": ["T", "H", "A", "N", "K"],
        "gesture_type": "dynamic"
    },
    "PLEASE": {
        "description": "Circular motion on chest with open palm",
        "pattern": ["P", "L", "E", "A", "S", "E"],
        "gesture_type": "dynamic"
    },
    "YES": {
        "description": "Fist nodding motion",
        "pattern": ["Y", "E", "S"],
        "gesture_type": "dynamic"
    },
    "NO": {
        "description": "Index and middle finger closing motion",
        "pattern": ["N", "O"],
        "gesture_type": "dynamic"
    },
    "SORRY": {
        "description": "Fist rotating on chest",
        "pattern": ["S", "O", "R", "R", "Y"],
        "gesture_type": "dynamic"
    },
    "HELP": {
        "description": "One hand supporting the other",
        "pattern": ["H", "E", "L", "P"],
        "gesture_type": "static"
    },
    "GOOD": {
        "description": "Thumbs up gesture",
        "pattern": ["G", "O", "O", "D"],
        "gesture_type": "static"
    },
    "BAD": {
        "description": "Thumbs down gesture",
        "pattern": ["B", "A", "D"],
        "gesture_type": "static"
    },
    "LOVE": {
        "description": "Crossed arms over chest",
        "pattern": ["L", "O", "V", "E"],
        "gesture_type": "static"
    }
}

def get_word_by_pattern(letter_sequence):
    """
    Match a sequence of letters to a known ISL word.
    
    Args:
        letter_sequence: List of letters detected in sequence
        
    Returns:
        Word name if matched, None otherwise
    """
    for word, data in ISL_WORDS.items():
        if data["pattern"] == letter_sequence:
            return word
    return None

def get_all_words():
    """Get list of all available ISL words"""
    return list(ISL_WORDS.keys())

def get_word_description(word):
    """Get description of a specific word"""
    return ISL_WORDS.get(word, {}).get("description", "")
