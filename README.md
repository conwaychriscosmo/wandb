## Overview
This project was developed as part of the Weights and Biases (W&B) Hackathon centered around their exciting new product, Weave. The goal of the project is to explore how machine learning tools can be used to evaluate models, iterating from the initial personality_test.py script to a more advanced and dynamic assessment tool in dynamic_personality_assessment.py.  The personality assesment was selected as an example to ensure the technology is functional more than to assign an mbti type to any specific llm or assert that an llm would have a specific personality.  

## Special Thanks
A heartfelt thank you to the W&B team for providing an amazing hackathon experience. The food was fantastic, the company was delightful, and the team’s swift assistance and guidance made working through challenges a breeze. Your support has been greatly appreciated!

## Use Case and Value
The Dynamic Personality Assessment aims to assign integer values to multiple catagories that can then be aggregated in a custom scorer class for weave.

## Use cases include:
Getting up and running with Weave.

If you would like to lend your expertise to evaluating how easy llms are to talk to please reach out!

## Prerequisites
To run this project, you’ll need:

Python 3.8 or higher
Weights and Biases API (W&B account required)
Dependencies listed in the requirements.txt
Installation and Setup
Clone this repository:

bash
Copy code
git clone <repository-link>
cd <repository-folder>
Install the required Python packages:

bash
Copy code
pip install -r requirements.txt
Log in to Weights and Biases:

bash
Copy code
wandb login
Run the dynamic_personality_assessment.py script:

bash
Copy code
python dynamic_personality_assessment.py
Use Weave to visualize your data: Head over to your W&B dashboard and explore the rich set of visualization tools offered by Weave.

Notes
You can adjust various parameters in the script to fine-tune the assessment process.
Make sure your environment is set up correctly with the right API keys for W&B.