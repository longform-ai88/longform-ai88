from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
topic = input("Enter book topic: ")
response = client.responses.create(
    model="gpt-4.1-mini",
    input=f"Create a detailed outline for a book about {topic}"

)
print(response.output_text)