from inspect import FrameInfo
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签 
plt.rcParams['axes.unicode_minus']=False


def readdata():
    result = []
    f = open('frequency.txt')
    datas = f.readlines()
    for data in datas:
        line = data.split(',')
        temp = []
        for i in range(1, len(line)):
            temp.append(float(line[i]))
        result.append(temp)
    return result


x = np.arange(0, 24, 1)
fig, axs = plt.subplots(4,3)
datas = readdata()

labels = np.arange(0, 25, 5)

i = 0
for data in datas:
    row = i//3
    col = i - row*3
    axs[row, col].plot(x, data, '-o', markersize=2, label="作业{}".format(i+1))
    axs[row, col].set_ylim(1.4, 2.6)
    axs[row, col].set_xticks(labels)
    
    axs[row, col].xaxis.set_tick_params(rotation=-30)
    axs[row, col].yaxis.set_tick_params(rotation=-30)
    if col!=0:
        axs[row, col].set_yticklabels([])
    if row !=3:
        axs[row, col].set_xticklabels([])
    if col == 0:
        axs[row, col].set_ylabel('频率/GHz')
    if row == 3:
        axs[row, col].set_xlabel('时段/h')

    axs[row, col].grid(True)
    axs[row, col].legend(fontsize=8, frameon=False, loc='upper right')
    i += 1

plt.tight_layout()
plt.savefig('fig1.png', dpi=300, bbox_inches = 'tight')