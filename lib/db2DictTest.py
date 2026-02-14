import sqlite3
from isoParser import getIso
from isonav import getPnum  # type: ignore

conn = sqlite3.connect('isoData.db')
c = conn.cursor()


def myString2List(s):
    if len(s) <= 2:
        return []
    c = s[2:-2].split("', '")
    return c


c.execute('SELECT * FROM isoMasses')
massVal = c.fetchall()

print("Creating a dictionary")
myDict = {}
for m in massVal:
    A, k = getIso(m[0])
    # print isoStuff,m[1],getPnum(isoStuff[1])
    p = getPnum(k)
    if k not in myDict:
        myDict[k] = [p, {}]
    myDict[k][1][A] = [float(m[1])]

# print "Populating the rest of it"
# for key in myDict:
#     for aVal in myDict[key][1]:
#         iso=str(aVal)+key
#         print iso
#         t=(iso,)
#         c.execute('SELECT levNum,xEnergy,extra FROM isoLevels WHERE iso=?', t)
#         #Creating subDictionary
#         levDict={}
#         for exData in c.fetchall():
#             # print exData,exData[0],exData[1],exData[2],myString2List(exData[2])
#             if int(exData[0]) not in levDict:
#                 levDict[exData[0]]=[float(exData[1]),myString2List(exData[2])]
#         # print levDict

#         myDict[key][1][aVal].append(levDict)

# print "Testing each element individually"
# for e in myDict:
#     if not myDict[e]==iDict[e]:
#         print "Anomaly in ", e
#         print "myDict", myDict[e]
#         print "iDict", iDict[e]

print("If only n and None are the anomalies, its probably fine")
# print listStuff
conn.close()
