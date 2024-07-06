from src.agents.BotAgent import BotAgent
from src.app.ChatWebApp import ChatWebApp
from src.LLMFactory import get_llm


###################
# constants
###################
TEMPLATES_DIR = "../../resources/templates"


def get_bot_instance():
    # get default llm provider
    llm = get_llm()
    return BotAgent(llm)


def get_app_instance(templates_dir_path=None):
    bot = get_bot_instance()
    return ChatWebApp(bot)
