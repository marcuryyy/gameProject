import time
import pygame
from abc import abstractmethod, ABC

import Controller
import Enemy
import drops
import gameMap
import player
import diffProjectiles
import math
import random

from EC.Component import components

pygame.init()
pygame.font.init()
pygame.mixer.init()
clock = pygame.time.Clock()


class Settings:
    def __init__(self):
        self._musicVolume: float = 0.1

    def getVolume(self) -> float:
        return self._musicVolume

    def setVolume(self, newVolume: float):
        self._musicVolume = newVolume


class MainMenu:
    def __init__(self):
        self._screen: pygame.Surface = pygame.display.set_mode((750, 750))
        self._screen.fill("Black")
        self._playbutton = PlayButton(self._screen, 250, 50)
        self._skillsButton = SkillsButton(self._screen, 250, 50)
        self._SettingsButton = SettingsButton(self._screen, 250, 50)
        self._QuitButton = QuitButton(self._screen, 250, 50)
        self._buttons: list[Button] = [self._playbutton, self._skillsButton, self._SettingsButton, self._QuitButton]
        self._runMenu: bool = True

    def runMenu(self):
        self._screen.fill("black")
        self.drawButtons()
        while self._runMenu:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self._buttons:
                        button.do_on_click(event)

    def getScreen(self) -> pygame.Surface:
        return self._screen

    def getState(self) -> bool:
        return self._runMenu

    def setState(self, state: bool):
        self._runMenu = state
        if state:
            self.runMenu()

    def drawButtons(self):
        self._playbutton.draw()
        self._skillsButton.draw()
        self._SettingsButton.draw()
        self._QuitButton.draw()


