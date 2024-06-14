from src.BotAgent import BotAgent
from src.VertexLangChain import VertexLangChain

###################
# constants
###################
from src.app.ChatWebApp import ChatWebApp

PROJECT_ID = "nsx-sandbox"  # @param {type:"string"}
REGION = "us-central1"  # @param {type:"string"}
TEMPLATES_DIR = "../../resources/templates"


def get_bot_instance(gcp_project_id, gcp_region):
    llm = VertexLangChain(gcp_project_id, gcp_region)
    return BotAgent(llm.get_vertexai())


def get_app_instance(gcp_project_id, gcp_region, templates_dir_path=None):
    bot = get_bot_instance(gcp_project_id, gcp_region)
    return ChatWebApp(bot)
