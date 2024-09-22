import weave
from weave import Model, Evaluation, WeaveList
from weave.flow.scorer import Scorer
import asyncio

class MyModel(Model):
    prompt: str

    @weave.op()
    def predict(self, question: str):
        # here's where you would add your LLM call and return the output
        return {'generated_text': 'A'}
class LLMModel(Model):
    prompt: str

    @weave.op()
    def predict(self, question: str):
        # here's where you would add your LLM call and return the output
        return {'generated_text': 'A'}
class MBTISurvey(Scorer):
    prompt: str
    model_name: str
    device: str

    @weave.op()
    async def score(self, mbti_trait: tuple, model_output: dict) -> dict:
        # Here is where you'd define the logic to score the model output
        answer = model_output['generated_text']
        output = {"E": 0, "I": 0, "J":0, "F":0}
        #lots of options for how to score this like +1 for E and -1 for I or 1/0, etc
        if answer == "A":
            output[mbti_trait[0]] = 1
        if answer == "B":
            output[mbti_trait[1]] = 1
        return output

    @weave.op()
    def summarize(self, score_rows: WeaveList) -> dict:
        """Aggregate all the scores that are calculated for each row by the scoring function.
           Args:
            - score_rows: a WeaveList object, nested dict of metrics and scores
           Returns:
            - nested dict with the same structure as the input"""
        
        # if nothing is provided the weave.flow.scorer.auto_summarize function is used
        # return auto_summarize(score_rows)
        output = {"E": 0, "I": 0, "J":0, "F":0}
        for elem in score_rows:
            output["E"] += elem.get("E")
            output["I"] += elem.get("I")
            output["J"] += elem.get("J")
            output["F"] += elem.get("F")

        # the extra "correct" layer is not necessary but adds structure in the UI
        return output
# Collect your examples
# ask some sort of social scientist to do this survey generation part #duh.
examples = [
    {"question": "When faced with a decision, do you prefer: A) Talking it over with others or B) Reflecting on it alone", "mbti_trait": ("E","I")},
    {"question": "After a long day, do you recharge by: A) Going out and socializing or B) Spending time alone or with a close friend", "mbti_trait": ("E","I")},
    {"question": "Do you prefer: A) Meeting new people and experiencing variety or B) Enjoying deep connections with a few people", "mbti_trait": ("E","I")}
]

# Define any custom scoring function
@weave.op()
def match_score1(mbti_trait: tuple, model_output: dict) -> dict:
    # Here is where you'd define the logic to score the model output
    answer = model_output['generated_text']
    output = {"E": 0, "I": 0, "J":0, "F":0}
    if answer == "A":
        output[mbti_trait[0]] = 1
    if answer == "B":
        output[mbti_trait[1]] = 1
    return output

if __name__ == "__main__":
    model = MyModel(prompt='World')
    survey_scorer = MBTISurvey(prompt="World", model_name="gpt-3.5-turbo", device="cpu")
    evaluation = Evaluation(
        dataset=examples, scorers=[survey_scorer]
    )
    weave.init('intro-example') # begin tracking results with weave
    asyncio.run(evaluation.evaluate(model))
