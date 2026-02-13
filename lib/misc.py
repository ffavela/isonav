from isonavBase import getKey, QStable, QDecay, nReaction
from loadingStuff import iDict

# Some miscellaneous functions
# May need to update them


def firstNoQNeg(val=5):
    fQDict = {}
    for i in range(117):
        k = getKey(i+1)
        print(i+1, k)
        if k is False:
            continue
        for iso in iDict[k][1]:
            isoVal = str(iso)+k
            d = QStable(isoVal)
        if d is False:
            continue
        if d != []:
            fQDict[k] = [i+1, iso]
            val -= 1
            print("Here again!", iso, d)
            print(iso)  # ,d
        if val <= 0:
            return fQDict
    return fQDict


def numberReact(iso1):
    for e in iDict:
        for i in iDict[e][1]:
            print(e, i)
            iso2 = str(i)+e
            nR = nReaction(iso1, iso2)
            if nR is False:
                print(0)
            else:
                print(len(nR))


# Print out the first unstable elements
# (in terms of Q)
def firstQPos(val=5):
    fQListX = []
    fQListY = []
    for i in range(117):
        k = getKey(i+1)
        print(i+1, k)
        if k is False:
            continue
        for iso in iDict[k][1]:
            isoVal = str(iso)+k
            d = QDecay(isoVal)
            if d is False:
                continue
            if d != []:
                fQListX.append(i+1)
                fQListY.append(iso)
                val -= 1
                print("Here!", iso)  # ,d
                print(iso)  # ,d
                break
            else:  # Just testing
                fQListX.append(i+1)
                fQListY.append(0)
            if val <= 0:
                return fQListX, fQListY
    return fQListX, fQListY
