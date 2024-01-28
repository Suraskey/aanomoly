import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import numpy as np

# SYNTHETIC DATA CREATION
time_values = np.arange(17 * 60 * 60, 17 * 60 * 60 + 100, 5)
base_data = [
    [f"{h:02d}:{m:02d}:{s:02d}", f"{40 + 0.2 * i:.1f} psi", f"{5000 + 300 * i:.0f} ft", f"{54 - i:.0f} F"]
    for i, (h, m, s) in enumerate(zip((time_values // 3600), (time_values % 3600) // 60, (time_values % 3600) % 60))
]
data_points = []
np.random.seed(42)
for _ in range(90):
    variation = [[entry[0], f"{float(entry[1].split()[0]) + np.random.uniform(-0.5, 0.5):.1f} psi",
                  f"{float(entry[2].split()[0]) + np.random.uniform(-100, 100):.0f} ft",
                  f"{float(entry[3].split()[0]) + np.random.uniform(-1, 1):.0f} F"] for entry in base_data]
    data_points.extend(variation)

data = pd.DataFrame(data_points, columns=["time", "oil_pressure", "altitude", "temperature"])
data["oil_pressure"] = data["oil_pressure"].str.extract('(\d+\.\d+)', expand=False).astype(float)
data["temperature"] = data["temperature"].str.extract('(\d+)', expand=False).astype(float)
X = data[["oil_pressure", "temperature"]]

# REDUCE THE NUMBER OF OUTLIERS
model = IsolationForest(contamination=0.01, random_state=42)
model.fit(X)

outlierScores = model.decision_function(X)

normalized_scores = (outlierScores - outlierScores.min()) / (outlierScores.max() - outlierScores.min())

colors = plt.cm.RdBu(normalized_scores)

plt.scatter(data.index, data["oil_pressure"], c=colors, cmap='RdBu')
plt.xlabel('Minutes Since Start')
plt.ylabel('Oil Pressure (psi)')
plt.title('AAnomoly CFM LEAP-1A')
plt.savefig('anomaly_chart.png')
plt.show()
