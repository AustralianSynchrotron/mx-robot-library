# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added Dewar sub-client to robot client.
- Added ability to map pucks with presence detection to the puck loading assistant datamatrix.
- Added datamatrix support for Puck schemas.
- Added equivalency check override for Pin and Puck schemas.

### Fixed

- `_client` in sub-clients now correctly represented as `Client` rather than `RootClient`.
- Fixed clear barcode command typo, clarified by Irelec.
- Fixed new pre-commit check failures occuring after dependency update.

### Changed

- Updated pre-commit checks.
- Updated dependencies.

## SCOMPMX-2023r1 - 2023-02-22

### Added

- Initial client framework to call mount/unmount trajectories.
- Support for HotPuck mount/unmount trajectories.

## SCOMPMX-2023r2 - 2023-05-10

### Added

- Support for plate mount/unmont trajectories.

### Changed

- Better handling of HotPuck `id: 101` out of range issue, now handled seemlessly.
- Puck, HotPuck and Plate models now accepts an ID int passed directly via the Pydantic validate method.
- Pin now accepts a tuple passed as `(<Puck ID>, <Pin ID>)` via the Pydantic validate method.
- Improved parsing robot state response, positions now defined in model field definition, with mapped values passed directly to the Pydantic validation method.

[unreleased]: https://github.com/AustralianSynchrotron/mx-robot-library/compare/0.1.3...HEAD
