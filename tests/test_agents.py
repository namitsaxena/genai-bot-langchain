import unittest

from langchain.globals import set_debug
from langchain.memory import ConversationBufferMemory

from src.LLMFactory import get_llm
from src.LLMFactory import PROVIDER_OPENAI, PROVIDER_VERTEX
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder
from src.tools.ToolFactory import get_tools


def _handle_error(error) -> str:
    print("Agent erred:- " + str(error))
    return str(error)[:50]


class TestAgents(unittest.TestCase):

    def setUp(self):
        print("opeai test: performing setup...")

    # https://api.python.langchain.com/en/latest/agents/langchain.agents.react.agent.create_react_agent.html
    # Issues:
    #  - recognizes tools but doesn't call
    #  - when it calls, it passes incorrect input
    #  - even if it passes inputput gets correct output back, it fails to parse and then retries with diff  prompt
    # ToDo
    #  - change prompt template
    #  - try different agent type
    #  - try a custom parser
    # can recognize tools based on input but doesn't get the answer
    #  ex: knows that it needs to run some_function for random number but then doesn't call and hallucinates the answer
    # runs certain jobs but with incorrect input
    # Example: see pipeline job input is some incorrect observation: getting status of pipeline job: 'job1
    #         Observation: job1 is not a valid job name.
    # '
    def test_react_agent(self):
        llm = get_llm(PROVIDER_VERTEX)
        # template = '''Answer the following questions as best you can. You have access to the following tools:
        #
        # {tools}
        #
        # Use the following format:
        #
        # Question: the input question you must answer
        # Thought: you should always think about what to do
        # Action: the action to take, should be one of [{tool_names}]
        # Action Input: the input to the action
        # Observation: the result of the action
        # ... (this Thought/Action/Action Input/Observation can repeat 1 times)
        # Thought: I now know the final answer
        # Final Answer: the final answer to the original input question
        #
        # Begin!
        #
        # Question: {input}
        # Thought:{agent_scratchpad}'''

        template = '''Answer the following questions as best you can. You have access to the following tools:

        {tools}

        Use the following format:

        ```
        Thought: Do I need to use a tool? No
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ```
        
        When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
        
        ```
        Thought: Do I need to use a tool?
        Final Answer: [your response here]
        ```
        Begin!
        
        
        New input: {input}
        {agent_scratchpad}
        Previous conversation history:
        {chat_history}
        '''

        tools = get_tools()
        prompt = PromptTemplate.from_template(template)
        self.agent = create_react_agent(llm, tools, prompt)
        # no checks for flags
        self.agent_executor = AgentExecutor(
              agent=self.agent
            , tools=tools
            , handle_parsing_errors=True
            # , handle_parsing_errors = _handle_error
            , verbose=True
            , return_intermediate_steps=False
        )
        self.agent_executor.max_iterations = 2

        # haven't tested this yet
        chat_history = MessagesPlaceholder(variable_name="chat_history")
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent_executor.memory = memory

        set_debug(False)

        # question = "what's the status of jenkins pipeline job job1?"
        question = "what's today's date?"
        # question = "what's your name?"
        # question = "can you execute kubernetes command: kubectl get pods"
        # question = "time now\n\nAction: get_current_time"
        # question = "give me a random number"
        # question = "what's the status of scheduler job job1?"
        response = self.agent_executor.invoke({"input": question})
        print(f"Response: {response}")

