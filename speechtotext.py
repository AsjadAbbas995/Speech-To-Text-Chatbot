import sys

print("Step 1: Importing libraries...")

# ===== Safe Imports =====

try:
    import sounddevice as sd
    print("  ✅ sounddevice OK")
except Exception as e:
    print(f"  ❌ sounddevice FAILED: {e}")
    input("Press Enter to exit...")
    sys.exit()

try:
    import scipy.io.wavfile as wav
    print("  ✅ scipy OK")
except Exception as e:
    print(f"  ❌ scipy FAILED: {e}")
    input("Press Enter to exit...")
    sys.exit()

try:
    from transformers import pipeline
    print("  ✅ transformers OK")
except Exception as e:
    print(f"  ❌ transformers FAILED: {e}")
    input("Press Enter to exit...")
    sys.exit()

try:
    import tempfile, os
    print("  ✅ tempfile/os OK")
except Exception as e:
    print(f"  ❌ {e}")
    input("Press Enter to exit...")
    sys.exit()

try:
    import numpy as np
    print("  ✅ numpy OK")
except Exception as e:
    print(f"  ❌ numpy FAILED: {e}")
    input("Press Enter to exit...")
    sys.exit()

try:
    from duckduckgo_search import DDGS
    import requests
    from bs4 import BeautifulSoup
    print("  ✅ Web search libraries OK")
except Exception as e:
    print(f"  ❌ Web search libs FAILED: {e}")
    input("Press Enter to exit...")
    sys.exit()

# ===== Load Whisper Model (CPU Only) =====

print("\nStep 2: Loading Whisper model (may take a minute on first run)...")

try:
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-base",
        device=-1
    )
    print("  ✅ Model loaded!\n")
except Exception as e:
    print(f"  ❌ Model load FAILED: {e}")
    input("Press Enter to exit...")
    sys.exit()

SAMPLE_RATE = 16000

# ===== Web Search Function =====

def search_web(query):
    print("🌐 Searching the web...")

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return "No results found."

        top_result = results[0]
        url = top_result["href"]

        response = requests.get(
            url,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs[:5]])

        if not text.strip():
            return top_result["body"]

        return text[:1000]

    except Exception as e:
        return f"Search error: {e}"

# ===== UI =====

print("=" * 50)
print("    🎤 Speech-to-Text Web Assistant (CPU)")
print("=" * 50)
print("Press Enter to start listening, or 'q' to quit.\n")

# ===== Main Loop =====

while True:
    try:
        user = input("Press Enter to record (q to quit): ").strip().lower()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break

    if user == "q":
        print("Goodbye!")
        break

    try:
        print("🎤 Calibrating microphone... Stay silent.")

        silence_duration = 1.5
        max_record_time = 120
        chunk_duration = 0.3
        chunk_samples = int(SAMPLE_RATE * chunk_duration)
        no_speech_timeout = 10

        recorded_frames = []
        silence_counter = 0
        speech_started = False
        wait_time = 0
        total_time = 0

        # ---- Calibrate Noise ----
        noise_levels = []
        for _ in range(15):
            audio_chunk = sd.rec(
                chunk_samples,
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="int16"
            )
            sd.wait()
            rms = np.sqrt(np.mean(audio_chunk.astype(np.float32) ** 2))
            noise_levels.append(rms)

        noise_floor = np.mean(noise_levels)
        silence_threshold = noise_floor + 300

        print(f"Noise floor: {noise_floor:.2f}")
        print(f"Threshold: {silence_threshold:.2f}")
        print("🎤 Speak now...")

        while True:
            audio_chunk = sd.rec(
                chunk_samples,
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="int16"
            )
            sd.wait()

            rms = np.sqrt(np.mean(audio_chunk.astype(np.float32) ** 2))

            # Wait for speech to begin
            if not speech_started:
                wait_time += chunk_duration

                if rms > silence_threshold:
                    speech_started = True
                    print("🔴 Recording started...")
                    recorded_frames.append(audio_chunk)
                    total_time = 0
                elif wait_time >= no_speech_timeout:
                    print("⚠ No speech detected. Cancelling.")
                    break
                continue

            # Recording in progress
            recorded_frames.append(audio_chunk)
            total_time += chunk_duration

            if rms < silence_threshold:
                silence_counter += chunk_duration
            else:
                silence_counter = 0

            if silence_counter >= silence_duration:
                print("🛑 Silence detected. Stopping...")
                break

            if total_time >= max_record_time:
                print("⏹ Max recording time reached.")
                break

        if not recorded_frames:
            print("⚠ No usable speech recorded.\n")
            continue

        audio = np.concatenate(recorded_frames, axis=0)

        print("⏳ Transcribing...")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wav.write(f.name, SAMPLE_RATE, audio)
            tmp_path = f.name

        result = pipe(tmp_path)
        os.unlink(tmp_path)

        user_text = result["text"].strip()

        if not user_text:
            print("⚠ No speech detected.\n")
            continue

        print(f"📝 You said: {user_text}\n")

        answer = search_web(user_text)

        print("🤖 Answer:")
        print(answer)
        print("\n")

    except Exception as e:
        print(f"❌ Error: {e}\n")

input("Press Enter to exit...")