import weave

# Collect your examples
examples = [
    {"question": "When faced with a decision, do you prefer: A) Talking it over with others or B) Reflecting on it alone", "mbti_trait": "E/I"},
    {"question": "Who wrote 'To Kill a Mockingbird'?", "expected": "Harper Lee"},
    {"question": "What is the square root of 64?", "expected": "8"},
]

# Define any custom scoring function
@weave.op()
def match_score1(expected: str, model_output: dict) -> dict:
    # Here is where you'd define the logic to score the model output
    return {'match': expected == model_output['generated_text']}