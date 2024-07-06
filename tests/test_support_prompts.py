import unittest

from src.LLMFactory import get_llm
from src.LLMFactory import PROVIDER_VERTEX


class TestVertexSupportBot(unittest.TestCase):
    def setUp(self):
        self.llm = get_llm(PROVIDER_VERTEX)

    def test_context_table(self):
        # llm = VertexLangChain(PROJECT_ID, REGION)
        prompt = """
        Answer from the below context using the table and the example questions and answers: 
		context: 
		    | environment   | gke_context   | kcc_context   |
		    |   dv          |   anthos-dev  | kcc_dev       |
		    |   qa          |   anthos-qa  | kcc_qa       |
		    |   nr          |   anthos-ut  | kcc_ut       |
		Examples:
		Q: What is KCC conext for qa
		A: kcc_qa
		Q: What is the GKE context for qa
		A: anthos-qa    
		
		question: "What's the KCC cluster conext for environment dv" 
		Ansewer exactly in the format given in the examples in context 
        """
        prediction = self.llm.predict(prompt)
        print(f"Predication: {prediction}")

    def test_context_with_qna(self):
        context = """
        Answer from the below context using the table and the example questions and answers: 
		context:
		Given the following data describing GKE(Google Kubernetes Cluster) anthos cluster for GCP environments:
            |  environment          |  gke_context | kcc_context   |
		    |   dv, dev             |   anthos-dev  | kcc_dev       |
		    |   qa                  |   anthos-qa   | kcc_qa       |
		    |   nr,new release, ut  |   anthos-ut   | kcc_ut       |
		    |   pr, production      |   anthos-pr   | kcc_pr       |
		Examples:
		Q: What is KCC conext for qa
		A: kcc_qa
		Q: What is the GKE context for qa
		A: anthos-qa    

		question: "{query}" 
		Ansewer exactly in the format given in the examples in context 
        """

        query = "What's the KCC cluster context for environment dv"
        query = "What's the gke dev cluster for new release"
        query = "What's the gke dev cluster for production"
        prompt = context.replace("{query}", query)
        prediction = self.llm.predict(prompt)
        print(f"Predication: {prediction}")
