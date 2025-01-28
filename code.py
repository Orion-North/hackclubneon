import time
import random
import math
import board
import displayio
import framebufferio
import rgbmatrix

displayio.release_displays()

# --- Setup the RGB matrix ---
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=3,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13,
    latch_pin=board.D0,
    output_enable_pin=board.D1
)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

# --- CONFIGURATION ---
neon_text = "NEON SIGN"  # Change this to your desired text

# Simple 5x7 font for drawing letters and symbols
font = {
    "A": ["  #  ", " # # ", "#####", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#### ", "#   #", "#### "],
    "C": [" ### ", "#    ", "#    ", "#    ", " ### "],
    "D": ["#### ", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#####", "#    ", "#####"],
    "F": ["#####", "#    ", "#####", "#    ", "#    "],
    "G": [" ### ", "#    ", "#  ##", "#   #", " ### "],
    "H": ["#   #", "#   #", "#####", "#   #", "#   #"],
    "I": [" ### ", "  #  ", "  #  ", "  #  ", " ### "],
    "J": ["  ###", "   # ", "   # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "###  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#### ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "#  ##", " ####"],
    "R": ["#### ", "#   #", "#### ", "#  # ", "#   #"],
    "S": [" ####", "#    ", " ### ", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "# # #", "## ##", "#   #"],
    "X": ["#   #", " # # ", "  #  ", " # # ", "#   #"],
    "Y": ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "   # ", "  #  ", " #   ", "#####"],
    "0": [" ### ", "#   #", "#   #", "#   #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", " ### "],
    "2": [" ### ", "#   #", "   # ", "  #  ", "#####"],
    "3": ["#####", "    #", " ### ", "    #", "#####"],
    "4": ["   # ", "  ## ", " # # ", "#####", "   # "],
    "5": ["#####", "#    ", "#### ", "    #", "#### "],
    "6": [" ### ", "#    ", "#### ", "#   #", " ### "],
    "7": ["#####", "    #", "   # ", "  #  ", "  #  "],
    "8": [" ### ", "#   #", " ### ", "#   #", " ### "],
    "9": [" ### ", "#   #", " ####", "    #", " ### "],
    "!": ["  #  ", "  #  ", "  #  ", "     ", "  #  "],
    "?": [" ### ", "#   #", "   # ", "  #  ", "  #  "],
    ":": ["     ", "  #  ", "     ", "  #  ", "     "],
    " ": ["     ", "     ", "     ", "     ", "     "],  # Space
}


# Calculate matrix size
MATRIX_WIDTH = 64
MATRIX_HEIGHT = 32

# Create palette with multiple brightness levels
palette = displayio.Palette(5)
palette[0] = 0x000000  # Off
palette[1] = 0x330033  # Dim purple
palette[2] = 0x660066  # Medium purple
palette[3] = 0x990099  # Bright purple
palette[4] = 0xFF00FF  # Full neon magenta

# Create the bitmap and tile grid
bitmap = displayio.Bitmap(MATRIX_WIDTH, MATRIX_HEIGHT, len(palette))
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group()
group.append(tile_grid)
display.root_group = group

# Clear bitmap
def clear_bitmap(bmp):
    for i in range(bmp.width * bmp.height):
        bmp[i] = 0

# Helper to draw scaled letters
def draw_letter(bmp, letter, x, y, scale, color_index):
    if letter not in font:
        return  # Skip unsupported characters
    for row, line in enumerate(font[letter]):
        for col, pixel in enumerate(line):
            if pixel == "#":
                # Scale each pixel to fit the desired size
                for dx in range(scale):
                    for dy in range(scale):
                        draw_x = x + col * scale + dx
                        draw_y = y + row * scale + dy
                        if 0 <= draw_x < bmp.width and 0 <= draw_y < bmp.height:
                            bmp[draw_x, draw_y] = color_index

# Helper to draw text, scaled to fit
def draw_scaled_text(bmp, text, color_index):
    # Calculate scaling factor to fit the text
    text_width = len(text) * 5  # Each letter is 5 units wide
    text_height = 7  # Each letter is 7 units tall
    scale_x = MATRIX_WIDTH // (text_width + len(text) - 1)  # Include spacing
    scale_y = MATRIX_HEIGHT // text_height
    scale = min(scale_x, scale_y)  # Uniform scaling factor

    # Calculate centered starting position
    total_text_width = (text_width + len(text) - 1) * scale
    x_start = (MATRIX_WIDTH - total_text_width) // 2
    y_start = (MATRIX_HEIGHT - text_height * scale) // 2

    # Draw each letter
    for i, char in enumerate(text):
        draw_letter(bmp, char, x_start + i * (5 * scale + scale), y_start, scale, color_index)

# Flicker effect
def flicker_effect(bmp, text):
    flicks = random.randint(1, 4)
    for _ in range(flicks):
        flick_brightness = random.randint(0, 4)
        clear_bitmap(bmp)
        draw_scaled_text(bmp, text, flick_brightness)
        time.sleep(random.uniform(0.02, 0.2))  # short bursts
    stable_brightness = random.choice([2, 3, 4])
    clear_bitmap(bmp)
    draw_scaled_text(bmp, text, stable_brightness)

# Main loop
while True:
    # Flicker occasionally
    flicker_chance = random.random()
    if flicker_chance < 0.3:
        flicker_effect(bitmap, neon_text)
    else:
        # Subtle glow shift
        for _ in range(random.randint(5, 15)):
            brightness = random.choice([2, 3, 4])  # Mid to bright
            clear_bitmap(bitmap)
            draw_scaled_text(bitmap, neon_text, brightness)
            time.sleep(0.05)
    time.sleep(random.uniform(0.5, 2))  # Take a short break, then repeat
