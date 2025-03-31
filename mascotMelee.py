import pygame
import time
import sys


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0



gravity = 800
jump_strength = -500  # Jumping velocity

heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (50, 50))  # Adjust size if needed

character_options = [
    {
        "image": pygame.image.load("player1_resized.png"),
        "size": (60, 120)  # Width, height for in-game use
    },
    {
        "image": pygame.image.load("player2_resized.gif"),
        "size": (45, 90)
    },
    # Add more if needed
]


def push_off_field_layout(sw, sh):
    return [pygame.Rect(0, int(sh * 0.78), sw, 20)]

def classic_arena_layout(sw, sh):
    return [pygame.Rect(int(sw * 0.25), int(sh * 0.56), int(sw * 0.48), 20)]

maps = [
    {
        "name": "The Field",
        "background": "background.jpg",
        "get_platforms": push_off_field_layout,
        "platform_image": None
    },
    {
        "name": "Final Destination",
        "background": "Final-Destination-Stage3.jpg",
        "get_platforms": classic_arena_layout,
        "platform_image": None
    }
]


player1_image = pygame.image.load('player1.png')
player2_image = pygame.image.load('player2.1.gif')

# Resize images


player1_image = pygame.transform.scale(player1_image, (60, 120))  # Resize to 50x100 pixels
player2_image = pygame.transform.scale(player2_image, (60, 120))  # Resize to 50x100 pixels
#background_image = pygame.transform.scale(background_image, (1280, 720))

character_options = [player1_image, player2_image]

