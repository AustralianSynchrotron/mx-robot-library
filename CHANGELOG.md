# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [SCOMPMX-2023r1] - 2023-02-22

### Added

- Initial client framework to call mount/unmount trajectories.
- Support for HotPuck mount/unmount trajectories.

## [SCOMPMX-2023r2] - 2023-05-10

### Added

- Support for plate mount/unmont trajectories.

### Changed

- Better handling of HotPuck `id: 101` out of range issue, now handled seemlessly.
- Puck, HotPuck and Plate models now accepts an ID int passed directly via the Pydantic validate method.
- Pin now accepts a tuple passed as `(<Puck ID>, <Pin ID>)` via the Pydantic validate method.
- Improved parsing robot state response, positions now defined in model field definition, with mapped values passed directly to the Pydantic validation method.

[SCOMPMX-2023r1]: https://confluence.synchrotron.org.au/confluence/display/SCOMPROJ/MX3+-+Releases+-+Project+Increment+2
[SCOMPMX-2023r2]: https://confluence.synchrotron.org.au/confluence/display/SCOMPROJ/MX3+-+Releases+-+Project+Increment+3
[Docs]: https://s3-api.asci.synchrotron.org.au/sphinx-docs/mx3/mx-robot-library/main/index.html
