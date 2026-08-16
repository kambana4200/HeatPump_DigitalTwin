import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Data
data = {
    "Set Point Temperature in °C": [
        16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
        26, 27, 28, 29, 30, 31, 32, 33, 34, 35
    ],
    "RTT_CC_ENCRYPTED_CNX": [
        68, 957, 951, 937, 1120, 1102, 966, 917, 961, 390,
        924, 1042, 1311, 85, 64, 721, 1078, 1143, 1390, 894
    ],
    "RTT_CC_UNENCRYPTED_CNX": [
        197, 122, 156, 42, 106, 183, 113, 159, 104, 152,
        132, 36, 159, 133, 38, 140, 142, 121, 138, 121
    ]
}

df = pd.DataFrame(data)

plt.figure(figsize=(14, 6))

# plot lollipops
# Encrypted in blue
plt.vlines(x=df["Set Point Temperature in °C"], ymin=0, ymax=df["RTT_CC_ENCRYPTED_CNX"], color='blue', alpha=0.7, linewidth=2)
plt.scatter(df["Set Point Temperature in °C"], df["RTT_CC_ENCRYPTED_CNX"], color='blue', s=80, label='RTT on OPC UA Client/server 4G LTE Encrypted Flow')

# Unencrypted in grey
plt.vlines(x=df["Set Point Temperature in °C"], ymin=0, ymax=df["RTT_CC_UNENCRYPTED_CNX"], color='grey', alpha=0.7, linewidth=2)
plt.scatter(df["Set Point Temperature in °C"], df["RTT_CC_UNENCRYPTED_CNX"], color='grey', s=80, label='RTT on OPC UA Client/server 4G LTE UNEncrypted Flow with Anonymized User Connexion')

# X Axis
plt.xticks(ticks=np.arange(df["Set Point Temperature in °C"].min(), df["Set Point Temperature in °C"].max() + 1, 1))
plt.title("Lollipop Chart of RTT when sending control commands from Digital Twin to Industrial Control System",fontsize=14,
    fontweight='bold')
plt.xlabel("Set Point Temperature (°C) sent",fontsize=11)
plt.ylabel("Round Trip Time of Command Control (RTT_CC) in ms",fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)

# compute statistical metrics
def print_stats(series, name):

    q1 = series.quantile(0.25, interpolation='midpoint')
    median = series.quantile(0.50, interpolation='midpoint')
    q3 = series.quantile(0.75, interpolation='midpoint')
    mean = series.mean()
    std = series.std()

    # Range
    minimum = series.min()
    maximum = series.max()
    data_range = maximum - minimum

    # Acquisition threshold (1 seconde)
    threshold = 1000

    exceeding = series > threshold
    number_exceeding = exceeding.sum()
    total_measurements = len(series)

    proportion_exceeding = (
        number_exceeding / total_measurements
    ) * 100

    print("=" * 60)
    print(name)
    print("=" * 60)

    print(f"Minimum:                    {minimum:.1f} ms")
    print(f"Maximum:                    {maximum:.1f} ms")
    print(f"Range:                      {data_range:.1f} ms")
    print(f"Q1:                         {q1:.1f} ms")
    print(f"Median:                     {median:.1f} ms")
    print(f"Q3:                         {q3:.1f} ms")
    print(f"Mean:                       {mean:.1f} ms")
    print(f"Standard deviation:         {std:.1f} ms")

    print(f"Measurements > 1 second:    {number_exceeding}/{total_measurements}")
    print(f"Proportion > 1 second:      {proportion_exceeding:.1f}%")

    print(f"Values > 1 second:          {series[exceeding].tolist()}")

    print()

stats_enc = print_stats(df["RTT_CC_ENCRYPTED_CNX"], "RTT_CC_ENCRYPTED_CNX")
stats_unenc = print_stats(df["RTT_CC_UNENCRYPTED_CNX"], "RTT_CC_UNENCRYPTED_CNX")

# Custom legend
custom_legend = [
    Patch(color='blue', label='RTT_CC on OPC UA Encrypted Flow over 4G LTE NETWORK'),
    Patch(color='grey', label='RTT_CC on OPC UA Unencrypted Flow over 4G LTE NETWORK with Anonymized User Connexion'),
    #Patch(color='none', label=f"RTT_CC on Encrypted Flow: Q1={stats_enc[0]:.0f} ms, Median={stats_enc[1]:.0f} ms, Q3={stats_enc[2]:.0f} ms, Mean={stats_enc[3]:.0f} ms, Std={stats_enc[4]:.0f} ms"),
    #Patch(color='none', label=f"RTT_CC on NON-Encrypted Flow: Q1={stats_unenc[0]:.0f} ms, Median={stats_unenc[1]:.0f} ms, Q3={stats_unenc[2]:.0f} ms, Mean={stats_unenc[3]:.0f} ms, Std={stats_unenc[4]:.0f} ms")
]

plt.legend(handles=custom_legend, loc='upper center', bbox_to_anchor=(0.5, -0.25),
           ncol=1, frameon=False, fontsize=12)

plt.tight_layout()
plt.show()
