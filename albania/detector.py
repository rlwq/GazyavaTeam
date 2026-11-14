import numpy as np
from collections import deque

cols = ["temperature_c", "humidity_pct", "vibration_g", "acoustic_db", "air_pressure_kpa", "co2_ppm"]


class Detector:
    def __init__(self, b=0.1, zp=6, ze=2, g=3, lam=10, warm=60, bf=0.4, zf=2):
        self.b, self.zp, self.ze, self.g, self.warm, self.bf, self.zf = b, zp, ze, g, warm, bf, zf
        self.t = 0
        self.AA = np.array([np.diag([1e-6, lam, lam, lam, lam]) for _ in cols])
        self.Av = np.zeros((6, 5))
        self.h = []
        self.r = deque(maxlen=300)
        self.ew = np.zeros(6)
        self.ef = np.zeros(6)

    def update(self, reading):
        v = np.array([float(reading[c]) for c in cols])
        t = self.t
        self.t += 1
        w = 2 * np.pi * t
        a = np.array([1, np.sin(w / 720), np.cos(w / 720), np.sin(w / 1200), np.cos(w / 1200)])
        if t < self.warm:
            self.AA += np.outer(a, a)
            self.Av += np.outer(v, a)
            self.h.append((a, v))
            if t == self.warm - 1:
                for aa, vv in self.h:
                    self.r.append(vv - np.array([aa @ np.linalg.solve(self.AA[i], self.Av[i]) for i in range(6)]))
            return 0.0
        p = np.array([a @ np.linalg.solve(self.AA[i], self.Av[i]) for i in range(6)])
        sd = np.sqrt(np.mean(np.square(self.r), 0)) + 1e-12
        z = (v - p) / sd
        self.r.append(np.clip(v - p, -3 * sd, 3 * sd))
        ok = np.abs(z) < self.g
        self.AA[ok] += np.outer(a, a)
        self.Av[ok] += np.outer(v, a)[ok]
        self.ew = (1 - self.b) * self.ew + self.b * np.clip(z, -10, 10)
        self.ef = (1 - self.bf) * self.ef + self.bf * np.clip(z, -10, 10)
        bad = np.abs(z).max() > self.zp or (np.linalg.norm(self.ew) > self.ze and np.linalg.norm(self.ef) > self.zf)
        return 1.0 if bad else 0.0
