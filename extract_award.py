#!/usr/bin/python3

# This program would read from the cleaned Oscar winners file,
# and find various ways to dice and slice and plot the winners.

from os import chdir as cd
import pandas as pd
import numpy as np
import urllib as ul
import json
#import pickle


# Get month number from the Releases date
def mon_to_num(Rel):
    if (len(Rel) != 11):
        return 0
    #endif

    if (Rel[3:6] in months):
        return months.index(Rel[3:6])
    #endif
#end


# Obtain movie details from OMDB using the API
# The Current free API key allows 1,000 free requests per day.
def omdb_json(yy, movnam):
    # Check if the movie name is ASCII, otherwise urllib runs into trouble.
    # Converting diacritics to ASCII is not accurate, so not done here.
    # (We can manually change all movies with diacritics for now.)
    if (not min([len(i)==len(i.encode()) for i in movnam])):
        return 0
    #endif

    # The http url to locate json entry for a particular movie
    toturl = omdburl + movnam.strip().replace(' ','+')

    # Use urllib package to open the url, and then
    # use json package to read the entry into a dictionary, d2
    d0 = ul.request.urlopen(toturl)     # http response
    d1 = d0.read()                      # bytes
    d2 = json.loads(d1)                 # dictionary

#    if ((d2['Response'] == 'False') or ):
    if ((d2['Response'] == 'False') or (d2['Type'] != 'movie')):
        return 0
    #endif
    d2Rel = d2['Released']
    if (len(d2Rel) == 11):
        if ((int(d2Rel[-4:]) != yy) and (int(d2Rel[-4:]) != yy+1)):
            return 0
        #endif
    #endif

    return d2
#end



### *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
### *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

# thap = '/media/anand/Chiba/Users/Anand/Documents/home/python/self/Oscars'
thap = 'C:/Users/Anand/Documents/home/python/self/Oscars'
cd(thap)

fl = 'clean_kag.csv'

# Read the cleaned .csv file into a single dataframe, df1
df1 = pd.read_csv(fl, sep=',', encoding='ISO-8859-1')

# Get all the years as a list
YYYY = np.sort(df1['Year'].unique())

# list of all months to be used in mon_to_num
months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', \
                'Sep', 'Oct', 'Nov', 'Dec']


# API key for OMDB - 1,000 free requests per day
apikey = '6910b6a9'

# The base URL for search
omdburl = 'http://www.omdbapi.com/?' + 'apikey='+apikey + '&plot=full' + '&t='

# The significant categories of Award that will be inspected
categ = ['Actor in a Leading Role', 'Actress in a Leading Role', \
            'Actor in a Supporting Role', 'Actress in a Supporting Role', \
            'Director', 'Best Picture', \
            'Writing (Original Screenplay)', 'Writing (Adapted Screenplay)']
# short forms for the above award categories
cateS = ['OLR', 'ELR', 'OSR', 'ESR', 'Dir', 'Pic', 'WOS', 'WAS']



# *~*~*~*~*~*~*~*~*~*~*~ ACTOR & ACTRESS ~*~*~*~*~*~*~*~*~*~*~*

# df1_OLR = df1.loc[df1['Award']=='Actor in a Leading Role' & df1['Winner']==1]



# *~*~*~*~*~*~*~*~*~*~*~ ACTOR & ACTRESS ~*~*~*~*~*~*~*~*~*~*~*


""" *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# *~*~*~*~*~*~*~*~*~*~*~* BEST PICTURE ~*~*~*~*~*~*~*~*~*~*~*~*

# DataFrame for Best Picture award
df1_Pic = df1.loc[df1['Award']=='Best Picture', \
            ['Year', 'Ceremony', 'Winner', 'Name', 'Film']]

# DataFrames for winners and the losing nominees split from df1_Pic
# Not specifying the column names explicitly selects all the columns
df1_Pic_W = df1_Pic.loc[df1['Winner']==1]
df1_Pic_N = df1_Pic.loc[df1['Winner']==0]

# List to store all the dictionaries for all the years
Pic_yywwnn = []

# The Year column as a list
Pic_yy = []

# Released, Genre, Plot for Winner = 1 and for Winner = 0
Pic1_Rel, Pic1_Gen, Pic1_Syn = [], [], []
Pic0_Rel, Pic0_Gen, Pic0_Syn = [], [], []

for yy in YYYY:
    # Update the Year list
    Pic_yy.append(yy)


    # DataFrame of all the winners by year, and list to store Released date
    Pic1 = df1_Pic_W.loc[df1_Pic_W['Year']==yy]['Film'].tolist()

    # Released, Genre, Plot for Winner = 1
    tmp1_Rel, tmp1_Gen, tmp1_Syn = [], [], []
    for p1 in Pic1:
        mov1 = omdb_json(yy, p1)

        if (mov1 == 0):
            tmp1_Rel.append(0);  tmp1_Gen.append([]);  tmp1_Syn.append([]);
            continue
        #endif

        tmp1_Rel.append(mon_to_num(mov1['Released']))
        tmp1_Gen.append(mov1['Genre'].replace(' ','').split(','))
        tmp1_Syn.append(mov1['Plot'])
    #endfor
    #
    # Update Released, Genre, and Plot for Winner = 1
    Pic1_Rel.append(tmp1_Rel)
    Pic1_Gen.append(tmp1_Gen);  Pic1_Syn.append(tmp1_Syn);


    # DataFrame of all the nominees by year, and list to store Released date
    Pic0 = df1_Pic_N.loc[df1_Pic_N['Year']==yy]['Film'].tolist()

    # Released, Genre, Plot for Winner = 0
    tmp0_Rel, tmp0_Gen, tmp0_Syn = [], [], []
    for p0 in Pic0:
        mov0 = omdb_json(yy, p0)

        if (mov0 == 0):
            tmp0_Rel.append(0);  tmp0_Gen.append([]);  tmp0_Syn.append([]);
            continue
        #endif

        tmp0_Rel.append(mon_to_num(mov0['Released']))
        tmp0_Gen.append(mov0['Genre'].replace(' ','').split(','))
        tmp0_Syn.append(mov0['Plot'])
    #endfor
    #
    # Update Released, Genre, and Plot for Winner = 1
    Pic0_Rel.append(tmp0_Rel)
    Pic0_Gen.append(tmp0_Gen)
    Pic0_Syn.append(tmp0_Syn)



#    # Create a dict of Released dates winner and nominees for that year
#    nm = {'Year':yy, 'Winner':tmp1_Rel, 'Nominee':tmp0_Rel}
#    # Add this dict to a combined list of dicts, one for each year
#    Pic_yywwnn.append(nm)
#
#    # Create separate lists for year and Released date for winner and nominees
#endfor


# Open the file f0 for writing outputs of Best Picture into
f0 = open('Pic.pickle','wb') 

# Include all the desired objects into the file
#pickle.dump(Pic_yywwnn, f0)            # We do not use the list of dict
pickle.dump([Pic_yy, Pic1_Rel, Pic0_Rel], f0)
pickle.dump([Pic1_Gen, Pic0_Gen, Pic1_Syn, Pic0_Syn], f0)

# Close the file
f0.close()
*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~* """

 
# *~*~*~*~*~*~*~*~*~*~*~* BEST PICTURE ~*~*~*~*~*~*~*~*~*~*~*~*



### *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
### *~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*