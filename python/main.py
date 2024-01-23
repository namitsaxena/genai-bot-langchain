# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import vertexai

# import pandas as pd
# import seaborn as sns
# from IPython.display import Markdown, display
# from sklearn.metrics.pairwise import cosine_similarity


PROJECT_ID = "nsx-sandbox"  # @param {type:"string"}
REGION = "us-central1"  # @param {type:"string"}

# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=REGION)

from vertexai.language_models import (
    TextGenerationModel,
    # TextEmbeddingModel,
    # ChatModel,
    # InputOutputTextPair,
    # CodeGenerationModel,
    # CodeChatModel,
)

# Uses only TextGenerationModel (From vertexai)
def text_generation(prompt="What is a large language model?", model="text-bison@001"):
    print(f'Querying: model: {model}, Prompt: {prompt}')
    generation_model = TextGenerationModel.from_pretrained(model)
    response = generation_model.predict(prompt=prompt)
    print(response.text)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    text_generation("What is an embedding in an LLM", "text-bison@001")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
