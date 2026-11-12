[![hacs_badge](https://img.shields.io/badge/HACS-Custom-yellow.svg?style=for-the-badge)](https://github.com/custom-components/hacs) [![GitHub release (latest by date)](https://img.shields.io/github/v/release/luuuis/hass_omie?label=Latest%20release&style=for-the-badge)](https://github.com/luuuis/hass_omie/releases) [![GitHub all releases](https://img.shields.io/github/downloads/luuuis/hass_omie/total?style=for-the-badge)](https://github.com/luuuis/hass_omie/releases)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

# OMIE Home Assistant Integration

## Features

Pulls data from [OMIE](https://www.omie.es/en) into Home Assistant. OMIE is the nominated electricity market operator (
NEMO)
for managing the Iberian Peninsula's day-ahead and intraday electricity markets.

💶 Follow the day-ahead [Spot prices](https://www.omie.es/en/spot-hoy) for 🇵🇹 and 🇪🇸.  
📈 Use sensor attributes to [graph hourly prices](https://github.com/luuuis/hass_omie/wiki/ApexChartsExamples).  
🧾 [Estimate your power bill](https://github.com/luuuis/hass_omie/wiki/Tarifários-Portugal) based on the spot prices.  
💡 [Check out our Wiki](https://github.com/luuuis/hass_omie/wiki) for examples!

<img alt="Screenshot of OMIE sensors" src="https://user-images.githubusercontent.com/161006/235292328-14b232dd-9d64-4030-a297-53e10a345cf1.jpg"  width="640"></img>  
<img alt="Screenshot of OMIE graphs using ApexCharts card" src="https://user-images.githubusercontent.com/161006/236689344-10f097c4-c47d-4833-b791-c4da7c188e6d.jpg" width="640"></img>

### Sensors

Provides the following sensors containing daily and day-ahead values.

| Sensor                        | Unit  | Description                                                                                              |
|-------------------------------|:-----:|----------------------------------------------------------------------------------------------------------|
| `omie_spot_price_es`          | €/MWh | Marginal price for the current hour in Spain, determined in the day-ahead market of the previous day.    |
| `omie_spot_price_pt`          | €/MWh | Marginal price for the current hour in Portugal, determined in the day-ahead market of the previous day. |

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
1. Paste in https://github.com/luuuis/hass_omie and select `Integration` as type.
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

## Configuration

Go to the `Integrations` page, click `Add Integration` and select the OMIE Home Assistant Integration or click the
following button.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=omie)


## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/en/reference/emoji-key/)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tabascoz"><img src="https://avatars.githubusercontent.com/u/10350083?v=4&size=100" width="100px" height="100px" alt="Fernando Cunha"/><br /><sub><b>Fernando Cunha</b></sub></a><br /><a href="https://github.com/luuuis/hass_omie/commits?author=tabascoz" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!