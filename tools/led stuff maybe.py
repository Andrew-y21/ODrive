from rpi_ws281x import PixelStrip, ColorRGBW, SK6812_STRIP_RGBW

strip = PixelStrip(30, 18, strip_type=SK6812_STRIP_RGBW)
strip.begin()

# Set a warm white color
strip.setPixelColor(0, ColorRGBW(0, 0, 0, 128))
strip.show()
