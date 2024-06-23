from langchain_google_vertexai import VertexAI
from langchain_core.prompts import PromptTemplate


def invoke_vertex(message="What are some of the pros and cons of Python as a programming language?"):
    model = VertexAI(model_name="gemini-pro")
    output = model.invoke(message)
    print(f"Output: {output}")
    # await model.ainvoke(message)


def invoke_chain():
    model = VertexAI(model_name="gemini-pro")
    template = """Question: {question}
    
    Answer: Let's think step by step."""
    prompt = PromptTemplate.from_template(template)

    chain = prompt | model

    question = """
    I have five apples. I throw two away. I eat one. How many apples do I have left?
    """
    print(chain.invoke({"question": question}))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    invoke_vertex("is milk a complete food source. explain")
    # invoke_chain()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
