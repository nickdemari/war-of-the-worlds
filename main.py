import pygame
import random
import sys
import os
import wave
import struct
import math
import numpy

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("War of the Worlds Adventure!")

# Colors (for shapes and UI)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)

# Create assets directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

# Generate simple sound effects
def generate_jump_sound():
    sample_rate = 44100
    duration = 0.1
    frequency = 440
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        sample = int(32767 * math.sin(2 * math.pi * frequency * t))
        samples.append([sample, sample])  # Same sample for both channels
    
    return pygame.sndarray.make_sound(numpy.array(samples, dtype=numpy.int16))

def generate_power_up_sound():
    sample_rate = 44100
    duration = 0.2
    frequency = 880
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        sample = int(32767 * math.sin(2 * math.pi * frequency * t))
        samples.append([sample, sample])  # Same sample for both channels
    
    return pygame.sndarray.make_sound(numpy.array(samples, dtype=numpy.int16))

def generate_hit_sound():
    sample_rate = 44100
    duration = 0.1
    frequency = 220
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        sample = int(32767 * math.sin(2 * math.pi * frequency * t))
        samples.append([sample, sample])  # Same sample for both channels
    
    return pygame.sndarray.make_sound(numpy.array(samples, dtype=numpy.int16))

def generate_laser_sound():
    sample_rate = 44100
    duration = 0.05
    frequency = 1200
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        sample = int(32767 * math.sin(2 * math.pi * frequency * t))
        samples.append([sample, sample])  # Same sample for both channels
    
    return pygame.sndarray.make_sound(numpy.array(samples, dtype=numpy.int16))

def generate_heat_ray_sound():
    sample_rate = 44100
    duration = 1.0
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        
        # Create fire-like sound with multiple frequencies
        base_freq = 2000 * (1 - t/duration)  # Descending base frequency
        crackle_freq = random.randint(1000, 4000)  # Random crackle frequencies
        
        # Main fire sound
        fire = math.sin(2 * math.pi * base_freq * t)
        
        # Add crackling effect
        crackle = random.uniform(-0.3, 0.3) * math.sin(2 * math.pi * crackle_freq * t)
        
        # Add low rumble
        rumble = 0.2 * math.sin(2 * math.pi * 100 * t)
        
        # Combine all elements
        combined = fire + crackle + rumble
        
        # Add amplitude modulation for "whoosh" effect
        mod = math.sin(2 * math.pi * 3 * t)
        
        # Final sample with modulation
        sample = int(32767 * combined * (1 + 0.3 * mod))
        samples.append([sample, sample])
    
    return pygame.sndarray.make_sound(numpy.array(samples, dtype=numpy.int16))

def generate_ufo_sound():
    sample_rate = 44100
    duration = 0.3
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        
        # Create UFO-like sound with multiple frequencies
        base_freq = 800 + math.sin(t * 10) * 200  # Oscillating base frequency
        high_freq = 2000 + math.sin(t * 15) * 500  # Oscillating high frequency
        
        # Main UFO sound
        ufo = math.sin(2 * math.pi * base_freq * t)
        
        # Add high-pitched whine
        whine = 0.5 * math.sin(2 * math.pi * high_freq * t)
        
        # Add amplitude modulation for "pulsing" effect
        mod = math.sin(2 * math.pi * 8 * t)
        
        # Final sample with modulation
        sample = int(32767 * (ufo + whine) * (1 + 0.3 * mod))
        samples.append([sample, sample])
    
    return pygame.sndarray.make_sound(numpy.array(samples, dtype=numpy.int16))

def generate_boss_sound():
    sample_rate = 44100
    duration = 0.5
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        
        # Create boss-like sound with multiple frequencies
        base_freq = 400 + math.sin(t * 5) * 100  # Oscillating base frequency
        mid_freq = 1000 + math.sin(t * 8) * 300  # Oscillating mid frequency
        high_freq = 2500 + math.sin(t * 12) * 600  # Oscillating high frequency
        
        # Main boss sound
        boss = math.sin(2 * math.pi * base_freq * t)
        
        # Add mid and high frequencies
        mid = 0.5 * math.sin(2 * math.pi * mid_freq * t)
        high = 0.3 * math.sin(2 * math.pi * high_freq * t)
        
        # Add amplitude modulation for "threatening" effect
        mod = math.sin(2 * math.pi * 6 * t)
        
        # Final sample with modulation
        sample = int(32767 * (boss + mid + high) * (1 + 0.4 * mod))
        samples.append([sample, sample])
    
    return pygame.sndarray.make_sound(numpy.array(samples, dtype=numpy.int16))

# Load or generate sound effects
try:
    jump_sound = pygame.mixer.Sound('assets/jump.wav')
    power_up_sound = pygame.mixer.Sound('assets/power_up.wav')
    hit_sound = pygame.mixer.Sound('assets/hit.wav')
    laser_sound = pygame.mixer.Sound('assets/laser.wav')
    heat_ray_sound = pygame.mixer.Sound('assets/heat_ray.wav')
    ufo_sound = pygame.mixer.Sound('assets/ufo.wav')
    boss_sound = pygame.mixer.Sound('assets/boss.wav')
