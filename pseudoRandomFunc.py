import numpy as np
from numpy import ndarray


class pseudoRandom:
    def __init__(self):
        self._boostChances: ndarray = np.array([0] * 100)
        self._petChances: ndarray = np.array([0] * 100)
        self._countBoostOnes: int = 1
        self._countPetOnes: int = 1
        self._boostChances[0], self._petChances[0] = 1, 1

    def countChances(self, dropType: str, result: bool):
        if result:
            if dropType.lower() == "boost":
                self._boostChances = np.array([0] * 100)
                self._boostChances[0] = 1
                self._countBoostOnes: int = 1
            elif dropType.lower() == "pet":
                self._petChances = np.array([0] * 100)
                self._petChances[0] = 1
                self._countPetOnes: int = 1
        else:
            if self._countBoostOnes < 20:
                lastBoostIdx: int = np.where(self._boostChances == 1)[0][-1]
                self._boostChances[lastBoostIdx + 1] = 1
            if self._countPetOnes < 10:
                lastPetIdx: int = np.where(self._petChances == 1)[0][-1]
                self._petChances[lastPetIdx + 1] = 1

    def getChances(self) -> tuple[ndarray, ndarray]:
        return self._boostChances, self._petChances
