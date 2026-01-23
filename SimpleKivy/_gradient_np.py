from kivy.graphics.texture import Texture
from math import cos, sin, radians, atan2, pi
import numpy as np

# ------------------------------------------------------------
# Cache grid coordinates per size for reuse
# ------------------------------------------------------------
_grid_cache = {}

def get_grid(size):
    """Return normalized X,Y grids from cache or compute new ones."""
    if size in _grid_cache:
        return _grid_cache[size]
    w, h = size
    y, x = np.mgrid[0:h, 0:w]
    x = x / (w - 1)
    y = y / (h - 1)
    _grid_cache[size] = (x, y)
    return x, y


# ------------------------------------------------------------
# Parse color stops (supports mixed explicit/implicit)
# ------------------------------------------------------------
def parse_color_stops(colors):
    parsed_colors = []
    parsed_stops = []

    for item in colors:
        if isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[1], (int, float)):
            parsed_colors.append(np.array(item[0], dtype=np.float32))
            parsed_stops.append(float(item[1]))
        elif isinstance(item, (list, tuple)) and len(item) in (3, 4):
            parsed_colors.append(np.array(item, dtype=np.float32))
            parsed_stops.append(None)
        else:
            raise ValueError(f"Invalid color stop: {item}")

    n = len(parsed_colors)
    if all(s is None for s in parsed_stops):
        parsed_stops = np.linspace(0, 1, n, dtype=np.float32)
    else:
        # Interpolate missing stops linearly
        known = [i for i, s in enumerate(parsed_stops) if s is not None]
        if not known:
            parsed_stops = np.linspace(0, 1, n, dtype=np.float32)
        else:
            for i in range(1, len(known)):
                a, b = known[i-1], known[i]
                sa, sb = parsed_stops[a], parsed_stops[b]
                step = (sb - sa) / (b - a)
                for j in range(a+1, b):
                    parsed_stops[j] = sa + step * (j - a)
            # Before first
            first = known[0]
            for i in range(first):
                parsed_stops[i] = max(0, parsed_stops[first] * i / first)
            # After last
            last = known[-1]
            for i in range(last+1, n):
                parsed_stops[i] = parsed_stops[last] + (1 - parsed_stops[last]) * (i - last) / (n - last)

    stops = np.clip(parsed_stops, 0, 1)
    sort_idx = np.argsort(stops)
    colors_sorted = np.array([parsed_colors[i] for i in sort_idx], dtype=np.float32)
    stops_sorted = np.array(stops)[sort_idx]
    return colors_sorted, stops_sorted


# ------------------------------------------------------------
# Vectorized interpolation helper
# ------------------------------------------------------------
def interpolate_gradient(grad, colors, stops):
    """Fast vectorized gradient interpolation using np.interp."""
    flat = grad.ravel()
    out = np.empty((flat.size, 4), dtype=np.float32)
    for c in range(4):
        out[:, c] = np.interp(flat, stops, colors[:, c])
    return (out.reshape((*grad.shape, 4)) * 255).astype(np.uint8)


# ------------------------------------------------------------
# LINEAR GRADIENT
# ------------------------------------------------------------
def linear_gradient(size, colors, angle=0):
    width, height = size
    x, y = get_grid(size)
    a = radians(angle)
    grad = np.clip(x * cos(a) + y * sin(a), 0, 1)
    colors, stops = parse_color_stops(colors)
    rgba = interpolate_gradient(grad, colors, stops)

    # tex = Texture.create(size=(width, height))
    # tex.blit_buffer(rgba.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
    # tex.wrap = 'clamp_to_edge'
    return rgba.tobytes()


# ------------------------------------------------------------
# RADIAL GRADIENT (circle/ellipse)
# ------------------------------------------------------------
def radial_gradient(size, colors, center=(0.5, 0.5), radius=0.5, shape='ellipse'):
    width, height = size
    x, y = get_grid(size)
    cx, cy = center
    if shape == 'circle':
        dist = np.sqrt((x - cx)**2 + (y - cy)**2) / radius
    else:
        if isinstance(radius, (tuple, list)):
            rx, ry = radius
        else:
            rx = ry = radius
        dist = np.sqrt(((x - cx)/rx)**2 + ((y - cy)/ry)**2)
    grad = np.clip(dist, 0, 1)

    colors, stops = parse_color_stops(colors)
    rgba = interpolate_gradient(grad, colors, stops)

    # tex = Texture.create(size=(width, height))
    # tex.blit_buffer(rgba.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
    # tex.wrap = 'clamp_to_edge'
    # return tex
    return rgba.tobytes()


# ------------------------------------------------------------
# CONIC GRADIENT
# ------------------------------------------------------------
def conic_gradient(size, colors, center=(0.5, 0.5), angle_offset=0):
    width, height = size
    x, y = get_grid(size)
    cx, cy = center
    angle = np.arctan2(y - cy, x - cx)
    angle = (angle + radians(angle_offset)) % (2 * pi)
    grad = angle / (2 * pi)

    colors, stops = parse_color_stops(colors)
    rgba = interpolate_gradient(grad, colors, stops)

    # tex = Texture.create(size=(width, height))
    # tex.blit_buffer(rgba.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
    # tex.wrap = 'repeat'
    # return tex
    return rgba.tobytes()


# ------------------------------------------------------------
# GRADIENT REGISTRY
# ------------------------------------------------------------
class Gradient:
    registry = {
        "linear-gradient": linear_gradient,
        "radial-gradient": radial_gradient,
        "conic-gradient": conic_gradient,
    }

    @staticmethod
    def create(gradient_type, **kwargs):
        func = Gradient.registry.get(gradient_type)
        if not func:
            raise ValueError(f"Unknown gradient type: {gradient_type}")
        return func(**kwargs)
