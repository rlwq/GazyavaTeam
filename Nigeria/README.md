# The Gángan Never Lies (Nigeria)

Audio / spectrogram steganography. Flag: `SIGMOID_TALKINGDRUM`

## Task

`challenge.wav`: 16-bit PCM, mono, 22050 Hz, ~10 s. To the ear it is a flat buzzing hum. Find what the engineer
hid inside it.

## Solution (`main.py`)

The story is about the Yoruba talking drum (gángan), which carries messages by changing **pitch**, so the message
is in the frequency domain, not in what you hear.

1. Read the file with `scipy.io.wavfile.read`.
2. Plot its spectrogram (`plt.specgram`, short-time Fourier transform: time on x, frequency on y, energy as colour).
3. In `spec.png`, in the 3000-4000 Hz band, the energy forms letters that read **TALKINGDRUM**.

The text was drawn into the spectrum: in each time slice only the frequencies that form the letter shapes have
energy. That sounds like a buzz but appears as a picture on the spectrogram.

## Run

```
pip install -r requirements.txt
python main.py   # writes spec.png
```
