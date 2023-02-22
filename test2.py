
import numpy as np
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签 
plt.rcParams['axes.unicode_minus']=False


def readdata():
    f = open('diff.txt', 'r')
    datas = f.readlines()
    ori_costs = []
    new_costs = []
    for data in datas:
        line = data.split(',')
        ori_cost = float(line[1])/1000
        new_cost = float(line[2])/1000
        ori_costs.append(ori_cost)
        new_costs.append(new_cost)
    
    f.close()
    return ori_costs, new_costs


fig, ax = plt.subplots(1,1)
labels = np.arange(1, 13, 1)

ori_costs, new_costs = readdata()

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars
ax.bar(x - width/2, ori_costs, width, label='正常', color='b', hatch="///")
ax.bar(x + width/2, new_costs, width, label='调频', color='g', hatch="xxx")
ax.grid(True)
#ax.set_ylim(0,75)
ax.set_ylabel('单核费用/元')
ax.legend(loc='upper right')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_xlabel('作业')


fig.tight_layout()
plt.savefig("diff.png", dpi=300, bbox_inches = 'tight')
