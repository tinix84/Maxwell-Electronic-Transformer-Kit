import os

ScriptPath = os.path.dirname(__file__)


class CoreData:
    def _init_(self):
        pass

    def GetCoreData(self):
        InCoreShapes = {"E": 8, "EI": 8, "EC": 6, "EFD": 8, "EP": 7, "EQ": 6, "ER": 7, "ETD": 6, "P": 8, "PT": 8,
                        "PH": 8, "PQ": 8, "RM": 8, "U": 5, "UI": 8}
        InFile = open(os.path.join(ScriptPath, "CoreData.tab"), "r")
        FinalCoreDict = {}
        InRead = InFile.read().split("\n")
        InRead.pop(0)
        for EL in InRead:
            InParams = list(filter(None, EL.split("\t")))
            if len(InParams) == 0:
                pass
            else:
                SupName = InParams.pop(0)
                if not SupName in FinalCoreDict.keys():
                    FinalCoreDict[SupName] = {}
                CType = InParams.pop(0)
                if not CType in InCoreShapes.keys():
                    return None
                if not CType in FinalCoreDict[SupName].keys():
                    FinalCoreDict[SupName][CType] = {}
                CModel = InParams.pop(0)
                FinalCoreDict[SupName][CType][CModel] = []
                if len(InParams) != InCoreShapes[CType]:
                    return None
                for EachD in InParams:
                    FinalCoreDict[SupName][CType][CModel].append(float(EachD))

        InFile.close()
        return FinalCoreDict


if __name__ == "__main__":
    foo_core = CoreData()
    print(foo_core.GetCoreData())
