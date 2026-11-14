# The Gángan Never Lies (Nigeria)

## Overview
We are given `challenge.wav` (16-bit PCM mono, 22050 Hz), which sounds like a flat buzzing hum. Based on the description of the Yoruba talking drum (*gángan*) encoding messages via pitch changes, the flag is hidden in the frequency spectrum.

## Solution
1. Plotted the spectrogram of `challenge.wav` using `scipy.io.wavfile` and `matplotlib`.
2. Checked the 3000–4000 Hz range on the generated `spec.png` and read the text `TALKINGDRUM`.

## Run
```bash
pip install -r requirements.txt
python main.py