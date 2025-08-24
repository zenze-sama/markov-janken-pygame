import pygame
import random
import sys
import os
from collections import defaultdict

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
small_font = pygame.font.Font(font, 18)

player_score = 0
computer_score = 0
player_choice = None
computer_choice = None
result = None

rock_rect = pygame.Rect(150, 400, 120, 120)
paper_rect = pygame.Rect(340, 400, 120, 120)
scisors_rect = pygame.Rect(530, 400, 120, 120)

player_history = []
pattern_counts = defaultdict(lambda: defaultdict(int))
patterns_file = "markov_patterns.txt"

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

def counter_move(move):
    if move == "rock": return "paper"
    if move == "paper": return "scisors"
    return "rock"

def get_frequency_based_move():
    if not player_history:
        return random.choice(["rock", "paper", "scisors"])
    
    freq = {"rock": 0, "paper": 0, "scisors": 0}
    for move in player_history:
        freq[move] += 1
    
    most_common = max(freq, key=freq.get)
    return counter_move(most_common)

def get_markov_move():
    if len(player_history) < 2:
        return get_frequency_based_move()
    
    if len(player_history) >= 4:
        last_moves = player_history[-4:]
        if all(move == last_moves[0] for move in last_moves):
            return counter_move(last_moves[0])
    
    prev2 = player_history[-2]
    prev1 = player_history[-1]
    pattern_key = (prev2, prev1)
    
    if not pattern_counts[pattern_key]:
        return get_frequency_based_move()
    
    predicted_move = max(pattern_counts[pattern_key], key=pattern_counts[pattern_key].get)
    return counter_move(predicted_move)

def computer_pick():
    return get_markov_move()

def determine_winner(player, computer):
    if player == computer:
        return "It's a tie!"
    elif (player == "rock" and computer == "scisors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scisors" and computer == "paper"):
        return "You win!"
    else:
        return "Computer wins!"

def save_patterns():
    try:
        with open(patterns_file, 'w') as f:
            for pattern_key, counts in pattern_counts.items():
                if counts:
                    f.write(f"[{pattern_key[0]} {pattern_key[1]}] -> ")
                    for move, count in counts.items():
                        f.write(f"{move} ({count}) ")
                    f.write("\n")
    except Exception as e:
        print(f"Error saving patterns: {e}")

def load_patterns():
    global pattern_counts
    try:
        if os.path.exists(patterns_file):
            with open(patterns_file, 'r') as f:
                for line in f:
                    if '->' in line:
                        pattern_part, counts_part = line.split('->', 1)
                        pattern_part = pattern_part.strip().strip('[]')
                        moves = pattern_part.split()
                        if len(moves) == 2:
                            pattern_key = (moves[0], moves[1])
                            count_items = counts_part.strip().split()
                            for i in range(0, len(count_items), 2):
                                if i + 1 < len(count_items):
                                    move = count_items[i]
                                    count_str = count_items[i+1].strip('()')
                                    try:
                                        count = int(count_str)
                                        pattern_counts[pattern_key][move] = count
                                    except ValueError:
                                        continue
    except Exception as e:
        print(f"Error loading patterns: {e}")

def reset_patterns():
    global pattern_counts, player_history
    pattern_counts = defaultdict(lambda: defaultdict(int))
    player_history = []
    try:
        if os.path.exists(patterns_file):
            os.remove(patterns_file)
    except Exception as e:
        print(f"Error resetting patterns: {e}")

def draw_game():
    screen.fill(BACKGROUND)
    
    title_surf = title_font.render("Rock Paper Scisors", True, TEXT_COLOR)
    screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 30))
    
    score_text = f"Player: {player_score}  |  Computer: {computer_score}"
    score_surf = score_font.render(score_text, True, TEXT_COLOR)
    screen.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, 100))
    
    pattern_count = sum(len(counts) for counts in pattern_counts.values())
    pattern_text = f"Patterns learned: {pattern_count} (R to Reset Patterns)"
    pattern_surf = small_font.render(pattern_text, True, TEXT_COLOR)
    screen.blit(pattern_surf, (WIDTH//2 - pattern_surf.get_width()//2, 160))
    
    mouse_pos = pygame.mouse.get_pos()
    draw_choice(rock_rect, rock_img, "Rock (1)", rock_rect.collidepoint(mouse_pos))
    draw_choice(paper_rect, paper_img, "Paper (2)", paper_rect.collidepoint(mouse_pos))
    draw_choice(scisors_rect, scisors_img, "Scisors (3)", scisors_rect.collidepoint(mouse_pos))
    
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

def make_choice(choice):
    global player_choice, computer_choice, result, player_score, computer_score
    
    player_choice = choice
    computer_choice = computer_pick()
    result = determine_winner(player_choice, computer_choice)
    
    if len(player_history) >= 2:
        prev2 = player_history[-2]
        prev1 = player_history[-1]
        pattern_key = (prev2, prev1)
        pattern_counts[pattern_key][player_choice] += 1
    
    player_history.append(player_choice)
    
    if result == "You win!":
        player_score += 1
    elif result == "Computer wins!":
        computer_score += 1

load_patterns()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_patterns()
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if rock_rect.collidepoint(mouse_pos):
                make_choice("rock")
                    
            elif paper_rect.collidepoint(mouse_pos):
                make_choice("paper")
                    
            elif scisors_rect.collidepoint(mouse_pos):
                make_choice("scisors")
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                make_choice("rock")
            elif event.key == pygame.K_2:
                make_choice("paper")
            elif event.key == pygame.K_3:
                make_choice("scisors")
            elif event.key == pygame.K_r:
                reset_patterns()
    
    draw_game()
    
    pygame.display.flip()
    clock.tick(60)

save_patterns()
pygame.quit()
sys.exit()