import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

# 1. Загрузка датасета
df = pd.read_csv('potato_fields.csv')

# 2. Вычисление короткой стороны поля (1 га = 10 000 м²)
df['short_side_m'] = (df['area_ha'] * 10000) / df['long_side_m']

# 3. Обучение линейной модели по декларированным параметрам
X = df[['long_side_m', 'short_side_m', 'ditch_m']]
y = df['edge_m']

model = LinearRegression()
model.fit(X, y)

print(f'R^2 score: {model.score(X, y):.6f}')

# 4. Расчёт предсказаний и остатков (residuals)
df['predicted_edge'] = model.predict(X)
df['residual'] = df['edge_m'] - df['predicted_edge']

# 5. Визуализация остатков — проявление слова SUPERVISION
plt.figure(figsize=(12, 4), dpi=150)
plt.scatter(df['predicted_edge'], df['residual'], s=8, alpha=0.8)
plt.title(
    'Model Residuals vs Predicted Edge Length (edge_m)',
    fontsize=13,
    fontweight='bold',
)
plt.xlabel('Predicted Edge Length (m)')
plt.ylabel('Residual (edge_m - predicted)')
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('supervision_flag.png')
plt.show()
