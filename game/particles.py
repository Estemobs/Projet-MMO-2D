"""
Système de particules pour le jeu MMO 2D
Effets : poussière marche, éclats récolte, flash dégâts, lueur items
"""

import pygame
import math
import random


class Particle:
    """Particule individuelle."""
    __slots__ = ('x', 'y', 'vx', 'vy', 'life', 'max_life', 'color', 'size', 'gravity', 'fade_out')

    def __init__(self, x, y, vx, vy, life, color, size=2, gravity=0, fade_out=True):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size
        self.gravity = gravity
        self.fade_out = fade_out

    def update(self, dt):
        """Met à jour la particule. Retourne False quand elle est morte."""
        self.life -= dt
        if self.life <= 0:
            return False
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt
        return True

    def draw(self, screen, camera_x, camera_y):
        """Dessine la particule."""
        sx = self.x - camera_x
        sy = self.y - camera_y
        alpha = int(255 * (self.life / self.max_life)) if self.fade_out else 255
        size = max(1, int(self.size * (self.life / self.max_life)))

        surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        color = (*self.color[:3], alpha)
        pygame.draw.circle(surf, color, (size, size), size)
        screen.blit(surf, (int(sx) - size, int(sy) - size))


class ParticleManager:
    """Gestionnaire de toutes les particules actives."""

    MAX_PARTICLES = 500

    def __init__(self):
        self.particles = []

    def update(self, dt):
        """Met à jour toutes les particules."""
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, screen, camera):
        """Dessine toutes les particules."""
        for p in self.particles:
            p.draw(screen, camera.x, camera.y)

    def _add(self, particle):
        """Ajoute une particule si on n'a pas dépassé la limite."""
        if len(self.particles) < self.MAX_PARTICLES:
            self.particles.append(particle)

    # ── Effets publics ─────────────────────────────────────────────────

    def emit_dust(self, x, y):
        """Poussière quand le joueur marche."""
        for _ in range(2):
            vx = random.uniform(-20, 20)
            vy = random.uniform(-30, -10)
            color = random.choice([
                (139, 117, 78),  # terre
                (160, 140, 100),  # sable
                (120, 100, 60),   # terre sombre
            ])
            self._add(Particle(
                x + random.uniform(-4, 4),
                y + random.uniform(0, 6),
                vx, vy,
                life=random.uniform(0.3, 0.6),
                color=color,
                size=random.choice([1, 1, 2]),
                gravity=40,
            ))

    def emit_harvest_sparks(self, x, y, tile_type):
        """Éclats quand on récolte une ressource."""
        color_map = {
            'wood': [(139, 100, 62), (180, 140, 80), (101, 67, 33)],
            'stone': [(169, 169, 169), (130, 130, 135), (200, 200, 200)],
            'ore': [(200, 160, 60), (180, 130, 50), (220, 180, 80)],
            'food': [(84, 214, 125), (255, 100, 100), (200, 120, 255)],
        }
        colors = color_map.get(tile_type, [(200, 200, 200)])

        for _ in range(8):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 120)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 40
            color = random.choice(colors)
            self._add(Particle(
                x + random.uniform(-6, 6),
                y + random.uniform(-6, 6),
                vx, vy,
                life=random.uniform(0.3, 0.7),
                color=color,
                size=random.choice([2, 2, 3]),
                gravity=80,
            ))

    def emit_damage_flash(self, x, y):
        """Flash rouge quand on inflige des dégâts."""
        for _ in range(5):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(30, 80)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self._add(Particle(
                x, y,
                vx, vy,
                life=random.uniform(0.2, 0.4),
                color=(255, random.randint(50, 120), random.randint(30, 80)),
                size=random.choice([2, 3]),
                gravity=0,
            ))

    def emit_item_glow(self, x, y):
        """Lueur dorée autour des items au sol."""
        for _ in range(1):
            vx = random.uniform(-5, 5)
            vy = random.uniform(-15, -5)
            self._add(Particle(
                x + random.uniform(-8, 8),
                y + random.uniform(-4, 4),
                vx, vy,
                life=random.uniform(0.5, 1.0),
                color=(255, 220, 100),
                size=2,
                gravity=-10,
            ))

    def emit_level_up(self, x, y):
        """Effet de montée de niveau."""
        for _ in range(20):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(60, 150)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 80
            color = random.choice([
                (255, 221, 129),  # or
                (112, 165, 255),  # bleu
                (84, 214, 125),   # vert
            ])
            self._add(Particle(
                x, y,
                vx, vy,
                life=random.uniform(0.5, 1.2),
                color=color,
                size=random.choice([2, 3, 4]),
                gravity=60,
            ))

    def emit_death_effect(self, x, y):
        """Effet de mort du joueur."""
        for _ in range(30):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(40, 100)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 50
            self._add(Particle(
                x, y,
                vx, vy,
                life=random.uniform(0.6, 1.5),
                color=(200, 50, 50),
                size=random.choice([2, 3]),
                gravity=50,
            ))
