from pygame import *   
import sounddevice as sd 
import tkinter as tk

# === Налаштування ===
fs = 44100     # Частота дискретизації (кількість вимірів за секунду)
chunk = 1024   # Кількість семплів (відліків) за один кадр
width, height = 800, 400

# === Кнопки ===
button_play_rect = Rect(width // 2 - 165, height - 50, 150, 40)
button_stop_rect = Rect(width // 2 + 15, height - 50, 150, 40)
button_play_color = (100, 200, 100)
button_stop_color = (200, 100, 100)
button_text_color = (255, 255, 255)

def draw_buttons(screen, font):
    """Малює кнопки для відтворення та зупинки музики"""
    # Кнопка Play
    draw.rect(screen, button_play_color, button_play_rect)
    draw.rect(screen, (255, 255, 255), button_play_rect, 2)  # Контур
    text_surface = font.render("Play Music", True, button_text_color)
    text_rect = text_surface.get_rect(center=button_play_rect.center)
    screen.blit(text_surface, text_rect)
    
    # Кнопка Stop
    draw.rect(screen, button_stop_color, button_stop_rect)
    draw.rect(screen, (255, 255, 255), button_stop_rect, 2)  # Контур
    text_surface = font.render("Stop Music", True, button_text_color)
    text_rect = text_surface.get_rect(center=button_stop_rect.center)
    screen.blit(text_surface, text_rect)

def click():
    mixer.music.load("pingpong/intothenightmix.ogg")
    mixer.music.play()

def click_stop():
    mixer.music.stop()

init()
mixer.music.load("pingpong/intothenightmix.ogg")
screen = display.set_mode((width, height))
display.set_caption("Live Audio (Mic)")
font = font.Font(None, 24)  
clock = time.Clock()



data = [0.0] * chunk

# === Функція, яку викликає sounddevice, коли приходить нова порція звуку ===
def audio_callback(indata, frames, time_info, status):
    global data
    if status:
        print(status)
    data = [sample * (height // 2) for sample in indata[:, 0].tolist()]

# === Запуск потоку з мікрофона ===
stream = sd.InputStream(
    callback=audio_callback, 
    channels=1,              
    samplerate=fs,             
    blocksize=chunk,           
    dtype='float32'            
)
stream.start()

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == MOUSEBUTTONDOWN:
            if button_play_rect.collidepoint(e.pos):
                click()
            elif button_stop_rect.collidepoint(e.pos):
                click_stop()

    screen.fill((0, 0, 0))

    points = []
    for i, sample in enumerate(data):
        x = int(i * width / chunk)         
        y = int(height / 2 + sample)        
        points.append((x, y))               


    if len(points) > 1:
        draw.lines(screen, (0, 255, 0), False, points, 2)

    draw_buttons(screen, font)

    display.update()
    clock.tick(60)

stream.stop()
quit()