[![hacs_badge](https://img.shields.io/badge/HACS-Custom-yellow.svg?style=for-the-badge)](https://github.com/custom-components/hacs) [![GitHub release (latest by date)](https://img.shields.io/github/v/release/luuuis/hass_omie?label=Latest%20release&style=for-the-badge)](https://github.com/luuuis/hass_omie/releases) [![GitHub all releases](https://img.shields.io/github/downloads/luuuis/hass_omie/total?style=for-the-badge)](https://github.com/luuuis/hass_omie/releases)

# Home Assistant OMIE Integration

## Features

Pulls data from [OMIE](https://omie.es) into Home Assistant. OMIE is the nominated electricity market operator (NEMO)
for managing the Iberian Peninsula's day-ahead and intraday electricity markets.

![OMIE sensors screenshot](https://user-images.githubusercontent.com/161006/219978890-4d34c2ca-321b-4f29-81fe-44a15768a155.jpg)

### Sensors

Provides the following sensors by default (unused sensors may be disabled after installation).

| Sensor                       |  Unit   | Description                                      |
|------------------------------|:-------:|--------------------------------------------------|
| `omie_spot_price_es`         | EUR/MWh | Marginal price - Spain                           |
| `omie_spot_price_pt`         | EUR/MWh | Marginal price - Portugal                        |
| `omie_adjustment_price_es`   | EUR/MWh | Adjustment mechanism price - Spain               |
| `omie_adjustment_price_pt`   | EUR/MWh | Adjustment mechanism price - Portugal            |
| `omie_adjustment_unit_price` | EUR/MWh | Adjustment unit amount for production facilities |

## Installation

Use [HACS](https://hacs.xyz) (preferred) or follow the manual instructions below.

### Installation using HACS

1. Open `Integrations` inside the HACS configuration.
1. Click on the 3 dots in the top-right corner and select `Custom Repositories`.
1. Paste in https://github.com/luuuis/hass_omie and select `Integration` as category.
1. Once installation is complete, restart Home Assistant.

<details>
  <summary>Manual installation instructions</summary>

### **Manual installation**

1. Download `hass_omie.zip` from the latest release in https://github.com/luuuis/hass_omie/releases/latest
2. Unzip into `<hass_folder>/config/custom_components`
    ```shell
    $ unzip hass_omie.zip -d <hass_folder>/custom_components/omie
    ```
3. Restart Home Assistant

</details>

# Configuration

Go to the `Integrations` page, click `Add Integration` and select the OMIE integration or click the following button.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=omie)
