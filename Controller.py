import Enemy
import projectileNpet
import player


class Controller:
    def __init__(self, playerEntity, enemies, gameMap, tile_map, projectiles, pet):
        self._player: player.Player = playerEntity
        self._enemies: list[Enemy.BaseEnemy] = enemies
        self._projectiles: list[projectileNpet.FireProjectile] = projectiles
        self._game_map: list[list[int]] = gameMap
        self._tile_map: list[list[gameMap.BaseTile]] = tile_map
        self._pet: list[projectileNpet.BabyGhost] = pet

    def handle_collisions(self):
        for projectile in self._projectiles:
            for enemy in self._enemies:
                if self._pet:
                    if self._pet[0].getHitbox().colliderect(enemy.getHitbox()):
                        enemy.Damage(self._pet[0].getDamage())
                if self._player.getHitbox().colliderect(enemy.getHitbox()):
                    self._player.getDamage(enemy.getDamage())
                maxDamageTimes, damageCounter = projectile.getDamageCounter()
                if projectile.getHitbox().colliderect(enemy.getHitbox()):
                    if maxDamageTimes > damageCounter:
                        enemy.Damage(projectile.getDamage())
                        self._projectiles.remove(projectile)
                        projectile.increaseDamageCounter()

        player_rect = self._player.getHitbox()
        for y, line in enumerate(self._game_map):
            for x, tile in enumerate(line):
                if self._tile_map[y][x].__class__.__name__ == "GrassTile" and player_rect.colliderect(
                        self._tile_map[y][x].getHitbox()):
                    self._player.setSpeed(self._player.getMaxSpeed())
                    self._player.setAllStates(True)
                if self._tile_map[y][x].__class__.__name__ == "RocksTile" and player_rect.colliderect(
                        self._tile_map[y][x].getHitbox()):
                    self._player.setSpeed(self._player.getMaxSpeed()//2)
                    self._player.setAllStates(True)
                if self._tile_map[y][x].__class__.__name__ == "WaterTile" and player_rect.colliderect(
                        self._tile_map[y][x].getHitbox()):
                    if self._player.getFacing().lower() == "left":
                        self._player.setWalkLeftState(False)
                    if self._player.getFacing().lower() == "right":
                        self._player.setWalkRightState(False)
                    if self._player.getFacing().lower() == "up":
                        self._player.setWalkUpState(False)
                    if self._player.getFacing().lower() == "down":
                        self._player.setWalkDownState(False)

    def update(self, playerEntity: player.Player, enemies: list[Enemy.BaseEnemy],
               projectiles: list[projectileNpet.FireProjectile], pet: list[projectileNpet.BabyGhost]):
        self._player = playerEntity
        self._enemies = enemies
        self._projectiles = projectiles
        self._pet = pet
        self.handle_collisions()

    def getProjectiles(self):
        return self._projectiles
