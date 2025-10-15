import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# --- Variables globales ---
original_surface = None
is_blurred = False


def apply_blur(surface, intensity=0.2):
    """
    Applique un flou sur toute la surface donnée.
    intensity : entre 0.1 (flou fort) et 0.9 (léger flou)
    """
    global original_surface, is_blurred

    if is_blurred:
        return  # déjà flou

    original_surface = surface.copy()
    w, h = surface.get_size()
    small = pygame.transform.smoothscale(surface, (int(w * intensity), int(h * intensity)))
    blurred = pygame.transform.smoothscale(small, (w, h))
    surface.blit(blurred, (0, 0))
    is_blurred = True


def remove_blur(surface):
    """
    Restaure la surface originale sans flou.
    """
    global original_surface, is_blurred

    if not is_blurred or original_surface is None:
        return  # rien à restaurer

    surface.blit(original_surface, (0, 0))
    is_blurred = False


# --- Exemple d'utilisation ---
background = pygame.Surface((800, 600))
background.fill((20, 20, 40))
pygame.draw.circle(background, (255, 100, 100), (400, 300), 150)

blur_active = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:  # Touche 'B' pour activer/désactiver le blur
                blur_active = not blur_active
                if blur_active:
                    apply_blur(screen)
                else:
                    remove_blur(screen)

    # Redessiner le fond avant chaque frame
    screen.blit(background, (0, 0))

    if blur_active:
        apply_blur(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
