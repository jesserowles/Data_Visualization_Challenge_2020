from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np

raw, evn, mf, tdc = read_data()
evn.index = evn['start']

dates = evn['start'].map(lambda t: t.date()).unique()
tots = pd.DataFrame(index=pd.DatetimeIndex(dates),columns=tdc[0])

othertots = tots.copy()

for i in tots.index:
    evnbt = evn.loc[(evn['start']>=i) & (evn['start'] < (i+dt.timedelta(hours=12))),:]
    for j in tots.columns:
        tots.loc[i,j] = evnbt.loc[evnbt['label']==j,'vol'].sum()
        othertots.loc[i,j] = evnbt.loc[evnbt['label']==j,'vol'].sum() * np.random.normal(loc=0.7,scale=0.2)

tots = tots.drop('irrigation',axis = 1)
othertots = othertots.drop('irrigation',axis = 1)
tots['Total'] = tots.sum(axis=1)
othertots['Total'] = othertots.sum(axis=1)

datlabs = [i.strftime('%b-%d') for i in dates]
for c in tots.columns:
    if c != 'Total':
        col = np.array(tdc[2])[tdc[0] == c][0]
    else:
        col = 'teal'
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    offset = max(tots[c])*0.03
    bins = np.linspace(0, max(max(othertots[c]), max(tots[c])+offset), 10)
    plt.hist(tots[c],color=col,alpha=0.9,edgecolor=col,linewidth=4,bins=bins)
    plt.hist(othertots[c],color='grey',alpha=0.5,edgecolor='black',linewidth=4,bins=bins-offset)
    plt.xlabel('Volume of Water Used (gal)')
    plt.ylabel('Number of Days')
    plt.title('Histogram of Total Water Used in Each Day: ' + c.capitalize() +'\nCompared to Nearby Homes')
    plt.legend(['Your Home','Nearby Homes'])
    plt.savefig('Images/Histogram Compare ' +c+'.png')
    plt.show()
