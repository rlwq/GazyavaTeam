# Twins Separated at Birth (India)

Flag released by the platform when the score passes.

We need pairs of images cut from the same photo (crop, resize, brightness change), not just two photos of the same
monument. First, cheap candidates: a small descriptor per image (colour histogram + 16x16 thumbnail). For each image
we keep its 10 most similar ones.

Then each candidate pair is checked exactly. We match SIFT points, fit a homography, warp one image onto the other
and compare pixels. A copy of the same photo lines up almost perfectly (< 5% different pixels). A different photo of
the same monument does not: people, sky, shadows and perspective differ.

```python
nn = np.argpartition(-(D @ D.T), K, axis=1)[:, :K]                  # 10 nearest by cosine = candidates

good = [m for m, n in knn if m.distance < 0.8 * n.distance]         # SIFT matches, ratio test
H, _ = cv2.findHomography(src, dst, cv2.USAC_MAGSAC, 4.0)            # align b onto a
warped = cv2.warpPerspective(gb, H, (w, h))
bad = np.mean(np.abs(a - b) > 0.5)                                    # normalised pixel difference
if bad < 0.05: pair is a duplicate
```

Run: `python main.py test-input.zip` (writes `output.csv`)
