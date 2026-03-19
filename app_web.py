from moviepy.editor import *
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

    img_url = "https://images.unsplash.com/photo-1519389950473-47ba0277781c"
    img_data = requests.get(img_url).content
    with open("bg.jpg", "wb") as f:
        f.write(img_data)
    # lag video med bilde
    image = ImageClip("bg.jpg").set_duration(audio.duration).resize((1280, 720))
    video = image.set_audio(audio)    

    video.write_videofile("output.mp4", fps=24)

    st.video("output.mp4") 