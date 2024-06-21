from gc import set_debug

from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.agents import AgentType, initialize_agent
from src.tools.ToolFactory import get_tools
import json

MODEL_NAME = "text-bison@001"


# sets up a chat agent (with conversation history)
def set_verbose(param):
    pass


class BotAgent:

    def __init__(self, llm, use_agent=True):
        self.llm = llm
        self.agent = None
        print(f"Initializing BotAgent..")
        self.is_agent_enabled = use_agent
        tools = None
        if self.is_agent_enabled:
            self.setup_agent()
        self.bot = None

    def setup_agent(self):
        """
        sets up agent with chat history
        if intermediate steps
            - `run` not supported when there is not exactly one output key. Got ['output', 'intermediate_steps'].
        :return:
        """
        print("Initializing the agent")
        chat_history = MessagesPlaceholder(variable_name="chat_history")
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        tools = get_tools()

        self.agent = initialize_agent(
            tools,
            self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            debug=True,
            agent_kwargs={
                "memory_prompts": [chat_history],
                "input_variables": ["input", "agent_scratchpad", "chat_history"]
            },
            memory=memory,
            return_intermediate_steps=False
        )

        # https://python.langchain.com/v0.1/docs/guides/development/debugging/
        # set_debug(True) # printing GC collector, etc details but not input/outputs
        # set_verbose(True)

    def process(self, prompt):
        response = None
        if self.is_agent_enabled:
            response = self.agent.run(prompt)
        else:
            response = self.llm(prompt)

        if "action_input" in response:
            print(f"Unexpected response found: {response}")
            try:
                json_output = json.loads(response)
                return json_output["action_input"]
            except ValueError as e:
                print(f"failed to parse json: {response}")
                if self.is_agent_enabled:
                    self.setup_agent()
                return "Sorry I had a an error with this!! Can you ask again"

        return response
