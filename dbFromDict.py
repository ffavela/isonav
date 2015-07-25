import sqlite3
from os import listdir
from os.path import isfile, join
import pickle
import os.path
from loadingStuff import populateDict

conn = sqlite3.connect('isoData.db')

c = conn.cursor()

print "#Populating the dictionary"
iDict=populateDict()
# Create table
c.execute('''CREATE TABLE isoMasses
             (iso text, mass real)''')

# Insert a row of data
# c.execute("INSERT INTO isoMasses VALUES ('4He',4.002604)")
# masses = [('1H',1.007829),
#           ('2H',2.014109),
#           ('t',3.016058),
#             ]
masses=[]
for e in iDict:
    for ee in iDict[e][1]:
        masses.append([str(ee)+str(e),iDict[e][1][ee][0]])
c.executemany('INSERT INTO isoMasses VALUES (?,?)', masses)

# Save (commit) the changes
conn.commit()

c.execute('''CREATE TABLE isoLevels
             (iso text, levNum integer, xEnergy real, extra text)''')

xlev=[]
for e in iDict:
    for ee in iDict[e][1]:
        iso=str(ee)+str(e)
        if iso=='1n' or iso=="0None":
            xlev.append([iso,1,0.0,""])
            continue
        for eee in iDict[e][1][ee][1]:
            xlev.append([iso,eee,iDict[e][1][ee][1][eee][0],
                         str(iDict[e][1][ee][1][eee][1])])
c.executemany('INSERT INTO isoLevels VALUES (?,?,?,?)', xlev)

conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
