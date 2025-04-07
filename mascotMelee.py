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

heart_image = pygame.image.load("img/heart.png")
heart_image = pygame.transform.scale(heart_image, (50, 50))  # Adjust size if needed
smash_font = pygame.font.Font("img/super_smash_4_1_by_pokemon_diamond-d7zxu6d.ttf", 36)
tag_font = pygame.font.Font("img/df-gothic-eb.ttf", 18)  # adjust size as needed
melee_effect_img = pygame.image.load("img/attack.png").convert_alpha()




character_options = [
    {
        "name": "Smokey",
        "select_image": pygame.image.load("img/player1.png"),
        "game_image": pygame.transform.scale(pygame.image.load("img/player1.png"), (68, 130)),
        "size": (60, 120)
    },
    {
        "name": "Hairy Dawg",
        "select_image": pygame.image.load("img/player2.1.gif"),
        "game_image": pygame.transform.scale(pygame.image.load("img/player2.1.gif"), (65, 125)),
        "size": (45, 90)
    },
    {
        "name": "Big Al",
        "select_image": pygame.image.load("img/big_al.png"),
        "game_image": pygame.transform.scale(pygame.image.load("img/big_al.png"), (90, 130)),  # adjust size as needed
        "size": (90, 130)
    },
    {
        "name": "Albert",
        "select_image": pygame.image.load("img/Albert_gator.png"),
        "game_image": pygame.transform.scale(pygame.image.load("img/Albert_gator.png"), (70, 130)),  # adjust size as needed
        "size": (70, 130)
    }

    # Add more if needed!
]



def push_off_field_layout(sw, sh):
    return [pygame.Rect(0, int(sh * 0.78), sw, 20)]
def classic_arena_layout(sw, sh):
    return [pygame.Rect(int(sw * 0.25), int(sh * 0.6), int(sw * 0.48), 20)]

maps = [
    {
        "name": "The Field",
        "background": "img/background.jpg",
        "get_platforms": push_off_field_layout,
        "platform_image": None
    },
    {
        "name": "Final Destination",
        "background": "img/Final-Destination-Stage3.jpg",
        "get_platforms": classic_arena_layout,
        "platform_image": None
    }
]

