# pingpong_game.py
import os
import sys
import pygame
import cv2
import numpy as np
import subprocess
import math
import time

# ===============================
# 📦 라이브러리 체크 & 설치
# ===============================
def install_if_missing(package):
    try:
        __import__(package)
    except ImportError:
        print(f"📦 {package} 설치 중...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in ["pygame", "opencv-python", "numpy"]:
    install_if_missing(pkg)

# ===============================
# 📂 경로 설정 (현재 파일 기준)
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(BASE_DIR, "인트로.mp4")
AUDIO_PATH = os.path.join(BASE_DIR, "인트로.mp3")

# ===============================
# 🎬 인트로 영상 + 소리 재생
# ===============================
def play_intro_video(video_path, audio_path, screen):
    pygame.mixer.init()
    if os.path.exists(audio_path):
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ 영상 열기 실패")
        return

    screen_width, screen_height = screen.get_size()
    clock = pygame.time.Clock()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen_width, screen_height))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                cap.release()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                cap.release()
                return

    cap.release()
    pygame.mixer.music.stop()

# ===============================
# 🧭 로비 화면 (애니메이션)
# ===============================
def show_lobby(screen):
    font_big = pygame.font.SysFont("Courier New", 72, bold=True)
    font_small = pygame.font.SysFont("Courier New", 32)
    clock = pygame.time.Clock()

    start_time = time.time()
    waiting = True

    while waiting:
        screen.fill((0, 0, 20))  # 짙은 남색 배경

        # 파도치는 텍스트 효과
        elapsed = time.time() - start_time
        title_text = "WECODE PINGPONG"
        wave_offset = math.sin(elapsed * 2) * 10
        text_surface = font_big.render(title_text, True, (255, 255, 255))
        rect = text_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 100 + wave_offset))
        screen.blit(text_surface, rect)

        # 반짝이는 Press Enter
        alpha = (math.sin(elapsed * 3) + 1) / 2  # 0~1
        press_surface = font_small.render("Press Enter to Start!", True, (int(255*alpha), 255, int(255*alpha)))
        press_rect = press_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 50))
        screen.blit(press_surface, press_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        clock.tick(60)

# ===============================
# 🏓 핑퐁 게임
# ===============================
def play_pong(screen):
    WIDTH, HEIGHT = screen.get_size()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
    paddle_speed = 7

    left_paddle = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    BALL_SIZE = 15
    ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
    ball_speed_x = 6
    ball_speed_y = 6

    font = pygame.font.SysFont("Courier New", 36)
    left_score = 0
    right_score = 0

    clock = pygame.time.Clock()
    FPS = 60

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += paddle_speed

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1

        if ball.left <= 0:
            right_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x *= -1
        if ball.right >= WIDTH:
            left_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x *= -1

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (WIDTH // 4, 20))
        screen.blit(right_text, (WIDTH * 3 // 4, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# ===============================
# 🚀 메인 함수
# ===============================
def main():
    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("WECODE 핑퐁")

    if os.path.exists(VIDEO_PATH):
        play_intro_video(VIDEO_PATH, AUDIO_PATH, screen)
    show_lobby(screen)
    play_pong(screen)

if __name__ == "__main__":
    main()
