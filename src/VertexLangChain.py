import vertexai
from langchain.llms import VertexAI


class VertexLangChain:

    def __init__(self, project_id, region, model_name="text-bison@001", max_output_tokens=1000):
        self.project_id = project_id
        self.region = region
        vertexai.init(project=self.project_id, location=self.region)
        self.llm = VertexAI(model_name=model_name, max_output_tokens=max_output_tokens)

    def get_vertexai(self):
        return self.llm

    def predict(self, prompt):
        return self.llm.predict(prompt)
