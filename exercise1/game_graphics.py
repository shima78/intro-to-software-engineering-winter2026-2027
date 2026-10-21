import math
import pygame

# Colors used for the drawings
ASPHALT = (60, 60, 65)
GRASS = (40, 140, 60)
LANE_WHITE = (230, 230, 230)
TIRE = (25, 25, 25)
GLASS = (150, 210, 255)
HEADLIGHT = (255, 245, 170)
TAILLIGHT = (220, 30, 30)

ROAD_MARGIN = 20
LANE_COUNT = 4
DASH_LENGTH, DASH_GAP = 40, 30


# Make a color darker (factor < 1) or lighter (factor > 1)
def shade(color, factor):
    return tuple(max(0, min(255, int(c * factor))) for c in color)


# Draw the road with moving lane markings; "scroll" shifts the dashes downwards
def draw_road(win, scroll):
    width, height = win.get_size()
    win.fill(GRASS)
    pygame.draw.rect(win, ASPHALT, (ROAD_MARGIN, 0, width - 2 * ROAD_MARGIN, height))

    # Solid lines at the road edges
    pygame.draw.rect(win, LANE_WHITE, (ROAD_MARGIN, 0, 4, height))
    pygame.draw.rect(win, LANE_WHITE, (width - ROAD_MARGIN - 4, 0, 4, height))

    # Dashed lines between the lanes
    lane_width = (width - 2 * ROAD_MARGIN) / LANE_COUNT
    period = DASH_LENGTH + DASH_GAP
    for lane in range(1, LANE_COUNT):
        x = ROAD_MARGIN + lane * lane_width - 2
        y = scroll % period - period
        while y < height:
            pygame.draw.rect(win, LANE_WHITE, (x, y, 4, DASH_LENGTH))
            y += period


# Return a transparent surface with a vehicle seen from above.
# The vehicle faces upwards; set facing_down=True for oncoming traffic.
def draw_vehicle(width, height, color, kind="car", facing_down=False):
    surface = pygame.Surface([width, height], pygame.SRCALPHA)

    if kind == "truck":
        _draw_truck(surface, width, height, color)
    elif kind == "bus":
        _draw_bus(surface, width, height, color)
    elif kind == "motorcycle":
        _draw_motorcycle(surface, width, height, color)
    else:
        _draw_car(surface, width, height, color)

    if facing_down:
        surface = pygame.transform.flip(surface, False, True)
    return surface


def _draw_wheels(surface, width, y_positions, wheel_w, wheel_h):
    for y in y_positions:
        pygame.draw.rect(surface, TIRE, (0, y, wheel_w, wheel_h), border_radius=3)
        pygame.draw.rect(surface, TIRE, (width - wheel_w, y, wheel_w, wheel_h), border_radius=3)


