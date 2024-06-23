from langchain.tools import StructuredTool
from langchain.agents import AgentType, initialize_agent, load_tools
# from langchain.tools import WikipediaQueryRun
# from langchain.utilities import WikipediaAPIWrapper
# import wikipedia


def get_current_date():
    """
    Gets the current date (today), in the format YYYY-MM-DD
    """
    from datetime import datetime
    todays_date = datetime.today().strftime("%Y-%m-%d")
    return todays_date


class ReActProcessor:

    def __init__(self, llm, use_agent=True):
        self.llm = llm
        self.agent = None
        print(f"Initializing ReActProcessor..")
        self.is_agent_enabled = use_agent
        if self.is_agent_enabled:
            self.setup_agent()

    def setup_agent(self):
        t_get_current_date = StructuredTool.from_function(
            # Note: func is NOT get_current_date() i.e.
            # the function's reference is sent to the callable rather than executing the function itself.
            func=get_current_date
            # ,name="today's date"
            # ,description="used to lookup today's date",
        )

        t_my_name = StructuredTool.from_function(self.get_my_name)

        tools = [
            t_get_current_date,
            t_my_name,
        ]

        self.agent = initialize_agent(
            tools,
            self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

    # expects doc string in this case
    # since description is not provided above
    # but didn't ask for the same in the other function(TODO)
    # What's your name, who are you both work
    def get_my_name(self):
        """
        :returns my name
        :return: the name of the agent
        """
        return "NSBOT"

    def process(self, prompt):
        if self.is_agent_enabled:
            return self.agent.run(prompt)
        else:
            return self.llm(prompt)
