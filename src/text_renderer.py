"""
Cross-platform Quran text renderer using Pillow with Arabic reshaping.

Replaces the previous Windows-only GDI renderer with a portable solution
that uses arabic_reshaper + python-bidi for correct Arabic glyph shaping
and Pillow for rendering.
"""

from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# Cache loaded fonts to avoid repeated disk reads
_font_cache = {}


def load_private_font(font_path):
    """
    Load a font file for later use.
    With Pillow this is a no-op since truetype() loads on demand,
    but we keep the interface for compatibility.
    """
    if not isinstance(font_path, str):
        font_path = str(font_path)
    # Pre-cache at a default size to verify the file is valid
    try:
        _font_cache[font_path] = ImageFont.truetype(font_path, 50)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to load font {font_path}: {e}")
        return False


def _get_font(font_path, size):
    """Get a font object, using cache when possible."""
    key = (font_path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(font_path, size)
    return _font_cache[key]


def _reshape_arabic(text):
    """Apply Arabic reshaping and bidi reordering for correct display."""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


def _wrap_text(text, font, max_width, draw):
    """
    Word-wrap Arabic text to fit within max_width.
    Returns a list of lines.
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = word if not current_line else current_line + " " + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines if lines else [text]


def render_text_to_image(text, font_path, font_size, width, height,
                         text_color=(255, 255, 255)):
    """
    Render Arabic text to a PIL RGBA Image with transparent background.

    Uses arabic_reshaper + python-bidi for correct glyph shaping,
    then Pillow for rasterisation. Works on all platforms.

    Args:
        text: Raw Uthmani Arabic text.
        font_path: Path to the .ttf font file (not a face name).
        font_size: Font size in pixels.
        width, height: Canvas dimensions.
        text_color: RGB tuple for the text colour.

    Returns:
        PIL.Image in RGBA mode.
    """
    # Reshape Arabic text for correct glyph rendering
    display_text = _reshape_arabic(text)

    font = _get_font(font_path, font_size)

    # Use a scratch image for measurement
    scratch = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scratch)

    margin = 50
    max_width = width - (margin * 2)

    # Word-wrap
    lines = _wrap_text(display_text, font, max_width, draw)

    # Measure total text block height
    line_spacing = int(font_size * 0.35)
    total_height = 0
    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        h = bbox[3] - bbox[1]
        line_heights.append(h)
        total_height += h
    total_height += line_spacing * max(0, len(lines) - 1)

    # Create final transparent image
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Vertical centering
    y = max(margin, (height - total_height) // 2)

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        # Horizontal centering
        x = (width - line_width) // 2

        # Draw shadow for readability
        shadow_offset = max(2, font_size // 30)
        draw.text((x + shadow_offset, y + shadow_offset), line, font=font,
                  fill=(0, 0, 0, 160))

        # Draw main text
        draw.text((x, y), line, font=font, fill=text_color + (255,))

        y += line_heights[i] + line_spacing

    return img


def measure_text_height(text, font_path, font_size, width):
    """
    Measure the height of wrapped Arabic text for a given width and font size.
    Returns the calculated height in pixels.
    """
    display_text = _reshape_arabic(text)
    font = _get_font(font_path, font_size)

    scratch = Image.new("RGBA", (width, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scratch)

    margin = 50
    max_width = width - (margin * 2)

    lines = _wrap_text(display_text, font, max_width, draw)

    line_spacing = int(font_size * 0.35)
    total_height = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        total_height += bbox[3] - bbox[1]
    total_height += line_spacing * max(0, len(lines) - 1)

    return total_height


if __name__ == "__main__":
    import sys
    import os

    # Self-test
    font_path = os.path.join(os.path.dirname(__file__), "..", "fonts",
                             "Amiri-Quran.ttf")
    if not os.path.exists(font_path):
        print(f"Font not found at {font_path}")
        sys.exit(1)

    if load_private_font(font_path):
        print("Font loaded")
        text = "\u0628\u0650\u0633\u06e1\u0645\u0650 \u0671\u0644\u0644\u0651\u064e\u0647\u0650 \u0671\u0644\u0631\u0651\u064e\u062d\u06e1\u0645\u064e\u0670\u0646\u0650 \u0671\u0644\u0631\u0651\u064e\u062d\u0650\u064a\u0645\u0650"
        img = render_text_to_image(text, font_path, 100, 800, 300)
        img.save("test_renderer.png")
        print("Saved test_renderer.png")

        h = measure_text_height(text, font_path, 100, 800)
        print(f"Measured Height: {h}")
    else:
        print("Failed to load font")
