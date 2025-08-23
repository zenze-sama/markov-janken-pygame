import pygame
import random
import sys
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Janken")

BACKGROUND = (240, 240, 245)
PRIMARY = (70, 130, 180)
SECONDARY = (220, 100, 100)
ACCENT = (90, 160, 90)
TEXT_COLOR = (50, 50, 50)
WHITE = (255, 255, 255)
HIGHLIGHT = (230, 230, 250)

font = "PixelifySans-VariableFont_wght.ttf"
title_font = pygame.font.Font(font, 48)
choice_font = pygame.font.Font(font, 32)
result_font = pygame.font.Font(font, 36)
score_font = pygame.font.Font(font, 28)
button_font = pygame.font.Font(font, 24)

player_score = 0
computer_score = 0
player_choice = None
computer_choice = None
result = None

rock_rect = pygame.Rect(150, 400, 120, 120)
paper_rect = pygame.Rect(340, 400, 120, 120)
scisors_rect = pygame.Rect(530, 400, 120, 120)

def load_image(name, size=(100, 100)):
    try:
        image = pygame.image.load(name)
        return pygame.transform.scale(image, size)
    except:
        surface = pygame.Surface(size, pygame.SRCALPHA)
        if "rock" in name:
            pygame.draw.circle(surface, PRIMARY, (size[0]//2, size[1]//2), size[0]//2 - 10)
            text = "ROCK"
        elif "paper" in name:
            pygame.draw.circle(surface, SECONDARY, (size[0]//2, size[1]//2), size[0]//2 - 10)
            text = "PAPER"
        else:
            pygame.draw.circle(surface, ACCENT, (size[0]//2, size[1]//2), size[0]//2 - 10)
            text = "SCISORS"
        
        text_surf = button_font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=(size[0]//2, size[1]//2))
        surface.blit(text_surf, text_rect)
        return surface

rock_img = load_image("rock.png")
paper_img = load_image("paper.png")
scisors_img = load_image("scisors.png")

def draw_choice(rect, image, text, hover=False):
    if hover:
        pygame.draw.rect(screen, HIGHLIGHT, rect, border_radius=15)
        pygame.draw.rect(screen, TEXT_COLOR, rect, 3, border_radius=15)
    else:
        pygame.draw.rect(screen, BACKGROUND, rect, border_radius=15)
        pygame.draw.rect(screen, TEXT_COLOR, rect, 2, border_radius=15)
    
    img_rect = image.get_rect(center=rect.center)
    screen.blit(image, img_rect)
    
    text_surf = button_font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(midtop=(rect.centerx, rect.bottom + 5))
    screen.blit(text_surf, text_rect)

def computer_pick():
    return random.choice(["rock", "paper", "scisors"])

def determine_winner(player, computer):
    if player == computer:
        return "It's a tie!"
    elif (player == "rock" and computer == "scisors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scisors" and computer == "paper"):
        return "You win!"
    else:
        return "Computer wins!"

def draw_game():
    screen.fill(BACKGROUND)
    
    title_surf = title_font.render("Rock Paper Scisors", True, TEXT_COLOR)
    screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 30))
    
    score_text = f"Player: {player_score}  |  Computer: {computer_score}"
    score_surf = score_font.render(score_text, True, TEXT_COLOR)
    screen.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, 100))
    
    mouse_pos = pygame.mouse.get_pos()
    draw_choice(rock_rect, rock_img, "Rock", rock_rect.collidepoint(mouse_pos))
    draw_choice(paper_rect, paper_img, "Paper", paper_rect.collidepoint(mouse_pos))
    draw_choice(scisors_rect, scisors_img, "Scisors", scisors_rect.collidepoint(mouse_pos))
    
    if player_choice is not None:
        if player_choice == "rock":
            screen.blit(rock_img, (WIDTH//4 - 50, 200))
        elif player_choice == "paper":
            screen.blit(paper_img, (WIDTH//4 - 50, 200))
        elif player_choice == "scisors":
            screen.blit(scisors_img, (WIDTH//4 - 50, 200))
            
        if computer_choice == "rock":
            screen.blit(rock_img, (3*WIDTH//4 - 50, 200))
        elif computer_choice == "paper":
            screen.blit(paper_img, (3*WIDTH//4 - 50, 200))
        elif computer_choice == "scisors":
            screen.blit(scisors_img, (3*WIDTH//4 - 50, 200))
            
        result_surf = result_font.render(result, True, TEXT_COLOR)
        screen.blit(result_surf, (WIDTH//2 - result_surf.get_width()//2, 320))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if rock_rect.collidepoint(mouse_pos):
                player_choice = "rock"
                computer_choice = computer_pick()
                result = determine_winner(player_choice, computer_choice)
                if result == "You win!":
                    player_score += 1
                elif result == "Computer wins!":
                    computer_score += 1
                    
            elif paper_rect.collidepoint(mouse_pos):
                player_choice = "paper"
                computer_choice = computer_pick()
                result = determine_winner(player_choice, computer_choice)
                if result == "You win!":
                    player_score += 1
                elif result == "Computer wins!":
                    computer_score += 1
                    
            elif scisors_rect.collidepoint(mouse_pos):
                player_choice = "scisors"
                computer_choice = computer_pick()
                result = determine_winner(player_choice, computer_choice)
                if result == "You win!":
                    player_score += 1
                elif result == "Computer wins!":
                    computer_score += 1
    
    draw_game()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()