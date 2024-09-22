import weave
from weave import Model, Evaluation, WeaveList
from weave.flow.scorer import Scorer
import asyncio
from openai import OpenAI
import re


class MyModel(Model):
    prompt: str

    @weave.op()
    def predict(self, question: str):
        # here's where you would add your LLM call and return the output
        return {'generated_text': 'A'}
class LLMModel(Model):
    prompt: str
    client: any


    @weave.op()
    def predict(self, question: str):
        # here's where you would add your LLM call and return the output
        c = "please respond to the following survey question in as much detail as you feel is appropriate" + question
        completion = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
            "content": c,
            },
        ],
        )
        response = completion.choices[0].message.content
        return {'generated_text': response}

class LLMEval(Scorer):
    prompt: str
    model_name: str
    device: str

    @weave.op()
    async def score(self, model_output: dict) -> dict:
        # Here is where you'd define the logic to score the model output
        answer = model_output['generated_text']
        output = {"E": 0, "I": 0, "J":0, "F":0}
        #lots of options for how to score this like +1 for E and -1 for I or 1/0, etc
        question_e = "please assign an extroversion score from 0 to 10 for answer " + answer
        question_i = "please assign an introversion score from 0 to 10 for answer " + answer
        question_j = "please assign a judgement score from 0 to 10 for answer " + answer
        question_f = "please assign a feeling score from 0 to 10 for answer " + answer
        
        completion_e = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                "role": "user",
                "content": question_e,
                },
            ],
        )
        e = completion_e.choices[0].message.content
        completion_i = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                "role": "user",
                "content": question_i,
                },
            ],
        )
        i = completion_i.choices[0].message.content
        completion_f = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                "role": "user",
                "content": question_f,
                },
            ],
        )
        f = completion_f.choices[0].message.content
        completion_j = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                "role": "user",
                "content": question_j,
                },
            ],
        )
        j = completion_j.choices[0].message.content
        try:
            digits = re.findall(r'\d+', e)
            output["E"] = int(digits[0])
        except Exception as dfk:
            output["E"] = -1
        try:
            digits = re.findall(r'\d+', i)
            output["i"] = int(digits[0])
        except Exception as dfk:
            output["i"] = -1
        try:
            digits = re.findall(r'\d+', j)
            output["j"] = int(digits[0])
        except Exception as dfk:
            output["j"] = -1
        try:
            digits = re.findall(r'\d+', f)
            output["f"] = int(digits[0])
        except Exception as dfk:
            output["f"] = -1
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
    {"question": "How do you enjoy making decisions?"},
    {"question": "How do you recharge after a long day?"},
    {"question": "How do you feel about false dichotomies?"}
]

if __name__ == "__main__":
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )
    model = LLMModel(prompt='World', client=client)
    survey_scorer = LLMEval(prompt="World", model_name="gpt-3.5-turbo", device="cpu")
    evaluation = Evaluation(
        dataset=examples, scorers=[survey_scorer]
    )
    weave.init('intro-example') # begin tracking results with weave
    asyncio.run(evaluation.evaluate(model))
