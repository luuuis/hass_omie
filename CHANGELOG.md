# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### [1.0.2](https://github.com/luuuis/hass_omie/compare/v1.0.1...v1.0.2) (2023-09-07)


### Bug Fixes

* **coordinator:** rely on our own _SCHEDULE_MAX_DELAY instead of private DataUpdateCoordinator property ([#35](https://github.com/luuuis/hass_omie/issues/35)) ([13ad28e](https://github.com/luuuis/hass_omie/commit/13ad28ebe68a2c7c68fbecf8872fca5e81baf3b8))

### [1.0.1](https://github.com/luuuis/hass_omie/compare/v1.0.0...v1.0.1) (2023-09-07)


### Bug Fixes

* **coordinator:** convert DataUpdateCoordinator._microsecond to int before usage ([#33](https://github.com/luuuis/hass_omie/issues/33)) ([7a5c119](https://github.com/luuuis/hass_omie/commit/7a5c1191bde66a166b571f7e967bcab85930467d))

## [1.0.0](https://github.com/luuuis/hass_omie/compare/v0.0.6...v1.0.0) (2023-05-06)


### ⚠ BREAKING CHANGES

* removes _tomorrow sensors and renamed all attributes

### Features

* changed what sensors are available, attributes and correctly handle non-CET local time zones. ([#14](https://github.com/luuuis/hass_omie/issues/14)) ([8e45e8b](https://github.com/luuuis/hass_omie/commit/8e45e8b507f3bf63c67ae13a77ac6c5b7f102f32))


### Bug Fixes

* StatisticsError raised when rolling over to a new day ([#15](https://github.com/luuuis/hass_omie/issues/15)) ([85e3528](https://github.com/luuuis/hass_omie/commit/85e3528ac6813921c765250263428e9671c2b409))
* use constants for "€/MWh" ([#16](https://github.com/luuuis/hass_omie/issues/16)) ([b5ac70f](https://github.com/luuuis/hass_omie/commit/b5ac70f3f8b7b988cb3cf584b7ad4b28e0be8d3f))

### [0.0.6](https://github.com/luuuis/hass_omie/compare/v0.0.5...v0.0.6) (2023-03-26)


### Bug Fixes

* clear _tomorrow sensor attributes when state is unknown ([#7](https://github.com/luuuis/hass_omie/issues/7)) ([204c427](https://github.com/luuuis/hass_omie/commit/204c42786bdf3446490a8a94630d1ee10cdfdc72))
* don't error on shorter days when entering DST ([#10](https://github.com/luuuis/hass_omie/issues/10)) ([58d8a69](https://github.com/luuuis/hass_omie/commit/58d8a69dae3a79404f3aefa2f9cfe6b68e0c886f))
* interpolate language into omie.es link ([#9](https://github.com/luuuis/hass_omie/issues/9)) ([a86a057](https://github.com/luuuis/hass_omie/commit/a86a05758f023a64a2d76eb52da94a4d81f36a34))

### [0.0.5](https://github.com/luuuis/hass_omie/compare/v0.0.4...v0.0.5) (2023-03-03)


### Bug Fixes

* spot/adjustment sensors don't update when a new day rolls over ([#6](https://github.com/luuuis/hass_omie/issues/6)) ([3408325](https://github.com/luuuis/hass_omie/commit/34083256a949ed8a7d359dca3b3b2aae141e2894))

### [0.0.4](https://github.com/luuuis/hass_omie/compare/v0.0.3...v0.0.4) (2023-02-26)


### Features

* reduce number of network calls ([#5](https://github.com/luuuis/hass_omie/issues/5)) ([fc4e8e8](https://github.com/luuuis/hass_omie/commit/fc4e8e887c9fd3b4b6507870cff3ac2924d2662d))


### Bug Fixes

* minor improvement to OMIE device info ([#4](https://github.com/luuuis/hass_omie/issues/4)) ([6a53089](https://github.com/luuuis/hass_omie/commit/6a53089de43b8b18dca77454088a92570ac4618b))

### [0.0.3](https://github.com/luuuis/hass_omie/compare/v0.0.2...v0.0.3) (2023-02-21)


### Bug Fixes

* adds _tomorrow price sensors ([#3](https://github.com/luuuis/hass_omie/issues/3)) ([03f9099](https://github.com/luuuis/hass_omie/commit/03f90997d28ca4f9444a9446a47a3c080da29fd3))

### [0.0.2](https://github.com/luuuis/hass_omie/compare/v0.0.1...v0.0.2) (2023-02-20)


### Bug Fixes

* `AttributeError` when getting next day's data ([#2](https://github.com/luuuis/hass_omie/issues/2)) ([70e7999](https://github.com/luuuis/hass_omie/commit/70e7999e6e9d342ba68f78b71953fe03427b52a9))

### 0.0.1 (2023-02-19)


### Features

* adds OMIE sensors for marginal price and adjustment. support for en/es/pt languages. ([67b52f9](https://github.com/luuuis/hass_omie/commit/67b52f9dbc5f2015ac9c143d76f72b923a17b8ca))
