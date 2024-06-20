class Health:
    def __init__(self, hp: int, max_health: int):
        self._hp = hp
        self._max_hp = max_health

    def getHP(self) -> int:
        return self._hp

    def getMAXHP(self) -> int:
        return self._max_hp

    def decreaseHP(self, amount: int | float):
        self._hp -= amount

    def increaseHP(self, amount: int | float):
        self._hp += amount

    def setHP(self, newHP: int | float):
        self._hp = newHP


class Speed:
    def __init__(self, speed: int):
        self._speed = speed

    def getSpeed(self) -> int:
        return self._speed

    def setSpeed(self, newSpeed: int | float):
        self._speed = newSpeed


class Position:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y


class Renderable:
    def __init__(self, image):
        self._image = image


class EnemyAI:
    def __init__(self, target):
        self._target = target


class Damage:
    def __init__(self, damage: int):
        self._damage = damage


class Stamina:
    def __init__(self, stamina: int):
        self._stamina = stamina

    def getStamina(self) -> int:
        return self._stamina

    def setStamina(self, newStamina: int | float):
        self._stamina = newStamina


    def decreaseStamina(self, amount: int | float):
        self._stamina -= amount

    def increaseStamina(self, amount: int | float):
        self._stamina += amount

