language_list = {
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Chinese (Mandarin, Simplified)": ["zh", "zh-CN", "zh-Hans"],
    "Chinese (Mandarin, Traditional)": ["zh-TW", "zh-Hant"],
    "Czech": "cs",
    "Danish": ["da", "da-DK"],
    "Dutch": "nl",
    "English": ["en", "en-US", "en-AU", "en-GB", "en-NZ", "en-IN"],
    "Estonian": "et",
    "Finnish": "fi",
    "Flemish": "nl-BE",
    "French": ["fr", "fr-CA"],
    "German": "de",
    "German (Switzerland)": "de-CH",
    "Greek": "el",
    "Hindi": ["hi", "hi-Latn"],
    "Hungarian": "hu",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": ["ko", "ko-KR"],
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Malay": "ms",
    "Norwegian": "no",
    "Polish": "pl",
    "Portuguese": ["pt", "pt-BR"],
    "Romanian": "ro",
    "Russian": 'ru',
    "Slovak": "sk",
    "Spanish": ["es", "es-419"],
    "Swedish": ["sv", "sv-SE"],
    "Thai": ["th", "th-TH"],
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Vietnamese": "vi"
}

voice_model_dict = {
    "👩‍🎓 Asteria": "aura-asteria-en", 
    "👩‍💼 Luna": "aura-luna-en", 
    "👩‍💻 Stella": "aura-stella-en", 
    "👨‍🎓 Athena": "aura-athena-en",
    "🧑‍🎓 Hera": "aura-hera-en",
    "👨‍✈️ Orion": "aura-orion-en",
    "👨‍⚖️ Arcas": "aura-arcas-en",
    "🤵‍♂️ Persus": "aura-perseus-en",
    "👨‍🏭 Angus": "aura-angus-en",
    "👨‍🌾 Orpheus": "aura-orpheus-en",
    "🧑🏽‍🚀 Helios": "aura-helios-en",
    "👨🏽‍🎤 Zeus": "aura-zeus-en"
}


def format_time(seconds):
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes = seconds // 60
    hours = minutes // 60
    return f"{hours:02}:{minutes % 60:02}:{seconds % 60:02},{millis:03}"

def generate_srt(transcription_result):
    srt_content = []
    index = 1
    
    words = transcription_result['results']['channels'][0]['alternatives'][0]['words']
    
    for i in range(0, len(words), 5):  # Grouping words by 5 for each subtitle entry
        group = words[i:i+5]
        start_time = format_time(group[0]['start'])
        end_time = format_time(group[-1]['end'])
        text = ' '.join(word['punctuated_word'] for word in group)
        srt_content.append(f"{index}")
        srt_content.append(f"{start_time} --> {end_time}")
        srt_content.append(text)
        srt_content.append("")
        
        index += 1
    
    return "\n".join(srt_content)