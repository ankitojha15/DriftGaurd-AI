import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")
prompt = PromptTemplate.from_template(
    "Table: orders. Prod columns: {prod}, Expected: {exp}. "
    "Give only one Postgres SELECT fix on orders, no explain."
)
chain = prompt | llm | StrOutputParser()

def get_fix(prod, exp):
    return chain.invoke({"prod": prod, "exp": exp}).strip()

if __name__ == "__main__":
    print(get_fix(["customer_id", "id", "price"], ["cust_id", "id", "price"]))