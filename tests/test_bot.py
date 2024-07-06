import unittest

from src.agents.BotAgent import BotAgent
# from src.VertexLangChain import VertexLangChain
from src.tools.ToolFunctions import BOT_NAME
from src.LLMFactory import get_llm
from src.LLMFactory import PROVIDER_OPENAI, PROVIDER_VERTEX

PROJECT_ID = "nsx-sandbox"  # @param {type:"string"}
REGION = "us-central1"  # @param {type:"string"}


class TestCodeBot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # llm = VertexLangChain(PROJECT_ID, REGION)
        # TestCodeBot.bot = BotAgent(llm.get_vertexai())
        llm = get_llm()
        TestCodeBot.bot = BotAgent(llm)


    def setUp(self):
        # llm = VertexLangChain(PROJECT_ID, REGION)
        # self.bot = BotAgent(llm.get_vertexai())
        # using same instance for all tests
        self.bot = TestCodeBot.bot

    # replying with bot's name instead of customer's name
    # if bot name removed from chain, works correctly
    def test_bot_history(self):
        user_name = "customer one"
        prediction = self.bot.process(f"My name is {user_name}")
        print(f"Predication: {prediction}")
        prediction = self.bot.process("Who am i?")
        print(f"Predication: {prediction}")
        assert user_name in prediction

    # starts failing when other predictions
    # are added in between (commented)
    # prediction is something like below (for the called functions)
    # Predication: Action: {"action": "get_job_status", "action_input": {"job_name": "my-job-2"}}
    def test_agent_capabilities(self):
        user_name = "customer one"
        prediction = self.bot.process(f"My name is {user_name}")
        print(f"Predication: {prediction}")

        # prediction = self.bot.process("What is today's date?")
        # print(f"Predication: {prediction}")
        #
        # prediction = self.bot.process("What is the time?")
        # print(f"Predication: {prediction}")

        prediction = self.bot.process("Who are you?")
        print(f"Predication: {prediction}")
        assert BOT_NAME in prediction

        prediction = self.bot.process("Who am i?")
        print(f"Predication: {prediction}")
        assert user_name in prediction

    def test_capability_time(self):
        """
        If the function is not clearly commented
        tries to get weather in san francisco
        and then errors
        Returns:

        """
        prompt = "what's the current time?"
        prediction = self.bot.process(prompt)
        print(f"Predication: {prediction}")

    def test_capability_agent_name(self):
        prediction = self.bot.process("Who are you?")
        print(f"Predication: {prediction}")
        assert BOT_NAME in prediction

    # gets capability from description
    # actual function is just a random name
    def test_capability_random_with_comments_desc(self):
        prompt = "give me a random number?"
        prediction = self.bot.process(prompt)

        print(f"Predication: {prediction}")
        # print("Intermediate Responses: " + prediction["intermediate_steps"])

    # observation: confuses between
    # scheduled and pipeline jobs

    # The code can parse and pass the job name
    # to the function
    def test_capability_scheduled_job(self):
        prompt = "what's the status of scheduler tool job my-job"
        prediction = self.bot.process(prompt)
        print(f"Predication: {prediction}")
        assert "running" in prediction

    # tests tools direct return functionality
    # returns agent's reply without any interpretation
    # the return_direct method has been set for this tool
    def test_capability_pipeline_job_direct_return(self):
        prompt = "what's the status of pipeline job my-job-2"
        prediction = self.bot.process(prompt)
        print(f"Predication: {prediction}")
        assert "pipeline job 'my-job-2' is running" == prediction

    # LLM tries to interpret the results of the
    # kubernetes output as well
    # esp if it's successful
    # reply varies by prompt
    # - The pods are running. or pod-1,.. are running
    def test_agent_custom_tool_class(self):
        kubernetes_command = "kubectl get pods"
        prompt = f"Can you execute the following kubernetes command: {kubernetes_command} in namespace: test_namespace."
        prediction = self.bot.process(prompt)
        print(f"Predication: {prediction}")
        # the final response fluctuates depending on the prompt
        assert "pod-1" in prediction or "running" in prediction

    def test_non_tool_question(self):
        prompt = "what's the weather right now"
        prediction = self.bot.process(prompt)
        print(f"Predication: {prediction}")
        # I don't have access to weather information.
        assert "access" in prediction
