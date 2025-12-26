# Unity DP UPS - Home Assistant Integration

Home Assistant custom component for monitoring and controlling UPS units equipped with Unity DP management cards (IS-UNITY-DP).

## Compatibility

This integration communicates with Unity DP cards installed in compatible UPS systems.

**Tested with:**
- Card Model: IS-UNITY-DP
- Card Firmware: 8.4.3.1  
- UPS Model: GXT3-1500RT120
- UPS Firmware: U027D024

## Features

### Sensors
- Battery charge percentage and time remaining
- Battery status and charger state
- Input voltage, current, and frequency
- Output voltage, current, power, and load percentage
- DC bus voltage

### Controls
- Manual battery test button

## Installation

### HACS (Recommended)
1. Open HACS
2. Go to "Integrations"
3. Click the three dots in the top right
4. Select "Custom repositories"
5. Add the GitHub mirror `https://github.com/CodePark-CA/home-assistant-unity-dp-ups-client` as an integration
6. Click "Install"
7. Restart Home Assistant

### Manual Installation
1. Copy the `custom_components/unity_dp_ups` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Unity DP UPS"
4. Enter your UPS management card details:
   - **Host:** IP address (e.g., `http://192.168.1.100`)
   - **Username:** Web interface username
   - **Password:** Web interface password

## Requirements

- UPS with IS-UNITY-DP management card
- Network access to the card's web interface

## Disclaimer

This is an unofficial third-party integration for Unity DP cards.
It is not affiliated with or endorsed by any UPS manufacturer.

## Support

For issues, please open an issue on [GitLab](https://gitlab.com/codepark-ca/home-assistant-unity-dp-ups-client/-/issues).

## License

MIT