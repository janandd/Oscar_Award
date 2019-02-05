#!/usr/bin/python3

# This program is used to plot the outputs and play with those.
# Outputs from file StanleyK.py are pickled together, thereby
# avoiding running the entire programme again.

from os import chdir as cd
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as pch
#from matplotlib.ticker import MaxNLocator


""" *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# Trying to write a function that would stop executiion of the python
# script without exiting or attempting to exit the python shell
def blank_return(num):
    for i in range(10):
        if (num < 0):
            break
        #endif
    #endfor
#end
*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~* """




### *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
### *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

# thap = '/media/anand/Chiba/Users/Anand/Documents/home/python/self/Oscars'
thap = 'C:/Users/Anand/Documents/home/python/self/Oscars'
cd(thap)

g0 = 'Pic.pickle';  g1 = open(g0, 'rb')

# un-pickle results of Best Picture saved in StanleyK.py
[Pic_yy, Pic1_Rel, Pic0_Rel] = pickle.load(g1)
[Pic1_Gen, Pic0_Gen, Pic1_Syn, Pic0_Syn] = pickle.load(g1)

g1.close()

# Delete the variables that you are not working on currently
del Pic1_Rel, Pic0_Rel, Pic1_Syn, Pic0_Syn

# *~*~*~*~*~*~*~*~*~*~*~*~*~ 'Genre' ~*~*~*~*~*~*~*~*~*~*~*~*~*

# unique Genres for both Pic1_Gen and Pic0_Gen
Pic1_G_unq = np.sort(list(set([p2 for p0 in Pic1_Gen for p1 in p0 \
            for p2 in p1]))).tolist()
Pic0_G_unq = np.sort(list(set([p2 for p0 in Pic0_Gen for p1 in p0 \
            for p2 in p1]))).tolist()

# Creating a parent dictionary
Pic1_G_par = {}
# A blank format for child dictionary
Pic1_G_chi = {el:0 for el in Pic1_G_unq}

for i,yy in enumerate(Pic_yy):
    # Initialise f1 to Pic1_G_chi and add Year to it
    f1 = Pic1_G_chi.copy();  f1['Year'] = yy

    # Use dict comprehension to fill in f1
    # This removes the empty keys automatically
    f1 = {p1:f1[p1]+1 for p0 in Pic1_Gen[i] for p1 in p0}
    Pic1_G_par[yy] = f1
#endfor


# Size of bins in years to construct a histogram
yy_hist = 5
# This will store the yy_hist intervalized dicts
Pic1_G_hi5 = {}

for k0,v0 in Pic1_G_par.items():
    if ((k0%yy_hist == 1) or (k0 == 1928)):
        # A dummy copy to store dicts before they are combined when k0%5==0
        f1 = Pic1_G_chi.copy()
    #endif
    f1 = {k1:(v1+Pic1_G_par[k0][k1] if k1 in Pic1_G_par[k0] else v1) \
                    for k1,v1 in f1.items()}
    if (k0%yy_hist == 0):
        # Combine 'Musical' and 'Music' keys into the former, and delete the latter
        f1['Musical'] += f1['Music'];  del f1['Music']
        # Not deleting emtpty keys
        Pic1_G_hi5[k0] = f1
        # Delete keys value 0 [or not]
        # Pic1_G_hi5[k0] = {k2:v2 for k2,v2 in f1.items() if (v2 != 0)}
    #endif
#endfor

# Store a list for every Genre giving number of awards in the 5-year periods
Pic1_G_ji5 = {el:[] for el in Pic1_G_unq if (el != 'Music')}
# loop over the dict where you will store 
for k0 in Pic1_G_ji5.keys():
    f1 = []
    for k1,v1 in Pic1_G_hi5.items():
        f1.append(Pic1_G_hi5[k1][k0])
    Pic1_G_ji5[k0] = f1

# Use different colours for each bar
#colour = plt.cm.rainbow(np.linspace(0,1,len(Pic1_G_ji5)))
colour = ['red', 'orange', 'lime green', 'lavender', 'green', 'tan', \
            'brown', 'teal', 'blue', 'grey', 'peach', 'forest green', \
            'mustard', 'pink', 'cyan', 'magenta', 'violet']
colour = ['xkcd:'+el for el in colour]

# Initialise the figure
fig, ax = plt.subplots()

