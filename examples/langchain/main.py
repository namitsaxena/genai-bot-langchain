# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import time

import vertexai
import os
from langchain.llms import VertexAI

from EmbeddingEngine import EmbeddingEngine
from GCSUtil import GCSUtil
from ReAct import ReActProcessor
from VectorSearch import VectorSearchDB

llm = None

PROJECT_ID = "nsx-sandbox"  # @param {type:"string"}
REGION = "us-central1"  # @param {type:"string"}
MODEL_NAME = "text-bison@001"  # @param {type:"string"}


def get_uid():
    from datetime import datetime
    return datetime.now().strftime("%m%d%H%M")


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
    # setupVertexAI()

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

    embeddings_json_file = "/tmp/questions.json"
    embed = EmbeddingEngine(PROJECT_ID, REGION)
    # if not os.path.exists(embeddings_json_file):
    #     print(f"embeddings file '{embeddings_json_file}' not found. creating new embeddings..")
    df = embed.load_data(50)
    df = embed.get_embeddings(df)
    embed.get_similarities(df)
    embed.export_embeddings(df, embeddings_json_file)
    # else:
    #     print(f"Embeddings already exist: {embeddings_json_file}")

    # Bucket create only if needed
    display_name_prefix = f"embvs-tutorial-index"
    uid = get_uid()
    display_name = f"{display_name_prefix}-{uid}"
    bucket_name = f"{display_name}"

    gcs = GCSUtil()
    bucket = None
    buckets = gcs.get_bucket_matching(display_name_prefix)
    if not buckets:
        print(f"No bucket found matching name prefix: {display_name_prefix}. Creating one")
        bucket = gcs.create_bucket(bucket_name, REGION)
        gcs.add_file(bucket.name, embeddings_json_file)
    else:
        print(f"bucket(s) already exists: {list(buckets)}. (first one will be used if more than one)")
        bucket = gcs.get_bucket(list(buckets)[0])

    bucket_uri = f"gs://{bucket.name}"
    print(f"Bucket uri: {bucket_uri}")

    try:
        vector_search = VectorSearchDB(PROJECT_ID, REGION)
        # TODO if existing bucket then vector search and bucket will have different names/id
        vector_search.create_index(display_name, bucket_uri)
        print("vector search index built!")

        time.sleep(60)  # TODO check if this resolves 503/SSL error
        print("Querying the vector...")
        # query
        query = "How to read JSON with Python?"
        test_embeddings = embed.get_embeddings_wrapper([query])
        response = vector_search.query(test_embeddings)

        # show the result
        import numpy as np

        for idx, neighbor in enumerate(response[0]):
            id = np.int64(neighbor.id)
            similar = df.query("id == @id", engine="python")
            print(f"{neighbor.distance:.4f} {similar.title.values[0]}")
    except Exception as e:
        print(f"Failed with error: {e}")
    finally:
        input("Press Enter to clean up...:")
        vector_search.destroy()
        # gcs.delete_bucket(bucket_name)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
