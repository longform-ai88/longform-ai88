import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Longform AI")

prompt = st.text_area("Enter your idea")

if st.button("Generate"):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"write a viral Youtube script about: {prompt}"}
        ]
    )
    
    st.write(response.choices[0].message.content)