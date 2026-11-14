import csv
import os
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
NFEAT = 500     # SIFT keypoints per image (memory grows linearly with this)
MAX_BAD = 0.05  # max fraction of mismatching pixels after alignment

WORKERS = min(8, os.cpu_count() or 1)

cv2.setNumThreads(1)


def descriptor(path):
    # rough image descriptor: colour histogram + 16x16 thumbnail
    im = Image.open(path)
    im.draft('RGB', (64, 64))  # decode JPEG at reduced size: big photos no longer blow up RAM
    img = np.asarray(im.convert('RGB').resize((64, 64)))
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 4, 4], [0, 180, 0, 256, 0, 256]).ravel()
    hist = np.sqrt(hist / hist.sum())
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32)
    thumb = cv2.resize(gray, (16, 16), interpolation=cv2.INTER_AREA).ravel()
    thumb = (thumb - thumb.mean()) / thumb.std() / 16
    v = np.concatenate([hist, thumb])
    return (v / np.linalg.norm(v)).astype(np.float32)


def load_gray(path):
    im = Image.open(path)
    im.draft('L', (SIDE, SIDE))  # let JPEG decode at reduced size: less RAM and time
    gray = np.asarray(im.convert('L'))
    scale = min(1, SIDE / max(gray.shape))
    return cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)


def sift_features(path):
    gray = load_gray(path)
    kp, desc = cv2.SIFT_create(nfeatures=NFEAT).detectAndCompute(gray, None)
    if desc is None:
        desc = np.zeros((0, 128), np.float32)
    desc = np.sqrt(desc / (desc.sum(axis=1, keepdims=True) + 1e-7))  # RootSIFT
    # Keep memory small: features of every image are held at once, and the old
    # float32 descriptors + grey images took ~3 GB, so the judge killed us (-9).
    # Descriptors are stored as uint8 (4x smaller); grey images are re-read when needed.
    desc = np.round(desc * 255).astype(np.uint8)
    return path, np.float32([k.pt for k in kp]), desc


def mismatch(fa, fb):
    # align b onto a using SIFT points and return the fraction of pixels that differ
    (ga, pa, da), (gb, pb, db) = fa, fb
    if len(da) < 2 or len(db) < 2:
        return 1.0
    matches = cv2.BFMatcher().knnMatch(da.astype(np.float32), db.astype(np.float32), k=2)
    good = [m for m, n in matches if m.distance < 0.8 * n.distance]
    if len(good) < 4:
        return 1.0
    src = pb[[m.trainIdx for m in good]]
    dst = pa[[m.queryIdx for m in good]]
    H, _ = cv2.findHomography(src, dst, cv2.USAC_MAGSAC, 4.0)
    if H is None:
        return 1.0

    ga, gb = load_gray(ga), load_gray(gb)
    h, w = ga.shape
    warped = cv2.warpPerspective(gb, H, (w, h))
    overlap = cv2.warpPerspective(np.full_like(gb, 255), H, (w, h)) > 250
    overlap = cv2.erode(overlap.astype(np.uint8), np.ones((5, 5))) > 0

    if overlap.sum() < 100:
        return 1.0
    a = cv2.GaussianBlur(ga, (5, 5), 0)[overlap].astype(np.float32)
    b = cv2.GaussianBlur(warped, (5, 5), 0)[overlap].astype(np.float32)
    a = (a - a.mean()) / (a.std() + 1e-6)   # normalise brightness and contrast
    b = (b - b.mean()) / (b.std() + 1e-6)
    return np.mean(np.abs(a - b) > 0.5)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        archive = sys.argv[1] if len(sys.argv) > 1 else 'test-input.zip'
        zipfile.ZipFile(archive).extractall(tmp)
        files = sorted(Path(tmp).rglob('*.jpg'), key=lambda p: p.name)

        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            D = np.stack(list(pool.map(descriptor, files)))
            feats = list(pool.map(sift_features, files))

            # candidates: K most similar images by cosine for each image
            S = D @ D.T
            np.fill_diagonal(S, -np.inf)
            nn = np.argpartition(-S, K, axis=1)[:, :K]
            del S
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
