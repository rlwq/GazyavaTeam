# Twins Separated at Birth (India)

## Problem statement

Given a shuffled set of photos of Indian monuments, find all unordered pairs of images that come from the same source
photograph (crops, resizes, recompression, brightness or contrast changes). Different photos of the same monument are
not duplicates, even with a similar viewpoint and lighting. Not every image has a duplicate. Find as many true pairs as
possible while avoiding false matches.

## Input

`test-input.zip`: JPEG images (the path is given as the first argument; default `test-input.zip`). For practice:
`train-input.zip` with `train-output.csv` (known duplicate pairs).

## Output

`output.csv` with header `image_a,image_b`, one row per duplicate pair (file names). The platform scores it and releases
the flag above the threshold.

## Solution

1. **Cheap candidates.** Each image gets a small global descriptor: HSV colour histogram + 16x16 grey thumbnail,
   normalised. Cosine similarity over all images; for each image keep its 10 most similar ones as candidate pairs. This
   cuts N^2 pairs down to about N x 10.
2. **Local features.** SIFT, 500 keypoints on the image resized to 512 px, with RootSIFT. Descriptors are stored as uint8
   and JPEGs are decoded at reduced size, to stay within the judge's memory limit.
3. **Geometric check of each candidate.** Match SIFT points (ratio test 0.8, at least 4 matches), fit a homography with
   MAGSAC, warp image b onto image a, and compare blurred, brightness-normalised pixels in the overlap. The pair is a
   duplicate if fewer than 5% of the pixels differ. A crop or resize of the same photo lines up almost exactly; another
   photo of the same monument does not (people, sky, shadows, perspective).

```python
H, _ = cv2.findHomography(src, dst, cv2.USAC_MAGSAC, 4.0)
warped = cv2.warpPerspective(gb, H, (w, h))
bad = np.mean(np.abs(a - b) > 0.5)      # duplicate if bad < 0.05
```
