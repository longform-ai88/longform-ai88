import os

os.system("pip install moviepy")

import streamlit as st
from openai import OpenAI
from gtts import gTTS
import requests

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

    script = response.choices[0].message.content

    tts = gTTS(script)
    tts.save("voice.mp3")

    st.audio("voice.mp3")
    audio = AudioFileClip("voice.mp3") 