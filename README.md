# HyperSPI for WRGB LED Strips

Custom fork of [awawa-dev/HyperSPI](https://github.com/awawa-dev/HyperSPI) v11.0.0 modified for **WRGB** byte-order LED strips.

## Changes from upstream

1. **NeoWrgbFeature**: Adds `NeoWrgbFeature` to NeoPixelBus (via build-time patch) for strips that expect bytes in W, R, G, B order on the wire.

2. **LED_DRIVER**: All RGBW `LED_DRIVER` definitions changed from `NeoGrbwFeature` to `NeoWrgbFeature`.

3. **Balanced calibration**: Neutral white calibration changed from `(0xFF, 0xB0, 0xB0, 0x70)` to `(0xFF, 0xB0, 0xB0, 0xB0)` — equal channel correction so RGB white input produces proper white output (no yellow tint).

## How it works

Standard SK6812 RGBW strips expect GRBW byte order, but some strips use WRGB. This firmware change tells NeoPixelBus to output bytes as W, R, G, B instead of G, R, B, W.

The `patch_wrgb.py` pre-build script automatically adds `NeoWrgbFeature` to the NeoPixelBus library when PlatformIO compiles.

## Building

```bash
# Install PlatformIO
python3 -m venv pio-env && source pio-env/bin/activate
pip install platformio

# Build for ESP32
pio run -e SK6812_RGBW_NEUTRAL
```

## Flashing

```bash
# Factory binary includes bootloader + partitions + firmware
esptool --port /dev/ttyUSB0 --baud 460800 --chip esp32 erase_flash
esptool --port /dev/ttyUSB0 --baud 460800 --chip esp32 write_flash 0x0 \
  .pio/build/SK6812_RGBW_NEUTRAL/hyperspi_esp32_SK6812_RGBW_NEUTRAL.factory.bin
```

## HyperHDR Configuration

- Device type: `hyperspi`
- SPI type: `esp32`
- Output: `/dev/spidev0.0`
- Rate: `20000000` (20 MHz)
- Color order: `rgb`
- White channel calibration: `false` (ESP32 handles RGBW conversion)

## Based on

- [HyperSPI v11.0.0](https://github.com/awawa-dev/HyperSPI/tree/v11.0.0)
- [HyperHDR](https://github.com/awawa-dev/HyperHDR)
