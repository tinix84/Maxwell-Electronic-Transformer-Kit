import os
import math


class Utilities:
    def _init_(self):
        pass

    def ReadMatData(self, FilePath):
        Inmat = open(os.path.join(FilePath, "matdata.tab"), "r")
        matList = []
        matDict = {}
        for EachL in Inmat:
            matList.append(EachL.split("\t"))
            matList[-1][-1] = matList[-1][-1].replace("\n", "")
        Inmat.close()
        matList.pop(0)
        for EachMat in matList:
            TempMat = EachMat[:]
            TempKey = TempMat.pop(0)
            matDict[TempKey] = TempMat
        return matDict

    def CheckCoreDim(self, CorDim, CoreType):

        if CoreType == "E":
            for EachD in CorDim:
                if EachD <= 0:
                    if not (CorDim.index(EachD) > 5):
                        return 0
                    else:
                        if EachD < 0:
                            return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[2]:
                return 0
            if CorDim[3] <= CorDim[4]:
                return 0

        if CoreType == "EC":
            for EachD in CorDim:
                if EachD <= 0:
                    return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[2]:
                return 0
            if CorDim[3] <= CorDim[4]:
                return 0

        if CoreType == "EFD":
            for EachD in CorDim:
                if EachD <= 0:
                    if not (CorDim.index(EachD) == 7):
                        return 0
                    else:
                        if EachD == 0:
                            return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[2]:
                return 0
            if CorDim[3] <= CorDim[4]:
                return 0

        if CoreType == "EI":
            for EachD in CorDim:
                if EachD <= 0:
                    if CorDim.index(EachD) != 7:
                        return 0
                    else:
                        if EachD < 0:
                            return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[2]:
                return 0
            if CorDim[3] <= CorDim[4]:
                return 0

        if CoreType == "EP":
            for EachD in CorDim:
                if EachD <= 0:
                    return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[2]:
                return 0
            if CorDim[3] <= CorDim[4]:
                return 0
            if CorDim[5] <= CorDim[6]:
                return 0

        if CoreType == "EQ":
            for EachD in CorDim:
                if EachD <= 0:
                    return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[2]:
                return 0
            if CorDim[3] <= CorDim[4]:
                return 0
            if CorDim[5] < CorDim[2]:
                return 0

        if CoreType == "ER":
            for EachD in CorDim:
                if EachD <= 0:
                    if EachD == 0:
                        if CorDim.index(EachD) != 6:
                            return 0
                    else:
                        return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[6]:
                return 0
            if CorDim[6] < 2 * math.sqrt((CorDim[1] / 2) ** 2 - (CorDim[5] / 2) ** 2):
                if CorDim[6] == 0:
                    pass
                else:
                    return 0
            if CorDim[3] <= CorDim[4]:
                return 0

        if CoreType == "ETD":
            for EachD in CorDim:
                if EachD <= 0:
                    return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[2]:
                return 0
            if CorDim[3] <= CorDim[4]:
                return 0

        if CoreType == "P":
            for EachD in range(0, len(CorDim)):
                if CorDim[EachD] <= 0:
                    if CorDim[EachD] == 0:
                        if EachD != 5:
                            return 0
                    else:
                        return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[2]:
                return 0
            if CorDim[3] <= CorDim[4]:
                return 0
            if CorDim[2] <= CorDim[5]:
                return 0
            if (CorDim[7] >= CorDim[1]) or (CorDim[7] <= CorDim[2]):
                return 0

        if CoreType == "PH":
            for EachD in range(0, len(CorDim)):
                if CorDim[EachD] <= 0:
                    if CorDim[EachD] == 0:
                        if EachD != 5:
                            return 0
                    else:
                        return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[2]:
                return 0
            if CorDim[3] <= CorDim[4]:
                return 0
            if CorDim[2] <= CorDim[5]:
                return 0
            if (CorDim[7] >= CorDim[1]) or (CorDim[7] <= CorDim[2]):
                return 0

        if CoreType == "PQ":
            for EachD in range(0, len(CorDim)):
                if CorDim[EachD] <= 0:
                    return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[2]:
                return 0
            if CorDim[3] <= CorDim[4]:
                return 0
            if CorDim[2] <= CorDim[6]:
                return 0
            if (CorDim[5] >= CorDim[0]) or CorDim[5] <= CorDim[2]:
                return 0

        if CoreType == "PT":
            for EachD in range(0, len(CorDim)):
                if CorDim[EachD] <= 0:
                    if CorDim[EachD] == 0:
                        if EachD != 6:
                            return 0
                    else:
                        return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[2]:
                return 0
            if CorDim[3] <= CorDim[4]:
                return 0
            if CorDim[2] <= CorDim[5]:
                return 0
            if (CorDim[7] >= CorDim[1]) or CorDim[7] <= CorDim[2]:
                return 0

        if CoreType == "RM":
            for EachD in range(0, len(CorDim)):
                if CorDim[EachD] <= 0:
                    if CorDim[EachD] == 0:
                        if EachD != 5:
                            return 0
                    else:
                        return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[1] <= CorDim[2]:
                return 0
            if CorDim[3] <= CorDim[4]:
                return 0
            if CorDim[2] <= CorDim[5]:
                return 0

        if CoreType == "U":
            for EachD in CorDim:
                if EachD <= 0:
                    return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[2] <= CorDim[3]:
                return 0

        if CoreType == "UI":
            for EachD in CorDim:
                if EachD <= 0:
                    return 0
            if CorDim[0] <= CorDim[1]:
                return 0
            if CorDim[2] <= CorDim[3]:
                return 0
        return 1

if __name__ == "__main__":
    ScriptPath = os.path.dirname(__file__)
    foo_utils = Utilities()
    mat_dict = foo_utils.ReadMatData((ScriptPath+'/../MaterialData'))
    print(mat_dict)