class SkillsScreen:

    def __init__(self):
        self._screen: pygame.Surface = pygame.display.set_mode((750, 750))
        self._runLoadingScreen: bool = False
        self._settingsLabel = SkillsLabel(self._screen)
        self._runSkillsScreen: bool = False
        self._speedIcon = pygame.image.load("skillsIcons/speed.png")
        self._buyButton = BuyButton(self._screen, 200, 50, "speed")
        self._whiteBackground = pygame.Surface((96, 96))
        self._whiteBackground.fill("white")
        self._speedIconRect = self._speedIcon.get_rect(
            center=(self._screen.get_width() // 2, self._screen.get_height() // 2))
        self._whiteRect = self._whiteBackground.get_rect(
            center=(self._screen.get_width() // 2, self._screen.get_height() // 2))
        self._backButton = BackButton(self._screen, 250, 50)
        self._buttons: list[Button] = [self._backButton, self._buyButton]

    def runSettings(self):
        self._screen.fill("black")
        self.drawButtonsAndNonUpdateText()
        self._screen.blit(self._whiteBackground, self._whiteRect)
        self._screen.blit(self._speedIcon, self._speedIconRect)

        while self._runSkillsScreen:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self._buttons:
                        button.do_on_click(event)

    def setState(self, state: bool):
        self._runSkillsScreen = state
        if state:
            self.runSettings()

    def drawButtonsAndNonUpdateText(self):
        self._settingsLabel.draw()
        self._backButton.draw()
        self._buyButton.draw()

    def drawUpdateText(self):
        pass


class LoadingScreen:
    def __init__(self):
        self._screen: pygame.Surface = pygame.display.set_mode((750, 750))
        self._runLoadingScreen: bool = False
        self._loadingLabel = LoadingLabel(self._screen)
        self._loadingSquare: pygame.Rect = pygame.Rect(275, 275, 200, 200)
        self._loadingSquareSurface: pygame.Surface = pygame.Surface(
            (self._loadingSquare.width, self._loadingSquare.height))
        self._finalMap: list[list[int]] = []

    def runLoadingScreen(self):
        self._screen.fill("black")
        self._loadingLabel.draw()
        pygame.draw.rect(self._screen, "white", self._loadingSquare, 2)
        pygame.display.update()
        self._mapCreator = gameMap.GameMapCreator()
        mapStory: gameMap.Queue = self._mapCreator.getMapQueue()
        while self._runLoadingScreen:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.updateMap(mapStory)

    def updateMap(self, mapStory):
        if mapStory.size():
            lastMapState = mapStory.dequeue()
            self._loadingSquareSurface.fill((0, 0, 0))
            for y, row in enumerate(lastMapState):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self._loadingSquareSurface, "red", (x * 10, y * 10, 10, 10))
            self._screen.blit(self._loadingSquareSurface, self._loadingSquare.topleft)
            pygame.draw.rect(self._screen, "white", self._loadingSquare, 2)
            pygame.display.flip()
            self._finalMap = lastMapState
            time.sleep(0.5)
        else:
            time.sleep(2)
            loadingScreen.setState(False)
            gameScene.setState(True)

    def setState(self, state: bool):
        self._runLoadingScreen = state
        if state:
            self.runLoadingScreen()

    def getMapUtils(self):
        return self._mapCreator, self._finalMap


class SettingsScreen:
    def __init__(self):
        self._screen: pygame.Surface = pygame.display.set_mode((750, 750))
        self._runLoadingScreen: bool = False
        self._settingsLabel = SettingsLabel(self._screen)
        self._musicLabelText = MusicLabelText(self._screen)
        self._musicVolumeLevel = MusicVolumeLevel(self._screen)
        self._runSettingsScreen: bool = False
        self._backButton = BackButton(self._screen, 250, 50)
        self._decreaseMusicVolume = DecreaseMusicVolume(self._screen, 50, 50)
        self._increaseMusicVolume = IncreaseMusicVolume(self._screen, 50, 50)
        self._buttons: list[Button] = [self._backButton, self._decreaseMusicVolume, self._increaseMusicVolume]

    def runSettings(self):
        self._screen.fill("black")
        self.drawButtonsAndNonUpdateText()
        while self._runSettingsScreen:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self._buttons:
                        button.do_on_click(event)

    def setState(self, state: bool):
        self._runSettingsScreen = state
        if state:
            self.runSettings()

    def drawButtonsAndNonUpdateText(self):
        self._settingsLabel.draw()
        self._musicLabelText.draw()
        self._backButton.draw()
        self._decreaseMusicVolume.draw()
        self._increaseMusicVolume.draw()

    def drawUpdateText(self):
        self._musicVolumeLevel.draw()


class PauseMenu:
    def __init__(self):
        self._screen: pygame.Surface = mainmenu.getScreen()
        self._ResumeButton = ResumeButton(self._screen, 250, 50)
        self._MenuButton = BackToMenuButton(self._screen, 250, 50)
        self._buttons: list[Button] = [self._ResumeButton, self._MenuButton]
        self._runMenu: bool = False

    def runMenu(self):
        self.drawButtons()
        transparent_rect = pygame.Surface((750, 750), pygame.SRCALPHA)
        transparent_rect.fill((255, 255, 255, 128))
        self._screen.blit(transparent_rect, (0, 0))
        while self._runMenu:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self._buttons:
                        button.do_on_click(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._runMenu = False
                        gameScene.setPauseState(False)

    def getScreen(self) -> pygame.Surface:
        return self._screen

    def getState(self) -> bool:
        return self._runMenu

    def setState(self, state: bool):
        self._runMenu = state
        if state:
            self.runMenu()

    def drawButtons(self):
        self._ResumeButton.draw()
        self._MenuButton.draw()


class GameScene:
    def __init__(self):
        self._controller = None
        self._map = None
        self._mapCreator = None
        self._screen = mainmenu.getScreen()
        self._running: bool = False

        self._screen_rect = pygame.display.get_surface().get_rect()
        self._camera_rect = pygame.Rect(0, 0, self._screen_rect.width, self._screen_rect.height)
        self._player: player.Player = player.Player(self._screen)
        self._playerX: int = self._player.getCoordinates()[0]
        self._playerY: int = self._player.getCoordinates()[1]
        self._closestEnemy: Enemy.BaseEnemy | None = None
        self._projectiles: list[diffProjectiles.FireProjectile] = []
        self._cameraSpeed: int = 1
        self._enemyCounter: int = 0
        self._difficulty: int = 2
        self._lastHPTicks: int = 0
        self._maxEnemyCount: int = self.setDifficulty(self._player.getHP(), self._player.getMaxHP(),
                                                      pygame.time.get_ticks())

        self._enemies: list[Enemy.BaseEnemy] = []
        self._droppedGoods: list[drops] = []
        self._pets: list[diffProjectiles.BabyGhost] = []
        self._petDict: dict = {"GhostPet": 0}

        self._paused: bool = False
        self._lastShotTicks: int = 0


    def run_game(self):
        clock.tick(60)
        self._mapCreator, self._map = loadingScreen.getMapUtils()
        self._tileMap = self._mapCreator.getMap()
        pygame.mixer.music.load("music/kevin-macleod-8bit-dungeon-boss.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(settings.getVolume())
        self._controller = Controller.Controller(self._player, self._enemies, self._map, self._tileMap)
        while self._running and not self._paused:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._paused = True
                        pygame.mixer.music.stop()
                        pauseMenu.setState(True)
                        pauseMenu.runMenu()

            self._maxEnemyCount = self.setDifficulty(self._player.getHP(), self._player.getMaxHP(),
                                                     pygame.time.get_ticks())
            self._mapCreator.fillMap(self._screen, self._camera_rect.x, self._camera_rect.y)
            self.processPlayer()
            self.processEnemies()
            self.processProjectiles()
            self.processDrops()
            self.processPets()
            self.processPlayerBars()
            self._controller.update(self._player, self._enemies)
            pygame.display.flip()

    def setState(self, state: bool):
        self._running = state
        if state:
            gameScene.run_game()

    def setDifficulty(self, player_health: int, player_max_health: int, ticks: int) -> int:
        difficulty: list = ["Very Easy", "Easy", "Medium", "Hard", "Very Hard", "Nearly Impossible", "Impossible"]
        enemyAmount: dict = {"Very Easy": 7, "Easy": 12, "Medium": 17, "Hard": 22,
                             "Very Hard": 27, "Nearly Impossible": 32, "Impossible": 40}
        if self._lastHPTicks == 0:
            self._lastHPTicks += 1
            return enemyAmount[difficulty[self._difficulty]]
        else:
            if ticks - self._lastHPTicks >= 10000:
                if player_max_health - player_health <= 50:
                    if (len(difficulty) - 1) - self._difficulty >= 3:
                        self._difficulty += 3
                    else:
                        self._difficulty = len(difficulty) - 1
                elif 50 < player_max_health - player_health <= 100:
                    if (len(difficulty) - 1) - self._difficulty >= 2:
                        self._difficulty += 2
                    else:
                        self._difficulty = len(difficulty) - 1
                elif 100 < player_max_health - player_health <= 150:
                    if (len(difficulty) - 1) - self._difficulty >= 1:
                        self._difficulty += 1
                    else:
                        self._difficulty = len(difficulty) - 1
                elif 150 < player_max_health - player_health <= 200:
                    pass
                elif 200 < player_max_health - player_health <= 275:
                    if self._difficulty >= 1:
                        self._difficulty -= 1
                elif 275 < player_max_health - player_health <= 375:
                    if self._difficulty >= 2:
                        self._difficulty -= 2
                    else:
                        self._difficulty = 0
                else:
                    if self._difficulty >= 3:
                        self._difficulty -= 3
                    else:
                        self._difficulty = 0
                self._lastHPTicks = ticks
            return enemyAmount[difficulty[self._difficulty]]

    def processProjectiles(self):
        current_ticks = pygame.time.get_ticks()
        if not self._projectiles:
            projectile = diffProjectiles.FireProjectile(self._player.getHitbox().centerx,
                                                        self._player.getHitbox().centery, self._closestEnemy,
                                                        pygame.time.get_ticks(), self._camera_rect.x,
                                                        self._camera_rect.y)
            self._projectiles.append(projectile)
        else:
            element = self._projectiles[-1]
            if current_ticks - self._lastShotTicks > element.get_cd():
                self._lastShotTicks = current_ticks
                projectile = diffProjectiles.FireProjectile(self._player.getHitbox().centerx,
                                                            self._player.getHitbox().centery, self._closestEnemy,
                                                            current_ticks, self._camera_rect.x,
                                                            self._camera_rect.y)
                self._projectiles.append(projectile)
        for element in self._projectiles[:]:
            if element.destroy(pygame.time.get_ticks()):
                self._projectiles.remove(element)
            else:
                element.update(self._screen, self._camera_rect.x, self._camera_rect.y)
                if element.killOnCollision(self._enemies):
                    self._projectiles.remove(element)

    def processEnemies(self):
        if self._enemyCounter < self._maxEnemyCount:
            self._enemies.append(random.choice([Enemy.GhostEnemy(self._screen), Enemy.ZombieEnemy(self._screen)]))
            self._enemyCounter += 1
        closest_distance = float('inf')
        for enemy in self._enemies:
            if enemy.getDrawState() is not True:
                enemy.draw(self._playerX, self._playerY, self._camera_rect.x, self._camera_rect.y,
                           self._mapCreator.getTileSize(), self._mapCreator.getTileAmount(),
                           self._screen.get_size())
                enemy.setDrawState()
            enemy_x, enemy_y = enemy.getCoordinates()
            current_distance = math.sqrt((enemy_x - self._playerX) ** 2 + (enemy_y - self._playerY) ** 2)
            if current_distance < closest_distance:
                closest_distance = current_distance
                self._closestEnemy = enemy
            enemy.followPlayer(self._player, self._playerX, self._playerY, self._camera_rect.x, self._camera_rect.y)
            enemy.checkCollisions(self._player, self._player.getHitbox())
            if enemy.getHP() <= 0:
                dropped = enemy.dropGoods(self._screen, enemy_x, enemy_y, self._petDict)
                if dropped:
                    self._droppedGoods.append(dropped)
                self._enemies.remove(enemy)
                self._enemyCounter -= 1

    def processDrops(self):
        for drop in self._droppedGoods:
            drop.update(self._camera_rect.x, self._camera_rect.y)
            result = drop.onPickUp(self._player)
            if result:
                if result == "GhostPet":
                    self._pets.append(diffProjectiles.BabyGhost(self._screen, self._playerX, self._playerY))
                    self._petDict["GhostPet"] += 1
                self._droppedGoods.remove(drop)

    def processPlayerBars(self):
        self._player.getHealthBar().draw(self._screen, self._player.getHP())
        self._player.getStaminaBar().draw(self._screen, self._player.getSTAMINA())

    def processPlayer(self):
        self._player.handle_keys(self._mapCreator)
        self._playerX, self._playerY = self._player.getCoordinates()
        self._camera_rect.center = (self._playerX, self._playerY)
        if self._player.getHP() > 0:
            self._player.update(self._camera_rect.x, self._camera_rect.y)
        else:
            self._paused = True
            pygame.mixer.music.stop()
            pauseMenu.setState(True)
            pauseMenu.runMenu()

    def processPets(self):
        for pet in self._pets:
            pet.followPlayer(self._playerX, self._playerY, self._camera_rect.x, self._camera_rect.y, self._enemies)

    def setPauseState(self, state: bool):
        self._paused = state

    def getPlayer(self):
        return self._player


class Button(ABC):
    def __init__(self):
        self._font: pygame.font.Font = pygame.font.SysFont(None, 50)

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def do_on_click(self, event: pygame.event.Event):
        pass


class PlayButton(Button):
    def __init__(self, screen: pygame.Surface, width: int, height: int):
        super().__init__()
        self._screen = screen
        self._width: int = width
        self._height: int = height
        self._button = pygame.Rect((screen.get_size()[0] // 2 - width // 2, screen.get_size()[1] // 2 - height // 2),
                                   (self._width, self._height))
        self._text: pygame.Surface = self._font.render("Играть", True, "black")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=self._button.center)

    def draw(self):
        pygame.draw.rect(mainmenu.getScreen(), "White", self._button)
        self._screen.blit(self._text, self._text_rectangle)
        pygame.display.update()

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            if mainmenu.getState():
                mainmenu.setState(False)
                loadingScreen.setState(True)


class SkillsButton(Button):
    def __init__(self, screen: pygame.Surface, width: int, height: int):
        super().__init__()
        self._screen = screen
        self._width: int = width
        self._height: int = height
        self._button = pygame.Rect(
            (screen.get_size()[0] // 2 - width // 2, screen.get_size()[1] // 2 - height // 2 + height * 1.5),
            (self._width, self._height))
        self._text: pygame.Surface = self._font.render("Навыки", True, "black")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=self._button.center)

    def draw(self):
        pygame.draw.rect(mainmenu.getScreen(), "White", self._button)
        self._screen.blit(self._text, self._text_rectangle)
        pygame.display.update()

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            if mainmenu.getState():
                mainmenu.setState(False)
                skillsMenu.setState(True)


class SettingsButton(Button):
    def __init__(self, screen: pygame.Surface, width: int, height: int):
        super().__init__()
        self._screen = screen
        self._width: int = width
        self._height: int = height
        self._button = pygame.Rect(
            (screen.get_size()[0] // 2 - width // 2, screen.get_size()[1] // 2 - height // 2 + height * 3),
            (self._width, self._height))
        self._text: pygame.Surface = self._font.render("Настройки", True, "black")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=self._button.center)

    def draw(self):
        pygame.draw.rect(mainmenu.getScreen(), "White", self._button)
        self._screen.blit(self._text, self._text_rectangle)
        pygame.display.update()

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            if mainmenu.getState():
                mainmenu.setState(False)
                settingsScreen.setState(True)


class QuitButton(Button):
    def __init__(self, screen: pygame.Surface, width: int, height: int):
        super().__init__()
        self._screen = screen
        self._width: int = width
        self._height: int = height
        self._button = pygame.Rect(
            (screen.get_size()[0] // 2 - width // 2, screen.get_size()[1] // 2 - height // 2 + height * 4.5),
            (self._width, self._height))
        self._text: pygame.Surface = self._font.render("Выйти", True, "black")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=self._button.center)

    def draw(self):
        pygame.draw.rect(mainmenu.getScreen(), "White", self._button)
        self._screen.blit(self._text, self._text_rectangle)
        pygame.display.update()

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            if mainmenu.getState():
                pygame.quit()


class BackButton(Button):

    def __init__(self, screen: pygame.Surface, width: int, height: int):
        super().__init__()
        self._screen = screen
        self._width: int = width
        self._height: int = height
        self._button = pygame.Rect(
            (screen.get_size()[0] // 2 - width // 2, screen.get_size()[1] // 2 - height // 2 + height * 5.5),
            (self._width, self._height))
        self._text: pygame.Surface = self._font.render("Выйти", True, "black")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=self._button.center)

    def draw(self):
        pygame.draw.rect(mainmenu.getScreen(), "White", self._button)
        self._screen.blit(self._text, self._text_rectangle)
        pygame.display.update()

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            mainmenu.setState(True)
            settingsScreen.setState(False)


class DecreaseMusicVolume(Button):
    def __init__(self, screen: pygame.Surface, width: int, height: int):
        super().__init__()
        self._screen = screen
        self._width: int = width
        self._height: int = height
        self._button = pygame.Rect(
            (screen.get_size()[0] // 2 - width * -3, screen.get_size()[1] // 2 - height // 2 + height * -4),
            (self._width, self._height))
        self._text: pygame.Surface = self._font.render("-", True, "black")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=self._button.center)
        self._fill_rect = pygame.Rect(0, 0, 80, 75)
        self._fill_rect.center = (self._screen.get_size()[0] - 135, 175)

    def draw(self):
        pygame.draw.rect(mainmenu.getScreen(), "White", self._button)
        self._screen.blit(self._text, self._text_rectangle)
        pygame.display.update()

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            if settings.getVolume() > 0:
                settings.setVolume(settings.getVolume() - 0.05)
                self._screen.fill("black", self._fill_rect)
                settingsScreen.drawUpdateText()


class IncreaseMusicVolume(Button):
    def __init__(self, screen: pygame.Surface, width: int, height: int):
        super().__init__()
        self._screen = screen
        self._width: int = width
        self._height: int = height
        self._button = pygame.Rect(
            (screen.get_size()[0] // 2 - width * -5.5, screen.get_size()[1] // 2 - height // 2 + height * -4),
            (self._width, self._height))
        self._text: pygame.Surface = self._font.render("+", True, "black")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=self._button.center)
        self._fill_rect = pygame.Rect(0, 0, 80, 75)
        self._fill_rect.center = (self._screen.get_size()[0] - 135, 175)

    def draw(self):
        pygame.draw.rect(mainmenu.getScreen(), "White", self._button)
        self._screen.blit(self._text, self._text_rectangle)
        pygame.display.update()

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            if settings.getVolume() < 1:
                settings.setVolume(settings.getVolume() + 0.05)
                self._screen.fill("black", self._fill_rect)
                settingsScreen.drawUpdateText()


class ResumeButton(Button):
    def __init__(self, screen: pygame.Surface, width: int, height: int):
        super().__init__()
        self._screen = screen
        self._width: int = width
        self._height: int = height
        self._button = pygame.Rect(
            (screen.get_size()[0] // 2 - width // 2, screen.get_size()[1] // 2 - height // 2 + height * 3),
            (self._width, self._height))
        self._text: pygame.Surface = self._font.render("Вернуться", True, "black")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=self._button.center)

    def draw(self):
        pygame.draw.rect(mainmenu.getScreen(), "White", self._button)
        self._screen.blit(self._text, self._text_rectangle)
        pygame.display.update()

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            gameScene.setPauseState(False)
            pauseMenu.setState(False)


class BackToMenuButton(Button):
    def __init__(self, screen: pygame.Surface, width: int, height: int):
        super().__init__()
        self._screen = screen
        self._width: int = width
        self._height: int = height
        self._button = pygame.Rect(
            (screen.get_size()[0] // 2 - width // 2, screen.get_size()[1] // 2 - height // 2 + height * 4.5),
            (self._width, self._height))
        self._text: pygame.Surface = self._font.render("Выйти", True, "black")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=self._button.center)

    def draw(self):
        pygame.draw.rect(mainmenu.getScreen(), "White", self._button)
        self._screen.blit(self._text, self._text_rectangle)
        pygame.display.update()

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            gameScene.setPauseState(False)
            mainmenu.setState(True)
            gameScene.setState(False)
            pauseMenu.setState(False)


class BuyButton(Button):
    def __init__(self, screen: pygame.Surface, width: int, height: int, product: str):
        super().__init__()
        self._screen = screen
        self._width: int = width
        self._height: int = height
        self._product: str = product
        self._button = pygame.Rect(
            (screen.get_size()[0] // 2 - width // 2, screen.get_size()[1] // 2 - height // 2 + height * 2),
            (self._width, self._height))
        self._text: pygame.Surface = self._font.render("Купить", True, "black")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=self._button.center)

    def draw(self):
        pygame.draw.rect(mainmenu.getScreen(), "White", self._button)
        self._screen.blit(self._text, self._text_rectangle)
        pygame.display.update()

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            gameScene.getPlayer().getSpeed().setMaxSpeed(6)
            pygame.mixer_music.load("music/buySound.mp3")
            pygame.mixer_music.play()


class TextLabel(ABC):
    def __init__(self):
        self._font: pygame.font.Font = pygame.font.SysFont(None, 50)

    @abstractmethod
    def draw(self):
        pass


class LoadingLabel(TextLabel):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._screen = screen
        self._text: pygame.Surface = self._font.render("Загрузка...", True, "white")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=(self._screen.get_size()[0] // 2, 50))

    def draw(self):
        self._screen.blit(self._text, self._text_rectangle)


class SettingsLabel(TextLabel):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._screen = screen
        self._text: pygame.Surface = self._font.render("Настройки", True, "white")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=(self._screen.get_size()[0] // 2, 50))

    def draw(self):
        self._screen.blit(self._text, self._text_rectangle)


class SkillsLabel(TextLabel):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._screen = screen
        self._text: pygame.Surface = self._font.render("Навыки", True, "white")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=(self._screen.get_size()[0] // 2, 50))

    def draw(self):
        self._screen.blit(self._text, self._text_rectangle)


class MusicLabelText(TextLabel):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._screen = screen
        self._text: pygame.Surface = self._font.render("Уровень громкости, %", True, "white")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=(self._screen.get_size()[0] // 3, 175))

    def draw(self):
        self._screen.blit(self._text, self._text_rectangle)


class MusicVolumeLevel(TextLabel):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._text_rectangle = None
        self._text = None
        self._screen = screen

    def draw(self):
        self._text: pygame.Surface = self._font.render(f"{round(settings.getVolume() * 100, 1)}", True, "white")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=(self._screen.get_size()[0] - 140, 175))
        self._screen.blit(self._text, self._text_rectangle)

    def getRect(self) -> pygame.Rect:
        return self._text_rectangle


settings = Settings()
mainmenu = MainMenu()
skillsMenu = SkillsScreen()
gameScene = GameScene()
pauseMenu = PauseMenu()
loadingScreen = LoadingScreen()
settingsScreen = SettingsScreen()
mainmenu.runMenu()
