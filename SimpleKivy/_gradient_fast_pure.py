# gradient_fast_pure.py
from kivy.graphics.texture import Texture
from math import cos, sin, radians, atan2, pi, sqrt
from array import array

# ------------------------------------------------------------
# Cache normalized grids by (width, height)
# ------------------------------------------------------------
_grid_cache = {}

def get_grid(size):
    if size in _grid_cache:
        return _grid_cache[size]
    w, h = size
    inv_w = 1.0 / (w - 1) if w > 1 else 0
    inv_h = 1.0 / (h - 1) if h > 1 else 0
    xs = [x * inv_w for x in range(w)]
    ys = [y * inv_h for y in range(h)]
    _grid_cache[size] = (xs, ys)
    return xs, ys


# ------------------------------------------------------------
# Parse color stops (supports mixed explicit/implicit)
# ------------------------------------------------------------
def parse_color_stops(colors):
    parsed_colors = []
    parsed_stops = []

    for item in colors:
        if isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[1], (int, float)):
            parsed_colors.append(tuple(float(x) for x in item[0]))
            parsed_stops.append(float(item[1]))
        elif isinstance(item, (list, tuple)) and len(item) in (3, 4):
            parsed_colors.append(tuple(float(x) for x in item))
            parsed_stops.append(None)
        else:
            raise ValueError(f"Invalid color stop format: {item}")

    n = len(parsed_colors)
    if all(s is None for s in parsed_stops):
        parsed_stops = [i / (n - 1) if n > 1 else 0 for i in range(n)]
    else:
        known = [i for i, s in enumerate(parsed_stops) if s is not None]
        if not known:
            parsed_stops = [i / (n - 1) if n > 1 else 0 for i in range(n)]
        else:
            # Fill between known stops
            for i in range(1, len(known)):
                a, b = known[i - 1], known[i]
                sa, sb = parsed_stops[a], parsed_stops[b]
                step = (sb - sa) / (b - a)
                for j in range(a + 1, b):
                    parsed_stops[j] = sa + step * (j - a)
            # Before first
            first = known[0]
            if first > 0:
                s0 = parsed_stops[first]
                for i in range(first):
                    parsed_stops[i] = s0 * (i / first)
            # After last
            last = known[-1]
            if last < n - 1:
                sl = parsed_stops[last]
                for i in range(last + 1, n):
                    parsed_stops[i] = sl + (1 - sl) * (i - last) / (n - last)

    # Clamp and sort
    stops = [max(0.0, min(1.0, s)) for s in parsed_stops]
    zipped = sorted(zip(stops, parsed_colors), key=lambda x: x[0])
    stops_sorted, colors_sorted = zip(*zipped)
    return list(colors_sorted), list(stops_sorted)


# ------------------------------------------------------------
# Fast linear interpolation between stops
# ------------------------------------------------------------
def interp_color(value, stops, colors):
    if value <= stops[0]:
        return colors[0]
    if value >= stops[-1]:
        return colors[-1]

    for i in range(len(stops) - 1):
        t0, t1 = stops[i], stops[i + 1]
        if value <= t1:
            f = (value - t0) / (t1 - t0 + 1e-9)
            c0, c1 = colors[i], colors[i + 1]
            return (
                c0[0] + (c1[0] - c0[0]) * f,
                c0[1] + (c1[1] - c0[1]) * f,
                c0[2] + (c1[2] - c0[2]) * f,
                c0[3] + (c1[3] - c0[3]) * f,
            )
    return colors[-1]


# ------------------------------------------------------------
# LINEAR GRADIENT
# ------------------------------------------------------------
def linear_gradient(size, colors, angle=0):
    width, height = size
    xs, ys = get_grid(size)
    colors, stops = parse_color_stops(colors)

    a = radians(angle)
    dx, dy = cos(a), sin(a)
    pixels = array("B")
    append = pixels.extend
    ic = interp_color

    for y in ys:
        for x in xs:
            t = x * dx + y * dy
            if t < 0.0: t = 0.0
            elif t > 1.0: t = 1.0
            r, g, b, a = ic(t, stops, colors)
            append((int(r * 255), int(g * 255), int(b * 255), int(a * 255)))

    # tex = Texture.create(size=(width, height))
    # tex.blit_buffer(pixels.tobytes(), colorfmt="rgba", bufferfmt="ubyte")
    # tex.wrap = "clamp_to_edge"
    # return tex
    return pixels.tobytes()


# ------------------------------------------------------------
# RADIAL GRADIENT
# ------------------------------------------------------------
def radial_gradient(size, colors, center=(0.5, 0.5), radius=0.5, shape="ellipse"):
    width, height = size
    xs, ys = get_grid(size)
    colors, stops = parse_color_stops(colors)
    cx, cy = center

    pixels = array("B")
    append = pixels.extend
    ic = interp_color

    if shape == "circle":
        for y in ys:
            dy = y - cy
            for x in xs:
                t = sqrt((x - cx)**2 + dy**2) / radius
                if t > 1.0: t = 1.0
                elif t < 0.0: t = 0.0
                r, g, b, a = ic(t, stops, colors)
                append((int(r * 255), int(g * 255), int(b * 255), int(a * 255)))
    else:
        if isinstance(radius, (tuple, list)):
            rx, ry = radius
        else:
            rx = ry = radius
        inv_rx2 = 1.0 / (rx * rx)
        inv_ry2 = 1.0 / (ry * ry)
        for y in ys:
            dy = y - cy
            dy2 = dy * dy * inv_ry2
            for x in xs:
                dx = x - cx
                dist = sqrt(dx * dx * inv_rx2 + dy2)
                if dist > 1.0: dist = 1.0
                elif dist < 0.0: dist = 0.0
                r, g, b, a = ic(dist, stops, colors)
                append((int(r * 255), int(g * 255), int(b * 255), int(a * 255)))

    # tex = Texture.create(size=(width, height))
    # tex.blit_buffer(pixels.tobytes(), colorfmt="rgba", bufferfmt="ubyte")
    # tex.wrap = "clamp_to_edge"
    # return tex
    return pixels.tobytes()

# ------------------------------------------------------------
# CONIC GRADIENT
# ------------------------------------------------------------
def conic_gradient(size, colors, center=(0.5, 0.5), angle_offset=0):
    width, height = size
    xs, ys = get_grid(size)
    colors, stops = parse_color_stops(colors)
    cx, cy = center
    offset = radians(angle_offset)
    twopi = 2 * pi

    pixels = array("B")
    append = pixels.extend
    ic = interp_color

    for y in ys:
        dy = y - cy
        for x in xs:
            t = (atan2(dy, x - cx) + offset) % twopi / twopi
            r, g, b, a = ic(t, stops, colors)
            append((int(r * 255), int(g * 255), int(b * 255), int(a * 255)))

    # tex = Texture.create(size=(width, height))
    # tex.blit_buffer(pixels.tobytes(), colorfmt="rgba", bufferfmt="ubyte")
    # tex.wrap = "repeat"
    # return tex
    return pixels.tobytes()


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
