#!/usr/bin/env python3
"""
test_tts.py

Validates that pyttsx3 text-to-speech works in the current environment.
Speaks a sample navigation alert to whatever audio output is active.

Usage:
    python scripts/test_tts.py

To test Bluetooth output:
    Pair your headphones first, set them as default audio output,
    then run this script.
"""

import pyttsx3

SAMPLE_ALERTS = [
    "Person detected, 2 meters ahead.",
    "Chair detected, 1 point 2 meters ahead.",
    "Warning. Obstacle detected, 0 point 8 meters ahead.",
]

def main():
    print("Initializing TTS engine...")
    engine = pyttsx3.init()

    # Set a comfortable speech rate — default is often too fast
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")
    print(f"Available voices: {len(voices)}")
    for i, v in enumerate(voices):
        print(f"  [{i}] {v.name} ({v.id})")

    print("\nSpeaking sample navigation alerts...\n")
    for alert in SAMPLE_ALERTS:
        print(f">> {alert}")
        engine.say(alert)
    engine.runAndWait()

    print("\nTTS test complete.")

if __name__ == "__main__":
    main()