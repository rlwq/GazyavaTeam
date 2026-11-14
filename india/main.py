import csv
import sys
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

K = 10          # how many most similar images to check for each image
SIDE = 512      # image size (longer side) for SIFT
MAX_BAD = 0.05  # max fraction of mismatching pixels after alignment

cv2.setNumThreads(1)


def descriptor(path):
    # rough image descriptor: colour histogram + 16x16 thumbnail
    img = np.asarray(Image.open(path).convert('RGB').resize((64, 64)))
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 4, 4], [0, 180, 0, 256, 0, 256]).ravel()
    hist = np.sqrt(hist / hist.sum())
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32)
    thumb = cv2.resize(gray, (16, 16), interpolation=cv2.INTER_AREA).ravel()
    thumb = (thumb - thumb.mean()) / thumb.std() / 16
    v = np.concatenate([hist, thumb])
    return v / np.linalg.norm(v)


def sift_features(path):
    gray = np.asarray(Image.open(path).convert('L'))
    scale = min(1, SIDE / max(gray.shape))
    gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    kp, desc = cv2.SIFT_create(nfeatures=1000).detectAndCompute(gray, None)
    desc = np.sqrt(desc / desc.sum(axis=1, keepdims=True))  # RootSIFT
    return gray, np.float32([k.pt for k in kp]), desc


def mismatch(fa, fb):
    # align b onto a using SIFT points and return the fraction of pixels that differ
    (ga, pa, da), (gb, pb, db) = fa, fb
    matches = cv2.BFMatcher().knnMatch(da, db, k=2)
    good = [m for m, n in matches if m.distance < 0.8 * n.distance]
    if len(good) < 4:
        return 1.0
    src = pb[[m.trainIdx for m in good]]
    dst = pa[[m.queryIdx for m in good]]
    H, _ = cv2.findHomography(src, dst, cv2.USAC_MAGSAC, 4.0)
    if H is None:
        return 1.0

    h, w = ga.shape
    warped = cv2.warpPerspective(gb, H, (w, h))
    overlap = cv2.warpPerspective(np.full_like(gb, 255), H, (w, h)) > 250
    overlap = cv2.erode(overlap.astype(np.uint8), np.ones((5, 5))) > 0

    a = cv2.GaussianBlur(ga, (5, 5), 0)[overlap].astype(np.float32)
    b = cv2.GaussianBlur(warped, (5, 5), 0)[overlap].astype(np.float32)
    a = (a - a.mean()) / (a.std() + 1e-6)   # normalise brightness and contrast
    b = (b - b.mean()) / (b.std() + 1e-6)
    return np.mean(np.abs(a - b) > 0.5)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        zipfile.ZipFile(sys.argv[1]).extractall(tmp)
        files = sorted(Path(tmp).rglob('*.jpg'), key=lambda p: p.name)

        with ThreadPoolExecutor() as pool:
            D = np.stack(list(pool.map(descriptor, files)))
            feats = list(pool.map(sift_features, files))

            # candidates: K most similar images by cosine for each image
            S = D @ D.T
            np.fill_diagonal(S, -np.inf)
            nn = np.argsort(-S, axis=1)[:, :K]
            cands = sorted({(min(i, j), max(i, j)) for i in range(len(files)) for j in nn[i]})

            bad = list(pool.map(lambda c: mismatch(feats[c[0]], feats[c[1]]), cands))

    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['image_a', 'image_b'])
        for (a, b), s in zip(cands, bad):
            if s < MAX_BAD:
                writer.writerow([files[a].name, files[b].name])


if __name__ == '__main__':
    main()
