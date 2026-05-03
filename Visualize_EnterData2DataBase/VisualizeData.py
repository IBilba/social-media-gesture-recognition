import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from pathlib import Path


#methods to read file and cluster them
def helperCluster(movement,hand,base):
    base = Path(base)
    tmp = []
    tmp1 = []
    tmp2 = []
    if hand == None:
        full_path = base / movement
    else:
        full_path = base / movement / hand

    for file in full_path.rglob('*.csv'):
        clean_name = file.stem.strip()
        type_label = clean_name[-1]
        if type_label == 'a':
            tmp.append(file)
        elif type_label == 'v':
            tmp1.append(file)
        else:
            tmp2.append(file)
    return tmp, tmp1,tmp2
def ClusteringResults(base):
    alexandros = []
    vasilis = []
    stamatia = []

    scenarios = [
        ("scroll-down", "index"),
        ("scroll-down", "thumb"),
        ("scroll-up", "index"),
        ("scroll-down", "thumb"),
        ("swipe-left", "index"),
        ("swipe-right", "thumb"),
        ("swipe-right", "index"),
        ("swipe-right", "thumb"),
        ("texting", None)
    ]

    for movement, hand in scenarios:
        tmp, tmp1, tmp2 = helperCluster(movement, hand,base)
        alexandros.extend(tmp)
        vasilis.extend(tmp1)
        stamatia.extend(tmp2)

    return alexandros, vasilis, stamatia
def getFilenames(base):
    path = Path(base)
    filenames = list(path.rglob('*.csv'))
    return filenames

#-------------------------------------------------------#

#plot data in 6axis
def update_6axis(frame, scat_a, df_a, scat_b, df_b):
    step = 100
    end = frame * step
    start = max(0, end - 700)

    data_a = df_a.iloc[start:end]
    scat_a._offsets3d = (data_a['X'], data_a['Y'], data_a['Z'])


    data_b = df_b.iloc[start:end]
    scat_b._offsets3d = (data_b['X'], data_b['Y'], data_b['Z'])


    return scat_a, scat_b
def Plot_6axis(df_a, df_b, name):
    df_a.columns = df_a.columns.str.strip()
    df_b.columns = df_b.columns.str.strip()

    for df in [df_a, df_b]:
        for col in ['X', 'Y', 'Z']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        # Προαιρετικά: αφαιρούμε γραμμές με κενά (NaN)
        df.dropna(subset=['X', 'Y', 'Z'], inplace=True)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Όρια που να καλύπτουν και τα δύο αρχεία
    ax.set_xlim(min(df_a['X'].min(), df_b['X'].min()), max(df_a['X'].max(), df_b['X'].max()))
    ax.set_ylim(min(df_a['Y'].min(), df_b['Y'].min()), max(df_a['Y'].max(), df_b['Y'].max()))
    ax.set_zlim(min(df_a['Z'].min(), df_b['Z'].min()), max(df_a['Z'].max(), df_b['Z'].max()))

    ax.set_title(f"Comparison: {name}")

    # Δημιουργία δύο διαφορετικών scatters με διαφορετικά χρώματα
    scat_a = ax.scatter([], [], [], c='red', s=2, label='Gyroscope')
    scat_b = ax.scatter([], [], [], c='blue', s=2, label='Acellerometer')
    ax.legend()

    num_frames = min(len(df_a), len(df_b)) // 100

    # Περνάμε και τα 2 scatters και τα 2 dfs στα fargs
    ani = FuncAnimation(fig, update_6axis, frames=num_frames,
                        fargs=(scat_a, df_a, scat_b, df_b),
                        interval=1, blit=False)

    out = f"{name}_paired_motion.mp4"
    ani.save(out, writer='ffmpeg', fps=80)

    plt.draw()
    plt.pause(5)
    plt.close(fig)
def readcsv_plot6axis(filenames1):
    for i in range(0, len(filenames1) - 1, 2):
        df = pd.read_csv(filenames1[i])
        df2 = pd.read_csv(filenames1[i+1])
        clean_name = filenames1[i].stem.strip()
        clean_name = clean_name + filenames1[i + 1].stem.strip()
        print(f"Σχεδίαση ζευγαριού: {clean_name}")
        Plot_6axis(df, df2, clean_name)
def PlotAllCluster(filenames1,filenames2,filenames3):
    readcsv_plot6axis(filenames1)
    readcsv_plot6axis(filenames2)
    readcsv_plot6axis(filenames3)

#-------------------------------------------------------#

#plot data in 3 axis
def update_3axis(frame,scat,df):
    step=100
    end = frame * step
    start = max(0, end - 700)
    data =df.iloc[start:end]


    scat._offsets3d = (data['X'], data['Y'], data['Z'])

    scat.set_array(data['Epoch'])
    return scat
def Plot_3axis(df,name):
    df.columns = df.columns.str.strip()
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim(df['X'].min(), df['X'].max())
    ax.set_ylim(df['Y'].min(), df['Y'].max())
    ax.set_zlim(df['Z'].min(), df['Z'].max())

    ax.set_title(f"3D Plot: {name}", fontsize=14, pad=20)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    scat = ax.scatter([], [], [], c=[], cmap='viridis', s=2)


    num_frames = len(df) // 100
    ani = FuncAnimation(fig, update_3axis, frames=num_frames, fargs=(scat, df) ,interval=1, blit=False)


    print("Αποθήκευση βίντεο... περιμένετε.")
    out = f"{name}.4d_motion.mp4"
    ani.save(out, writer='ffmpeg', fps=80)
    print("Το βίντεο αποθηκεύτηκε ως", out)

    plt.draw()
    plt.pause(5)
    plt.close(fig)
def readcsv_plot(filenames):
    for name in filenames:
        df = pd.read_csv(name)
        for col in ['X', 'Y', 'Z']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna(subset=['X', 'Y', 'Z'])
        clean_name = name.stem.strip()
        Plot_3axis(df,clean_name)

#------------------------------------------------------#

