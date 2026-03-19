import os
os.system("apt-get update && apt-get install -y ffmpeg")
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Longform AI")

prompt = st.text_area("Enter your idea")

if st.button("Generate"):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"""
Write a highly engaging viral Youtube script about: {prompt}
Include
- Hook in first 5 seconds
- Storytelling
- Clear structure
- Call to action
Make it entertaining and easy to follow.
"""}
        ]
    )
    
    st.write(response.choices[0].message.content)