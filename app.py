import os
import re
import json
import streamlit as st
from dotenv import load_dotenv
from deepgram import DeepgramClient, SpeakOptions, AnalyzeOptions, TextSource, PrerecordedOptions, FileSource, UrlSource
from io import BytesIO
from utils import voice_model_dict, generate_srt

st.set_page_config(page_title="TTS with Deepgram only English", page_icon='🔊', layout='wide')

load_dotenv()
api_key = os.getenv("G_API_KEY")


def get_speech_from_text(api_key, text, voice_model):
    try:
        deepgram = DeepgramClient(api_key=api_key)
        options = SpeakOptions(model=voice_model_dict[voice_model], encoding="linear16", container="wav")
        response = deepgram.speak.v("1").save("output.wav", {"text": text}, options)
    except Exception as e:
        st.error(f"Error: {e}")

def get_text_analysis(api_key, text, intents, summarize, topics):
    try:
        deepgram = DeepgramClient(api_key=api_key)
        payload = TextSource(buffer=text)
        options = AnalyzeOptions(language='en', sentiment=True, intents=intents, summarize=summarize, topics=topics)
        response = deepgram.read.analyze.v("1").analyze_text(payload, options)
        return response.to_dict()  # to_dict() method to convert AnalyzeResponse to a dictionary
    except Exception as e:
        st.error(f"Error: {e}")

def transcribe_speech_file(api_key, uploaded_file):
    try:
        deepgram = DeepgramClient(api_key)
        buffer_data = uploaded_file.read()
        # payload = FileSource(buffer=BytesIO(buffer_data))
        payload = {"buffer": buffer_data}
        
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        # print(response.to_json(indent=4))

        return response.to_dict()

    except Exception as e:
        st.error(f"Exception: {e}")
        return None

def transcribe_speech_url(api_key, audio_url):
    try:
        pattern = re.compile(r'^(https?|ftp|file):\/\/(www\.)?(.*?)\.(mp3|wav|flac)$')
        if pattern.match(audio_url):
            deepgram = DeepgramClient(api_key)
            payload = UrlSource(url=audio_url)
            options = PrerecordedOptions(
                model="nova-2",
                smart_format=True,
            )

            response = deepgram.listen.prerecorded.v("1").transcribe_url(payload, options)
            # print(response.to_json(indent=4))
            # print(deepgram.extra.to_SRT(response))
            return response.to_dict()
        else:
            st.warning("Please input a correct audio URL!")
    except Exception as e:
        st.error(f"Exception: {e}")

#Asosiy oyna boshlandi
st.title("♻️ Deep Recognition")

#Chap yondagi hodisalar
st.sidebar.markdown("#### 👇👇 Please enter your API key 👇👇")
api_keys = st.sidebar.text_input("Token", placeholder="API KEY", help="To create your first API key refer to our Guide Creating API Keys")

#3 ta tabulatsiya
tts, stt, ttt = st.tabs(["⚡️ TTS (Text to Speech)", "⚡️ STT (Speech to Text)", "⚡️ TTT (Text to Text)"])

#Tab1
with tts:
    st.header("🥇 TTS")
    input_text = st.text_area("Input text", value="Hello, how can I help you today?", disabled=not api_keys)
    select_voice_models = st.selectbox("Select voice model", options=list(voice_model_dict.keys()), disabled=not api_keys)
    if st.button("Submit", key="tts_submit", disabled=not api_keys) and select_voice_models:
        with st.spinner("Processing..."):
            get_speech_from_text(api_keys, input_text, select_voice_models)
        st.audio("output.wav", autoplay=True)
#Tab2
with stt:
    st.header("🥈 STT")
    tanlov = st.checkbox(label="With links", disabled=not api_keys)
    if tanlov:
        stt_input_links = st.text_input("Input links", value='https://dpgr.am/spacewalk.wav', disabled=not api_keys)
        stt_btn_links = st.button("Submit", key="stt_submit_links", disabled=not api_keys or not stt_input_links)
        st.audio(stt_input_links, "Please listen")
        if stt_btn_links:
            with st.spinner("Processing..."):
                result_response = transcribe_speech_url(api_keys, stt_input_links)
                srt_output = generate_srt(result_response)
            st.write(f"`Transcripted text:` 👇👇👇<br>{result_response['results']['channels'][0]['alternatives'][0]['transcript']}", unsafe_allow_html=True)
            with st.expander("SRT output ..."):
                st.text_area("Generated SRT", srt_output, height=350)

    else:
        stt_col1, stt_col2 = st.columns(2)
        with stt_col1:
            audio_path = st.file_uploader("Upload audio file", type=["mp3", "wav", "flac"], disabled=not api_keys)
            stt_btn = st.button("Submit", key="stt_submit", disabled=not api_keys or not audio_path)
            st.audio(audio_path, "Please listen to this")
        with stt_col2:
            if stt_btn and audio_path:
                with st.spinner("Processing..."):
                    natija = transcribe_speech_file(api_keys, audio_path)
                    srt_output = generate_srt(natija)
                st.write(f"`Transcripted text:` 👇👇👇<br>{natija['results']['channels'][0]['alternatives'][0]['transcript']}", unsafe_allow_html=True)
                with st.expander("SRT output ..."):
                    st.text_area("Generated SRT", srt_output, height=350)
#Tab3
with ttt:
    st.header("🥉 TTT")
    ttt_col1, ttt_col2 = st.columns(2)
    with ttt_col1:
        tab3_input_text = st.text_area("Input text", disabled=not api_keys, height=400)
        select1, select2, select3 = st.columns(3)
        
        ttt_select_intents = select1.checkbox("Activate intents", disabled=not api_keys, value=True)
        ttt_select_summarize = select2.checkbox("Activate summarize", disabled=not api_keys)
        ttt_select_topics = select3.checkbox("Activate topics", disabled=not api_keys)
        button = st.button("Submit", key="ttt_submit", disabled=not api_keys)
    with ttt_col2:
        if button:
            with st.spinner("Processing..."):
                result = get_text_analysis(api_keys, tab3_input_text, ttt_select_intents, ttt_select_summarize, ttt_select_topics)
                st.json(result)

#About me 
st.write("Creators: [🏆 Shokh Abbos](https://t.me/shohabbosdev)", unsafe_allow_html=True)