except:
    jump_sound = generate_jump_sound()
    power_up_sound = generate_power_up_sound()
    hit_sound = generate_hit_sound()
    laser_sound = generate_laser_sound()
    heat_ray_sound = generate_heat_ray_sound()
    ufo_sound = generate_ufo_sound()
    boss_sound = generate_boss_sound()

# Set volume for sound effects
jump_sound.set_volume(0.3)
power_up_sound.set_volume(0.4)
hit_sound.set_volume(0.3)
laser_sound.set_volume(0.2)
heat_ray_sound.set_volume(0.5)
ufo_sound.set_volume(0.4)
boss_sound.set_volume(0.5)

# Create simple graphics
def create_tripod(leg_angles=None):
    surface = pygame.Surface((60, 100))
    surface.fill((0, 0, 0))  # Black body
    
    # Calculate leg positions based on angles
    center_x = 30
    body_bottom_y = 40  # Bottom of the body circle
    
    # Draw legs with rotation
    for i in range(3):
        # Calculate leg end points based on angle
        leg_length = 100
        # Set specific angles for each leg
        if i == 0:  # Left leg
            spread_angle = 45  # Left leg at 45 degrees
        elif i == 1:  # Middle leg
            spread_angle = 90  # Middle leg at 90 degrees (straight down)
        else:  # Right leg
            spread_angle = 75  # Right leg at 75 degrees
        
        # Get the leg angle (0 if not provided)
        leg_angle = leg_angles[i] if leg_angles else 0
        
        # Calculate the actual angle including the spread
        actual_angle = leg_angle + spread_angle
        
        # Calculate leg end points (rotated 90 degrees to make legs point downward)
        end_x = center_x + leg_length * math.cos(math.radians(actual_angle))
        end_y = body_bottom_y + leg_length * math.sin(math.radians(actual_angle))
        
        # Draw leg
        pygame.draw.line(surface, (100, 100, 100), 
                        (center_x, body_bottom_y),  # Start at bottom of body
                        (end_x, end_y), 5)
    
    # Draw head
    pygame.draw.circle(surface, (200, 0, 0), (30, 20), 15)
    return surface

def create_player():
    surface = pygame.Surface((40, 60))
    surface.fill((0, 0, 255))  # Blue body
    # Draw head
    pygame.draw.circle(surface, (255, 255, 255), (20, 15), 10)
    # Draw arms
    pygame.draw.line(surface, (255, 255, 255), (10, 25), (30, 25), 5)
    return surface