def show_start_screen():
    title_image = pygame.image.load("img/MascotMeleeTitle.png")
    title_image = pygame.transform.scale(title_image, (screen.get_width(), screen.get_height()))

    start_screen = True
    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                start_screen = False

        screen.blit(title_image, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def character_select():
    selected_p1 = 0
    selected_p2 = 1
    # Add this near the top of the function (outside the loop)
    confirmed_p1 = False
    confirmed_p2 = False
    clock = pygame.time.Clock()
    font = smash_font
    
    running = True
    while running:
        screen.fill((30,30,30))
        screen_width, screen_height = screen.get_size()

        # ========== Top Character Row ==========
        row_height = screen_height // 2
        box_width = 120
        box_height = 180
        spacing = 100
        row_y = row_height // 2 - box_height // 2

        for i, char in enumerate(character_options):
            x = spacing + i * (box_width + spacing)
            rect = pygame.Rect(x, row_y, box_width, box_height)

            if i == selected_p1:
                pygame.draw.rect(screen, "blue", rect, 4)
            elif i == selected_p2:
                pygame.draw.rect(screen, "green", rect, 4)
            else:
                pygame.draw.rect(screen, "white", rect, 2)

            portrait = pygame.transform.scale(char["select_image"], (box_width - 10, box_height - 10))
            screen.blit(portrait, (x + 5, row_y + 5))

        # ========== Bottom Preview Boxes ==========
        preview_width = 170
        preview_height = 280
        preview_y = screen_height * 3 // 4 - preview_height // 2
        preview_spacing = screen_width // 4

        # Player 1 preview
        preview1_rect = pygame.Rect(preview_spacing - preview_width // 2, preview_y, preview_width, preview_height)
        pygame.draw.rect(screen, "blue", preview1_rect, 4)
        p1_preview_img = pygame.transform.scale(character_options[selected_p1]["select_image"], (preview_width - 10, preview_height - 10))
        screen.blit(p1_preview_img, (preview1_rect.x + 5, preview1_rect.y + 5))
        p1_name = character_options[selected_p1]["name"]
        name_surface1 = smash_font.render(p1_name, True, "white")
        name_rect1 = name_surface1.get_rect(center=(preview1_rect.centerx, preview1_rect.bottom + 25))
        screen.blit(name_surface1, name_rect1)



        # Player 2 preview
        preview2_rect = pygame.Rect(screen_width - preview_spacing - preview_width // 2, preview_y, preview_width, preview_height)
        pygame.draw.rect(screen, "green", preview2_rect, 4)
        p2_preview_img = pygame.transform.scale(character_options[selected_p2]["select_image"], (preview_width - 10, preview_height - 10))
        screen.blit(p2_preview_img, (preview2_rect.x + 5, preview2_rect.y + 5))
        p2_name = character_options[selected_p2]["name"]
        name_surface2 = smash_font.render(p2_name, True, "white")
        name_rect2 = name_surface2.get_rect(center=(preview2_rect.centerx, preview2_rect.bottom + 25))
        screen.blit(name_surface2, name_rect2)


        # Handle inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                # Player 1 input
                if not confirmed_p1:
                    if event.key == pygame.K_a:
                        next_index = (selected_p1 - 1) % len(character_options)
                        while next_index == selected_p2:
                            next_index = (next_index - 1) % len(character_options)
                        selected_p1 = next_index

                    if event.key == pygame.K_d:
                        next_index = (selected_p1 + 1) % len(character_options)
                        while next_index == selected_p2:
                            next_index = (next_index + 1) % len(character_options)
                        selected_p1 = next_index

                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        confirmed_p1 = True

                # Player 2 input
                if not confirmed_p2:
                    if event.key == pygame.K_LEFT:
                        next_index = (selected_p2 - 1) % len(character_options)
                        while next_index == selected_p1:
                            next_index = (next_index - 1) % len(character_options)
                        selected_p2 = next_index

                    if event.key == pygame.K_RIGHT:
                        next_index = (selected_p2 + 1) % len(character_options)
                        while next_index == selected_p1:
                            next_index = (next_index + 1) % len(character_options)
                        selected_p2 = next_index

                    if event.key in [pygame.K_8, pygame.K_9, pygame.K_0]:
                        confirmed_p2 = True



                # When both players have confirmed, return their characters
                if confirmed_p1 and confirmed_p2:
                    return character_options[selected_p1]["game_image"], character_options[selected_p2]["game_image"]


        pygame.display.flip()
        clock.tick(60)


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
        font = smash_font
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
                elif event.key == (pygame.K_1 or pygame.K_2 or pygame.K_3 or pygame.K_8 or pygame.K_9 or pygame.K_0):
                    choosing = False

        pygame.display.flip()
        clock.tick(60)

    return maps[selected]


class Player:
    def __init__(self, x, y, image, player_tag):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.image = image
        self.on_ground = False
        self.lives = 3
        image_width = self.image.get_width()
        image_height = self.image.get_height()
        self.hitbox_offset_x = 8  # Adjust this to nudge hitbox right
        hitbox_width = int(image_width * 0.6)   # adjust as needed
        hitbox_height = int(image_height * 0.9)
        self.player_tag = player_tag

        # Centered horizontally, anchored at feet
        hitbox_x = x - hitbox_width // 2
        hitbox_y = y - hitbox_height

        self.rect = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)
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
            self.rect.topleft = (
                self.pos.x - self.rect.width // 2 ,
                self.pos.y - self.rect.height
            )
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
        self.rect.topleft = (
            self.pos.x - self.rect.width // 2 ,
            self.pos.y - self.rect.height
        )


    
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
                self.pos.y = platform.top
                self.rect.topleft = (
                    self.pos.x - self.rect.width // 2 ,
                    self.pos.y - self.rect.height
                )
                break
        if self.on_ground:
            self.velocity.y = 0

    def check_player_collision(self, other):
        if self.rect.colliderect(other.rect):
            dx = self.rect.centerx - other.rect.centerx
            dy = self.rect.centery - other.rect.centery

            overlap_x = min(self.rect.right - other.rect.left, other.rect.right - self.rect.left)
            overlap_y = min(self.rect.bottom - other.rect.top, other.rect.bottom - self.rect.top)

            # Resolve the shallower overlap
            if overlap_x < overlap_y:
                push_amount = max(overlap_x / 2, 1)  # Prevent micro-jitter

                if dx > 0:
                    self.pos.x += push_amount
                    other.pos.x -= push_amount
                else:
                    self.pos.x -= push_amount
                    other.pos.x += push_amount
            else:
                push_amount = max(overlap_y / 2, 1)

                if dy > 0:
                    self.pos.y += push_amount
                    other.pos.y -= push_amount
                else:
                    self.pos.y -= push_amount
                    other.pos.y += push_amount

            # Update both players' rects
            self.rect.topleft = (
                self.pos.x - self.rect.width // 2 + self.hitbox_offset_x,
                self.pos.y - self.rect.height
            )

            other.rect.topleft = (
                other.pos.x - other.rect.width // 2 + other.hitbox_offset_x,
                other.pos.y - other.rect.height
            )


    def check_off_screen(self, screen_width, screen_height):
        if self.pos.x < 0 or self.pos.x > screen_width or self.pos.y > screen_height:
            self.lives -= 1
            self.pos = pygame.Vector2(screen_width / 2, screen_height / 2)
            self.velocity = pygame.Vector2(0, 0)
            self.rect.topleft = (
                self.pos.x - self.rect.width // 2 ,
                self.pos.y - self.rect.height
            )


    def apply_knockback(self, direction, strength):
        self.velocity += direction * strength

    def draw(self, screen):
        if self.is_shielding:
            shield_color = (0, 0, 255, 100)
            shield_surface = pygame.Surface((self.rect.width * 2, self.rect.height * 2), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, shield_color, (self.rect.width, self.rect.height), self.rect.width)

            # Get top of the visible sprite
            image_top = self.rect.bottom - self.image.get_height()

            # Center the shield on the visual character
            shield_x = self.rect.centerx - self.rect.width + 5  # Shift slightly right
            shield_y = image_top + self.image.get_height() // 2 - self.rect.height - 5  # Shift slightly up

            screen.blit(shield_surface, (shield_x, shield_y))


        blit_x = self.rect.left - self.hitbox_offset_x
        blit_y = self.rect.bottom - self.image.get_height()

        if self.facing_right:
            screen.blit(self.image, (blit_x, blit_y))

        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            
            screen.blit(flipped_image, (blit_x, blit_y))

        # Floating player label (e.g. "P1" or "P2")
        tag_surface = tag_font.render(self.player_tag, True, "white")
        outline_surface = tag_font.render(self.player_tag, True, "black")


        # Calculate position above character's image
        text_x = self.rect.centerx - tag_surface.get_width() // 2
        text_y = self.rect.top - 30  # Adjust vertical offset as needed

        # Draw outline (8 directions)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    screen.blit(outline_surface, (text_x + dx, text_y + dy))

        # Draw the main white text
        screen.blit(tag_surface, (text_x, text_y))

        # Draw hitbox outline for debugging (in red)
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)



def show_winner_screen(winner):
    """Display the winner screen and wait for player input to restart or quit."""
    screen.fill((0, 0, 0))  # Black background
    font = smash_font
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

def draw_text_with_outline(surface, text, font, x, y, text_color="white", outline_color="black"):
    text_surface = font.render(text, True, text_color)
    outline_surface = font.render(text, True, outline_color)

    # Draw outline in 8 directions
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                surface.blit(outline_surface, (x + dx, y + dy))
    
    # Draw main text in the center
    surface.blit(text_surface, (x, y))


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
    player1 = Player(screen.get_width() / 3, screen.get_height() / 2, player1_img, "P1")
    player2 = Player(2 * screen.get_width() / 3, screen.get_height() / 2, player2_img, "P2")

    # Font setup for displaying lives
    font = smash_font

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

        effect_size = 80  # adjust this for how big the visual should be
        effect_img = pygame.transform.scale(melee_effect_img, (effect_size, effect_size))

            # Attack mechanics
        # Player 1 Attack Logic
        if keys[pygame.K_1]:  
            if player1.attack_mode == "melee" and (current_time - player1.last_attack_time) >= player1.attack_cooldown:
                player1.last_attack_time = current_time
                image_top1 = player1.rect.bottom - player1.image.get_height()
                attack_box1 = pygame.Rect(
                    player1.rect.centerx + (30 if player1.facing_right else -30),
                    image_top1 + player1.image.get_height() // 2 - 20,  # Middle of sprite
                    40, 40
                )

                effect_x = attack_box1.centerx - effect_size // 2
                effect_y = attack_box1.centery - effect_size // 2
                screen.blit(effect_img, (effect_x, effect_y))

                if attack_box1.colliderect(player2.rect) and not player2.is_shielding:
                    direction = pygame.Vector2(1, 0) if player1.facing_right else pygame.Vector2(-1, 0)
                    player2.apply_knockback(direction, 1000)

        elif keys[pygame.K_2]:
            player1.is_shielding = True  # Activate shield while button is held

        elif keys[pygame.K_3] and (current_time - player1.last_attack_time) >= player1.attack_cooldown:
            player1.last_attack_time = current_time

            offset_x = 40 if player1.facing_right else -40  
            projectile_speed = 7 if player1.facing_right else -7  

            # Align projectile spawn with visual middle of sprite
            image_top1 = player1.rect.bottom - player1.image.get_height()
            projectile_y1 = image_top1 + player1.image.get_height() // 2 - 5  # -5 centers 10px tall projectile

            projectiles.append(Projectile(player1.rect.centerx + offset_x, projectile_y1, projectile_speed, "blue"))

        else:
            player1.is_shielding = False  # Deactivate shield when attack key is released

        # Player 2 Attack Logic
        if keys[pygame.K_8]:  
            if player2.attack_mode == "melee" and (current_time - player2.last_attack_time) >= player2.attack_cooldown:
                player2.last_attack_time = current_time
                image_top2 = player2.rect.bottom - player2.image.get_height()
                attack_box2 = pygame.Rect(
                    player2.rect.centerx + (30 if player2.facing_right else -30),
                    image_top2 + player2.image.get_height() // 2 - 20,
                    40, 40
                )
                effect_x = attack_box2.centerx - effect_size // 2
                effect_y = attack_box2.centery - effect_size // 2
                screen.blit(effect_img, (effect_x, effect_y))

                if attack_box2.colliderect(player1.rect) and not player1.is_shielding:
                    direction = pygame.Vector2(1, 0) if player2.facing_right else pygame.Vector2(-1, 0)
                    player1.apply_knockback(direction, 1200)

        elif keys[pygame.K_9]:
            player2.is_shielding = True

        elif keys[pygame.K_0] and (current_time - player2.last_attack_time) >= player2.attack_cooldown:
            player2.last_attack_time = current_time

            offset_x = 40 if player2.facing_right else -40  
            projectile_speed = 7 if player2.facing_right else -7  

            image_top2 = player2.rect.bottom - player2.image.get_height()
            projectile_y2 = image_top2 + player2.image.get_height() // 2 - 5

            projectiles.append(Projectile(player2.rect.centerx + offset_x, projectile_y2, projectile_speed, "green"))

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

        # Draw Player 1 label (above hearts, bottom-left)
        draw_text_with_outline(screen, "Player 1", font, 20, screen.get_height() - 90)

        p2_text = "Player 2"
        p2_rect = font.render(p2_text, True, "white").get_rect()
        p2_x = screen.get_width() - 180 + (player2.lives * 50 - p2_rect.width) // 2
        draw_text_with_outline(screen, p2_text, font, p2_x, screen.get_height() - 90)


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

