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

# Load or generate sound effects
try:
    jump_sound = pygame.mixer.Sound('assets/jump.wav')
    power_up_sound = pygame.mixer.Sound('assets/power_up.wav')
    hit_sound = pygame.mixer.Sound('assets/hit.wav')
    laser_sound = pygame.mixer.Sound('assets/laser.wav')
except:
    jump_sound = generate_jump_sound()
    power_up_sound = generate_power_up_sound()
    hit_sound = generate_hit_sound()
    laser_sound = generate_laser_sound()

# Set volume for sound effects
jump_sound.set_volume(0.3)
power_up_sound.set_volume(0.4)
hit_sound.set_volume(0.3)
laser_sound.set_volume(0.2)

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
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WINDOW_WIDTH:
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
        self.damage = 1  # Base damage
        self.damage_boost = 0  # Additional damage from power-ups

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
                self.damage_boost = 0  # Reset damage boost when power-up ends

    def jump(self):
        if not self.jumping:
            self.velocity_y = self.jump_power
            self.jumping = True
            jump_sound.play()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            laser = Laser(self.rect.right, self.rect.centery)
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

    def update(self):
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
                    laser = Laser(self.rect.left, self.rect.centery)
                    laser.speed = 8
                    laser.angle = angle
                    all_sprites.add(laser)
                    self.lasers.add(laser)
                    laser_sound.play()
            else:
                # Other aliens shoot single lasers
                laser = Laser(self.rect.left, self.rect.centery)
                all_sprites.add(laser)
                self.lasers.add(laser)
                laser_sound.play()
        
        if self.rect.right < 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))  # Yellow power-up
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - 30)
        self.rect.y = random.randint(100, WINDOW_HEIGHT - 100)
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

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
            all_sprites.add(energy_ball)
            self.energy_balls.add(energy_ball)

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

# Create sprite groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
lasers = pygame.sprite.Group()
boss = None  # Will be set when boss appears
player = Player()
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
    global player, aliens, power_ups, lasers, all_sprites, spawn_timer, power_up_timer, level_complete, boss
    # Clear all sprite groups
    aliens.empty()
    power_ups.empty()
    lasers.empty()
    all_sprites.empty()
    
    # Reset player and boss
    player = Player()
    boss = None
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
        return "basic"
    elif level < 5:
        return random.choice(["basic", "fast"])
    elif level < 7:
        return random.choice(["basic", "fast", "tank"])
    else:
        return random.choice(["basic", "fast", "tank", "shooter"])

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
                    alien.kill()
                    player.score += 1
                    player.aliens_defeated += 1
                    power_up_sound.play()
        
        # Check laser collisions with boss
        if boss:
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
                    player.health -= 15  # More damage from boss attacks
                    if player.health <= 0:
                        game_over = True
            
            # Check direct collision with boss
            if pygame.sprite.collide_rect(player, boss):
                if not player.power_up:
                    player.health -= 20  # Even more damage from direct boss collision
                    if player.health <= 0:
                        game_over = True
                    # Bounce player back more forcefully
                    if player.rect.centerx < boss.rect.centerx:
                        player.rect.right = boss.rect.left - 10
                    else:
                        player.rect.left = boss.rect.right + 10
        
        # Check power-up collisions
        power_hits = pygame.sprite.spritecollide(player, power_ups, True)
        for hit in power_hits:
            player.power_up = True
            player.power_up_timer = 180  # 3 seconds of power-up
            player.image = pygame.transform.scale(create_player(), (60, 90))  # Bigger player
            player.damage_boost = 2  # Add 2 damage during power-up
            power_up_sound.play()
        
        # Check alien laser collisions with player
        for alien in aliens:
            laser_hits = pygame.sprite.spritecollide(player, alien.lasers, True)
            for hit in laser_hits:
                if not player.power_up:
                    player.health -= 5  # Less damage from regular aliens
                    if player.health <= 0:
                        game_over = True
        
        # Check direct collisions between player and aliens
        alien_collisions = pygame.sprite.spritecollide(player, aliens, False)
        for alien in alien_collisions:
            if not player.power_up:
                player.health -= 10  # More damage from direct collision
                if player.health <= 0:
                    game_over = True
                # Bounce player back slightly
                if player.rect.centerx < alien.rect.centerx:
                    player.rect.right = alien.rect.left
                else:
                    player.rect.left = alien.rect.right
        
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
    clock.tick(60)

pygame.quit()