

## Installation
* create and activate virtual env
* Upgrade pip
  ```
	| => pip3 install --upgrade pip
	Collecting pip
	  Using cached pip-24.0-py3-none-any.whl (2.1 MB)
	Installing collected packages: pip
	  Attempting uninstall: pip
	    Found existing installation: pip 20.1.1
	    Uninstalling pip-20.1.1:
	      Successfully uninstalled pip-20.1.1
	Successfully installed pip-24.0  
  ```  
* ```pip3 install -r requirements.txt```  
* ```pip3 list```
* Authenticate to Google Using ```gcloud auth application-default login```
* Update project settings, primarily
  * project id
  * region
* Running:
  ```
  python3 main.py
  ```


## Resources
* Structured Tools
  - Defining Custom Tools | LangChain[[python.langchain.com](https://python.langchain.com/v0.1/docs/modules/tools/custom_tools/)]
  - Structured Tools[[blog.langchain.dev](https://blog.langchain.dev/structured-tools/)]
* Chat with History
  - Structured chat | LangChain[[python.langchain.com](https://python.langchain.com/v0.1/docs/modules/agents/agent_types/structured_chat/#adding-in-memory)]
  - Does the new Structured Chat Agent support ConversationMemory? · Issue #4000 · langchain-ai/langchain · GitHub[[github.com](https://github.com/langchain-ai/langchain/issues/4000)]
* Agents
  - langchain.agents.agent_types.AgentType — LangChain 0.2.1[[api.python.langchain.com](https://api.python.langchain.com/en/latest/agents/langchain.agents.agent_types.AgentType.html)]
  - Building a LangChain Custom Medical Agent with Memory - YouTube[[www.youtube.com](https://www.youtube.com/watch?v=6UFtRwWnHws)]
    - [Colab Code Link](https://colab.research.google.com/drive/1ipuSd6Jnl9KMF39LbA1n6FDDx5HBntZd?usp=sharing)
* GCP CLoud Logging
  - Introducing Google Cloud Logging Python v3.0.0 | by Daniel Sanche | Google Cloud - Community | Medium[[medium.com](https://medium.com/google-cloud/introducing-google-cloud-logging-python-v3-0-0-4c548663bab4)]
* UI
  - Create an Generative-AI chatbot using Python and Flask: A step by step guide | by InnovatewithDataScience | Medium[[medium.com](https://medium.com/@mailsushmita.m/create-an-generative-ai-chatbot-using-python-and-flask-a-step-by-step-guide-ea39439cf9ed)]