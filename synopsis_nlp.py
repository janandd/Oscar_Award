#!/usr/bin/python3

# This program is used to plot the outputs and play with those.
# Outputs from file StanleyK.py are pickled together, thereby
# avoiding running the entire programme again.

from os import chdir as cd
import sys
import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from wordcloud import STOPWORDS
from nltk.stem.snowball import SnowballStemmer
from matplotlib import patches
from matplotlib import pyplot as plt
import collections



### *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
### *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

if (sys.platform == 'linux'):
    thap = '/media/anand/Chiba/Users/Anand/Documents/home/python/self/Oscars'
else:
    thap = 'C:/Users/Anand/Documents/home/python/self/Oscars'
cd(thap)

# Open the pickle file
g0 = 'Pic.pickle';  g1 = open(g0, 'rb');

# un-pickle results of Best Picture saved in StanleyK.py
[YYYY, \
            Pic1_Fil, Pic0_Fil, Pic1_Nam, Pic0_Nam, Pic1_Gen, Pic0_Gen, \
            Pic1_Syn, Pic0_Syn, Pic1_Rel, Pic0_Rel] = pickle.load(g1)
g1.close()

# Delete the variables that you are not working on currently
del Pic1_Nam, Pic0_Nam, Pic1_Rel, Pic0_Rel, Pic1_Gen, Pic0_Gen


# *~*~*~*~*~*~*~*~*~*~*~*~*~ sklearn ~*~*~*~*~*~*~*~*~*~*~*~*~*
# *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

# Number of most frequent words to be output
npr = 15
i = 0
idx = np.arange(npr);  wdt = 0.6;

# Combine stop-words from nltk and wordcloud
buss = stopwords.words('english')
cuss = [c0 for c0 in STOPWORDS]
bcss = buss.copy()
for c1 in cuss:
    if (c1 not in bcss):
        bcss.append(c1)

# More characters to eliminate
wnot = ['.', ',', ':', '!', '*', '-']
bcss += wnot



# Stemmer object
stmr = SnowballStemmer('english')

for a0 in [Pic0_Syn,Pic1_Syn]:
    j = 1
    a2, a5 = [], []
    Syn_10, Tyn_10 = [], []

    # the CountVectorizer
    vec = CountVectorizer()

    # title of plot and filename of saved figure and
    # Y coord of 'word'
    if (i == 0):
        title = 'Nominee Plot words '
        filna = 'Pic0_Syn_'
    elif (i == 1):
        title = 'Winner Plot words '
        filna = 'Pic1_Syn_'
    #endif

    # For creating a multiplot
    fig = plt.figure()
    fig.set_size_inches(15,12)

    for yy,a1 in zip(YYYY,a0):
        if ((yy)%10 != 0):
            a2.append(a1)
            if (((yy+1)%10 != 0) and (yy != 2015)):
                continue
        else:
            a2 = []
            a2.append(a1);
            continue

        # join all the Synopses together
        a5 = [a4 for a3 in a2 for a4 in a3 if (a4 != '')]
        Syn_10.append(' '.join(a5))

        # Stemming
        b1 = ' '.join(a5).strip().split(' ')
        b3 = [stmr.stem(b2) for b2 in b1]
#        Tyn_10.append(b3)

        # dict to store the Bag of Words excluding STOPWORDS
        wwcc = {}

        for c0 in b3:
            if c0 not in bcss:
                if c0 not in wwcc:
                    wwcc[c0] = 1
                else:
                    wwcc[c0] += 1
        #endfor

        # The Word Counter
        woco = collections.Counter(wwcc)

        # Construct a DataFrame for the most frequent words and their counts
        r0 = woco.most_common(npr)
        r1 = pd.DataFrame(r0, columns=['word','count'])

        # Get the title and filename correct
        if (yy == 2015):
            titld = title + str(2010) + ' - SKL'
            filnb = filna + str(2010) + '_SKL.png'
        else:
            titld = title + str(yy-9) + ' - SKL'
            filnb = filna + str(yy-9) + '_SKL.png'

        Ytxt = max(r1['count'])/10

        # For individual plots
#        fig, ax = plt.subplots()
#        plt.savefig(filnb)

        ax = fig.add_subplot(5,2,j)
        p0 = ax.bar(idx, r1['count'], wdt, color='c')
