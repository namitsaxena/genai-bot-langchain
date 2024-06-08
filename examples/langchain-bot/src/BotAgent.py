from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.agents import AgentType, initialize_agent
from src.agents.ToolFactory import get_tools

MODEL_NAME = "text-bison@001"


# sets up a chat agent (with conversation history)
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
        :return:
        """
        chat_history = MessagesPlaceholder(variable_name="chat_history")
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        tools = get_tools()

        self.agent = initialize_agent(
            tools,
            self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            agent_kwargs={
                "memory_prompts": [chat_history],
                "input_variables": ["input", "agent_scratchpad", "chat_history"]
            },
            memory=memory,
        )

    def process(self, prompt):
        if self.is_agent_enabled:
            return self.agent.run(prompt)
        else:
            return self.llm(prompt)
