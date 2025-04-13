# Tigo Energy Integration for Home Assistant

This is a custom integration for [Home Assistant](https://www.home-assistant.io/) that allows you to monitor your **Tigo Energy solar system**, including each individual panel, in real-time using Tigo’s public API.

> ✅ **Important**: This integration requires an active **Tigo EI Premium subscription**.  
> More info: [Tigo EI Premium Plan](https://it.tigoenergy.com/ei-solution/premium)

## 🔧 Features

- Supports both **system-level** and **panel-level** data
- Automatically discovers all **panels**, grouped by Inverter / MPPT / String
- Creates one device per panel, with multiple sensors:
  - Power (W)
  - Voltage In (V)
  - Current In (A)
  - Signal Strength (RSSI)
- Includes system summary sensors:
  - Daily Energy (kWh)
  - YTD Energy (kWh)
  - Lifetime Energy (kWh)
  - Current DC Power (W)
- Fully compatible with **Home Assistant Energy Dashboard**
- Uses **Tigo API v3** (`api2.tigoenergy.com`)
- No polling overload: optimized with a **shared data coordinator**

## 📦 Installation

### 1. Manual Installation

1. Download this repository
2. Copy the contents into your Home Assistant `custom_components/tigo/` folder
3. Restart Home Assistant

### 2. HACS (optional, if published)

To be added when available via HACS.

## ⚙️ Configuration

1. Go to **Settings > Devices & Services**
2. Click **Add Integration**
3. Search for **Tigo Energy**
4. Enter your **Tigo account email and password**
5. Done! Entities will be created automatically

## 🧪 Entities Created

### Panel Devices (One per panel)

- `sensor.panel_<name>_power`
- `sensor.panel_<name>_voltage_in`
- `sensor.panel_<name>_current_in`
- `sensor.panel_<name>_rssi`

### System Summary Sensors

- `sensor.tigo_daily_energy` *(kWh)*
- `sensor.tigo_ytd_energy` *(kWh)*
- `sensor.tigo_lifetime_energy` *(kWh)*
- `sensor.tigo_current_power` *(W)*

All energy sensors are classified with the appropriate `device_class` and `state_class` for dashboard compatibility.

## 🔐 Security Notice

This integration requires your **Tigo account email and password** to authenticate. Credentials are stored securely in Home Assistant's config entry system. All communication with Tigo servers is HTTPS encrypted.

## 🧱 Dependencies

- `aiohttp` (installed automatically by Home Assistant)

## 🛠 Development Notes

- API calls are rate-limited; the integration performs **one single API call per parameter** and shares the result across all sensors.
- This integration uses **`DataUpdateCoordinator`** to cache and refresh data every 60 seconds (panels) and 5 minutes (system summary).
- System layout is retrieved once during setup and reused.

## 🙏 Credits

Built and maintained by [Bobsilvio]

Inspired by the great work of [MartinStoffel's Tigo Integration](https://github.com/MartinStoffel/tigo)

---

**Not affiliated with Tigo Energy. Use at your own risk.**
