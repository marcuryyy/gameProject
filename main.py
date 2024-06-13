import pygame
from abc import abstractmethod, ABC
import Enemy
import drops
import gameMap
import player
import diffProjectiles
import math

pygame.init()


class MainMenu:
    def __init__(self):
        self._screen = pygame.display.set_mode((750, 750))
        self._screen.fill("Black")
        self._playbutton = PlayButton(50, 50)
        self._buttons: list[Button] = [self._playbutton]
        self._runMenu: bool = True

    def runMenu(self):
        self._playbutton.draw()
        while self._runMenu:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self._buttons:
                        button.do_on_click(event)

    def getScreen(self):
        return self._screen

    def getState(self):
        return self._runMenu

    def setState(self, state: bool):
        self._runMenu = state


class GameScene:
    def __init__(self):
        self._mapCreator = gameMap.GameMapCreator()
        self._map = self._mapCreator.getMap()
        self._screen = mainmenu.getScreen()
        self._running = False
        self._screen_rect = pygame.display.get_surface().get_rect()
        self._camera_rect = pygame.Rect(0, 0, self._screen_rect.width, self._screen_rect.height)
        self._player = player.Player(self._screen)
        self._playerX, self._playerY = self._player.getCoordinates()
        self._playerWeapon = self._player.getWeapon()
        self._closestEnemy = None
        self._projectiles: list[diffProjectiles.FireProjectile] = []
        self._cameraSpeed = 1
        self._enemyCounter = 0
        self._maxEnemyCount = 10
        self._enemies: list[Enemy.BaseEnemy] = []
        self._droppedGoods = []
        self._pets: list[diffProjectiles.BabyGhost] = []
        self._petDict = {"GhostPet" : 0}
        self._clock = pygame.time.Clock()
        self._paused = False
        self._lastShotTicks = 0

    def run_game(self):
        while self._running and not self._paused:
            pygame.display.update()
            self._clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._paused = True
                        self.pause()
            self._player.handle_keys(self._mapCreator)
            self._playerX, self._playerY = self._player.getCoordinates()
            self._camera_rect.center = (self._playerX, self._playerY)
            self._mapCreator.fillMap(self._screen, self._camera_rect.x, self._camera_rect.y)
            self._player.getHealthBar().draw(self._screen, self._player.getHP())
            self._player.getStaminaBar().draw(self._screen, self._player.getSTAMINA())
            if self._enemyCounter < self._maxEnemyCount:
                self._enemies.append(Enemy.EasyEnemy(self._screen))
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
            for drop in self._droppedGoods:
                drop.update(self._camera_rect.x, self._camera_rect.y)
                result = drop.onPickUp(self._player)
                if result:
                    if result == "GhostPet":
                        self._pets.append(diffProjectiles.BabyGhost(self._screen, self._playerX, self._playerY))
                        self._petDict["GhostPet"] += 1
                    self._droppedGoods.remove(drop)
            for pet in self._pets:
                pet.followPlayer(self._playerX, self._playerY, self._camera_rect.x, self._camera_rect.y, self._enemies)
            if self._player.getHP() > 0:
                self._player.update(self._camera_rect.x, self._camera_rect.y)
            else:
                self.pause()
            pygame.display.flip()

    def setState(self, state):
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


class Button(ABC):
    @abstractmethod
    def __init__(self, width, height):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def do_on_click(self, event: pygame.event):
        pass


class PlayButton(Button):
    def __init__(self, width, height):
        self._width: int = width
        self._height: int = height
        self._button = None

    def draw(self):
        self._button = pygame.Rect((0, 0), (self._width, self._height))
        pygame.draw.rect(mainmenu.getScreen(), "White", self._button)
        pygame.display.update()

    def do_on_click(self, event):
        if self._button.collidepoint(event.pos):
            if mainmenu.getState():
                mainmenu.setState(False)
                gameScene.setState(True)


mainmenu = MainMenu()
gameScene = GameScene()
mainmenu.runMenu()
