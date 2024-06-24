import time
import pygame
from abc import abstractmethod, ABC

import Controller
import Enemy
import View
import drops
import gameMap
import player
import projectileNpet
import math
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()
clock = pygame.time.Clock()
ButtonsViewer = View.ButtonsViewer()
TextViewer = View.LabelViewer()
clock.tick(60)


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
        self._playbutton: PlayButton = PlayButton(self._screen, 250, 50)
        self._skillsButton: SkillsButton = SkillsButton(self._screen, 250, 50)
        self._SettingsButton: SettingsButton = SettingsButton(self._screen, 250, 50)
        self._QuitButton: QuitButton = QuitButton(self._screen, 250, 50)
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
        for button in self._buttons:
            utils = button.getUtils()
            ButtonsViewer.drawButtons(self._screen, *utils)


class SkillsScreen:

    def __init__(self):
        self._screen: pygame.Surface = pygame.display.set_mode((750, 750))
        self._runLoadingScreen: bool = False
        self._settingsLabel: SkillsLabel = SkillsLabel(self._screen)
        self._runSkillsScreen: bool = False
        self._speedIcon: pygame.Surface = pygame.image.load("skillsIcons/speed.png")
        self._buyButton: BuyButton = BuyButton(self._screen, 200, 50, "speed")
        self._whiteBackground: pygame.Surface = pygame.Surface((96, 96))
        self._whiteBackground.fill("white")
        self._speedIconRect: pygame.Rect = self._speedIcon.get_rect(
            center=(self._screen.get_width() // 2, self._screen.get_height() // 2))
        self._whiteRect: pygame.Rect = self._whiteBackground.get_rect(
            center=(self._screen.get_width() // 2, self._screen.get_height() // 2))
        self._backButton: BackButton = BackButton(self._screen, 250, 50)
        self._buttons: list[Button] = [self._backButton, self._buyButton]

    def runSettings(self):
        self._screen.fill("black")
        self.drawNonUpdateText()
        self.drawButtons()
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

    def drawNonUpdateText(self):
        utils = self._settingsLabel.getUtils()
        TextViewer.drawLabels(self._screen, *utils)

    def drawButtons(self):
        for button in self._buttons:
            utils = button.getUtils()
            ButtonsViewer.drawButtons(self._screen, *utils)


class LoadingScreen:
    def __init__(self):
        self._screen: pygame.Surface = pygame.display.set_mode((750, 750))
        self._runLoadingScreen: bool = False
        self._loadingLabel: LoadingLabel = LoadingLabel(self._screen)
        self._loadingSquare: pygame.Rect = pygame.Rect(275, 275, 200, 200)
        self._loadingSquareSurface: pygame.Surface = pygame.Surface(
            (self._loadingSquare.width, self._loadingSquare.height))
        self._finalMap: list[list[int]] = []

    def runLoadingScreen(self):
        self._screen.fill("black")
        utils = self._loadingLabel.getUtils()
        TextViewer.drawLabels(self._screen, *utils)
        pygame.draw.rect(self._screen, "white", self._loadingSquare, 2)
        pygame.display.update()
        self._mapView = View.GameSceneView()
        mapStory: gameMap.Queue = self._mapView.getMapQueue()
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
        return self._mapView


class SettingsScreen:
    def __init__(self):
        self._screen: pygame.Surface = pygame.display.set_mode((750, 750))
        self._runLoadingScreen: bool = False
        self._settingsLabel: SettingsLabel = SettingsLabel(self._screen)
        self._musicLabelText: MusicLabelText = MusicLabelText(self._screen)
        self._labels: list[TextLabel] = [self._settingsLabel, self._musicLabelText]
        self._musicVolumeLevel: MusicVolumeLevel = MusicVolumeLevel(self._screen)
        self._runSettingsScreen: bool = False
        self._backButton: BackButton = BackButton(self._screen, 250, 50)
        self._decreaseMusicVolume: DecreaseMusicVolume = DecreaseMusicVolume(self._screen, 50, 50)
        self._increaseMusicVolume: IncreaseMusicVolume = IncreaseMusicVolume(self._screen, 50, 50)
        self._buttons: list[Button] = [self._backButton, self._decreaseMusicVolume, self._increaseMusicVolume]

    def runSettings(self):
        self._screen.fill("black")
        self.drawNonUpdateText()
        self.drawButtons()
        self.drawUpdateText()
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

    def drawNonUpdateText(self):
        for label in self._labels:
            utils = label.getUtils()
            TextViewer.drawLabels(self._screen, *utils)

    def drawButtons(self):
        for button in self._buttons:
            utils = button.getUtils()
            ButtonsViewer.drawButtons(self._screen, *utils)

    def drawUpdateText(self):
        self._musicVolumeLevel.updateText()
        utils = self._musicVolumeLevel.getUtils()
        TextViewer.drawLabels(self._screen, *utils)


class PauseMenu:
    def __init__(self):
        self._screen: pygame.Surface = mainmenu.getScreen()
        self._ResumeButton: ResumeButton = ResumeButton(self._screen, 250, 50)
        self._MenuButton: BackToMenuButton = BackToMenuButton(self._screen, 250, 50)
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
        for button in self._buttons:
            utils = button.getUtils()
            ButtonsViewer.drawButtons(self._screen, *utils)


class GameScene:
    def __init__(self):
        self._controller = None
        self._map = None
        self._mapCreator = None
        self._screen = mainmenu.getScreen()
        self._running: bool = False

        self._screen_rect: pygame.Rect = pygame.display.get_surface().get_rect()
        self._camera_rect: pygame.Rect = pygame.Rect(0, 0, self._screen_rect.width, self._screen_rect.height)
        self._player: player.Player = player.Player(self._screen)
        self._playerX: int = self._player.getCoordinates()[0]
        self._playerY: int = self._player.getCoordinates()[1]
        self._closestEnemy: Enemy.BaseEnemy | None = None
        self._projectiles: list[projectileNpet.FireProjectile] = []
        self._cameraSpeed: int = 1
        self._enemyCounter: int = 0
        self._difficulty: int = 2
        self._lastHPTicks: int = 0
        self._maxEnemyCount: int = self.setDifficulty(self._player.getHP(), self._player.getMaxHP(),
                                                      pygame.time.get_ticks())

        self._enemies: list[Enemy.BaseEnemy] = []
        self._droppedGoods: list[drops] = []
        self._pets: list[projectileNpet.BabyGhost] = []
        self._petDict: dict = {"GhostPet": 0}

        self._paused: bool = False
        self._lastShotTicks: int = 0
        self._coinsLabel = player.Coins()
        self._killsLabel = player.Kills()

    def run_game(self):
        pygame.event.clear()
        self._mapCreator = loadingScreen.getMapUtils()
        self._map, self._tileMap = self._mapCreator.getMap()
        pygame.mixer.music.load("music/kevin-macleod-8bit-dungeon-boss.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(settings.getVolume())
        self._controller = Controller.Controller(self._player, self._enemies, self._map, self._tileMap,
                                                 self._projectiles, self._pets)
        self._entityViewer = View.EntityView(self._screen, self._player, self._enemies, self._projectiles, self._pets)
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
            self._controller.update(self._player, self._enemies, self._projectiles, self._pets)
            self._controller.handle_input()
            self._entityViewer.updateView(self._player, self._enemies, self._projectiles, self._pets)
            self._entityViewer.drawUI(self._coinsLabel, self._killsLabel)
            pygame.display.flip()

    def setState(self, state: bool):
        self._running = state
        if state:
            gameScene.run_game()

    def restartGame(self):

        self._player: player.Player = player.Player(self._screen)
        self._closestEnemy: Enemy.BaseEnemy | None = None
        self._projectiles: list[projectileNpet.FireProjectile] = []
        self._enemyCounter: int = 0

        self._enemies: list[Enemy.BaseEnemy] = []
        self._droppedGoods: list[drops] = []
        self._pets: list[projectileNpet.BabyGhost] = []
        self._petDict: dict = {"GhostPet": 0}

        self._paused: bool = False
        self._lastShotTicks: int = 0

        mainmenu.setState(True)
        gameScene.setState(False)
        gameScene.setPauseState(False)
        mainmenu.runMenu()

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
        self._projectiles = self._controller.getProjectiles()
        current_ticks = pygame.time.get_ticks()
        if not self._projectiles:
            projectile = projectileNpet.FireProjectile(self._player.getHitbox().centerx,
                                                       self._player.getHitbox().centery, self._closestEnemy,
                                                       pygame.time.get_ticks(), self._camera_rect.x,
                                                       self._camera_rect.y)
            self._projectiles.append(projectile)
        else:
            element = self._projectiles[-1]
            if current_ticks - self._lastShotTicks > element.get_cd():
                self._lastShotTicks = current_ticks
                projectile = projectileNpet.FireProjectile(self._player.getHitbox().centerx,
                                                           self._player.getHitbox().centery, self._closestEnemy,
                                                           current_ticks, self._camera_rect.x,
                                                           self._camera_rect.y)
                self._projectiles.append(projectile)
        for element in self._projectiles[:]:
            if element.destroyOnTime(pygame.time.get_ticks()):
                self._projectiles.remove(element)
            else:
                element.update()
                self._entityViewer.updateProjectiles(element, self._camera_rect.x, self._camera_rect.y)

    def processEnemies(self):
        if self._enemyCounter < self._maxEnemyCount:
            self._enemies.append(random.choice([Enemy.GhostEnemy(self._screen), Enemy.ZombieEnemy(self._screen)]))
            self._enemyCounter += 1
        closest_distance = float('inf')
        for enemy in self._enemies:
            if enemy.getDrawState() is not True:
                enemy.create(self._playerX, self._playerY, self._camera_rect.x, self._camera_rect.y,
                             self._mapCreator.getTileSize(), self._mapCreator.getTileAmount(),
                             self._screen.get_size())
                enemy.setDrawState()
            enemy_x, enemy_y = enemy.getCoordinates()
            current_distance = math.sqrt((enemy_x - self._playerX) ** 2 + (enemy_y - self._playerY) ** 2)
            if current_distance < closest_distance:
                closest_distance = current_distance
                self._closestEnemy = enemy
            enemy.updateCoordinates(self._player, self._playerX, self._playerY, self._camera_rect.x,
                                    self._camera_rect.y)
            self._entityViewer.updateEnemies(enemy, self._camera_rect.x, self._camera_rect.y)
            if enemy.getHP() <= 0:
                self._player.increaseCoins()
                self._player.increaseKills()
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
                    self._pets.append(projectileNpet.BabyGhost(self._screen, self._playerX, self._playerY))
                    self._petDict["GhostPet"] += 1
                self._droppedGoods.remove(drop)

    def processPlayer(self):
        self._playerX, self._playerY = self._player.getCoordinates()
        self._camera_rect.center = (self._playerX, self._playerY)
        if self._player.getHP() > 0:
            self._entityViewer.updatePlayer(self._camera_rect.x, self._camera_rect.y)
        else:
            pygame.mixer.music.stop()
            self.restartGame()

    def processPets(self):
        for pet in self._pets:
            pet.followPlayer(self._playerX, self._playerY, self._enemies)
            self._entityViewer.updatePets(pet, self._camera_rect.x, self._camera_rect.y)

    def setPauseState(self, state: bool):
        self._paused = state

    def getPlayer(self):
        return self._player


class Button(ABC):
    def __init__(self):
        self._font: pygame.font.Font = pygame.font.SysFont(None, 50)

    @abstractmethod
    def do_on_click(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def getUtils(self):
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

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            if mainmenu.getState():
                mainmenu.setState(False)
                loadingScreen.setState(True)

    def getUtils(self):
        return self._button, self._text, self._text_rectangle


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

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            if mainmenu.getState():
                mainmenu.setState(False)
                skillsMenu.setState(True)

    def getUtils(self):
        return self._button, self._text, self._text_rectangle


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

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            if mainmenu.getState():
                mainmenu.setState(False)
                settingsScreen.setState(True)

    def getUtils(self):
        return self._button, self._text, self._text_rectangle


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

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            if mainmenu.getState():
                pygame.quit()

    def getUtils(self):
        return self._button, self._text, self._text_rectangle


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

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            mainmenu.setState(True)
            settingsScreen.setState(False)

    def getUtils(self):
        return self._button, self._text, self._text_rectangle


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

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            if settings.getVolume() > 0.01:
                settings.setVolume(settings.getVolume() - 0.05)
                self._screen.fill("black", self._fill_rect)
                settingsScreen.drawUpdateText()

    def getUtils(self):
        return self._button, self._text, self._text_rectangle


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

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            if settings.getVolume() < 1:
                settings.setVolume(settings.getVolume() + 0.05)
                self._screen.fill("black", self._fill_rect)
                settingsScreen.drawUpdateText()

    def getUtils(self):
        return self._button, self._text, self._text_rectangle


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

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            gameScene.setPauseState(False)
            pauseMenu.setState(False)

    def getUtils(self):
        return self._button, self._text, self._text_rectangle


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

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos):
            gameScene.getPlayer().resetKills()
            gameScene.setPauseState(False)
            mainmenu.setState(True)
            gameScene.setState(False)
            pauseMenu.setState(False)

    def getUtils(self):
        return self._button, self._text, self._text_rectangle


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

    def do_on_click(self, event: pygame.event.Event):
        if self._button.collidepoint(event.pos) and gameScene.getPlayer().getCoins() >= 100:
            gameScene.getPlayer().setMaxSpeed(5)
            gameScene.getPlayer().decreaseCoins(100)
            print(1)
            pygame.mixer_music.load("music/buySound.mp3")
            pygame.mixer.music.set_volume(settings.getVolume())
            pygame.mixer_music.play()

    def getUtils(self):
        return self._button, self._text, self._text_rectangle


class TextLabel(ABC):
    def __init__(self):
        self._font: pygame.font.Font = pygame.font.SysFont(None, 50)

    @abstractmethod
    def getUtils(self):
        pass


class LoadingLabel(TextLabel):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._screen = screen
        self._text: pygame.Surface = self._font.render("Загрузка...", True, "white")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=(self._screen.get_size()[0] // 2, 50))

    def getUtils(self):
        return self._text, self._text_rectangle


class SettingsLabel(TextLabel):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._screen = screen
        self._text: pygame.Surface = self._font.render("Настройки", True, "white")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=(self._screen.get_size()[0] // 2, 50))

    def getUtils(self):
        return self._text, self._text_rectangle


class SkillsLabel(TextLabel):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._screen = screen
        self._text: pygame.Surface = self._font.render("Навыки", True, "white")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=(self._screen.get_size()[0] // 2, 50))

    def getUtils(self):
        return self._text, self._text_rectangle


class MusicLabelText(TextLabel):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._screen = screen
        self._text: pygame.Surface = self._font.render("Уровень громкости, %", True, "white")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=(self._screen.get_size()[0] // 3, 175))

    def getUtils(self):
        return self._text, self._text_rectangle


class MusicVolumeLevel(TextLabel):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._screen = screen
        self._text: pygame.Surface = self._font.render(f"{round(settings.getVolume() * 100, 1)}", True, "white")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=(self._screen.get_size()[0] - 140, 175))

    def getUtils(self):
        return self._text, self._text_rectangle

    def updateText(self):
        self._text: pygame.Surface = self._font.render(f"{round(settings.getVolume() * 100, 1)}", True, "white")
        self._text_rectangle: pygame.Rect = self._text.get_rect(center=(self._screen.get_size()[0] - 140, 175))


settings = Settings()
mainmenu = MainMenu()
skillsMenu = SkillsScreen()
gameScene = GameScene()
pauseMenu = PauseMenu()
loadingScreen = LoadingScreen()
settingsScreen = SettingsScreen()
mainmenu.runMenu()
