"""
Screen Sharing Library - Receiver
"""

# Imports
from socket import socket
from zlib import decompress
import pygame
import math

# Main Vars
WIDTH_IN = 1920
HEIGHT_IN = 1080
WIDTH_DISPLAY = 1920
HEIGHT_DISPLAY = 1080

MAX_IN_ONE_ROW = 5

# Main Functions
def ReceiveAllPixels(conn, length):
    '''
    Retreive all pixels from the server
    '''
    # Init
    buf = b''
    # Retreive data
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data

    return buf

def ScreenShareClient(name="", hosts=["127.0.0.1", "127.0.0.1", "127.0.0.1", "127.0.0.1"], ports=[5000, 5000, 5000, 5000]):
    '''
    Screen Share Client
    '''
    # Init
    pygame.init()
    pygame.display.set_caption(name)
    screen = pygame.display.set_mode((WIDTH_DISPLAY, HEIGHT_DISPLAY))
    clock = pygame.time.Clock()
    watching = True    
    # Connect to the server
    socks = []
    for host, port in zip(hosts, ports):
        socks.append(socket())
        socks[-1].connect((host, port))
    # Run
    try:
        hostsLen = len(hosts)
        N_ROWS = int(math.ceil(hostsLen/MAX_IN_ONE_ROW))
        WIDTH_ONEWINDOW = int(WIDTH_DISPLAY/MAX_IN_ONE_ROW)
        HEIGHT_ONEWINDOW = int(HEIGHT_DISPLAY/N_ROWS)
        if N_ROWS == 1:
            WIDTH_ONEWINDOW = int(WIDTH_DISPLAY/hostsLen)
        while watching:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    watching = False
                    break
            imgs_socks = []
            for sock in socks:
                # Retreive the size of the pixels length, the pixels length and pixels
                size_len = int.from_bytes(sock.recv(1), byteorder="big")
                size = int.from_bytes(sock.recv(size_len), byteorder="big")
                pixels = decompress(ReceiveAllPixels(sock, size))
                # Create the Surface from raw pixels
                img = pygame.image.fromstring(pixels, (WIDTH_IN, HEIGHT_IN), "RGB")
                img = pygame.transform.scale(img, (HEIGHT_ONEWINDOW, WIDTH_ONEWINDOW))
                imgs_socks.append(img)
            # Display Image
            for i in range(N_ROWS):
                for j in range(MAX_IN_ONE_ROW):
                    ind = i*MAX_IN_ONE_ROW + j
                    if ind >= hostsLen:
                        break
                    screen.blit(imgs_socks[ind], (j*WIDTH_ONEWINDOW, i*HEIGHT_ONEWINDOW))
            pygame.display.flip()
            clock.tick(60)
    finally:
        for sock in socks:
            sock.close()