def create_boss_tripod(leg_angles):
    surface = pygame.Surface((120, 200))
    surface.fill((100, 0, 0))  # Dark red body
    
    # Calculate leg positions based on angles
    center_x = 60
    body_bottom_y = 80  # Bottom of the body circle
    
    # Draw legs with rotation
    for i in range(3):
        # Calculate leg end points based on angle
        leg_length = 180
        # Set specific angles for each leg
        if i == 0:  # Left leg
            spread_angle = 45  # Left leg at 45 degrees
        elif i == 1:  # Middle leg
            spread_angle = 90  # Middle leg at 90 degrees (straight down)
        else:  # Right leg
            spread_angle = 75  # Right leg at 75 degrees
        
        # Get the leg angle
        leg_angle = leg_angles[i]
        
        # Calculate the actual angle including the spread
        actual_angle = leg_angle + spread_angle
        
        # Calculate leg end points (rotated 90 degrees to make legs point downward)
        end_x = center_x + leg_length * math.cos(math.radians(actual_angle))
        end_y = body_bottom_y + leg_length * math.sin(math.radians(actual_angle))
        
        # Draw leg
        pygame.draw.line(surface, (150, 150, 150), 
                        (center_x, body_bottom_y),  # Start at bottom of body
                        (end_x, end_y), 10)
    
    # Draw head
    pygame.draw.circle(surface, (255, 0, 0), (60, 30), 30)
    # Draw energy core
    pygame.draw.circle(surface, (255, 255, 0), (60, 60), 20)
    return surface

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, shooter_type="player"):
        super().__init__()
        self.shooter_type = shooter_type
        self.image = pygame.Surface((10, 5))
        
        # Set color and damage based on shooter type
        if shooter_type == "player":
            self.image.fill(YELLOW)
            self.damage = 1
        elif shooter_type == "boss":
            self.image.fill((255, 0, 255))  # Purple for boss
            self.damage = 15
        elif shooter_type == "shooter":
            self.image.fill((255, 165, 0))  # Orange for shooter aliens
            self.damage = 4
        elif shooter_type == "ufo":
            self.image.fill((0, 255, 255))  # Cyan for UFOs
            self.damage = 3
        elif shooter_type == "rpg":
            self.image.fill((255, 165, 0))  # Orange for RPG
            self.damage = 20
        elif shooter_type == "assault_rifle":
            self.image.fill((128, 128, 128))  # Gray for assault rifle
            self.damage = 3
        elif shooter_type == "pistol":
            self.image.fill((192, 192, 192))  # Silver for pistol
            self.damage = 8
        elif shooter_type == "sniper":
            self.image.fill((0, 255, 255))  # Cyan for sniper
            self.damage = 25
        elif shooter_type == "finger_gun":
            self.image.fill((255, 192, 203))  # Pink for finger gun
            self.damage = 50
        else:
            self.image.fill((255, 0, 0))  # Red for other aliens
            self.damage = 5
            
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10
        self.angle = 0

    def update(self):
        # Move in the direction of the angle
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y += self.speed * math.sin(math.radians(self.angle))
        
        # Kill if off screen
        if (self.rect.right < 0 or self.rect.left > WINDOW_WIDTH or 
            self.rect.bottom < 0 or self.rect.top > WINDOW_HEIGHT):
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = create_player()
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 4
        self.rect.bottom = WINDOW_HEIGHT - 20
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.velocity_y = 0
        self.jumping = False
        self.health = 100
        self.score = 0
        self.power_up = False
        self.power_up_timer = 0
        self.last_health = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.level = 1
        self.aliens_defeated = 0
        self.aliens_needed = 5
        self.damage = 1
        self.damage_boost = 0
        # New weapon attributes
        self.current_weapon = "laser"
        self.weapon_timer = 0
        self.weapon_duration = 0
        self.rpg_ammo = 0
        self.assault_rifle_ammo = 0
        self.finger_gun_ammo = 0
        self.pistol_ammo = 0
        self.sniper_ammo = 0

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        if self.rect.bottom > WINDOW_HEIGHT - 20:
            self.rect.bottom = WINDOW_HEIGHT - 20
            self.velocity_y = 0
            self.jumping = False
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

        if self.power_up:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.power_up = False
                self.image = create_player()
                self.damage_boost = 0

    def jump(self):
        if not self.jumping:
            self.velocity_y = self.jump_power
            self.jumping = True
            jump_sound.play()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            # Calculate angle based on mouse position
            mouse_pos = pygame.mouse.get_pos()
            dx = mouse_pos[0] - self.rect.centerx
            dy = mouse_pos[1] - self.rect.centery
            angle = math.degrees(math.atan2(dy, dx))
            
            # Create laser based on current weapon
            if self.current_weapon == "rpg" and self.rpg_ammo > 0:
                laser = Laser(self.rect.centerx, self.rect.centery, "rpg")
                laser.angle = angle
                laser.speed = 8
                laser.damage = 20
                self.rpg_ammo -= 1
                all_sprites.add(laser)
                lasers.add(laser)
                laser_sound.play()
            elif self.current_weapon == "assault_rifle" and self.assault_rifle_ammo > 0:
                # Create spread shot
                for spread in [-10, -5, 0, 5, 10]:
                    laser = Laser(self.rect.centerx, self.rect.centery, "assault_rifle")
                    laser.angle = angle + spread
                    laser.speed = 15
                    laser.damage = 3
                    self.assault_rifle_ammo -= 1
                    all_sprites.add(laser)
                    lasers.add(laser)
                laser_sound.play()
            elif self.current_weapon == "pistol" and self.pistol_ammo > 0:
                laser = Laser(self.rect.centerx, self.rect.centery, "pistol")
                laser.angle = angle
                laser.speed = 14
                laser.damage = 8
                self.pistol_ammo -= 1
                all_sprites.add(laser)
                lasers.add(laser)
                laser_sound.play()
            elif self.current_weapon == "sniper" and self.sniper_ammo > 0:
                laser = Laser(self.rect.centerx, self.rect.centery, "sniper")
                laser.angle = angle
                laser.speed = 25
                laser.damage = 25
                self.sniper_ammo -= 1
                all_sprites.add(laser)
                lasers.add(laser)
                laser_sound.play()
            elif self.current_weapon == "finger_gun" and self.finger_gun_ammo > 0:
                laser = Laser(self.rect.centerx, self.rect.centery, "finger_gun")
                laser.angle = angle
                laser.speed = 20
                laser.damage = 50
                self.finger_gun_ammo -= 1
                all_sprites.add(laser)
                lasers.add(laser)
                laser_sound.play()
            else:
                # Default laser
                laser = Laser(self.rect.centerx, self.rect.centery, "player")
                laser.angle = angle
                laser.speed = 12
                all_sprites.add(laser)
                lasers.add(laser)
                laser_sound.play()

