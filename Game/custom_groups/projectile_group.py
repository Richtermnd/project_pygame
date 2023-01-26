import pygame


class ProjectileGroup(pygame.sprite.Group):
    def __init__(self, targets, obstacles):
        super().__init__()
        self.targets = targets
        self.obstacles = obstacles

    def update(self, *args, **kwargs) -> None:
        """ Check hits """
        for sprite in self.sprites():
            targets_collide = pygame.sprite.spritecollide(sprite, self.targets, False)
            if targets_collide:
                [spr.change_hp(-sprite.damage) for spr in targets_collide]
                if not sprite.is_piercing:
                    sprite.kill()
            obstacle_collide = pygame.sprite.spritecollideany(sprite, self.obstacles)
            if obstacle_collide:
                if not sprite.is_spectral:
                    sprite.kill()