# Plot the bar-chart for 5-year periods for different Genres
idx = np.arange(len(Pic1_G_hi5.keys()))
wdt = 0.04;  opc = 0.4
wdt = 0.17;  opc = 0.4

# Feed all the information into ax
i = 0                  # countexiter for the colour variable
j0, j1 = [], []        # to store top 5 Genres for each 5-year period
# Getting the unique Genre;  without Music
Pic1_G_unr = Pic1_G_unq.copy();  Pic1_G_unr.remove('Music');

#for k0,v0 in Pic1_G_ji5.items():
#    # This one plots all the genres for all the half-decade periods
#    # DO NOT delete this one
#    ax.bar(idx+wdt*(i-8), v0, wdt, opc, color=colour[i], label=k0)
#    i += 1
#    print(k0, v0)
#    # This one plots all the genres for all the half-decade periods
#    # DO NOT delete this one
#
# Pic1_G_hi5 - contains the [5-year] sum of Genre of the winners of Best Picture
# Pic1_G_ji5 - rearranges Pic1_G_hi5 to contain Genre winners of Best Picture
#              as per their 5-year period, indexed at yy%5 = 0
# Pic1_G_ki5 - should further modify Pic1_G_ji5 to contain only the top 5 Genres
#              in the 5-year period. Only these will be passed to ax.bar
#              to make the bar-chart uncluttered and hence legible


# We convert the dict to DataFrame for a lot more ease in the extraction of
# desired columns, their sorting, labelling and passing to ax
Pic1_G_hj5 = pd.DataFrame.from_dict(Pic1_G_hi5)
for i,y5 in enumerate(Pic1_G_hj5.columns.tolist()):
    # DataFrame of top 5 Genres for the 5-year period
    d0 = Pic1_G_hj5.sort_values(by=y5,ascending=False)[y5][:5]
    #
    # List of the Genre
    k0 = d0.index.tolist()
    # Number of movies in each Genre
    v0 = d0.tolist()
    # And the corresponding colours
    c0 = [colour[Pic1_G_unr.index(el)] for el in k0]

    for j in range(5):
        ax.bar(idx[i]+wdt*(j-2), v0[j], wdt, opc, color=c0[j], label=k0[j])

#    print(k0, v0)
    del d0
    
    
    




ax.set_xlabel('half-decade period')
ax.set_ylabel('number of movies')
ax.set_title('Genre distribution of Best Picture winner over years')
ax.set_xticks(idx)
ax.set_xticklabels(list(Pic1_G_hi5.keys()))

box = ax.get_position()

ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
#ax.legend(loc='center left', bbox_to_anchor=(1,0.5))

#legpatch = pch.Patch(color=colour, label=Pic1_G_unr)
#ax.legend(handles=[legpatch], loc='center left', bbox_to_anchor=(1,0.5))

plt.ylim(0,5.5)
plt.xticks(rotation=75)
fig.set_size_inches(10, 6)
fig.tight_layout()
plt.show()





""" *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# Histogram for an aggregate of all the award winning categories
Pic1_G_his = Pic1_G_chi.copy()
for k0,v0 in Pic1_G_par.items():
    Pic1_G_his = {k1:(v1+Pic1_G_par[k0][k1] if k1 in Pic1_G_par[k0] else v1) \
                  for k1,v1 in Pic1_G_his.items()}
#endfor

# Combine 'Musical' and 'Music' keys into the former, and delete the latter
Pic1_G_his['Musical'] += Pic1_G_his['Music']
del Pic1_G_his['Music']

# Plot the histogram for all the Genres through all the years
fig, (axL, axS) = plt.subplots(2, 1, sharex=True)
idx = np.arange(len(Pic1_G_his))

# Set width, wdt and opacity, opc, of the bars
wdt = 0.6;  opc = 0.4

# Generate aggregate bar chart of Best Picture winning Genre over all the years
axS.bar(idx, list(Pic1_G_his.values()), wdt, alpha=opc, color='b')
axL.bar(idx, list(Pic1_G_his.values()), wdt, alpha=opc, color='b')

# Set the labels, tickmarks, etc.
axS.set_xlabel('Genre')
axS.set_ylabel('Number of winners')
axL.set_title('Genre of Best Picture winner')
axS.set_xticks(idx)
axS.set_xticklabels(list(Pic1_G_his.keys()))

# Set the limits of the lower (axS) and upper (axL) y-axis
axS.set_ylim(0, 35)
axL.set_ylim(77, 81)

# TO get a broken y-axis
axL.spines['bottom'].set_visible(False)
axS.spines['top'].set_visible(False)
axL.xaxis.tick_top()
axL.tick_params(labeltop=False)
axS.xaxis.tick_bottom()

# The diagonal cut on the y-axis
ct = 0.015
kwargs = dict(transform=axL.transAxes, color='k', clip_on=False)
axL.plot((-ct,+ct), (-ct,+ct), **kwargs)        # top-left diagonal
axL.plot((1-ct,1+ct), (-ct,+ct), **kwargs)      # top-right diagonal

kwargs.update(transform=axS.transAxes)          # switch to the bottom axes
axS.plot((-ct,+ct), (1-ct,1+ct), **kwargs)      # bottom-left diagonal
axS.plot((1-ct,1+ct), (1-ct,1+ct), **kwargs)    # bottom-right diagonal

# Final plotting and showing
plt.xticks(rotation=75)
fig.tight_layout()
plt.show()
*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~* """


