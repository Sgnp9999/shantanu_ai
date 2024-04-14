from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

#Mistral
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(repo_id=repo_id, temperature=0.5)

#Personal_Mistral
template = """
Following is the context, based on the context answer given question:
Context={context}
{question}"""
prompt = PromptTemplate.from_template(template)
prompt_final=PromptTemplate(template=template, input_variables=['question', 'Context'])
llm_chain = LLMChain(prompt=prompt_final, llm=llm)

def ask_mistral(question):      
    return llm(question)

def personal_mistral(question, db):
    context=db.similarity_search(query=question ,fetch_k=4)
    print(len(context))
    return llm_chain.run(question=question, context=context)

def mistral_csv(df, question):
    df_agent = create_pandas_dataframe_agent(llm, df)
    def handle_parsing_error(error):
        print(f"Error parsing LLM output: {error}")
    response = df_agent.invoke(question, handle_parsing_errors=handle_parsing_error)
    return response['output']
