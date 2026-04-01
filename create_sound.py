import numpy as np
from scipy.io.wavfile import write

sample_rate = 44100
duration = 0.2

t = np.linspace(0, duration, int(sample_rate * duration), False)

# Laser type sharp sound
tone = np.sin(2 * np.pi * 1200 * t) * np.exp(-6 * t)

audio = tone * (2**15 - 1) / np.max(np.abs(tone))
audio = audio.astype(np.int16)

write("laser.wav", sample_rate, audio)

print("laser.wav created successfully!")
