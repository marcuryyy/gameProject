import pygame
from abc import ABC, abstractmethod
import os

pygame.init()


class Player:
    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        self.player_image: pygame.Surface = pygame.image.load("playerAnimations/idle/idle1.png")
        self._idleFrames: list[str] = os.listdir("playerAnimations/idle")
        self._idleFrame: int = 0
        self._runFramesRight: list[str] = os.listdir("playerAnimations/rightRun")
        self._runFrameRight: int = 0
        self._runFramesLeft: list[str] = os.listdir("playerAnimations/leftRun")
        self._runFrameLeft: int = 0
        self._hitbox: pygame.Rect = pygame.Rect((0, 0), (90, 90))
        self._x: int = self._hitbox.topleft[0] + 1000
        self._y: int = self._hitbox.topleft[1] + 1000
        self._speed: int = 3
        self._maxSpeed: int = 3
        self._isDashing: bool = False
        self._isRunningRight: bool = False
        self._isRunningLeft: bool = False
        self._canWalkRight = self._canWalkLeft = self._canWalkUp = self._canWalkDown = True
        self._facing: str = "None"
        self._maxHealth: int = 500
        self._hp: int = self._maxHealth
        self._stamina: int = 100
        self._heatlhbar: HealthBar = HealthBar(5, 5, 200, 30, self._hp)
        self._staminabar: StaminaBar = StaminaBar(5, 50, 200, 30, self._stamina)
        self._dashLength: int = 100
        self._coins: int = 0

    def updateAnimation(self):
        self._hitbox.topleft = (self._x, self._y)
        if not (self._isRunningLeft or self._isRunningRight):
            self.processIdleAnimation()
        else:
            if self._isRunningRight:
                self.processRightRunAnimation()
            else:
                self.processLeftRunAnimation()
        if self._stamina < 100:
            self._stamina += 0.1
            self._isDashing = False
        self._isRunningRight = self._isRunningLeft = False

    def setSpeedIfWalkingDiagonally(self):
        self._speed = self._speed / (2 * 0.5)

    def processIdleAnimation(self):
        self._idleFrame += 0.05
        if self._idleFrame >= len(self._idleFrames) - 1:
            self._idleFrame = 0
        self.player_image = pygame.image.load(
            f"playerAnimations/idle/{self._idleFrames[int(self._idleFrame)]}").convert_alpha()

    def processRightRunAnimation(self):
        self._runFrameRight += 0.05
        if self._runFrameRight >= len(self._runFramesRight) - 1:
            self._runFrameRight = 0
        self.player_image = pygame.image.load(
            f"playerAnimations/rightRun/{self._runFramesRight[int(self._runFrameRight)]}").convert_alpha()

    def processLeftRunAnimation(self):
        self._runFrameLeft += 0.05
        if self._runFrameLeft >= len(self._runFramesLeft) - 1:
            self._runFrameLeft = 0
        self.player_image = pygame.image.load(
            f"playerAnimations/leftRun/{self._runFramesLeft[int(self._runFrameLeft)]}").convert_alpha()

    def walkLeft(self):
        if self._canWalkLeft:
            self._x -= self._speed
            self._facing = "Left"
            self.setRunningStateLeft(True)
            if self._isDashing and self._stamina >= 100:
                self._x -= self._speed * self._dashLength
                self._stamina = 0

    def walkRight(self):
        if self._canWalkRight:
            self._x += self._speed
            self._facing = "Right"
            self.setRunningStateRight(True)
            if self._isDashing and self._stamina >= 100:
                self._x += self._speed * self._dashLength
                self._stamina = 0

    def walkUp(self):
        if self._canWalkUp:
            self._y -= self._speed
            self._facing = "Up"
            self.setRunningStateLeft(True)
            if self._isDashing and self._stamina >= 100:
                self._y -= self._speed * self._dashLength
                self._stamina = 0

    def walkDown(self):
        if self._canWalkDown:
            self._y += self._speed
            self._facing = "Down"
            self.setRunningStateRight(True)
            if self._isDashing and self._stamina >= 100:
                self._y += self._speed * self._dashLength
                self._stamina = 0

    def getPlayerImage(self) -> pygame.Surface:
        return self.player_image

    def getCoordinates(self) -> tuple[int, int]:
        return self._x, self._y

    def getHitbox(self) -> pygame.Rect:
        return self._hitbox

    def getHP(self) -> int:
        return self._hp

    def getMaxHP(self) -> int:
        return self._maxHealth

    def getDamage(self, amount: int):
        self._hp -= amount

    def getHealthBar(self):
        return self._heatlhbar

    def getStaminaBar(self):
        return self._staminabar

    def getSTAMINA(self) -> int:
        return self._stamina

    def setWalkLeftState(self, state: bool):
        self._canWalkLeft = state

    def setWalkRightState(self, state: bool):
        self._canWalkRight = state

    def setWalkUpState(self, state: bool):
        self._canWalkUp = state

    def setWalkDownState(self, state: bool):
        self._canWalkDown = state

    def setAllStates(self, state: bool):
        self._canWalkLeft = self._canWalkRight = self._canWalkDown = self._canWalkUp = state

    def setDashState(self, state: bool):
        self._isDashing = state

    def getFacing(self) -> str:
        return self._facing

    def addHealth(self, newHealth: int):
        if self._hp + newHealth <= 500:
            self._hp += newHealth
        else:
            self._hp = 500

    def setRunningStateRight(self, state: bool):
        self._isRunningRight = state

    def setRunningStateLeft(self, state: bool):
        self._isRunningLeft = state

    def setMaxSpeed(self, newSpeed: int):
        self._maxSpeed = newSpeed

    def setSpeed(self, newSpeed: int):
        self._speed = newSpeed

    def getMaxSpeed(self) -> int:
        return self._maxSpeed

    def getCoins(self) -> int:
        return self._coins

    def increaseCoins(self):
        self._coins += 1


class Bar(ABC):
    @abstractmethod
    def draw(self, *args):
        pass


class HealthBar(Bar):
    def __init__(self, x: int, y: int, width: int, height: int, max_hp: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._max_hp = max_hp

    def draw(self, screen: pygame.Surface, player_hp: int):
        ratio: float = player_hp / self._max_hp
        pygame.draw.rect(screen, "red", (self._x, self._y, self._width, self._height))
        pygame.draw.rect(screen, "green", (self._x, self._y, self._width * ratio, self._height))


class StaminaBar(Bar):
    def __init__(self, x: int, y: int, width: int, height: int, max_stamina: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._max_stamina = max_stamina

    def draw(self, screen: pygame.Surface, player_stamina: int):
        ratio = player_stamina / self._max_stamina
        pygame.draw.rect(screen, "red", (self._x, self._y, self._width, self._height))
        pygame.draw.rect(screen, "yellow", (self._x, self._y, self._width * ratio, self._height))


class CoinsAmount:
    def __init__(self):
        self._coin_font = pygame.font.Font(None, 36)

    def draw_coins(self, screen, coins: int):
        coin_text = self._coin_font.render(f"Монеты: {coins}", True, (255, 255, 255))
        screen.blit(coin_text, (5, 95))
