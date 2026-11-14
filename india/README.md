# Twins Separated at Birth (India)

Computer vision / near-duplicate detection. Flag released by the platform when the score passes the threshold.

## Task

A shuffled set of photos of Indian monuments. Find all unordered pairs of images that come from the **same
source photograph** (crops, resizes, recompression, brightness/contrast changes). Two different photos of the
same monument (similar viewpoint and light) are NOT a pair. Not every image has a twin. Output `output.csv`
with `image_a,image_b`.

## Solution (`main.py`): cheap candidates, then exact geometric check

1. **Candidates (fast, global).** Every image gets a small descriptor: HSV colour histogram + 16x16 grey
   thumbnail, L2-normalised. Cosine similarity of all pairs; for each image keep its K = 10 most similar
   images. This removes almost all of the N^2 pairs.
2. **Local features.** SIFT (500 keypoints, image resized to 512 px), RootSIFT normalisation.
3. **Verification of each candidate pair.**
   - Match SIFT descriptors with Lowe's ratio test (0.8), at least 4 good matches.
   - Fit a homography with MAGSAC (robust to wrong matches) and warp image b onto image a.
   - In the overlapping area compare the two blurred, brightness/contrast-normalised images pixel by pixel.
   - Pair accepted if less than 5% of the pixels differ (`MAX_BAD = 0.05`).

Why this separates twins from look-alikes: a crop/resize of the same photo aligns perfectly after the
homography, so almost every pixel matches. A different photo of the same monument may match many SIFT points on
the building, but people, clouds, trees, shadows and slightly different perspective make many pixels differ.

Engineering: JPEGs are decoded at reduced size (`draft`), SIFT descriptors are stored as uint8 and grey images
are re-read on demand, because the first version used ~3 GB and was killed by the judge; work runs in a thread pool.

## Run

```
pip install opencv-python pillow numpy
python main.py test-input.zip    # writes output.csv
```
