import pygame
import os

# --- Fonction pour charger les frames d’un dossier ---
def load_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            frame = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
            frames.append(frame)
    return frames


# --- Classe Player ---
class Player(pygame.sprite.Sprite):
    def __init__(self, frames):
        super().__init__()
        self.frames = frames
        self.idle_image = self.frames[0]  # 1.png = frame de repos
        self.walk_frames = self.frames[1:]  # les autres frames = marche
        self.frame_index = 0
        self.image = self.idle_image
        self.rect = self.image.get_rect(center=(400, 300))
        self.animation_speed = 0.15
        

    def update(self, keys):
        dx, dy = 0, 0

        # --- Déplacements ---
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1

        moving = dx != 0 or dy != 0

        # --- Animation ---
        if moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.walk_frames):
                self.frame_index = 0
            self.image = self.walk_frames[int(self.frame_index)]
            self.rect.move_ip(dx * 4, dy * 4)
        else:
            self.frame_index = 0
            self.image = self.idle_image

        pygame.draw.rect(self.image, "red", self.image.get_rect(), width=1)
       

        


# --- Initialisation ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Animation avec image de repos")
clock = pygame.time.Clock()

# --- Chargement des images ---
# Dossier : assets/south/
frames = load_frames("assets/south")

player = Player(frames)
all_sprites = pygame.sprite.Group(player)
mur_rect = pygame.Rect(200, 200, 50, 50)
# --- Boucle principale ---
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(keys)


    screen.fill((30, 30, 30))
    all_sprites.draw(screen)
    # rectangle du mur
    
    pygame.draw.rect(screen, (200,0,0), mur_rect)  # dessine le mur
    # collision ?
    if player.rect.colliderect(mur_rect):
        print("Collision détectée !")

    pygame.display.flip()
    clock.tick(60)
    

pygame.quit()
