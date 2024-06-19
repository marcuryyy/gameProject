import pygame
from abc import abstractmethod, ABC
import Enemy
import drops
import gameMap
import player
import diffProjectiles
import math
import random

pygame.init()
pygame.font.init()


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
        self._playbutton.draw()
        self._skillsButton.draw()
        self._SettingsButton.draw()
        self._QuitButton.draw()
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


class GameScene:
    def __init__(self):
        self._mapCreator = None
        self._map = None
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
        self._clock = pygame.time.Clock()
        self._paused: bool = False
        self._lastShotTicks: int = 0

    def run_game(self):
        self._mapCreator = gameMap.GameMapCreator()
        self._map = self._mapCreator.getMap()
        self._clock.tick(60)
        while self._running and not self._paused:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._paused = True
                        self.pause()
            self._maxEnemyCount = self.setDifficulty(self._player.getHP(), self._player.getMaxHP(),
                                                     pygame.time.get_ticks())
            self._mapCreator.fillMap(self._screen, self._camera_rect.x, self._camera_rect.y)
            self.processPlayer()
            self.processEnemies()
            self.processProjectiles()
            self.processDrops()
            self.processPlayerBars()
            self.processPets()
            pygame.display.flip()

    def setState(self, state: bool):
        self._running = state
        if state:
            gameScene.run_game()

    def pause(self):
        self._paused = True
        while self._paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._paused = False

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
        if not self._projectiles:
            projectile = diffProjectiles.FireProjectile(self._player.getHitbox().centerx,
                                                        self._player.getHitbox().centery, self._closestEnemy,
                                                        pygame.time.get_ticks(), self._camera_rect.x,
                                                        self._camera_rect.y)
            self._projectiles.append(projectile)
        else:
            element = self._projectiles[-1]
            current_ticks = pygame.time.get_ticks()
            if current_ticks - self._lastShotTicks > element.get_cd():
                self._lastShotTicks = pygame.time.get_ticks()
                projectile = diffProjectiles.FireProjectile(self._player.getHitbox().centerx,
                                                            self._player.getHitbox().centery, self._closestEnemy,
                                                            pygame.time.get_ticks(), self._camera_rect.x,
                                                            self._camera_rect.y)
                self._projectiles.append(projectile)
        for element in self._projectiles:
            if element.destroy(pygame.time.get_ticks()):
                self._projectiles.remove(element)
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
            self.pause()

    def processPets(self):
        for pet in self._pets:
            pet.followPlayer(self._playerX, self._playerY, self._camera_rect.x, self._camera_rect.y, self._enemies)


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
                gameScene.setState(True)


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
                gameScene.setState(True)


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
                gameScene.setState(True)


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


mainmenu = MainMenu()
gameScene = GameScene()
mainmenu.runMenu()
