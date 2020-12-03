from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd

raw, evn, mf, tdc = read_data()
tots = pd.DataFrame({'col':tdc[2],'vol':0})
tots.index = tdc[0]

for i in tots.index:
    tots.loc[i,'vol'] = evn.loc[evn['label']==i,'vol'].sum()


tots = tots.append(pd.DataFrame({'vol':sum(tots['vol'])},index=['sum']))
tots = tots.append(pd.DataFrame({'vol':sum(tots.loc[(tots.index != 'sum') & (tots.index != 'irrigation'), 'vol'])},index=['sum_noir']))
tots['prop_all'] = (tots['vol']/tots.loc['sum','vol'])*100
tots['prop_noir'] = (tots['vol']/tots.loc['sum_noir','vol'])*100


laball = tots.index[(tots.index != 'sum') & (tots.index != 'sum_noir')]
szeall = list((tots.loc[laball,'vol']*100).astype('int'))
clrall = tots.loc[(tots.index != 'sum') & (tots.index != 'sum_noir'),'col']
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
p=ax.pie(szeall,labels=laball, startangle=0,autopct='%1.1f%%',colors=clrall,pctdistance = 1.13,labeldistance=1.28)
[p[0][i].set_alpha(0.5) for i in range(len(p[0]))]
plt.title('Proportion of Cumulative Water Used by Type (Volume)')
plt.savefig('Images/Pie Water Use By Type.png')
plt.show()


labnir = tots.index[(tots.index != 'sum') & (tots.index != 'sum_noir') & (tots.index != 'irrigation')]
szenir = list((tots.loc[labnir,'vol']*100).astype('int'))
clrnir = tots.loc[(tots.index != 'sum') & (tots.index != 'sum_noir') & (tots.index != 'irrigation'),'col']
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
p=ax.pie(szenir,labels=labnir, startangle=0,autopct='%1.1f%%',colors=clrnir,labeldistance=1.1)
[p[0][i].set_alpha(0.5) for i in range(len(p[0]))]
plt.title('Proportion of Cumulative Water Used by Type Without Irrigation (Volume)')
plt.savefig('Images/Pie Water Use No Irr.png')
plt.show()
