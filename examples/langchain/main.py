# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import vertexai
import os
from langchain.llms import VertexAI

from EmbeddingEngine import EmbeddingEngine
from ReAct import ReActProcessor

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


def chain_of_thought_self_consistency_example():
    from operator import itemgetter
    from langchain.prompts import PromptTemplate
    from langchain.schema import StrOutputParser
    from langchain.schema.runnable import RunnablePassthrough

    question = """The cafeteria had 23 apples.
    If they used 20 to make lunch and bought 6 more, how many apples do they have?"""

    context = """Answer questions showing the full math and reasoning.
    Follow the pattern in the example.
    """

    one_shot_exemplar = """Example Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
    Each can has 3 tennis balls. How many tennis balls does he have now?
    A: Roger started with 5 balls. 2 cans of 3 tennis balls
    each is 6 tennis balls. 5 + 6 = 11.
    The answer is 11.
    
    Q: """

    planner = (
            PromptTemplate.from_template(context + one_shot_exemplar + " {input}")
            | VertexAI()
            | StrOutputParser()
            | {"base_response": RunnablePassthrough()}
    )

    answer_1 = (
            PromptTemplate.from_template("{base_response} A: 33")
            | VertexAI(temperature=0, max_output_tokens=400)
            | StrOutputParser()
    )

    answer_2 = (
            PromptTemplate.from_template("{base_response} A:")
            | VertexAI(temperature=0.1, max_output_tokens=400)
            | StrOutputParser()
    )

    answer_3 = (
            PromptTemplate.from_template("{base_response} A:")
            | VertexAI(temperature=0.7, max_output_tokens=400)
            | StrOutputParser()
    )

    final_responder = (
            PromptTemplate.from_template(
                "Output all the final results in this markdown format: Result 1: {results_1} \n Result 2:{results_2} \n Result 3: {results_3}"
            )
            | VertexAI(max_output_tokens=1024)
            | StrOutputParser()
    )

    chain = (
            planner
            | {
                "results_1": answer_1,
                "results_2": answer_2,
                "results_3": answer_3,
                "original_response": itemgetter("base_response"),
            }
            | final_responder
    )

    answers = chain.invoke({"input": question})
    # display(Markdown(answers))
    print(f"Answers: {answers}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    setupVertexAI()

    # Simple Prediction Example
    prompt = "Write a 2-day itinerary for France."
    # prompt = "Improve this description : In this notebook we'll explore advanced prompting techniques, and building ReAct agents using LangChain and Vertex AI "
    # prediction = llm.predict(prompt)
    # print(f"Predication: {prediction}")

    # Chain of Thought Examples
    # chainOfThoughtExample()
    # chain_of_thought_self_consistency_example()

    # Tools with ReAct (short for Reasoning & Acting) setup
    # react = ReActProcessor(llm)
    # prediction = react.process("What is today's date?")
    # print(f"Predication: {prediction}")
    # prediction = react.process("Who are you?")
    # print(f"Predication: {prediction}")

    embed = EmbeddingEngine(PROJECT_ID, REGION)
    df = embed.load_data(50)
    df = embed.get_embeddings(df)
    embed.get_similarities(df)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
