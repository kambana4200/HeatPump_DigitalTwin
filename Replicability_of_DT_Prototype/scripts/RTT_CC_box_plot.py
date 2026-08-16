import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.patches import ConnectionPatch


# DATA

encrypted = [
    68,957,951,937,1120,1102,966,917,961,390,
    924,1042,1311,85,64,721,1078,1143,1390,894
]

unencrypted = [
    197,122,156,42,106,183,113,159,104,152,
    132,36,159,133,38,140,142,121,138,121
]


# MAIN FIGURE

fig, ax = plt.subplots(figsize=(8,6))


box = ax.boxplot(
    [encrypted, unencrypted],
    patch_artist=True,
    widths=0.55,
    showmeans=True,
    meanline=True,
    labels=[
        "Encrypted\nOPC UA",
        "Unencrypted\nOPC UA"
    ]
)

ax.tick_params(axis='x', labelsize=8)


# COLORS

colors = ['royalblue', 'lightgray']

for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)


# Median

for median in box['medians']:
    median.set(
        color='red',
        linewidth=2
    )


# Mean

for mean in box['means']:
    mean.set(
        color='black',
        linewidth=2
    )


# Whiskers

for whisker in box['whiskers']:
    whisker.set(color='black')


# Caps

for cap in box['caps']:
    cap.set(color='black')


# Outliers

for flier in box['fliers']:
    flier.set(
        marker='o',
        markerfacecolor='orange',
        markeredgecolor='black',
        markersize=7,
        alpha=0.8
    )



# LABELS

ax.set_ylabel(
    "Round-Trip Time RTT_CC in ms",
    fontsize=8
)


ax.set_title(
    "Distribution of Command Control RTT Measurements",
    fontsize=9,
    fontweight='bold'
)


ax.grid(
    axis='y',
    linestyle='--',
    alpha=0.4
)



# STATISTICS

mean_enc = np.mean(encrypted)
std_enc = np.std(encrypted, ddof=1)

mean_un = np.mean(unencrypted)
std_un = np.std(unencrypted, ddof=1)


text = (
    f"OPC UA Encrypted\n"
    f"Mean = {mean_enc:.1f} ms\n"
    f"Std = {std_enc:.1f} ms\n\n"

    f"OPC UA Unencrypted\n"
    f"Mean = {mean_un:.1f} ms\n"
    f"Std = {std_un:.1f} ms"
)


ax.text(
    1.03,
    0.97,
    text,
    transform=ax.transAxes,
    fontsize=8,
    verticalalignment='top',
    bbox=dict(
        facecolor='white',
        edgecolor='gray',
        alpha=0.95,
        boxstyle='round'
    )
)


# INSET : ZOOM ON UNENCRYPTED OPC UA

axins = inset_axes(
    ax,
    width="35%",
    height="35%",
    loc="upper right",
    borderpad=2
)


zoom_box = axins.boxplot(
    [unencrypted],
    patch_artist=True,
    widths=0.5,
    showmeans=True,
    meanline=True
)



zoom_box['boxes'][0].set_facecolor('lightgray')


zoom_box['medians'][0].set(
    color='red',
    linewidth=2
)


zoom_box['means'][0].set(
    color='black',
    linewidth=2
)


for whisker in zoom_box['whiskers']:
    whisker.set(color='black')


for cap in zoom_box['caps']:
    cap.set(color='black')


for flier in zoom_box['fliers']:
    flier.set(
        marker='o',
        markerfacecolor='orange',
        markeredgecolor='black',
        markersize=5
    )



axins.set_ylim(
    min(unencrypted)-15,
    max(unencrypted)+15
)


axins.set_xticks([])


axins.set_title(
    "Unencrypted OPC UA",
    fontsize=8,
    fontweight='bold'
)


axins.grid(
    axis='y',
    linestyle='--',
    alpha=0.3
)


# CLEAN FOUR-CORNER CONNECTION

x_left = 1.65
x_right = 2.35

y_bottom = min(unencrypted)-15
y_top = max(unencrypted)+15



# Target rectangle

ax.add_patch(
    plt.Rectangle(
        (x_left, y_bottom),
        x_right-x_left,
        y_top-y_bottom,
        fill=False,
        edgecolor="0.5",
        linewidth=1
    )
)



# Upper-left connection

fig.add_artist(
    ConnectionPatch(
        xyA=(x_left, y_top),
        coordsA=ax.transData,
        xyB=(0, 1),
        coordsB=axins.transAxes,
        color="0.5",
        linewidth=1
    )
)



# Upper-right connection

fig.add_artist(
    ConnectionPatch(
        xyA=(x_right, y_top),
        coordsA=ax.transData,
        xyB=(1, 1),
        coordsB=axins.transAxes,
        color="0.5",
        linewidth=1
    )
)



# Lower-left connection

fig.add_artist(
    ConnectionPatch(
        xyA=(x_left, y_bottom),
        coordsA=ax.transData,
        xyB=(0, 0),
        coordsB=axins.transAxes,
        color="0.5",
        linewidth=1
    )
)



# Lower-right connection

fig.add_artist(
    ConnectionPatch(
        xyA=(x_right, y_bottom),
        coordsA=ax.transData,
        xyB=(1, 0),
        coordsB=axins.transAxes,
        color="0.5",
        linewidth=1
    )
)


# LEGEND


legend_elements = [

    Line2D(
        [0], [0],
        color='black',
        lw=2,
        label='Mean'
    ),

    Line2D(
        [0], [0],
        color='red',
        lw=2,
        label='Median'
    ),

    Line2D(
        [0], [0],
        marker='o',
        linestyle='None',
        markerfacecolor='orange',
        markeredgecolor='black',
        markersize=7,
        label='Outlier'
    )

]


ax.legend(
    handles=legend_elements,
    loc='lower left',
    bbox_to_anchor=(1.05,0.05),
    frameon=True,
    fontsize=8
)



# EXPORT / DISPLAY

plt.tight_layout()

plt.show()