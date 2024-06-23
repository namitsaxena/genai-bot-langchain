# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import vertexai
from langchain.llms import VertexAI

PROJECT_ID = "nsx-sandbox"  # @param {type:"string"}
REGION = "us-central1"  # @param {type:"string"}
MODEL_NAME = "text-bison@001"  # @param {type:"string"}

llm = None


# Initialize Vertex AI SDK
def setup_vertex_ai():
    vertexai.init(project=PROJECT_ID, location=REGION)
    global llm
    llm = VertexAI(model_name=MODEL_NAME, max_output_tokens=1000)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    setup_vertex_ai()

    # Simple Prediction Example
    prompt = "Write a 2-day itinerary for France."
    prediction = llm.predict(prompt)
    print(f"Predication: {prediction}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
