import sys
import struct
import ctypes
from sdl2 import *

windowsizex = 160
windowsizey = 120
bpp = 4

def CopytToTarget(waterBuffer, pixelBuffer):
    for y in range(windowsizey):
        for x in range(windowsizex):
            waterHeight = int(waterBuffer[y*windowsizex +x])

            remappedColor = int((waterHeight - -255) / (255 - -255) * (255 - 0))
            SetColor(pixelBuffer, x, y, remappedColor, remappedColor, remappedColor, 255)

def SetColor(buffer, x, y, r, g, b, a):
    lookupStart = (y*windowsizex*bpp) + (x*bpp)

    buffer[lookupStart] = r
    buffer[lookupStart + 1] = g
    buffer[lookupStart + 2] = b
    buffer[lookupStart + 3] = a

def Smoothen(buffer, index):
    return (buffer[index-1] + buffer[index+1] + buffer[index-windowsizex] + buffer[index+windowsizex]) / 4

def ProcessWater(source, destination):
    damping = 0.9
    start = windowsizex
    end = (windowsizex*windowsizey) - windowsizex
    for index in range(start, end):
        destination[index] = Smoothen(source, index) * 2 - destination[index]
        destination[index] *= damping


def main():
    SDL_Init(SDL_INIT_VIDEO)
    window = SDL_CreateWindow(b"Water ripples", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, windowsizex, windowsizey, SDL_WINDOW_SHOWN)
    
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)
    texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_ABGR8888, SDL_TEXTUREACCESS_STATIC, windowsizex, windowsizey)

    size = bpp*windowsizex*windowsizey
    pixelBuffer = bytearray(size)
    for y in range(windowsizey):
        for x in range(windowsizex): 
            SetColor(pixelBuffer, x, y, 0,0,0,255)

    # Setup buffers
    waterBuffer1 = [0] * (windowsizex*windowsizey)
    waterBuffer2 = [0] * (windowsizex*windowsizey)
    currentSource = True

    leftMouseButtonDown = False
    running = True
    event = SDL_Event()
    while running:

        # Update the water
        if currentSource:
            ProcessWater(waterBuffer1, waterBuffer2)
            CopytToTarget(waterBuffer2, pixelBuffer)
            currentSource = False
        else:
            ProcessWater(waterBuffer2, waterBuffer1)
            CopytToTarget(waterBuffer1, pixelBuffer)
            currentSource = True

        pointer = ctypes.cast(c_char_p(bytes(pixelBuffer)), ctypes.c_void_p)
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
                    if currentSource:
                        waterBuffer1[event.button.y*windowsizex + event.button.x] = 255
                    else:
                        waterBuffer2[event.button.y*windowsizex + event.button.x] = 255
                break
        
        SDL_RenderClear(renderer)
        SDL_RenderCopy(renderer, texture, None, None)
        SDL_RenderPresent(renderer)

    SDL_DestroyWindow(window)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())