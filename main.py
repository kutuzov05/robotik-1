import pygame
import numpy as np


# Initialisierung
pygame.init()
width, height = 550, 550
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Roboter Arm")
clock = pygame.time.Clock()
fps = 60
timer = 0

# Farben
GREY = (100, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Roboterarm-angaben
l_1, l_2 = 3, 2.25
num_frames = 300
draw_list = []
# x/y Anfangswert + Endwert
interval_list = [[-3.5, -2, 1, -3, 1, -2.5, -1, 1, -1, 1, 1.75, 2.25, 2, 2.25, 1.75, 2.8, 2.7, 3, 1, 3.5, 4.5, 4.1, 4.7, 1, 4.5], [-2, -3, 0, -2.5, 0, -1, 1, -1, 1, 1.75, 2.25, 2, 2.25, 1.75, 2.8, 2.7, 3, 3.5, 0, 4.5, 4.1, 4.7, 4.5, 0, -3.5]]
# True = Punkte werden gezeichnet; False = Punkte werden nicht gezeichnet
save_list = [True, False, True, False, True, False, True, False, True, False, True, True, True, True, False, True, False, True, True, False, True, True, False, True, False]
line_num = len(save_list)


def deg2rad(angle):
    return angle / 180 * np.pi


def rad2deg(angle):
    return angle * 180 / np.pi


# Direktes kinematisches Problem
def dkp(angle_1, angle_2):
    theta_1, theta_2 = deg2rad(angle_1), deg2rad(angle_2)
    s_x, s_y = 0, 0
    e_x, e_y = l_1 * np.cos(theta_1), l_1 * np.sin(theta_1)
    t_x, t_y = e_x + l_2 * np.cos(theta_1 + theta_2), e_y + l_2 * np.sin(theta_1 + theta_2)
    return [[s_x, s_y], [e_x, e_y], [t_x, t_y]]


# Inverses kinematische Problem
def ikp(t):
    theta_1 = rad2deg(np.arctan2(t[1], t[0]) - np.arccos(
        (t[0] ** 2 + t[1] ** 2 + l_1 ** 2 - l_2 ** 2) / (2 * l_1 * (t[0] ** 2 + t[1] ** 2) ** 0.5)))
    theta_2 = 180 - rad2deg(np.arccos((l_1 ** 2 + l_2 ** 2 - t[0] ** 2 - t[1] ** 2) / (2 * l_1 * l_2)))
    return [theta_1, theta_2]


# Koordinatensystem wird erstellt
def draw_coordinate_system():
    screen.fill(GREY)
    pygame.draw.rect(screen, WHITE, (25, 25, 500, 500))
    # y-Achse
    for nums in range(11):
        pygame.draw.line(screen, BLACK, (20, 25+50*nums), (30, 25+50*nums), 3)
    # x-Achse
    for nums in range(11):
        pygame.draw.line(screen, BLACK, (25+50*nums, 520), (25+50*nums, 530), 3)

    font = pygame.font.Font(None, 20)
    # y-Achse
    for nums in range(6):
        text = font.render(str(-nums), True, BLACK)
        text_pos = text.get_rect()
        text_pos.center = (10, 275+50*nums)
        screen.blit(text, text_pos)
    for nums in range(6):
        text = font.render(str(nums), True, BLACK)
        text_pos = text.get_rect()
        text_pos.center = (10, 275-50*nums)
        screen.blit(text, text_pos)
    # x-Achse
    for nums in range(6):
        text = font.render(str(nums), True, BLACK)
        text_pos = text.get_rect()
        text_pos.center = (275+50*nums, 540)
        screen.blit(text, text_pos)
    for nums in range(6):
        text = font.render(str(-nums), True, BLACK)
        text_pos = text.get_rect()
        text_pos.center = (275-50*nums, 540)
        screen.blit(text, text_pos)


# Roboterarm wird gezeichnet
def draw_robot_arm(s, e, t):
    pygame.draw.circle(screen, BLACK, (275+s[0]*50, 275-s[1]*50), 5)
    pygame.draw.circle(screen, BLACK, (275+e[0]*50, 275-e[1]*50), 5)
    pygame.draw.circle(screen, BLACK, (275+t[0]*50, 275-t[1]*50), 5)
    pygame.draw.line(screen, BLACK, (275+s[0]*50, 275-s[1]*50), (275+e[0]*50, 275-e[1]*50), 3)
    pygame.draw.line(screen, BLACK, (275+e[0]*50, 275-e[1]*50), (275+t[0]*50, 275-t[1]*50), 3)


# speichert Punkte, welche gezeichnet werden sollen
def save_points(t):
    draw_list.append(t)


# erstellt Listen von Koordinaten mithilfe von Funktionen
def create_coords(f, interval, frame):
    # Funktionen
    if f == 1:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = np.linspace(1, 1, num_frames)
    if f == 2:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = np.linspace(1, 1, num_frames)
    if f == 3:
        x = np.linspace(-3, -3, num_frames)
        y = np.linspace(interval[0][frame], interval[1][frame], num_frames)
    if f == 4:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = 2*x+6
    if f == 5:
        x = np.linspace(-2.5, -2.5, num_frames)
        y = np.linspace(interval[0][frame], interval[1][frame], num_frames)
    if f == 6:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = 26/75*x+0.54+26/75
    if f == 7:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = 0.8-0.343*np.sin(4*x)
    if f == 8:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = 0.46*x+0.6
    if f == 9:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = 0.8-0.343*np.sin(4*x) - 0.4
    if f == 10:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = 3/25*x+0.54
    if f == 11:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = (0.25**2-(x-2)**2)**0.5 + 0.75
    if f == 12:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = -((0.25**2-(x-2)**2)**0.5 + 0.75) + 1.5
    if f == 13:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = (0.25**2-(x-2)**2)**0.5 + 0.25
    if f == 14:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = -((0.25**2-(x-2)**2)**0.5 + 0.75) + 1
    if f == 15:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = -5/21 * x + 14/21
    if f == 16:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = 20*x**2-105*x+137.2
    if f == 17:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = x/0.3-9.5
    if f == 18:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = x-2.5
    if f == 19:
        x = np.linspace(3.5, 3.5, num_frames)
        y = np.linspace(interval[0][frame], interval[1][frame], num_frames)
    if f == 20:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = x-3.5
    if f == 21:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = 5/4*x-37/8
    if f == 22:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = np.linspace(0.5, 0.5, num_frames)
    if f == 23:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = -2.5*x+12.25
    if f == 24:
        x = np.linspace(4.5, 4.5, num_frames)
        y = np.linspace(interval[0][frame], interval[1][frame], num_frames)
    if f == 25:
        x = np.linspace(interval[0][frame], interval[1][frame], num_frames)
        y = -1/8 * x + 9/16
    return [x-0.5, y+1]


def animation(x, y, frame, save):
    result = dkp(ikp([x[frame], y[frame]])[0], ikp([x[frame], y[frame]])[1])
    draw_robot_arm(result[0], result[1], result[2])
    if save:
        save_points(result[2])


# rote Punkte werden gezeichnet
def draw_points():
    for nums in range(len(draw_list)):
        pygame.draw.circle(screen, RED, (275+draw_list[nums][0]*50, 275-draw_list[nums][1]*50), 3)


# Main-Loop
running = True
while running:
    clock.tick(fps)
    timer += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_coordinate_system()
    if timer == 1:
        draw_robot_arm(dkp(ikp([-4, 2])[0], ikp([-4, 2])[1])[0], dkp(ikp([-4, 2])[0], ikp([-4, 2])[1])[1],
                       dkp(ikp([-4, 2])[0], ikp([-4, 2])[1])[2])
        pygame.display.update()
        pygame.time.wait(1000)
        # Schleife für jede einzelne Linie
        for run in range(line_num):
            # Schleife für jeden Frame
            for n in range(num_frames):
                draw_coordinate_system()
                draw_points()
                animation(create_coords(run+1, interval_list, run)[0], create_coords(run+1, interval_list, run)[1], n, save_list[run])
                pygame.display.update()
        pygame.time.wait(1000)
    draw_points()
    pygame.display.update()
pygame.quit()
