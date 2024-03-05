import gradio as gr
import openai
from decouple import config
from gtts import gTTS
import os
import win32com.client
import pythoncom

openai.api_key = config("OPENAI_API_KEY")

# The Models Job or role
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]


#  language = 'en'


# Main method goes here
def decipher(audio):
    global messages

    # Using openAI's speech to text model
    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, language="zh")
    print(transcript["text"])

    messages.append({"role": "user", "content": transcript["text"]})

    response =  openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    system_message = response["choices"][0]["message"]["content"]
    print(system_message)

    pythoncom.CoInitialize()
    speaker = win32com.client.Dispatch("SAPI.SpVoice")

    for voice in speaker.GetVoices():
        if "Chinese (Taiwan)" in voice.GetDescription():
            speaker.Voice = voice
            break

    speaker.Speak(system_message)
    # myobj = gTTS(text=system_message, lang=language, slow=False)
    # myobj.save("welcome.mp3")
    # # Playing the converted file
    # os.system("start welcome.mp3")
    messages.append({"role": "assistant", "content": system_message},)

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript


# Using Gradio's audio Interface 
interface = gr.Interface(fn=decipher, inputs=gr.Audio(
    source="microphone", type="filepath"), outputs="text", share=True).launch()
interface.launch()