def _draw_car(surface, w, h, color):
    wheel_w, wheel_h = max(4, w // 8), h // 5
    _draw_wheels(surface, w, [h * 0.15, h * 0.68], wheel_w, wheel_h)

    # Body, roof and windows
    body = pygame.Rect(wheel_w // 2, 0, w - wheel_w, h)
    pygame.draw.rect(surface, color, body, border_radius=w // 4)
    pygame.draw.rect(surface, shade(color, 0.6), body, width=2, border_radius=w // 4)
    pygame.draw.rect(surface, GLASS, (w * 0.22, h * 0.22, w * 0.56, h * 0.16), border_radius=4)
    pygame.draw.rect(surface, shade(color, 0.8), (w * 0.22, h * 0.38, w * 0.56, h * 0.32), border_radius=4)
    pygame.draw.rect(surface, GLASS, (w * 0.25, h * 0.70, w * 0.50, h * 0.10), border_radius=4)

    # Headlights at the front, taillights at the back
    light_w, light_h = w * 0.18, h * 0.05
    pygame.draw.rect(surface, HEADLIGHT, (w * 0.18, 2, light_w, light_h), border_radius=2)
    pygame.draw.rect(surface, HEADLIGHT, (w * 0.82 - light_w, 2, light_w, light_h), border_radius=2)
    pygame.draw.rect(surface, TAILLIGHT, (w * 0.18, h - light_h - 2, light_w, light_h), border_radius=2)
    pygame.draw.rect(surface, TAILLIGHT, (w * 0.82 - light_w, h - light_h - 2, light_w, light_h), border_radius=2)


def _draw_truck(surface, w, h, color):
    wheel_w, wheel_h = max(5, w // 10), h // 10
    _draw_wheels(surface, w, [h * 0.08, h * 0.55, h * 0.68, h * 0.84], wheel_w, wheel_h)

    # Cab at the front with a windshield
    cab_h = h * 0.22
    pygame.draw.rect(surface, color, (wheel_w // 2, 0, w - wheel_w, cab_h), border_radius=8)
    pygame.draw.rect(surface, GLASS, (w * 0.15, cab_h * 0.15, w * 0.70, cab_h * 0.30), border_radius=3)
    pygame.draw.rect(surface, HEADLIGHT, (w * 0.12, 2, w * 0.15, 5), border_radius=2)
    pygame.draw.rect(surface, HEADLIGHT, (w * 0.73, 2, w * 0.15, 5), border_radius=2)

    # Trailer with roof ribs
    trailer = pygame.Rect(wheel_w // 2, cab_h + 4, w - wheel_w, h - cab_h - 4)
    pygame.draw.rect(surface, shade(color, 0.75), trailer, border_radius=3)
    pygame.draw.rect(surface, shade(color, 0.5), trailer, width=2, border_radius=3)
    for y in range(int(trailer.top + 15), trailer.bottom - 5, 20):
        pygame.draw.line(surface, shade(color, 0.6), (trailer.left + 4, y), (trailer.right - 4, y), 2)
    pygame.draw.rect(surface, TAILLIGHT, (trailer.left + 3, h - 6, 10, 4))
    pygame.draw.rect(surface, TAILLIGHT, (trailer.right - 13, h - 6, 10, 4))


def _draw_bus(surface, w, h, color):
    wheel_w, wheel_h = max(5, w // 10), h // 10
    _draw_wheels(surface, w, [h * 0.12, h * 0.75], wheel_w, wheel_h)

    body = pygame.Rect(wheel_w // 2, 0, w - wheel_w, h)
    pygame.draw.rect(surface, color, body, border_radius=10)
    pygame.draw.rect(surface, shade(color, 0.6), body, width=2, border_radius=10)
    pygame.draw.rect(surface, GLASS, (w * 0.15, 6, w * 0.70, h * 0.07), border_radius=4)

    # Row of side windows along both edges
    for y in range(int(h * 0.15), int(h * 0.92), 22):
        pygame.draw.rect(surface, GLASS, (body.left + 3, y, 6, 16), border_radius=2)
        pygame.draw.rect(surface, GLASS, (body.right - 9, y, 6, 16), border_radius=2)

    # Air conditioning unit on the roof
    pygame.draw.rect(surface, shade(color, 0.8), (w * 0.30, h * 0.40, w * 0.40, h * 0.15), border_radius=4)
    pygame.draw.rect(surface, HEADLIGHT, (w * 0.15, 1, w * 0.15, 4), border_radius=2)
    pygame.draw.rect(surface, HEADLIGHT, (w * 0.70, 1, w * 0.15, 4), border_radius=2)


def _draw_motorcycle(surface, w, h, color):
    # Wheels in front of and behind the body
    pygame.draw.ellipse(surface, TIRE, (w * 0.3, 0, w * 0.4, h * 0.28))
    pygame.draw.ellipse(surface, TIRE, (w * 0.3, h * 0.72, w * 0.4, h * 0.28))

    # Body, handlebar and rider
    pygame.draw.ellipse(surface, color, (w * 0.15, h * 0.18, w * 0.7, h * 0.64))
    pygame.draw.line(surface, TIRE, (0, h * 0.25), (w, h * 0.25), 3)
    pygame.draw.circle(surface, shade(color, 0.5), (w // 2, int(h * 0.45)), w // 3)
    pygame.draw.circle(surface, GLASS, (w // 2, int(h * 0.45) - w // 6), w // 8)
    pygame.draw.circle(surface, HEADLIGHT, (w // 2, 3), 3)


# Draw a star-shaped crash burst centered on "center"
def _draw_crash(win, center, radius):
    for color, scale in [((255, 120, 0), 1.0), ((255, 220, 0), 0.6), ((255, 255, 255), 0.25)]:
        points = []
        for i in range(16):
            r = radius * scale * (1.0 if i % 2 == 0 else 0.5)
            angle = math.pi * i / 8
            points.append((center[0] + r * math.cos(angle), center[1] + r * math.sin(angle)))
        pygame.draw.polygon(win, color, points)


_fonts = {}


# Load each font size only once instead of every frame
def _font(size):
    if size not in _fonts:
        _fonts[size] = pygame.font.Font(None, size)
    return _fonts[size]


# Render text with a drop shadow at (x, y); x=None centers it horizontally
def _draw_text(win, text, size, color, y, x=None):
    font = _font(size)
    shadow = font.render(text, True, (0, 0, 0))
    label = font.render(text, True, color)
    if x is None:
        x = (win.get_width() - label.get_width()) // 2
    win.blit(shadow, (x + 2, y + 2))
    win.blit(label, (x, y))


# Draw a semi-transparent rounded box
def _draw_box(win, rect, alpha=160):
    box = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(box, (0, 0, 0, alpha), box.get_rect(), border_radius=10)
    win.blit(box, rect.topleft)


# Show score, time and speed in the top left corner and the best score in the top right
def draw_hud(win, stats):
    _draw_box(win, pygame.Rect(30, 10, 170, 90))
    _draw_text(win, f"Score: {stats['score']}", 30, LANE_WHITE, 18, 42)
    _draw_text(win, f"Time: {stats['time']:.1f} s", 30, LANE_WHITE, 45, 42)
    _draw_text(win, f"Speed: {stats['speed']}", 30, LANE_WHITE, 72, 42)

    best = _font(30).size(f"Best: {stats['best']}")[0]
    _draw_box(win, pygame.Rect(win.get_width() - best - 54, 10, best + 24, 36))
    _draw_text(win, f"Best: {stats['best']}", 30, HEADLIGHT, 18, win.get_width() - best - 42)


# Dim the current frame and show a "game over" panel with the round's stats on top of it
def draw_game_over(win, crash_point, stats):
    width, height = win.get_size()

    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    win.blit(overlay, (0, 0))

    if crash_point is not None:
        _draw_crash(win, crash_point, 45)

    panel = pygame.Rect(0, 0, width * 0.8, 330)
    panel.center = (width // 2, height // 2)
    pygame.draw.rect(win, (30, 30, 40), panel, border_radius=20)
    pygame.draw.rect(win, (220, 40, 40), panel, width=5, border_radius=20)

    _draw_text(win, "GAME OVER", 96, (255, 70, 60), panel.top + 30)
    _draw_text(win, f"Vehicles dodged: {stats['score']}", 40, LANE_WHITE, panel.top + 115)
    _draw_text(win, f"Time survived: {stats['time']:.1f} s", 40, LANE_WHITE, panel.top + 155)
    _draw_text(win, f"Top speed: {stats['speed']}", 40, LANE_WHITE, panel.top + 195)
    if stats["new_best"]:
        _draw_text(win, "NEW BEST!", 44, HEADLIGHT, panel.top + 238)
    else:
        _draw_text(win, f"Best: {stats['best']}", 40, HEADLIGHT, panel.top + 238)
    _draw_text(win, "SPACE: play again    ESC: quit", 32, (170, 170, 180), panel.top + 290)
