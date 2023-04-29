[![hacs_badge](https://img.shields.io/badge/HACS-Custom-yellow.svg?style=for-the-badge)](https://github.com/custom-components/hacs) [![GitHub release (latest by date)](https://img.shields.io/github/v/release/luuuis/hass_omie?label=Latest%20release&style=for-the-badge)](https://github.com/luuuis/hass_omie/releases) [![GitHub all releases](https://img.shields.io/github/downloads/luuuis/hass_omie/total?style=for-the-badge)](https://github.com/luuuis/hass_omie/releases)

# OMIE Home Assistant Integration

## Features

Pulls data from [OMIE](https://omie.es) into Home Assistant. OMIE is the nominated electricity market operator (NEMO)
for managing the Iberian Peninsula's day-ahead and intraday electricity markets.

<img alt="OMIE sensors screenshot" src="https://user-images.githubusercontent.com/161006/235292328-14b232dd-9d64-4030-a297-53e10a345cf1.jpg" width="640"></img>

### Sensors

Provides the following sensors containing daily and day-ahead values.

| Sensor                        | Unit  | Description                                                                                              |
|-------------------------------|:-----:|----------------------------------------------------------------------------------------------------------|
| `omie_spot_price_es`          | €/MWh | Marginal price for the current hour in Spain, determined in the day-ahead market of the previous day.    |
| `omie_spot_price_pt`          | €/MWh | Marginal price for the current hour in Portugal, determined in the day-ahead market of the previous day. |
| `omie_adjustment_price_es`(P) | €/MWh | Adjustment mechanism price for the current hour paid by consumers in Spain.                              |
| `omie_adjustment_price_pt`(P) | €/MWh | Adjustment mechanism price for the current hour paid by consumers in Portugal.                           |

General notes regarding the sensors:

* Daily average and hourly values are available in each sensor's attributes.
* Unwanted sensors may be disabled in each sensor's Settings after installation.
* Sensors marked with a (P) contain **Provisional** values until the results of the last intraday market session are
  published at around 10:30 PM on the day.

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

Go to the `Integrations` page, click `Add Integration` and select the OMIE Home Assistant Integration or click the
following button.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=omie)

