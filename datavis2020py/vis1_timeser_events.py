from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as ptc
import matplotlib.dates as mdt
import datetime as dt
import numpy as np
import math

raw, evn, mf, tdc = read_data()





dates = evn['start'].map(lambda t: t.date()).unique()
# dates = dates[range(2)]
daysper = 3
n=1
collapse = 1 #0 to show on different y values, 1 to show on same y
for d in range(len(dates)):
    tots = pd.DataFrame(index=tdc[0], columns=['vol'])
    tots['vol'] = 0
    pnum = math.fmod(d, daysper)+1
    # print(pnum)
    if pnum == 1:
        fig = plt.figure(figsize=[16, 16])
    ax = fig.add_subplot(daysper,1,pnum)
    dtstr = dates[d].strftime('%b-%d-%Y')
    dmn = dt.datetime.combine(dates[d], dt.time())
    td = dmn
    tm = dmn + dt.timedelta(days=1)
    print(dtstr)
    ax.set_ylabel(dtstr + '\nFlow Rate Water Used (gal/min)')


    dayraw = raw[(raw.index >= td) & (raw.index < tm)]
    dayevn = evn[(evn['start'] >= td) & (evn['start'] < tm)].reset_index()
    pts = ax.plot(dayraw.index,dayraw.gpm,'-',color='black',alpha=1,label = 'Flow Rate Water Used (gal/min)')
    ax2 = ax.twinx()
    for i in range(0,len(dayevn.index)):
        l = dayevn.loc[i,'label']
        v = dayevn.loc[i,'vol']
        tots.loc[l,'vol'] = tots.loc[l,'vol'] + v
        s = mdt.date2num(dayevn.loc[i,'start'])
        e = mdt.date2num(dayevn.loc[i,'end'])
        if collapse == 0:
            y = dayevn.loc[i,'cnum']
        else:
            y = 0
        r = ptc.Rectangle((s,y),e-s,1,color=dayevn.loc[i,'col'],alpha=0.4)
        ax2.add_patch(r)
    fmt = mdt.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(fmt)
    if collapse == 0:
        ax2.set_ylim([0,6])
        ax2.set_yticks(np.arange(0.5,7,1))
        ax2.set_yticklabels(tdc[0])
    else:
        ax2.set_ylim([0,1])
        ax2.axes.get_yaxis().set_visible(False)

    tots = tots.append(pd.DataFrame({'vol':sum(tots['vol'])},index=['sum']))
    tots['prop'] = (tots['vol']/tots.loc['sum','vol'])*100
    leg=pts
    for t in tots.index:
        if not t == 'sum':
            lab = t+': ' + str(round(tots.loc[t,'prop'],1)) + '% (' + \
                str(round(tots.loc[t, 'vol'], 1)) + ' gal)'
            c = np.unique(evn.loc[evn['label']==t,'col'])[0]
            hdl = ptc.Patch(color = c, label = lab)
            leg.append(hdl)
    lgd = ax2.legend(handles = leg,title = 'Daily Totals',bbox_to_anchor=(1.1,1))
    ax.set_xlim([td,tm])
    if pnum == daysper:
        plt.savefig('Images/Time Series ' + str(n) +'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
        n = n + 1
plt.draw()
plt.show()