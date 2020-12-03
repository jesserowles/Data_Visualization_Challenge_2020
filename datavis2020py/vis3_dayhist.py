from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np


raw, evn, mf, tdc = read_data()
evn.index = evn['start']

tots = pd.DataFrame({'col':tdc[2]})
tots.index = tdc[0]
bins = pd.date_range('2020-07-01', periods=24, freq='1H')
for i in bins:
    ct = i.strftime('%H:%M')
    tots[ct] = 0
    evnbt = evn.between_time(ct, (i+dt.timedelta(minutes=60)).strftime('%H:%M'))
    totyp = evnbt.groupby('label').sum()['vol']
    tots.loc[totyp.index, ct] = totyp

labels = bins.strftime('%H:%M')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
bot = np.zeros(len(bins))
hands = []
for t in tots.index:
    vals = tots.loc[t,:].values[1:]
    c = evn.loc[evn['label'] == t, 'col'][0]
    ax.bar(labels,vals,bottom=bot,color=c)
    hands.append(t)
    bot = vals + bot
ax.legend(hands)
ax.set_ylim([0,300])
ax.set_ylabel('Volume Water Used (gal)')
plt.title('Total Volume of Water Used by Type of Use\nIn Each Hour of Day')
plt.xticks(rotation=90)
plt.savefig('Images/Hourly Stacked Bar.png')
plt.show()
