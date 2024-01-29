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

# Import only what is strictly needed
from vertexai.language_models import (
    TextGenerationModel,
    # TextEmbeddingModel,
    ChatModel,
    # InputOutputTextPair,
    # CodeGenerationModel,
    # CodeChatModel,
)


# Uses only TextGenerationModel (From vertexai)
def text_generation(
          prompt="What is a large language model?"
        , temperature=0.0  # 0.0 - 1.0
        , max_output_tokens=128  # 1-1024
        , top_p=0.95  # 0.0 - 1.0
        , top_k=40  # 0.0 - 40
        , model="text-bison@001"
):
    print(f'Querying: model: {model}, Prompt: {prompt}')
    generation_model = TextGenerationModel.from_pretrained(model)
    response = generation_model.predict(
        prompt=prompt
        , temperature=temperature
        , max_output_tokens=max_output_tokens
        , top_p=top_p
        , top_k=top_k
    )
    print(response.text)

def chatting(
    prompt="Hello! Can you write a 300 word abstract for a research paper I need to write about the impact of AI on society?"
):
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    chat = chat_model.start_chat()

    print(chat.send_message(prompt))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # #####################################
    # TEXT
    # #####################################
    my_industry = "tech"
    # prompt example example
    prompt = f"""Create a numbered list of 10 items. Each item in the list should
        be a trend in the {my_industry} industry.

        Each trend should be less than 5 words."""

    # temperature example prompt
    # prompt = "Complete the sentence: As I prepared the picture frame, I reached into my toolkit to fetch my:"

    # top_p example
    # prompt = "Create a marketing campaign for jackets that involves blue elephants and avocados."

    # top_k example
    prompt = "Write a 2-day itinerary for France."

    # text_generation(
    #       prompt=prompt
    #     , temperature=0
    #     , max_output_tokens=1024
    #     , top_p=0.95
    #     , top_k=40
    # )

    # #####################################
    # CHAT
    # #####################################
    chatting()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
