import sys
import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F
from torchvision.models import mobilenet_v3_large

# Определяем пути (по умолчанию для проверки на сервере)
input_path = "test-input.png"
output_path = "test-output.png"

if "--input" in sys.argv:
    input_path = sys.argv[sys.argv.index("--input") + 1]
if "--output" in sys.argv:
    output_path = sys.argv[sys.argv.index("--output") + 1]

# 1. Загружаем модель
model = mobilenet_v3_large(weights=None)
weights = torch.load("classifier/mobilenet_v3_large-5c1a4163.pth", map_location="cpu", weights_only=True)
model.load_state_dict(weights)
model.eval()

# 2. Загружаем картинку и переводим в тензор [1, 3, H, W] в диапазоне [0, 1]
orig_uint8 = np.array(Image.open(input_path).convert("RGB"), dtype=np.uint8)
orig = torch.from_numpy(orig_uint8).permute(2, 0, 1).unsqueeze(0).float() / 255.0

low = torch.clamp(orig - 1.0 / 255.0, 0.0, 1.0)
high = torch.clamp(orig + 1.0 / 255.0, 0.0, 1.0)

mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)

# 3. Итеративная атака (I-FGSM / PGD) на класс 665 (moped)
adv = orig.clone()
target = torch.tensor([665])
step_size = 0.25 / 255.0

best_img = orig_uint8
best_prob = 0.0

for _ in range(60):
    adv.requires_grad_(True)
    logits = model((adv - mean) / std)
    loss = F.cross_entropy(logits, target)
    loss.backward()

    # Делаем шаг против градиента и обрезаем в рамки +-1 пиксель
    with torch.no_grad():
        adv = torch.clamp(adv - step_size * adv.grad.sign(), low, high)

        # Проверяем уверенность после округления в целые пиксели (как при сохранении PNG)
        cand_uint8 = np.rint(adv.squeeze(0).permute(1, 2, 0).numpy() * 255.0).astype(np.uint8)
        cand_t = torch.from_numpy(cand_uint8).permute(2, 0, 1).unsqueeze(0).float() / 255.0
        probs = F.softmax(model((cand_t - mean) / std), dim=1)[0]
        prob_665 = probs[665].item()

        if prob_665 > best_prob:
            best_prob = prob_665
            best_img = cand_uint8

        if probs.argmax().item() == 665 and prob_665 >= 0.995:
            break

# 4. Сохраняем результат
Image.fromarray(best_img, mode="RGB").save(output_path, format="PNG", optimize=True)