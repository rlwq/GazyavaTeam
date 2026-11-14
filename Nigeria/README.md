# The Gángan Never Lies (Nigeria)

Flag: `SIGMOID_TALKINGDRUM`

The WAV sounds like a flat hum. The story is about the talking drum, which speaks by changing pitch, so the message
is hidden in frequencies, not in what you hear.

We plot a spectrogram (time x frequency). In the 3000-4000 Hz band the energy forms letters: TALKINGDRUM.

```python
sr, data = wavfile.read("challenge.wav")
plt.specgram(data, Fs=sr, cmap="inferno")     # time on x, frequency on y
plt.savefig("spec.png", dpi=200)              # read the text at 3-4 kHz
```

Run: `python main.py` (writes `spec.png`)
