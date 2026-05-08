import time
from pathlib import Path
from typing import Iterable

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

from utils import VALID_BASES


AXIS_COLORS = {"x": "#d62728", "y": "#2ca02c", "z": "#1f77b4"}
ACC_COLS = ("acc_x", "acc_y", "acc_z")
GYR_COLS = ("gyr_x", "gyr_y", "gyr_z")




# Plot Window to visualize The data for Each User

def plot(ax, df, sensor, user_name, hand):
    if not df.empty:
        df_plot = df.copy()

        cols = [f'{sensor}_x', f'{sensor}_y', f'{sensor}_z']
        for col in cols:
            df_plot[col] = pd.to_numeric(df_plot[col], errors='coerce')

        ax.plot(df_plot.index, df_plot[f'{sensor}_x'], label='X', color='red', lw=1)
        ax.plot(df_plot.index, df_plot[f'{sensor}_y'], label='Y', color='green', lw=1)
        ax.plot(df_plot.index, df_plot[f'{sensor}_z'], label='Z', color='blue', lw=1)

    if hand == 0:
        ax.set_xlabel("Sample Thumb")
    else:
        ax.set_xlabel("Sample Index")

    ax.set_title(f"{user_name} | {sensor.upper()}")
    ax.grid(True, alpha=0.2)


def Plot_6axis_window2(all_users_dicts, gesture, limit=128):

    fig, axes = plt.subplots(4, 3, figsize=(20, 18))
    fig.suptitle(f"6-Axis Analysis (Thumb vs Index): {gesture}", fontsize=20, fontweight='bold')

    user_names = ['Vasilis', 'Stamy', 'Alex']

    for col, name in enumerate(user_names):
        u_dict = all_users_dicts.get(name, {})
        gesture_data = u_dict.get(gesture, {})
        if gesture == 'texting':
            df_t = gesture_data.get('na', pd.DataFrame())
            df_i = None
        else:
            df_t = gesture_data.get('thumb', pd.DataFrame())
            df_i = gesture_data.get('index', pd.DataFrame())

        df_t = df_t.iloc[:limit]
        for row, sensor in enumerate(['acc', 'gyr']):
            ax = axes[row, col]
            ax.cla()
            plot(ax, df_t, sensor, user_names[col],0)

        if df_i is not None and not df_i.empty:
            df_i = df_i.iloc[:limit]
            for row, sensor in enumerate(['acc', 'gyr']):

                ax = axes[row + 2, col]
                ax.cla()
                plot(ax, df_i, sensor, user_names[col], 1)
        else:
            axes[2, col].set_visible(False)
            axes[3, col].set_visible(False)


    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def Plot_6axis(all_users_dicts):

    for gesture in VALID_BASES:
        Plot_6axis_window2(all_users_dicts, gesture)