def show_start_screen():
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    start_screen = True
    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                start_screen = False

        screen.fill((0, 0, 0))  # Fill the screen with black
        font = pygame.font.Font(None, 74)
        text = font.render("Press any key to start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(60)

def character_select():
    selected1 = False
    selected2 = False
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    cols = len(character_options)
    rows = 1
    box_width = int(screen_width * 0.12)
    box_height = int(screen_height * 0.30)
    box_spacing = int(screen_width * 0.04)
    start_x = int((screen_width - (cols * (box_width + box_spacing) - box_spacing)) // 2)
    start_y = int(screen_height * 0.4)

    # Each player's cursor position (index in list/grid)
    p1_pos = 0
    p2_pos = cols - 1

    font = pygame.font.Font(None, int(screen_height * 0.06))

    while not (selected1 and selected2):
        screen.fill((50, 50, 50))
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        for i in range(len(character_options)):
            x = start_x + i * (box_width + box_spacing)
            y = start_y

            # Draw character box
            pygame.draw.rect(screen, (200, 200, 200), (x, y, box_width, box_height), 3)

            # Highlight for Player 1
            if i == p1_pos and not selected1:
                pygame.draw.rect(screen, (255, 0, 0), (x - 4, y - 4, box_width + 8, box_height + 8), 4)

            # Highlight for Player 2
            if i == p2_pos and not selected2:
                pygame.draw.rect(screen, (0, 0, 255), (x - 4, y - 4, box_width + 8, box_height + 8), 4)

            # Draw the character sprite
            img = pygame.transform.scale(character_options[i], (box_width - 20, box_height - 20))
            screen.blit(img, (x + 10, y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                # Player 1 movement
                if not selected1:
                    if event.key == pygame.K_a:
                        p1_pos = (p1_pos - 1) % cols
                    elif event.key == pygame.K_d:
                        p1_pos = (p1_pos + 1) % cols
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        selected1 = True

                # Player 2 movement
                if not selected2:
                    if event.key == pygame.K_LEFT:
                        p2_pos = (p2_pos - 1) % cols
                    elif event.key == pygame.K_RIGHT:
                        p2_pos = (p2_pos + 1) % cols
                    elif event.key in (pygame.K_8, pygame.K_9, pygame.K_0):
                        selected2 = True

        clock.tick(60)

    return character_options[p1_pos], character_options[p2_pos]

class Projectile:
    def __init__(self, x, y, speed, color):
        self.rect = pygame.Rect(x, y, 20, 10)  # Small rectangle projectile
        self.speed = speed  # Speed in pixels per frame
        self.color = color  # Color of projectile

    def move(self):
        self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


def map_select():
    selected = 0
    choosing = True

    

    while choosing:
        screen_width = screen.get_width()
        screen_height = screen.get_height()


        screen.fill((30, 30, 30))
        font = pygame.font.Font(None, 60)
        title = font.render("Choose Your Map", True, (255, 255, 255))
        screen.blit(title, (int(screen_width * 0.38), int(screen_height * 0.07)))

        for i, m in enumerate(maps):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            label = font.render(m["name"], True, color)
            screen.blit(label, (int(screen_width * 0.4), int(screen_height * 0.28 + i * screen_height * 0.14)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(maps)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(maps)
                elif event.key == pygame.K_RETURN:
                    choosing = False

        pygame.display.flip()
        clock.tick(60)

    return maps[selected]


class Player:
    def __init__(self, x, y, image):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.image = image
        self.on_ground = False
        self.lives = 3
        self.rect = pygame.Rect(x - 20, y - 40, 40, 80)  # Rectangle hitbox
        self.facing_right = True
        self.attack_cooldown = 0.5  # Cooldown in seconds
        self.last_attack_time = 0   # Timestamp of last attack
        self.attack_mode = "melee"  # Default attack mode
        self.is_shielding = False  # Track shield status

    def move(self, keys, left_key, right_key, jump_key, melee_key, shield_key, projectile_key):
        # Handle attack mode switching
        if keys[melee_key]:
           self.attack_mode = "melee"
        if keys[shield_key]:
            self.attack_mode = "shield"
        if keys[projectile_key]:
            self.attack_mode = "projectile"

        # Prevent only horizontal movement while shielding, but allow falling
        if self.attack_mode == "shield" and self.is_shielding:
            self.rect.topleft = (self.pos.x - 20, self.pos.y - 40)
            return  

        # 🔹 Counteract knockback by allowing movement to override it
        move_speed = 300 * dt

        if keys[left_key]:
            if self.velocity.x > 0:  # 🔹 If moving left while knocked right, reduce knockback
                self.velocity.x -= move_speed
            else:
                self.pos.x -= move_speed
                self.facing_right = False

        if keys[right_key]:
            if self.velocity.x < 0:  # 🔹 If moving right while knocked left, reduce knockback
                self.velocity.x += move_speed
            else:
                self.pos.x += move_speed
                self.facing_right = True

        if keys[jump_key] and self.velocity.y == 0:
            self.velocity.y = jump_strength

        # Always update rect position
        self.rect.topleft = (self.pos.x - 20, self.pos.y - 40)

    
    def apply_gravity(self):
        """Applies gravity and friction to stop infinite knockback."""
        self.velocity.y += gravity * dt  # ✅ Apply gravity normally

        # 🔹 Apply friction to slow down horizontal movement
        friction = 0.97  # Adjust to fine-tune stopping speed
        self.velocity.x *= friction  # ✅ This gradually reduces velocity

        # Move the player based on velocity
        self.pos += self.velocity * dt  


    def check_collision(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                self.on_ground = True
                self.velocity.y = 0
                self.pos.y = platform.top - 40
                self.rect.topleft = (self.pos.x - 20, self.pos.y - 40)
                break
        if self.on_ground:
            self.velocity.y = 0

    def check_player_collision(self, other):
        if self.rect.colliderect(other.rect):
            overlap_x = min(self.rect.right - other.rect.left, other.rect.right - self.rect.left)
            overlap_y = min(self.rect.bottom - other.rect.top, other.rect.bottom - self.rect.top)
            if overlap_x < overlap_y:
                if self.pos.x < other.pos.x:
                    self.pos.x -= overlap_x / 2
                    other.pos.x += overlap_x / 2
                else:
                    self.pos.x += overlap_x / 2
                    other.pos.x -= overlap_x / 2
            else:
                if self.pos.y < other.pos.y:
                    self.pos.y -= overlap_y / 2
                    other.pos.y += overlap_y / 2
                else:
                    self.pos.y += overlap_y / 2
                    other.pos.y -= overlap_y / 2
            self.rect.topleft = (self.pos.x - 20, self.pos.y - 40)
            other.rect.topleft = (other.pos.x - 20, other.pos.y - 40)

    def check_off_screen(self, screen_width, screen_height):
        if self.pos.x < 0 or self.pos.x > screen_width or self.pos.y > screen_height:
            self.lives -= 1
            self.pos = pygame.Vector2(screen_width / 2, screen_height / 2)
            self.velocity = pygame.Vector2(0, 0)
            self.rect.topleft = (self.pos.x - 20, self.pos.y - 40)

    def apply_knockback(self, direction, strength):
        self.velocity += direction * strength

    def draw(self, screen):
        if self.is_shielding:
            # 🔹 Draw a faint blue circle around the player
            shield_color = (0, 0, 255, 100)  # RGBA (Blue with transparency)
            shield_surface = pygame.Surface((self.rect.width * 2, self.rect.height * 2), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, shield_color, (self.rect.width, self.rect.height), self.rect.width)
            screen.blit(shield_surface, (self.rect.centerx - self.rect.width, self.rect.centery - self.rect.height))


        if self.facing_right:
            screen.blit(self.image, self.rect.topleft)
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect.topleft)

def show_winner_screen(winner):
    """Display the winner screen and wait for player input to restart or quit."""
    screen.fill((0, 0, 0))  # Black background
    font = pygame.font.Font(None, 74)
    text = font.render(f"{winner} Wins!", True, (255, 255, 255))
    screen.blit(text, (screen.get_width() // 2 - 150, screen.get_height() // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False  # Restart the game

while True:
    # Show the start screen
    show_start_screen()

    player1_img, player2_img = character_select()


    selected_map = map_select()

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Load background
    background_image = pygame.image.load(selected_map["background"])
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Load platform image if needed
    platform_image = None
    if selected_map["platform_image"]:
        platform_image = pygame.image.load(selected_map["platform_image"])

    
    platforms = selected_map["get_platforms"](screen_width, screen_height)


    projectiles = []

    # Create players with selected images
    player1 = Player(screen.get_width() / 2, screen.get_height() / 2, player1_img)
    player2 = Player(screen.get_width() / 3, screen.get_height() / 2, player2_img)

    # Font setup for displaying lives
    font = pygame.font.Font(None, 36)

    running = True


    previous_time = time.time()
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        # Update game state and draw everything here

        pygame.display.flip()
        # Calculate delta time
        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time

        # Draw background
        screen.blit(background_image, (0, 0))


        # Draw platforms
        for platform in platforms:
            if platform_image:
                img = pygame.transform.scale(platform_image, (platform.width, platform.height))
                screen.blit(img, (platform.x, platform.y))
            else:
                # Optional: draw invisible platforms for debugging
                # pygame.draw.rect(screen, (255, 0, 0), platform, 2)
                pass

        # Get key states
        keys = pygame.key.get_pressed()

        # Move players
        player1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_1, pygame.K_2, pygame.K_3)
        player2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_8, pygame.K_9, pygame.K_0)


        # Apply gravity
        player1.apply_gravity()
        player2.apply_gravity()

        # Check for platform collisions
        player1.check_collision(platforms)
        player2.check_collision(platforms)

        # Check for player collisions
        player1.check_player_collision(player2)
        player2.check_player_collision(player1)

        # Check if players go off screen
        player1.check_off_screen(screen.get_width(), screen.get_height())
        player2.check_off_screen(screen.get_width(), screen.get_height())

            # Attack mechanics
        # Player 1 Attack Logic
        if keys[pygame.K_1]:  
            if player1.attack_mode == "melee" and (current_time - player1.last_attack_time) >= player1.attack_cooldown:
                player1.last_attack_time = current_time
                attack_box1 = pygame.Rect(player1.pos.x + (30 if player1.facing_right else -30), player1.pos.y - 20, 40, 40)
                pygame.draw.rect(screen, "blue", attack_box1)  # Debugging display
                if attack_box1.colliderect(player2.rect) and not player2.is_shielding:
                    direction = pygame.Vector2(1, 0) if player1.facing_right else pygame.Vector2(-1, 0)
                    player2.apply_knockback(direction, 1000)

        elif keys[pygame.K_2]:
            player1.is_shielding = True  # Activate shield while button is held

        elif keys[pygame.K_3] and (current_time - player1.last_attack_time) >= player1.attack_cooldown:
            player1.last_attack_time = current_time  # Reset cooldown
            
            # Determine the projectile's starting position (offset in front of player)
            offset_x = 40 if player1.facing_right else -40  
            projectile_speed = 7 if player1.facing_right else -7  
            
            projectiles.append(Projectile(player1.rect.centerx + offset_x, player1.rect.centery, projectile_speed, "blue"))  # Now starts in front of player
        else:
            player1.is_shielding = False  # Deactivate shield when attack key is released

        # Player 2 Attack Logic
        if keys[pygame.K_8]:  
            if player2.attack_mode == "melee" and (current_time - player2.last_attack_time) >= player2.attack_cooldown:
                player2.last_attack_time = current_time
                attack_box2 = pygame.Rect(player2.pos.x + (30 if player2.facing_right else -30), player2.pos.y - 20, 40, 40)
                pygame.draw.rect(screen, "green", attack_box2)
                if attack_box2.colliderect(player1.rect) and not player1.is_shielding:
                    direction = pygame.Vector2(1, 0) if player2.facing_right else pygame.Vector2(-1, 0)
                    player1.apply_knockback(direction, 1200)

        elif keys[pygame.K_9]:
            player2.is_shielding = True

        elif keys[pygame.K_0] and (current_time - player2.last_attack_time) >= player2.attack_cooldown:
            player2.last_attack_time = current_time
            
            offset_x = 40 if player2.facing_right else -40  
            projectile_speed = 7 if player2.facing_right else -7  
            
            projectiles.append(Projectile(player2.rect.centerx + offset_x, player2.rect.centery, projectile_speed, "green"))
        else:
            player2.is_shielding = False  # Deactivate shield when attack key is released



        for projectile in projectiles[:]:  # Iterate over a copy to allow removal
            projectile.move()
            projectile.draw(screen)

            # 🔹 Check for collisions with Player 1
            if projectile.rect.colliderect(player1.rect) and not player1.is_shielding:
                knockback_force = 400  # 🔹 Weaker than melee attack
                direction = pygame.Vector2(1, 0) if projectile.speed > 0 else pygame.Vector2(-1, 0)
                player1.apply_knockback(direction, knockback_force)  # 🔹 Apply knockback once
                projectiles.remove(projectile)  # 🔹 Remove projectile after impact
                continue  # Prevent further checks on this projectile

            # 🔹 Check for collisions with Player 2
            if projectile.rect.colliderect(player2.rect) and not player2.is_shielding:
                knockback_force = 400  # 🔹 Weaker than melee attack
                direction = pygame.Vector2(1, 0) if projectile.speed > 0 else pygame.Vector2(-1, 0)
                player2.apply_knockback(direction, knockback_force)  # 🔹 Apply knockback once
                projectiles.remove(projectile)  # 🔹 Remove projectile after impact
                continue

            # 🔹 Remove projectile if it goes off-screen
            if projectile.rect.x < 0 or projectile.rect.x > screen.get_width():
                projectiles.remove(projectile)




                
        # Draw players
        player1.draw(screen)
        player2.draw(screen)

        # Player 1 hearts (bottom-left)
        for i in range(player1.lives):
            screen.blit(heart_image, (20 + i * 50, screen.get_height() - 60))

        # Player 2 hearts (bottom-right)
        for i in range(player2.lives):
            screen.blit(heart_image, (screen.get_width() - 160 + i * 50, screen.get_height() - 60))

        # Update display and tick clock
        pygame.display.flip()
        dt = clock.tick(60) / 1000

        if player1.lives <= 0:
            show_winner_screen("Player 2")
            running = False  # Stop the game loop

        if player2.lives <= 0:
            show_winner_screen("Player 1")
            running = False  # Stop the game loop


#pygame.quit()

