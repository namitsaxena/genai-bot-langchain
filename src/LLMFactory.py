import os

import vertexai
from langchain.llms import VertexAI
from langchain_openai import ChatOpenAI
import os

# constants
# providers
PROVIDER_OPENAI = "openai"
PROVIDER_VERTEX = "vertex"
# Vertex/GCP
PROJECT_ID = "nsx-sandbox"  # @param {type:"string"}
REGION = "us-central1"  # @param {type:"string"}
# OpenAI
os.environ["OPENAI_API_KEY"] = "ANYDUMMYVALUE"
os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"


# default provider will be supplied
# unless specifically asked for
def get_llm(provider=PROVIDER_VERTEX):
    if provider == PROVIDER_VERTEX:
        return get_vertex_llm(PROJECT_ID, REGION)
    elif provider == PROVIDER_OPENAI:
        return get_openai_llm()
    else:
        raise Exception("Unknown provider specified: " + provider)


#############################
# get vertex llm
#############################
def get_vertex_llm(project_id, region, model_name="text-bison@001", max_output_tokens=1000):
    vertexai.init(project=project_id, location=region)
    llm = VertexAI(model_name=model_name, max_output_tokens=max_output_tokens)
    return llm


#############################
# api key: for local llama can be any dummy value (but not blank/null) or OPENAI_API_KEY
# base_url: address to llama server (OPENAI_API_BASE)
# https://python.langchain.com/v0.2/docs/integrations/chat/openai/
#############################
def get_openai_llm():
    llm = ChatOpenAI(
        temperature=0,
        max_tokens=2048,
        timeout=None,
        max_retries=1,
        # api_key="any_dummy_val",
        # base_url="http://localhost:8000/v1",
        # organization="...",
        # other params...
    )
    return llm
