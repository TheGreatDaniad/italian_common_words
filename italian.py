from gtts import gTTS
from pydub import AudioSegment
import math

# Function to split text into chunks for approximately 5 minutes each
def split_text_into_chunks(text, max_duration_in_seconds=300):
    words = text.split(' ')
    chunks = []
    chunk = ''
    
    # Estimate the length of speech (about 150 words per minute)
    words_per_minute = 150
    words_per_second = words_per_minute / 60
    max_words_per_chunk = math.floor(max_duration_in_seconds * words_per_second)

    for word in words:
        if len(chunk.split(' ')) < max_words_per_chunk:
            chunk += word + ' '
        else:
            chunks.append(chunk.strip())
            chunk = word + ' '
    
    if chunk.strip():
        chunks.append(chunk.strip())

    return chunks

# Function to create speech files for each chunk
def create_speech_file(text, file_index, lang='it'):
    tts = gTTS(text=text, lang=lang, slow=False)
    filename = f"speech_chunk_{file_index}.mp3"
    tts.save(filename)
    print(f"Created {filename}")
    return filename

# Function to check the duration of the audio file
def get_audio_duration(filename):
    audio = AudioSegment.from_file(filename)
    return len(audio) / 1000  # Duration in seconds

# Read the Italian text from file
with open('italian_text.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Split the text into 5-minute chunks
chunks = split_text_into_chunks(text)

# Generate speech files for each chunk
for index, chunk in enumerate(chunks):
    audio_filename = create_speech_file(chunk, index + 1)
    
    # Check the audio duration and split if needed
    duration = get_audio_duration(audio_filename)
    print(f"Duration of {audio_filename}: {duration:.2f} seconds")
    
    if duration > 300:  # If longer than 5 minutes
        print(f"{audio_filename} is longer than 5 minutes, splitting...")
        audio = AudioSegment.from_mp3(audio_filename)
        parts = math.ceil(duration / 300)
        
        for i in range(parts):
            start_time = i * 300 * 1000
            end_time = (i + 1) * 300 * 1000
            part_audio = audio[start_time:end_time]
            part_filename = f"speech_chunk_{index + 1}_part_{i + 1}.mp3"
            part_audio.export(part_filename, format="mp3")
            print(f"Created {part_filename}")

print("All speech files generated!")
