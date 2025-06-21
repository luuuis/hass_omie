# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [1.0.11-beta.1](https://github.com/luuuis/hass_omie/compare/v1.0.10...v1.0.11-beta.1) (2025-06-21)


### Build System

* add .release-please-manifest.json ([#76](https://github.com/luuuis/hass_omie/issues/76)) ([c97d68b](https://github.com/luuuis/hass_omie/commit/c97d68bb986d16417bc3995635c89cd853cfd43a))
* remove reference to release-please manifest ([#78](https://github.com/luuuis/hass_omie/issues/78)) ([8e35e31](https://github.com/luuuis/hass_omie/commit/8e35e31b12a47a27fd46268c0e4aed2b1bbd9872))
* remove reference to release-please manifest ([#80](https://github.com/luuuis/hass_omie/issues/80)) ([3835c79](https://github.com/luuuis/hass_omie/commit/3835c79938227f73835aba0c2913dac2a7ee59c5))
* use single package release-please config ([#77](https://github.com/luuuis/hass_omie/issues/77)) ([cd2649a](https://github.com/luuuis/hass_omie/commit/cd2649ae8f8b89f257553de08ff8425c7c39ccb5))

### [1.0.10](https://github.com/luuuis/hass_omie/compare/v1.0.9...v1.0.10) (2024-04-17)


### Bug Fixes

* revert temporarily disable SSL verification due to changes in OMIE.es" ([#64](https://github.com/luuuis/hass_omie/issues/64)) ([688c0ea](https://github.com/luuuis/hass_omie/commit/688c0ea2ea722f9c76c719a6d999820b99d47557))

### [1.0.9](https://github.com/luuuis/hass_omie/compare/v1.0.8...v1.0.9) (2024-04-17)


### Bug Fixes

* temporarily disable SSL verification due to changes in OMIE.es ([#63](https://github.com/luuuis/hass_omie/issues/63)) ([0245c78](https://github.com/luuuis/hass_omie/commit/0245c78245fba0f7177c5cfa2096c2559fa6dee7))

### [1.0.8](https://github.com/luuuis/hass_omie/compare/v1.0.7...v1.0.8) (2024-04-02)


### Bug Fixes

* introduce OMIEDailyCoordinator.__job ([#59](https://github.com/luuuis/hass_omie/issues/59)) ([a89b9ae](https://github.com/luuuis/hass_omie/commit/a89b9ae3b3afa09bcb0b904e87d2f5ef9d1b6f14))

### [1.0.7](https://github.com/luuuis/hass_omie/compare/v1.0.6...v1.0.7) (2024-04-02)


### Bug Fixes

* remove usage of removed DataUpdateCoordinator._job ([#58](https://github.com/luuuis/hass_omie/issues/58)) ([1c49168](https://github.com/luuuis/hass_omie/commit/1c49168a5e0eb28eeddebda78dad42a60848fedb))

### [1.0.6](https://github.com/luuuis/hass_omie/compare/v1.0.5...v1.0.6) (2024-03-16)


### Bug Fixes

* AttributeError: 'dict' object has no attribute 'market_date' ([#54](https://github.com/luuuis/hass_omie/issues/54)) ([13003ad](https://github.com/luuuis/hass_omie/commit/13003ad361a1a55b6db957a9c02cc1e7a202c4ab))

### [1.0.5](https://github.com/luuuis/hass_omie/compare/v1.0.4...v1.0.5) (2024-03-12)


### Bug Fixes

* coordinator refresh handling compatibility with HA 2024.3.0 ([#53](https://github.com/luuuis/hass_omie/issues/53)) ([975950d](https://github.com/luuuis/hass_omie/commit/975950dea43926585021264f58396f34765a3b58))
* **coordinator:** don't attempt to read adjustment value on or after 2024-01-01 ([#52](https://github.com/luuuis/hass_omie/issues/52)) ([57bf258](https://github.com/luuuis/hass_omie/commit/57bf258ca01d676981cb6c05812479e31716eea0))

### [1.0.4](https://github.com/luuuis/hass_omie/compare/v1.0.3...v1.0.4) (2024-03-07)


### Bug Fixes

* use async_forward_entry_setups and async_unload_platforms ([#51](https://github.com/luuuis/hass_omie/issues/51)) ([aeaa3cf](https://github.com/luuuis/hass_omie/commit/aeaa3cf5a2d5bfdc7c8156e69ed52a62304e4bce))

### [1.0.3](https://github.com/luuuis/hass_omie/compare/v1.0.2...v1.0.3) (2024-03-07)


### Bug Fixes

* await async_forward_entry_setup and async_forward_entry_unload tasks during setup/unload ([#50](https://github.com/luuuis/hass_omie/issues/50)) ([0a8bad0](https://github.com/luuuis/hass_omie/commit/0a8bad08d8d474c0fe3868a1571e76930545577b))

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
