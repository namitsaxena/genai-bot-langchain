# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import vertexai
import os
from langchain.llms import VertexAI

llm = None

PROJECT_ID = "nsx-sandbox"  # @param {type:"string"}
REGION = "us-central1"  # @param {type:"string"}
MODEL_NAME = "text-bison@001"  # @param {type:"string"}


# Initialize Vertex AI SDK
def setupVertexAI():
    vertexai.init(project=PROJECT_ID, location=REGION)
    global llm
    llm = VertexAI(model_name=MODEL_NAME, max_output_tokens=1000)

def chainOfThoughtExample():
    prompt = """Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
    Each can has 3 tennis balls. How many tennis balls does he have now?
    A: The answer is 11.
    Q: The cafeteria had 23 apples.
    If they used 20 to make lunch and bought 6 more, how many apples do they have?
    A:"""

    prompt = """Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
    Each can has 3 tennis balls. How many tennis balls does he have now?
    A: Roger started with 5 balls. 2 cans of 3 tennis balls
    each is 6 tennis balls. 5 + 6 = 11. The answer is 11.
    Q: The cafeteria had 23 apples.
    If they used 20 to make lunch and bought 6 more, how many apples do they have?
    A:"""

    prompt = """Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
    Each can has 3 tennis balls. How many tennis balls does he have now?
    A: The answer is 11.

    Q: The cafeteria had 23 apples.
    If they used 20 to make lunch and bought 6 more, how many apples do they have?
    A: Let's think step by step."""

    print(f"prompt: {prompt}")
    output = llm.predict(prompt)
    print(f"Predication: {output}")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    setupVertexAI()
    prompt = "Write a 2-day itinerary for France."
    # prompt = "Improve this description : In this notebook we'll explore advanced prompting techniques, and building ReAct agents using LangChain and Vertex AI "
    # prediction = llm.predict(prompt)
    # print(f"Predication: {prediction}")

    chainOfThoughtExample()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