class Alien(pygame.sprite.Sprite):
    def __init__(self, level, alien_type="basic"):
        super().__init__()
        self.alien_type = alien_type
        # Initialize leg angles (120 degrees apart)
        self.leg_angles = [0, 0, 0]  # All legs start at 0
        self.leg_speeds = [2, 2, 2]  # Speed of each leg's movement
        self.leg_directions = [1, 1, 1]  # 1 for forward, -1 for backward
        self.animation_timer = 0
        self.animation_delay = 2  # Lower number = faster animation
        
        # Set properties based on alien type
        if alien_type == "basic":
            self.image = create_tripod(self.leg_angles)
            self.speed = random.randint(3 + level, 6 + level)
            self.health = 2 + (level // 2)
            self.attack_delay = 120
            self.damage = 5
            self.color = (100, 100, 100)
        elif alien_type == "fast":
            self.image = create_tripod(self.leg_angles)
            self.speed = random.randint(6 + level, 9 + level)
            self.health = 1 + (level // 3)
            self.attack_delay = 180
            self.damage = 3
            self.color = (0, 255, 0)
        elif alien_type == "tank":
            self.image = create_tripod(self.leg_angles)
            self.speed = random.randint(2 + level, 4 + level)
            self.health = 4 + (level // 2)
            self.attack_delay = 90
            self.damage = 8
            self.color = (128, 128, 128)
        elif alien_type == "shooter":
            self.image = create_tripod(self.leg_angles)
            self.speed = random.randint(2 + level, 4 + level)
            self.health = 2 + (level // 3)
            self.attack_delay = 60
            self.damage = 4
            self.color = (255, 0, 0)
        
        self.rect = self.image.get_rect()
        self.rect.right = WINDOW_WIDTH + 50
        self.rect.bottom = WINDOW_HEIGHT - 20
        self.level = level
        self.attack_timer = 0
        self.lasers = pygame.sprite.Group()
        self.destroyed = False  # Add destroyed attribute
        self.destruction_timer = 0
        self.destruction_particles = []

    def update(self):
        if self.destroyed:
            self.destruction_timer += 1
            if self.destruction_timer % 2 == 0:  # Add debris every other frame
                for _ in range(12):  # Increased number of debris particles
                    debris = Debris(
                        random.randint(self.rect.left, self.rect.right),
                        random.randint(self.rect.top, self.rect.bottom),
                        self.color
                    )
                    all_sprites.add(debris)
            if self.destruction_timer >= 30:  # Kill after 30 frames of destruction
                self.kill()
            return

        self.rect.x -= self.speed
        
        # Animate legs
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            for i in range(3):
                # Update leg angle
                self.leg_angles[i] += self.leg_speeds[i] * self.leg_directions[i]
                
                # Change direction if leg reaches limits
                if self.leg_angles[i] > 15:  # Forward limit
                    self.leg_directions[i] = -1
                elif self.leg_angles[i] < -15:  # Backward limit
                    self.leg_directions[i] = 1
        
        # Update alien image with new leg angles
        self.image = create_tripod(self.leg_angles)
        
        # Attack pattern based on alien type
        self.attack_timer += 1
        if self.attack_timer >= self.attack_delay:
            self.attack_timer = 0
            if self.alien_type == "shooter":
                # Shooter aliens shoot in a spread pattern
                for angle in [-30, -15, 0, 15, 30]:
                    laser = Laser(self.rect.left, self.rect.centery, "shooter")
                    laser.speed = 8
                    laser.angle = angle
                    all_sprites.add(laser)
                    self.lasers.add(laser)
            else:
                # All aliens shoot at player
                laser = Laser(self.rect.left, self.rect.centery, "alien")
                # Calculate angle to player
                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery
                angle = math.degrees(math.atan2(dy, dx))
                laser.angle = angle
                laser.speed = 8
                all_sprites.add(laser)
                self.lasers.add(laser)
        
        if self.rect.right < 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))  # Yellow background
        
        # Create a font for the symbol
        font = pygame.font.Font(None, 36)
        
        # Define power-up types with their rarity (higher number = rarer)
        power_types = {
            "damage": 30,
            "health": 20,
            "speed": 15,
            "rpg": 10,
            "assault_rifle": 8,
            "pistol": 12,
            "sniper": 5,
            "finger_gun": 2
        }
        
        # Choose power-up type based on rarity
        total_weight = sum(power_types.values())
        random_num = random.randint(1, total_weight)
        current_sum = 0
        for power_type, weight in power_types.items():
            current_sum += weight
            if random_num <= current_sum:
                self.power_type = power_type
                break
        
        # Set symbol and color based on power-up type
        if self.power_type == "damage":
            symbol = "⚔"
            color = (255, 0, 0)  # Red
        elif self.power_type == "health":
            symbol = "❤"
            color = (0, 255, 0)  # Green
        elif self.power_type == "speed":
            symbol = "⚡"
            color = (0, 0, 255)  # Blue
        elif self.power_type == "rpg":
            symbol = "🚀"
            color = (255, 165, 0)  # Orange
        elif self.power_type == "assault_rifle":
            symbol = "🔫"
            color = (128, 128, 128)  # Gray
        elif self.power_type == "pistol":
            symbol = "🔪"
            color = (192, 192, 192)  # Silver
        elif self.power_type == "sniper":
            symbol = "🎯"
            color = (0, 255, 255)  # Cyan
        else:  # finger_gun
            symbol = "👆"
            color = (255, 192, 203)  # Pink
            
        # Render the symbol
        symbol_text = font.render(symbol, True, color)
        # Center the symbol on the power-up
        symbol_rect = symbol_text.get_rect(center=(15, 15))
        self.image.blit(symbol_text, symbol_rect)
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - 30)
        self.rect.y = random.randint(-100, -30)  # Start above the screen
        self.speed = 2
        self.rotation = 0
        self.rotation_speed = 2

    def update(self):
        # Move down
        self.rect.y += self.speed
        
        # Rotate the power-up
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation = 0
            
        # Kill if it goes off screen
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

    def apply_power_up(self, player):
        if self.power_type == "damage":
            player.power_up = True
            player.power_up_timer = 180  # 3 seconds of power-up
            player.image = pygame.transform.scale(create_player(), (60, 90))  # Bigger player
            player.damage_boost = 2  # Add 2 damage during power-up
        elif self.power_type == "health":
            player.health = min(100, player.health + 30)  # Heal 30 HP
        elif self.power_type == "speed":
            player.speed = 7  # Increased speed
            pygame.time.set_timer(pygame.USEREVENT, 5000)  # Reset after 5 seconds
            def reset_speed():
                player.speed = 5
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Clear the timer
        elif self.power_type == "rpg":
            player.current_weapon = "rpg"
            player.rpg_ammo = 5
            player.weapon_duration = 300  # 5 seconds
            player.weapon_timer = 300
        elif self.power_type == "assault_rifle":
            player.current_weapon = "assault_rifle"
            player.assault_rifle_ammo = 30
            player.weapon_duration = 300  # 5 seconds
            player.weapon_timer = 300
        elif self.power_type == "pistol":
            player.current_weapon = "pistol"
            player.pistol_ammo = 15
            player.weapon_duration = 300  # 5 seconds
            player.weapon_timer = 300
        elif self.power_type == "sniper":
            player.current_weapon = "sniper"
            player.sniper_ammo = 8
            player.weapon_duration = 300  # 5 seconds
            player.weapon_timer = 300
        elif self.power_type == "finger_gun":
            player.current_weapon = "finger_gun"
            player.finger_gun_ammo = 10
            player.weapon_duration = 300  # 5 seconds
            player.weapon_timer = 300

class BossAlien(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        # Initialize leg angles (120 degrees apart)
        self.leg_angles = [0, 0, 0]  # All legs start at 0
        self.leg_speeds = [2, 2, 2]  # Speed of each leg's movement
        self.leg_directions = [1, 1, 1]  # 1 for forward, -1 for backward
        self.animation_timer = 0
        self.animation_delay = 2  # Lower number = faster animation
        
        self.image = create_boss_tripod(self.leg_angles)
        self.rect = self.image.get_rect()
        self.rect.right = WINDOW_WIDTH + 50
        self.rect.bottom = WINDOW_HEIGHT - 20
        self.speed = 2
        self.health = 10 + (level * 5)  # More health for higher levels
        self.level = level
        self.attack_timer = 0
        self.attack_delay = 60  # Attack every second
        self.energy_balls = pygame.sprite.Group()

    def update(self):
        # Move towards player
        if self.rect.right > WINDOW_WIDTH - 100:
            self.rect.x -= self.speed
        
        # Animate legs
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            for i in range(3):
                # Update leg angle
                self.leg_angles[i] += self.leg_speeds[i] * self.leg_directions[i]
                
                # Change direction if leg reaches limits
                if self.leg_angles[i] > 15:  # Forward limit
                    self.leg_directions[i] = -1
                elif self.leg_angles[i] < -15:  # Backward limit
                    self.leg_directions[i] = 1
        
        # Update boss image with new leg angles
        self.image = create_boss_tripod(self.leg_angles)
        
        # Attack pattern
        self.attack_timer += 1
        if self.attack_timer >= self.attack_delay:
            self.attack_timer = 0
            # Create energy ball
            energy_ball = EnergyBall(self.rect.centerx, self.rect.centery)
            energy_ball.image.fill((255, 0, 255))  # Purple for boss energy balls
            all_sprites.add(energy_ball)
            self.energy_balls.add(energy_ball)
            boss_sound.play()  # Play boss sound when shooting

class EnergyBall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))  # Yellow energy ball
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 5
        self.angle = random.uniform(-30, 30)  # Random angle for spread shot

    def update(self):
        # Move in the direction of the angle
        self.rect.x -= self.speed * math.cos(math.radians(self.angle))
        self.rect.y -= self.speed * math.sin(math.radians(self.angle))
        if self.rect.right < 0 or self.rect.left > WINDOW_WIDTH or self.rect.bottom < 0:
            self.kill()

