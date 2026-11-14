import matplotlib.pyplot as plt
from scipy.io import wavfile

sr, data = wavfile.read("challenge.wav")
plt.specgram(data, Fs=sr, cmap="inferno")
plt.savefig("spec.png", dpi=200)