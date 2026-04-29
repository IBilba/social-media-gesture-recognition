import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from pathlib import Path

def readcsv(filename):
    df = pd.read_csv(filename)
    return df

def getFilenames(base):
    path = Path(base)
    filenames = list(path.rglob('*.csv'))
    return filenames


def update(frame,scat,df):
    step=100
    end = frame * step
    start = max(0, end - 700)
    data =df.iloc[start:end]


    scat._offsets3d = (data['X'], data['Y'], data['Z'])

    scat.set_array(data['Epoch'])
    return scat

def plotUncropedData(df,name):
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
    ani = FuncAnimation(fig, update, frames=num_frames, fargs=(scat, df) ,interval=1, blit=False)


    print("Αποθήκευση βίντεο... περιμένετε.")
    out = f"{name}.4d_motion.mp4"
    ani.save(out, writer='ffmpeg', fps=80)
    print("Το βίντεο αποθηκεύτηκε ως", out)

    plt.draw()
    plt.pause(5)
    plt.close(fig)



def main():
    base = "/home/stamylaptop/PycharmProjects/CropDataProject/data"
    filenames = getFilenames(base)
    for name in filenames:
        df = readcsv(name)
        clean_name = name.stem.strip()
        plotUncropedData(df,clean_name)



if __name__ == "__main__":
    main()