#        ax.set_position([0.12,0.10,0.85,0.85])
        ax.legend(handles=[patches.Patch(color='c', label=titld)])
        ax.set_xlabel('word');  ax.set_ylabel('count');  ax.set_xticks(idx);
        ax.set_xticklabels('')
        ax.tick_params(axis='x', length=0)
        for k in range(npr):
            ax.text(k, Ytxt, r1['word'][k], rotation=90, \
                        ha='center', va='bottom', size=12)

        j += 1

#    plt.savefig(filna+'SKL.png')
    i += 1




# *~*~*~*~*~*~*~*~*~*~*~*~*~ sklearn ~*~*~*~*~*~*~*~*~*~*~*~*~*
# *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*



# """ *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# *~*~*~*~*~*~*~*~*~*~*~*~*~*~ TJS ~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

# Number of most frequent words to be output
npr = 15
i = 0
idx = np.arange(npr);  wdt = 0.6;


for a0 in [Pic0_Syn,Pic1_Syn]:
    j = 1
    a2 = []
    
    # title of plot and filename of saved figure
    if (i == 0):
        title = 'Nominee Plot words '
        filna = 'Pic0_Syn_'
    elif (i == 1):
        title = 'Winner Plot words '
        filna = 'Pic1_Syn_'

    fig = plt.figure()
    fig.set_size_inches(15,12)

    for yy,a1 in zip(YYYY,a0):
        if ((yy)%10 != 0):
            a2.append(a1)
            if (((yy+1)%10 != 0) and (yy != 2015)):
                continue
        else:
            a2 = []
            a2.append(a1);
            continue
    
        # join all the Synopses together
        a5 = [a4 for a3 in a2 for a4 in a3]
        Syn_10 = ' '.join(a5)
    
        # dict to store the Bag of Words excluding STOPWORDS
        wwcc = {}
    
        # Characters to eliminate
        wnot = ['.', ',', ':', '!', '*']
    
        for b0 in Syn_10.lower().split():
            for w0 in wnot:
                b0 = b0.replace(w0, '')
            #
            if b0 not in STOPWORDS:
                if b0 not in wwcc:
                    wwcc[b0] = 1
                else:
                    wwcc[b0] += 1
    
        # The Word Counter
        woco = collections.Counter(wwcc)
    
        # Get the title and filename correct
        if (yy == 2015):
            titld = title + str(2010) + ' - TJS'
            filnb = filna + str(2010) + '_TJS.png'
        else:
            titld = title + str(yy-9) + ' - TJS'
            filnb = filna + str(yy-9) + '_TJS.png'

        # Construct a DataFrame for the most frequent words and their counts
        r0 = woco.most_common(npr)
        r1 = pd.DataFrame(r0, columns=['word','count'])

        # plot it

        # Using pandas.DataFrame plot routine
#        plotbar = r1.plot.bar(x='word', y='count', color='c', \
#                    figsize=(6,4), legend=False, title=titld)
#        # save the figure
#        plotbar.get_figure().savefig(filnb)

        # Using matplotlib.pyplot
#        fig, ax = plt.subplots()
#        plt.show()
#        plt.savefig(filnb)

        ax = fig.add_subplot(5,2,j)
        p0 = ax.bar(idx, r1['count'], wdt, color='c')
#        ax.set_position([0.125,0.2,0.8,0.8])
        ax.legend(handles=[patches.Patch(color='c', label=titld)])
        ax.set_xlabel('word');  ax.set_ylabel('count');  ax.set_xticks(idx);
        ax.set_xticklabels('')
        ax.tick_params(axis='x', length=0)
        for k in range(npr):
            ax.text(k, Ytxt, r1['word'][k], rotation=90, \
                        ha='center', va='bottom', size=12)

        j += 1

#    plt.savefig(filna+'TJS.png')
    i += 1
    

# *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# *~*~*~*~*~*~*~*~*~*~*~*~*~*~ TJS ~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~* """ 



### *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
### *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*



""" *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# 'https://blog.goodaudience.com/how-to-generate-a-word-cloud-\
#             of-any-shape-in-python-7bce27a55f6e'
*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~* """