class UFO(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.Surface((40, 20))
        self.image.fill((0, 255, 255))  # Cyan color for UFO
        # Draw UFO shape
        pygame.draw.ellipse(self.image, (100, 100, 100), (0, 0, 40, 20))  # Main body
        pygame.draw.ellipse(self.image, (150, 150, 150), (5, 5, 30, 10))  # Top dome
        
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH + 50
        self.rect.y = random.randint(50, WINDOW_HEIGHT - 100)  # Random height
        self.speed = random.randint(2 + level, 4 + level)
        self.health = 1 + (level // 2)
        self.attack_delay = 90
        self.attack_timer = 0
        self.lasers = pygame.sprite.Group()
        self.level = level
        self.color = (0, 255, 255)  # Add color attribute for explosion effects
        self.destroyed = False
        self.destruction_timer = 0

    def update(self):
        if self.destroyed:
            self.destruction_timer += 1
            if self.destruction_timer % 2 == 0:  # Add debris every other frame
                for _ in range(12):  # More debris for UFOs
                    debris = Debris(
                        random.randint(self.rect.left, self.rect.right),
                        random.randint(self.rect.top, self.rect.bottom),
                        self.color
                    )
                    all_sprites.add(debris)
            return

        self.rect.x -= self.speed
        
        # Move up and down in a wave pattern
        self.rect.y += math.sin(pygame.time.get_ticks() * 0.005) * 2
        
        # Attack pattern - shoot at buildings
        self.attack_timer += 1
        if self.attack_timer >= self.attack_delay:
            self.attack_timer = 0
            # Find closest building
            closest_building = None
            closest_distance = float('inf')
            
            for building in buildings:
                if not building.destroyed:
                    distance = math.sqrt((building.rect.centerx - self.rect.centerx)**2 + 
                                      (building.rect.centery - self.rect.centery)**2)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_building = building
            
            if closest_building:
                # Shoot at building
                laser = Laser(self.rect.left, self.rect.centery, "ufo")
                # Calculate angle to building
                dx = closest_building.rect.centerx - self.rect.centerx
                dy = closest_building.rect.centery - self.rect.centery
                angle = math.degrees(math.atan2(dy, dx))
                laser.angle = angle
                laser.speed = 8
                all_sprites.add(laser)
                self.lasers.add(laser)
                ufo_sound.play()  # Play UFO sound when shooting
        
        if self.rect.right < 0:
            self.kill()

class Building(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 120))
        self.image.fill((100, 100, 100))  # Gray building
        # Add windows
        for i in range(3):
            for j in range(4):
                pygame.draw.rect(self.image, (255, 255, 0), (10 + i*15, 20 + j*25, 10, 15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = WINDOW_HEIGHT - 20
        self.health = 100
        self.destroyed = False
        self.on_fire = False
        self.fire_animation_timer = 0
        self.fire_particles = []
        self.original_image = self.image.copy()
        self.destruction_timer = 0
        self.destruction_particles = []
        self.fall_angle = 0  # Angle for falling animation
        self.fall_speed = 0  # Speed of falling
        self.fall_direction = random.choice([-1, 1])  # Random direction to fall

    def update(self):
        if self.on_fire:
            self.fire_animation_timer += 1
            self.image = self.original_image.copy()
            
            # Add fire particles
            if self.fire_animation_timer % 2 == 0:
                for _ in range(3):
                    particle = {
                        'x': random.randint(0, 60),
                        'y': random.randint(0, 120),
                        'speed': random.randint(2, 5),
                        'life': 20
                    }
                    self.fire_particles.append(particle)
            
            # Update and draw fire particles
            for particle in self.fire_particles[:]:
                particle['y'] -= particle['speed']
                particle['life'] -= 1
                
                # Draw fire particle
                color = (255, random.randint(100, 200), 0)
                pygame.draw.circle(self.image, color, 
                                 (int(particle['x']), int(particle['y'])), 2)
                
                if particle['life'] <= 0:
                    self.fire_particles.remove(particle)
            
            # Add fire glow effect
            glow_surface = pygame.Surface((60, 120), pygame.SRCALPHA)
            glow_color = (255, 100, 0, 30)
            pygame.draw.rect(glow_surface, glow_color, (0, 0, 60, 120))
            self.image.blit(glow_surface, (0, 0))

        if self.destroyed:
            self.destruction_timer += 1
            
            # Update falling animation
            if self.fall_angle < 90:  # Only fall up to 90 degrees
                self.fall_angle += 2
                self.fall_speed += 0.5  # Accelerate falling
                
                # Rotate the building
                self.image = pygame.transform.rotate(self.original_image, self.fall_angle * self.fall_direction)
                self.rect = self.image.get_rect(center=self.rect.center)
                
                # Move the building down and sideways
                self.rect.y += self.fall_speed
                self.rect.x += self.fall_direction * (self.fall_speed * 0.5)
            
            # Add debris particles
            if self.destruction_timer % 2 == 0:
                for _ in range(5):
                    debris = Debris(
                        random.randint(self.rect.left, self.rect.right),
                        random.randint(self.rect.top, self.rect.bottom),
                        (100, 100, 100)  # Gray debris
                    )
                    all_sprites.add(debris)
            
            # Kill the building after it falls off screen
            if self.rect.top > WINDOW_HEIGHT + 100:
                self.kill()

# Modify the Debris class for better explosion effects
class Debris(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        # Random size for debris
        size = random.randint(3, 6)
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        # More varied speeds for better explosion effect
        self.speed_x = random.randint(-8, 8)
        self.speed_y = random.randint(-8, 8)
        self.gravity = 0.2
        self.life = random.randint(45, 75)  # Varied lifetime
        self.velocity_y = 0
        self.rotation = random.randint(0, 360)
        self.rotation_speed = random.randint(-5, 5)
        self.alpha = 255  # Add alpha for fade effect

    def update(self):
        self.rect.x += self.speed_x
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        self.rotation += self.rotation_speed
        self.life -= 1
        
        # Fade out effect
        if self.life < 20:  # Start fading in last 20 frames
            self.alpha = int((self.life / 20) * 255)
            self.image.set_alpha(self.alpha)
            
        if self.life <= 0:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
lasers = pygame.sprite.Group()
buildings = pygame.sprite.Group()
player = Player()  # Create player but don't add to all_sprites yet
boss = None  # Will be set when boss appears

# Create initial buildings
for i in range(5):
    building = Building(100 + i*150, WINDOW_HEIGHT - 20)
    all_sprites.add(building)
    buildings.add(building)

# Add player last so it's drawn on top
all_sprites.add(player)

# Game variables
clock = pygame.time.Clock()
spawn_timer = 0
power_up_timer = 0
running = True
game_over = False
level_complete = False
level_complete_timer = 0

def reset_game():
    global player, aliens, power_ups, lasers, all_sprites, spawn_timer, power_up_timer, level_complete, boss, buildings
    # Clear all sprite groups
    aliens.empty()
    power_ups.empty()
    lasers.empty()
    buildings.empty()
    all_sprites.empty()
    
    # Reset player and boss
    player = Player()
    player.health = 100
    player.last_health = 100
    boss = None
    
    # Create new buildings
    for i in range(5):
        building = Building(100 + i*150, WINDOW_HEIGHT - 20)
        all_sprites.add(building)
        buildings.add(building)
    
    # Add player last so it's drawn on top
    all_sprites.add(player)
    
    # Reset timers and flags
    spawn_timer = 0
    power_up_timer = 0
    level_complete = False

def advance_level():
    global player, level_complete, level_complete_timer
    player.level += 1
    player.aliens_defeated = 0
    player.aliens_needed = 5 + (player.level - 1)  # More aliens needed per level
    player.health = min(100, player.health + 20)  # Heal a bit when advancing
    level_complete = True
    level_complete_timer = 60  # Show level complete message for 1 second

def get_alien_type(level):
    # Define spawn chances based on level
    if level < 3:
        return random.choice(["basic", "ufo"])
    elif level < 5:
        return random.choice(["basic", "fast", "ufo"])
    elif level < 7:
        return random.choice(["basic", "fast", "tank", "ufo"])
    else:
        return random.choice(["basic", "fast", "tank", "shooter", "ufo"])

# Game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over and not level_complete:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_x:  # Shoot with X key
                    player.shoot()
            elif event.key == pygame.K_r:  # Reset game with R key
                game_over = False
                reset_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over and not level_complete:
                if event.button == 1:  # Left click
                    player.shoot()

    if not game_over and not level_complete:
        # Update
        all_sprites.update()
        
        # Spawn boss when close to completing level
        if player.aliens_defeated >= player.aliens_needed - 1 and boss is None:
            boss = BossAlien(player.level)
            all_sprites.add(boss)
        
        # Spawn regular aliens (faster spawn rate with higher levels)
        spawn_timer += 1
        spawn_delay = max(20, 60 - (player.level * 3))  # Faster spawns per level
        if spawn_timer >= spawn_delay and boss is None:  # Don't spawn regular aliens during boss fight
            alien_type = get_alien_type(player.level)
            if alien_type == "ufo":
                new_alien = UFO(player.level)
            else:
                new_alien = Alien(player.level, alien_type)
            all_sprites.add(new_alien)
            aliens.add(new_alien)
            spawn_timer = 0
        
        # Spawn power-ups
        power_up_timer += 1
        if power_up_timer >= 300:  # Every 5 seconds
            new_power_up = PowerUp()
            all_sprites.add(new_power_up)
            power_ups.add(new_power_up)
            power_up_timer = 0
        
        # Check laser collisions with aliens and boss
        laser_hits = pygame.sprite.groupcollide(lasers, aliens, True, False)
        for laser, alien_list in laser_hits.items():
            for alien in alien_list:
                total_damage = player.damage + player.damage_boost
                alien.health -= total_damage
                if alien.health <= 0:
                    alien.destroyed = True  # Set destroyed flag instead of killing immediately
                    player.score += 1
                    player.aliens_defeated += 1
                    power_up_sound.play()
                    # Create explosion effect with more debris
                    for _ in range(20):  # Increased number of debris particles
                        debris = Debris(
                            random.randint(alien.rect.left, alien.rect.right),
                            random.randint(alien.rect.top, alien.rect.bottom),
                            alien.color
                        )
                        all_sprites.add(debris)
        
        # Check laser collisions with boss
        if boss and boss.health > 0:  # Add check for boss existence and health
            laser_hits = pygame.sprite.spritecollide(boss, lasers, True)
            for laser in laser_hits:
                total_damage = player.damage + player.damage_boost
                boss.health -= total_damage
                if boss.health <= 0:
                    boss.kill()
                    boss = None
                    player.score += 5  # Bonus points for defeating boss
                    player.aliens_defeated += 1
                    power_up_sound.play()
                    advance_level()
        
        # Check energy ball collisions with player
        if boss:
            energy_hits = pygame.sprite.spritecollide(player, boss.energy_balls, True)
            for hit in energy_hits:
                if not player.power_up:
                    player.health -= 5  # Reduced from 15 to 5
                    if player.health <= 0:
                        game_over = True
            
            # Check direct collision with boss
            if pygame.sprite.collide_rect(player, boss):
                if not player.power_up:
                    player.health -= 8  # Reduced from 20 to 8
                    if player.health <= 0:
                        game_over = True
        
        # Check power-up collisions
        power_hits = pygame.sprite.spritecollide(player, power_ups, True)
        for hit in power_hits:
            hit.apply_power_up(player)
            power_up_sound.play()
        
        # Check alien laser collisions with player
        for alien in aliens:
            laser_hits = pygame.sprite.spritecollide(player, alien.lasers, True)
            for hit in laser_hits:
                if not player.power_up:
                    player.health -= 2  # Reduced from 5 to 2
                    if player.health <= 0:
                        game_over = True
        
        # Check direct collisions between player and aliens
        alien_collisions = pygame.sprite.spritecollide(player, aliens, False)
        for alien in alien_collisions:
            if not player.power_up:
                # Reduced damage from tripod collisions
                player.health -= 1  # Reduced from 2 to 1
                if player.health <= 0:
                    game_over = True
        
        # Check UFO laser collisions with buildings
        for ufo in aliens:
            if isinstance(ufo, UFO):
                laser_hits = pygame.sprite.groupcollide(ufo.lasers, buildings, True, False)
                for laser, building_list in laser_hits.items():
                    for building in building_list:
                        if not building.destroyed:
                            building.health -= 10
                            building.on_fire = True
                            if building.health <= 0:
                                building.destroyed = True
                                building.image.fill((50, 50, 50))
                                player.score += 5
                                # Create initial explosion effect
                                for _ in range(20):
                                    debris = Debris(
                                        random.randint(building.rect.left, building.rect.right),
                                        random.randint(building.rect.top, building.rect.bottom),
                                        (100, 100, 100)
                                    )
                                    all_sprites.add(debris)
                                # Make building start falling immediately
                                building.fall_angle = 0
                                building.fall_speed = 0
                                building.fall_direction = random.choice([-1, 1])
        
        player.last_health = player.health
    
    elif level_complete:
        level_complete_timer -= 1
        if level_complete_timer <= 0:
            level_complete = False
    
    # Draw everything
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, GREEN, (0, WINDOW_HEIGHT - 20, WINDOW_WIDTH, 20))
    all_sprites.draw(screen)
    
    # Draw health bar
    pygame.draw.rect(screen, RED, (10, 10, 100, 20))
    pygame.draw.rect(screen, GREEN, (10, 10, player.health, 20))
    
    # Draw boss health if boss exists
    if boss:
        boss_health_width = (boss.health / (10 + (player.level * 5))) * 200
        pygame.draw.rect(screen, RED, (WINDOW_WIDTH//2 - 100, 10, 200, 20))
        pygame.draw.rect(screen, (255, 0, 255), (WINDOW_WIDTH//2 - 100, 10, boss_health_width, 20))
        boss_text = font.render('BOSS', True, WHITE)
        screen.blit(boss_text, (WINDOW_WIDTH//2 - 30, 15))
    
    # Draw score and level info
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {player.score}', True, BLACK)
    screen.blit(score_text, (WINDOW_WIDTH - 120, 10))
    
    # Draw level info
    level_text = font.render(f'Level: {player.level}', True, BLACK)
    screen.blit(level_text, (10, 40))
    
    # Draw aliens defeated progress
    progress_text = font.render(f'Aliens: {player.aliens_defeated}/{player.aliens_needed}', True, BLACK)
    screen.blit(progress_text, (WINDOW_WIDTH - 200, 40))
    
    # Draw power-up status and damage info
    if player.power_up:
        power_text = font.render('POWER UP!', True, (255, 255, 0))
        screen.blit(power_text, (WINDOW_WIDTH // 2 - 60, 10))
        damage_text = font.render(f'Damage: {player.damage + player.damage_boost}', True, (255, 0, 0))
        screen.blit(damage_text, (WINDOW_WIDTH // 2 - 60, 40))
    
    # Draw weapon info
    if player.current_weapon != "laser":
        weapon_text = font.render(f'{player.current_weapon.upper()}: ', True, WHITE)
        screen.blit(weapon_text, (WINDOW_WIDTH - 200, 70))
        
        if player.current_weapon == "rpg":
            ammo_text = font.render(f'{player.rpg_ammo}', True, (255, 165, 0))
        elif player.current_weapon == "assault_rifle":
            ammo_text = font.render(f'{player.assault_rifle_ammo}', True, (128, 128, 128))
        elif player.current_weapon == "pistol":
            ammo_text = font.render(f'{player.pistol_ammo}', True, (192, 192, 192))
        elif player.current_weapon == "sniper":
            ammo_text = font.render(f'{player.sniper_ammo}', True, (0, 255, 255))
        else:  # finger_gun
            ammo_text = font.render(f'{player.finger_gun_ammo}', True, (255, 192, 203))
            
        screen.blit(ammo_text, (WINDOW_WIDTH - 100, 70))
    
    # Draw level complete screen
    if level_complete:
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw level complete text
        level_complete_font = pygame.font.Font(None, 74)
        level_complete_text = level_complete_font.render(f'LEVEL {player.level} COMPLETE!', True, YELLOW)
        screen.blit(level_complete_text, (WINDOW_WIDTH//2 - level_complete_text.get_width()//2, WINDOW_HEIGHT//2))
    
    # Draw game over screen
    elif game_over:
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw game over text
        game_over_font = pygame.font.Font(None, 74)
        game_over_text = game_over_font.render('GAME OVER', True, RED)
        screen.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, WINDOW_HEIGHT//2 - 50))
        
        # Draw final score and level
        final_score_text = font.render(f'Final Score: {player.score}', True, WHITE)
        screen.blit(final_score_text, (WINDOW_WIDTH//2 - final_score_text.get_width()//2, WINDOW_HEIGHT//2 + 10))
        
        final_level_text = font.render(f'Level Reached: {player.level}', True, WHITE)
        screen.blit(final_level_text, (WINDOW_WIDTH//2 - final_level_text.get_width()//2, WINDOW_HEIGHT//2 + 50))
        
        # Draw restart instructions
        restart_text = font.render('Press R to Restart', True, WHITE)
        screen.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, WINDOW_HEIGHT//2 + 100))
    
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

pygame.quit()