import sys
import struct
import ctypes
from sdl2 import *

windowsizex = 640
windowsizey = 480
bpp = 4

def SetColor(buffer, x, y, r, g, b, a):
    lookupStart = (y*windowsizex*bpp) + (x*bpp)

    buffer[lookupStart] = r
    buffer[lookupStart + 1] = g
    buffer[lookupStart + 2] = b
    buffer[lookupStart + 3] = a

def main():
    SDL_Init(SDL_INIT_VIDEO)
    window = SDL_CreateWindow(b"Water ripples", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, windowsizex, windowsizey, SDL_WINDOW_SHOWN)
    
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)
    texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_ABGR8888, SDL_TEXTUREACCESS_STATIC, windowsizex, windowsizey)

    size = bpp*windowsizex*windowsizey
    buffer = bytearray(size)
    for y in range(windowsizey):
        for x in range(windowsizex): 
            SetColor(buffer, x, y, 0,0,0,255)

    leftMouseButtonDown = False
    running = True
    event = SDL_Event()
    while running:
        pointer = ctypes.cast(c_char_p(bytes(buffer)), ctypes.c_void_p)
        SDL_UpdateTexture(texture, None, pointer, windowsizex*bpp)
        
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                break
            if event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_ESCAPE:
                    running = False
                break
            if event.type == SDL_MOUSEBUTTONUP:
                if event.button.button == SDL_BUTTON_LEFT:
                    leftMouseButtonDown = False
                break
            if event.type == SDL_MOUSEBUTTONDOWN:
                if event.button.button == SDL_BUTTON_LEFT:
                    leftMouseButtonDown = True
                break
            if event.type == SDL_MOUSEMOTION:
                if leftMouseButtonDown:
                    SetColor(buffer, event.motion.x, event.motion.y, 255, 255, 255, 255)
                break
        
        SDL_RenderClear(renderer)
        SDL_RenderCopy(renderer, texture, None, None)
        SDL_RenderPresent(renderer)

    SDL_DestroyWindow(window)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())