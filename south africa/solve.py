import numpy as np, librosa, soundfile as sf, matplotlib.pyplot as plt
from scipy.ndimage import median_filter

# 1. Load the whole recording (10.5 min)
y, sr = librosa.load("data/voice_note.wav", sr=16000)

# 2. Remove the horns: their sound stays the same for seconds, speech changes fast.
#    Typical (median) level of every frequency over ~2 s = horn noise -> subtract it.
D = librosa.stft(y, n_fft=2048, hop_length=256)
noise = median_filter(np.abs(D), size=(1, 125))
mask = np.clip(1 - 1.5 * noise / (np.abs(D) + 1e-9), 0, 1)
clean = librosa.istft(D * mask, hop_length=256, length=len(y))
sf.write("clean.wav", clean / np.abs(clean).max(), sr)

# 3. Listen to the whole clean.wav by ear and wait for "ikhodi":
#    at 7:18 - 7:21 she says "... uzosebenzisa ikhodi ULWAZI isicelo ..."

# 4. Picture: before / after cleaning around the found phrase (7:13 - 7:26)
A, B = 433, 446
fig, ax = plt.subplots(2, 1, figsize=(12, 7))
for a, sig, title in [(ax[0], y, "Before: horns = horizontal lines"), (ax[1], clean, "After: only speech left")]:
    a.imshow(librosa.amplitude_to_db(np.abs(librosa.stft(sig[A * sr:B * sr], n_fft=1024)), ref=np.max),
             origin="lower", aspect="auto", extent=[A, B, 0, 8000], vmin=-70, cmap="magma")
    a.set_ylim(0, 5000); a.set_title(title); a.axvspan(438.6, 439.3, color="cyan", alpha=0.3); a.axvspan(440.0, 440.6, color="lime", alpha=0.3)
ax[1].text(438.6, 4500, "ikhodi", color="cyan", fontsize=13); ax[1].text(440.0, 4500, "ULWAZI", color="lime", fontsize=13)
ax[1].set_xlabel("time, s"); fig.suptitle("Flag: SIGMOID_ULWAZI"); plt.tight_layout(); plt.savefig("result.png", dpi=90)
