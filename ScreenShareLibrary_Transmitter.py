'''
Screen Sharing Library for Transmitter
'''

# Imports
from socket import socket
from threading import Thread
from zlib import compress
from mss import mss

# Main Parameters
WIDTH_OUT = 1920
HEIGHT_OUT = 1080

# Main Functions
def getScreenshot(conn):
    with mss() as sct:
        # The region to capture
        rect = {'top': 0, 'left': 0, 'width': WIDTH_OUT, 'height': HEIGHT_OUT}

        while 'recording':
            # Capture the screen
            img = sct.grab(rect)
            # Tweak the compression level here (0-9)
            pixels = compress(img.rgb, 6)

            # Send the size of the pixels length
            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))

            # Send the actual pixels length
            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)

            # Send pixels
            conn.sendall(pixels)

def ScreenShareServer(host='0.0.0.0', port=5000):
    sock = socket()
    sock.bind((host, port))
    try:
        sock.listen(5)
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            thread = Thread(target=getScreenshot, args=(conn,))
            thread.start()
    finally:
        sock.close()

# Driver Code
