from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.schema import SystemMessage

from tools import too
from langchain.embeddings import OpenAIEmbeddings


from rag_utils import create_retriever, data_loader

with open("system_message.txt", "r") as file:
    system_message = file.read()

openai_embeddings = OpenAIEmbeddings()

chunks = data_loader()

retriever =  create_retriever(chunks, openai_embeddings)

openai_4_llm = ChatOpenAI(temperature=0.1, model = 'gpt-4-1106-preview'),


def get_gpt_agent_executor():
    agent_kwargs = {
    "system_message": SystemMessage(content=system_message),
    "retriever": retriever  # Pass the retriever to the agent
    }

    analyst_agent_openai = initialize_agent(
        llm= ChatOpenAI(temperature=0.1, model = 'gpt-4-1106-preview'),
        tools=[too],
        agent_kwargs=agent_kwargs,
        verbose=True,
        max_iterations=20,
        early_stopping_method='generate'
    )

    return analyst_agent_openai
