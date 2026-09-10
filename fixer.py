
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b"
)


prompt = PromptTemplate.from_template(
    "Table: orders. Prod columns: {prod}, Expected: {exp}. "
    "Give only one Postgres SELECT fix on orders, no explain."
    )


chain = prompt | llm | StrOutputParser()

sql = chain.invoke({
    "prod": ["customer_id", "id", "price"],
    "exp": ["cust_id", "id", "price"]
})

print(sql.strip())