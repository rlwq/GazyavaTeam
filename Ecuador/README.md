# Ciclopaseo Mirage (Ecuador - Adversarial ML)

Solution for the **Ciclopaseo Mirage** challenge in the **Learning Marathon of Machine Learning 2.0 (Sigmoid AI)** CTF.

## Task Overview
The goal is to perform a targeted $L_\infty$ adversarial attack against a pretrained `MobileNetV3-Large` (`IMAGENET1K_V2`) image classifier. Given an input photograph of a bicycle (ImageNet class `671` — `mountain bike`), the script must generate a modified image that the model classifies as a **moped** (ImageNet class `665`) with a softmax confidence of at least `0.99`.

### Constraints & Scoring Criteria
* **Pixel Budget:** Each RGB channel of every pixel may differ from the original image by at most `1` on the `0–255` integer scale (`max(abs(output_rgb - input_rgb)) <= 1`).
* **Artifact Format:** Valid RGB PNG file (no alpha channel) preserving the exact width and height of the input image, with a file size of at most `1 MiB`.
* **Runtime Environment:** Runs offline on CPU (2 cores, 2 GiB RAM) with a `60-second` timeout.

## Approach (`main.py`)
1. **Preprocessing:** Loads the input image in RGB mode at its native resolution (without resizing or cropping), scales pixel values to `[0, 1]`, and applies standard ImageNet normalization (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`).
2. **Targeted I-FGSM / PGD Attack:** Runs up to 60 gradient descent steps minimizing `CrossEntropyLoss` toward target class `665`, projecting perturbations back into the valid `[orig - 1/255, orig + 1/255]` box after each step.
3. **Quantization-Aware Verification:** Rounds candidate tensors to `uint8` (`0–255`) at every iteration and re-evaluates model confidence on the discrete pixel array to prevent precision loss upon PNG encoding. Exits early once quantized confidence reaches `>= 0.995`.

## Directory Structure
* `main.py` — standalone submission script.
* `challenge_model.py` — challenge constants and helper utilities.
* `classifier/mobilenet_v3_large-5c1a4163.pth` — pretrained model checkpoint.
* `train-input.png` / `train-output.png` — sample input and reference output images.
* `requirements.txt` — pinned Python dependencies.

## Usage

Install dependencies:
```bash
pip install -r requirements.txt --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)