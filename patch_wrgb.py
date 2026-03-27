"""Pre-build script to add NeoWrgbFeature to NeoPixelBus library.

The awawa-dev NeoPixelBus fork only includes NeoGrbwFeature and NeoRgbwFeature.
This script patches NeoColorFeatures.h to add NeoWrgbFeature for WRGB LED strips.
"""
import os
import glob

Import("env")

def patch_neopixelbus(source, target, env):
    # Find NeoColorFeatures.h in the libdeps
    base = os.path.join(env.subst("$PROJECT_LIBDEPS_DIR"), env.subst("$PIOENV"))
    pattern = os.path.join(base, "NeoPixelBus", "src", "internal", "NeoColorFeatures.h")
    matches = glob.glob(pattern)
    if not matches:
        print("WARNING: NeoColorFeatures.h not found, skipping WRGB patch")
        return

    filepath = matches[0]
    with open(filepath, 'r') as f:
        content = f.read()

    if 'NeoWrgbFeature' in content:
        print("NeoWrgbFeature already present, skipping patch")
        return

    # Insert NeoWrgbFeature after NeoRgbwFeature
    marker = """class NeoRgbFeature : public Neo3ByteElementsNoSettings"""

    wrgb_class = """class NeoWrgbFeature : public Neo4ByteElementsNoSettings
{
public:
    static void applyPixelColor(uint8_t* pPixels, uint16_t indexPixel, ColorObject color)
    {
        uint8_t* p = getPixelAddress(pPixels, indexPixel);

        *p++ = color.W;
        *p++ = color.R;
        *p++ = color.G;
        *p = color.B;
    }

    static ColorObject retrievePixelColor(const uint8_t* pPixels, uint16_t indexPixel)
    {
        ColorObject color;
        const uint8_t* p = getPixelAddress(pPixels, indexPixel);

        color.W = *p++;
        color.R = *p++;
        color.G = *p++;
        color.B = *p;

        return color;
    }

    static ColorObject retrievePixelColor_P(PGM_VOID_P pPixels, uint16_t indexPixel)
    {
        ColorObject color;
        const uint8_t* p = getPixelAddress(reinterpret_cast<const uint8_t*>(pPixels), indexPixel);

        color.W = pgm_read_byte(p++);
        color.R = pgm_read_byte(p++);
        color.G = pgm_read_byte(p++);
        color.B = pgm_read_byte(p);

        return color;
    }

};

"""

    if marker in content:
        content = content.replace(marker, wrgb_class + marker)
        with open(filepath, 'w') as f:
            f.write(content)
        print("Patched NeoColorFeatures.h with NeoWrgbFeature")
    else:
        print("WARNING: Could not find insertion point in NeoColorFeatures.h")

# Run patch before compilation
env.AddPreAction("$BUILD_DIR/src/main.cpp.o", patch_neopixelbus)
