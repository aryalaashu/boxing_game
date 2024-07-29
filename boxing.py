import serial
import pygame
import sys
import json
import os
import threading

ser = serial.Serial('COM6', 9600)

pygame.init()
pygame.mixer.init()

# Display setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Sensor Display')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (54, 161, 93)

# Fonts
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 36)

# Images
background_img = pygame.image.load('images/bg.jpg')
barbie_img = pygame.image.load('images/barbie.jpeg')
cena_img = pygame.image.load('images/cena.jpeg')

# JSON file to store high scores
high_score_file = 'high_scores.json'

def read_high_scores():
    if os.path.exists(high_score_file):
        with open(high_score_file, 'r') as file:
            return json.load(file)
    return {"high_score": 0}

def write_high_score(score):
    with open(high_score_file, 'w') as file:
        json.dump({"high_score": score}, file)

def play_song(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

# Read high scores
high_scores = read_high_scores()
highest_score = high_scores["high_score"]

# Starting page
screen.blit(pygame.transform.scale(background_img, (800, 600)), (0, 0))
title_text = font_large.render("Welcome to the Boxing Game", True, BLACK)
sub_text = font_small.render("Lets see what you got? Hit the pad Watch your score soar!", True, BLACK)
sub_text_two = font_small.render(" Show off your power and dominate the leaderboard!", True, BLACK)
high_score_text = font_large.render(f"High Score: {highest_score}", True, GREEN)

screen.blit(title_text, (35, 50))
screen.blit(sub_text, (50, 150))
screen.blit(sub_text_two, (50, 200))
screen.blit(high_score_text, (190, 500))
pygame.display.flip()

def read_serial_data():
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(",")
                if len(parts) == 3:
                    fsr1_str = parts[0].split(": ")[1]
                    fsr2_str = parts[1].split(": ")[1]
                    avg_force_str = parts[2].split(": ")[1]

                    fsr1 = int(fsr1_str)
                    fsr2 = int(fsr2_str)
                    average_force = int(avg_force_str)
                    update_display(fsr1, fsr2, average_force)
        except ValueError:
            continue

def update_display(fsr1, fsr2, average_force):
    global highest_score
    screen.blit(pygame.transform.scale(background_img, (800, 600)), (0, 0))

    avg_force_text = font_large.render(f"Your Score is: {average_force}", True, GREEN)
    pygame.draw.rect(screen, WHITE, pygame.Rect(30, 240, 500, 100), border_radius=10)
    screen.blit(avg_force_text, (50, 265))
    

    if average_force < 950:
        screen.blit(barbie_img, (550, 200))
        avg_force_text = font_large.render(f"Your Score is: {average_force}", True, GREEN)
        pygame.draw.rect(screen, WHITE, pygame.Rect(30, 240, 500, 100), border_radius=10)
        screen.blit(avg_force_text, (50, 265))
        threading.Thread(target=play_song, args=('barbie.mp3',)).start()
    else:
        screen.blit(cena_img, (500, 100))
        threading.Thread(target=play_song, args=('cena.mp3',)).start()

        if average_force > highest_score:
            highest_score = average_force
            write_high_score(highest_score)
            high_score_text = font_medium.render(f"High Score: {highest_score}", True, GREEN)
            screen.blit(high_score_text, (300, 500))

    pygame.display.flip()

serial_thread = threading.Thread(target=read_serial_data)
serial_thread.daemon = True
serial_thread.start()

while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    except KeyboardInterrupt:
        print("Exiting...")
        break
