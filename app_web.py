import os
import streamlit as st
from openai import OpenAI
from gtts import gTTS
import requests
import uuid
import base64

from moviepy.editor import ImageClip, concatenate_videoclips, ColorClip, CompositeVideoClip

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "uses" not in st.session_state:
    st.session_state.uses = 0

client = OpenAI(api_key=st=os.getenv("OPENAI_API_KEY"))

st.title("Longform AI")

st.write("USES:", st.session_state.uses) # 👈 HER

st.write(f"Free uses left: {max(0, 3 - st.session_state.uses)}")

prompt = st.text_area("Enter your idea")
tone = st.selectbox("Choose tone", ["Viral", "Funny", "Professional", "Storytelling"])
platform = st.selectbox("Platform", ["Youtube", "TikTok", "Instagram"])
length = st.selectbox("Length", ["Short (30s)", "Medium (1 min)", "Long (5 min)"])

if st.button("Generate"):

    # 🚫 STOP hvis limit nådd
    if st.session_state.uses >= 3:
        st.warning("You reached the free limit 🚀")
        st.markdown("[👉 Upgrade to Pro (§12/month)](https://buy.stripe.com/6oUeVecpDcqSgLcgLlfnO00)")
        st.stop()

    # ✅ Øk teller
    st.session_state.uses += 1

    # 🔥 GENERER
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": f"""
Write a highly engaging {platform} script about: {prompt}
Tone {tone}
Length: {length}
"""
        }
    ]
)
text = response.choices[0].message.content
st.write(text)
# 🔊 AUDIO
from gtts import gTTS
tts = gTTS(text)
tts.save("output.mp3")
st.audio("output.mp3")
from moviepy.editor import AudioFileClip, ImageClip

from moviepy.editor import *

audio = AudioFileClip("output.mp3")

import base64

image_prompts = [
    f"{prompt} cinematic scene",
    f"{prompt} futuristic style",
    f"{prompt} realistic photo"
]
images = []

for i, img_prompt in enumerate(image_prompts):
    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=img_prompt,
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        filename = f"image_{i}.png"
        with open(filename, "wb") as f:
            f.write(image_bytes)

        images.append(filename)  # 🔥 DETTE MANGLER HOS DEG

    except Exception as e:
        st.error(f"Image error: {e}")

duration_per_image = audio.duration / len(images)

clips = []

for img in images:
    background = ColorClip(size=(1080,1920), color=(0,0,0), duration=duration_per_image)

    clip = ImageClip(img).resize(width=1080)
    clip = clip.set_position("center").set_duration(duration_per_image)

    final_clip = CompositeVideoClip([background, clip])

    clips.append(final_clip)

video = concatenate_videoclips(clips)
video = video.set_audio(audio)
import time

filename = f"output_{int(time.time())}.mp4"

video.write_videofile(filename, fps=10, preset="ultrafast")

st.video(filename)

video.write_videofile("output.mp4", fps=10, preset="ultrafast")

st.video("output.mp4")
