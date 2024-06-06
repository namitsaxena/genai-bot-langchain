import unittest

from src.BotAgent import BotAgent
from src.VertexLangChain import VertexLangChain

PROJECT_ID = "nsx-sandbox"  # @param {type:"string"}
REGION = "us-central1"  # @param {type:"string"}


class TestCodeBot(unittest.TestCase):

    def test_bot_history(self):
        llm = VertexLangChain(PROJECT_ID, REGION)
        react = BotAgent(llm.get_vertexai())
        user_name = "customer one"
        prediction = react.process(f"My name is {user_name}")
        print(f"Predication: {prediction}")
        prediction = react.process("Who am i?")
        print(f"Predication: {prediction}")
        assert user_name in prediction

    def test_agent_capabilities(self):
        llm = VertexLangChain(PROJECT_ID, REGION)
        react = BotAgent(llm.get_vertexai())
        user_name = "customer one"
        prediction = react.process(f"My name is {user_name}")
        print(f"Predication: {prediction}")

        prediction = react.process("What is today's date?")
        print(f"Predication: {prediction}")

        prediction = react.process("Who are you?")
        print(f"Predication: {prediction}")
        assert "NSBOT" in prediction

        prediction = react.process("Who am i?")
        print(f"Predication: {prediction}")
        assert user_name in prediction

    # LLM tries to interpret the results of the
    # kubernetes output as well
    # esp if it's successful
    def test_agent_custom_tool_class(self):
        llm = VertexLangChain(PROJECT_ID, REGION)
        agent = BotAgent(llm.get_vertexai())
        kubernetes_command = "kubectl get pods"
        prediction = agent.process(f"Can you execute the following kubernetes command: {kubernetes_command} in namespace: test_namespace.")
        print(f"Predication: {prediction}")