# *~*~*~*~*~*~*~*~*~*~*~*~*~ 'Genre' ~*~*~*~*~*~*~*~*~*~*~*~*~*



# *~*~*~*~*~*~*~*~*~*~*~*~*~ 'Plot' *~*~*~*~*~*~*~*~*~*~*~*~*~*

# *~*~*~*~*~*~*~*~*~*~*~*~*~ 'Plot' *~*~*~*~*~*~*~*~*~*~*~*~*~*


""" *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# *~*~*~*~*~*~*~*~*~*~*~*~ 'Released' *~*~*~*~*~*~*~*~*~*~*~*~*


# Average month of Released of all the nominees
Pic0_Rel_avg = [np.sum(i)/np.count_nonzero(i) for i in Pic0_Rel]

# Average of difference between the Released month of winner(s) and
# Released month of nominees
PicM_Rel_dif = []
for i, yy in enumerate(Pic_yy):
    PicM_Rel_dif.append(np.sum([Pic1_Rel[i][0]-p0 for p0 in Pic0_Rel[i] if (p0 != 0)]) / \
                np.count_nonzero(Pic0_Rel[i]))

# Barplot of the average difference winner and nominee over the years
# Negative difference means winner released before the nominees
# Positive difference means winner released after the nominees
#plt.bar(Pic_yy, PicM_Rel_dif)

# Split the years into 5-year bins
yy5 = [1925+5*i for i in range((Pic_yy[-1]-Pic_yy[0])//5+1)]

# Split PicM_Rel_dif also into 5-year bins
PicM_Rel_df5 = [np.sum(PicM_Rel_dif[5*i+3:5*i+8])/5 for i in list(range(17))]
PicM_Rel_df5.insert(0, np.sum(PicM_Rel_dif[:2])/3)

# The barplot for average differences between Released month of winner and
# that of nominees, averaged over 5 years
#plt.bar(yy5, PicM_Rel_df5)


# *~*~*~*~*~*~*~*~*~*~*~*~ 'Released' *~*~*~*~*~*~*~*~*~*~*~*~*
*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~* """



### *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
### *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*


""" *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
PicM_Rel_df5, wn5 = [], 0
for i, p0 in enumerate(Pic_yy):
    if (p0%5 != 0):
        wn5 += PicM_Rel_dif[i]
    else:
        wn5 += PicM_Rel_dif[i]
        if (i == 2):
            print(2, p0, wn5)
            PicM_Rel_df5.append(wn5 / 3)
            wn5 = 0
        else:
            print(i, p0, wn5)
            PicM_Rel_df5.append(wn5 / 5)
            wn5 = 0
*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~* """



""" *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# somthing like this should work
    for k0 in Pic1_G_hi5.keys():
        j0.append(Pic1_G_hi5[k0][0])
        for i in range(5):
            print(Pic1_G_unr[j0.index(max(j0))])
            j0[j0.index(max(j0))] = -1
        break
# or something else of the same order

# this works for a sinlge example
    j0 = []
    Pic1_G_unr = Pic1_G_unq.copy();  Pic1_G_unr.remove('Music');
    for k0 in Pic1_G_ji5.keys():
        j0.append(Pic1_G_ji5[k0][0])
    print(Pic1_G_unr[j0.index(max(j0))])
    #> Drama
    j0[j0.index(max(j0))] = -1
    print(Pic1_G_unr[j0.index(max(j0))])
# need to find a way to put this in a loop
*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~* """