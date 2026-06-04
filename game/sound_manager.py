"""
Gestionnaire de sons synthétiques pour le jeu MMO 2D
Génère des sons procéduralement avec pygame.mixer
"""

import pygame
import math
import array
import os


class SoundManager:
    """Gestionnaire de sons du jeu."""

    def __init__(self):
        self.sounds = {}
        self.music_enabled = True
        self.sfx_enabled = True
        self.volume = 0.5

        try:
            pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.mixer.init()
            self._generate_all_sounds()
            print("✅ Système audio initialisé")
        except Exception as e:
            print(f"⚠️ Audio indisponible: {e}")
            self.sfx_enabled = False

    def _generate_tone(self, frequency, duration, volume=0.3, wave_type='sine', fade_out=True):
        """Génère un son synthétique."""
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = array.array('h', [0] * n_samples)

        for i in range(n_samples):
            t = i / sample_rate
            # Enveloppe ADSR simple
            envelope = 1.0
            attack = 0.01
            release = duration * 0.3
            if t < attack:
                envelope = t / attack
            elif t > duration - release:
                envelope = (duration - t) / release

            if wave_type == 'sine':
                val = math.sin(2 * math.pi * frequency * t)
            elif wave_type == 'square':
                val = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
            elif wave_type == 'noise':
                import random
                val = random.uniform(-1, 1)
            else:
                val = math.sin(2 * math.pi * frequency * t)

            sample = int(val * envelope * volume * 32767)
            sample = max(-32767, min(32767, sample))
            buf[i] = sample

        sound = pygame.mixer.Sound(buffer=buf.tobytes())
        return sound

    def _generate_noise_burst(self, duration, volume=0.2):
        """Génère un bruit court (pour récolte, impact)."""
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = array.array('h', [0] * n_samples)

        import random
        for i in range(n_samples):
            t = i / sample_rate
            envelope = max(0, 1.0 - t / duration)
            val = random.uniform(-1, 1) * envelope * volume
            buf[i] = max(-32767, min(32767, int(val * 32767)))

        return pygame.mixer.Sound(buffer=buf.tobytes())

    def _generate_all_sounds(self):
        """Génère tous les sons du jeu."""
        # Pas du joueur (3 variantes)
        self.sounds['step1'] = self._generate_tone(180, 0.06, 0.15, 'noise')
        self.sounds['step2'] = self._generate_tone(150, 0.05, 0.12, 'noise')
        self.sounds['step3'] = self._generate_tone(200, 0.05, 0.10, 'noise')

        # Récolte
        self.sounds['harvest_wood'] = self._generate_tone(300, 0.12, 0.25, 'square')
        self.sounds['harvest_stone'] = self._generate_noise_burst(0.1, 0.3)
        self.sounds['harvest_ore'] = self._generate_tone(800, 0.15, 0.2, 'sine')

        # Craft
        self.sounds['craft'] = self._generate_tone(523, 0.1, 0.3, 'sine')
        self.sounds['craft_fail'] = self._generate_tone(200, 0.2, 0.2, 'square')

        # Attaque
        self.sounds['swing'] = self._generate_tone(250, 0.08, 0.2, 'noise')
        self.sounds['hit'] = self._generate_noise_burst(0.08, 0.35)
        self.sounds['hurt'] = self._generate_tone(180, 0.15, 0.25, 'square')

        # Menu
        self.sounds['menu_click'] = self._generate_tone(440, 0.05, 0.15, 'sine')
        self.sounds['menu_hover'] = self._generate_tone(350, 0.03, 0.08, 'sine')

        # Événements
        self.sounds['level_up'] = self._generate_tone(660, 0.3, 0.3, 'sine')
        self.sounds['pickup'] = self._generate_tone(550, 0.08, 0.2, 'sine')
        self.sounds['death'] = self._generate_tone(120, 0.5, 0.3, 'square')
        self.sounds['save'] = self._generate_tone(440, 0.15, 0.2, 'sine')

        print(f"  🔊 {len(self.sounds)} sons générés")

    def play(self, sound_name, volume=None):
        """Joue un son par son nom."""
        if not self.sfx_enabled:
            return
        if sound_name in self.sounds:
            vol = volume if volume is not None else self.volume
            self.sounds[sound_name].set_volume(vol)
            self.sounds[sound_name].play()

    def play_random_step(self):
        """Joue un son de pas aléatoire."""
        import random
        self.play(random.choice(['step1', 'step2', 'step3']), volume=0.15)

    def play_harvest(self, tile_category):
        """Joue le son de récolte selon le type de tile."""
        sound_map = {
            'wood': 'harvest_wood',
            'stone': 'harvest_stone',
            'ore': 'harvest_ore',
            'food': 'harvest_wood',
        }
        self.play(sound_map.get(tile_category, 'harvest_stone'))

    def set_volume(self, vol):
        """Règle le volume global des SFX (0.0 à 1.0)."""
        self.volume = max(0.0, min(1.0, vol))

    def toggle_sfx(self):
        """Active/Désactive les sons."""
        self.sfx_enabled = not self.sfx_enabled
        return self.sfx_enabled


# Instance globale
_sound_manager = None


def get_sound_manager():
    """Retourne l'instance singleton du gestionnaire de sons."""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
