# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Bumped juniper.device to version 1.0.9, and added the installation of a patched to avoid [issue #775](https://github.com/Juniper/ansible-junos-stdlib/issues/775) until it is fixed

### Fixed

- Fixed a test with an unexpected behavior. In previous Ansible version, a task with a `when` condition to `false` wasn't running its `register` statement, but that's not the case anymore
- Refactored templates to suppress some `mgd: statement has no contents` warnings caused by empty blocks
- Removed useless `version` entry from configuration templates

## [1.0.2] - 2025-09-23

### Fixed

- Firmware reboot handler wasn't called anymore

## [1.0.1] - 2025-09-23

### Fixed

- Outdated firmware snapshot was never replaced
- The firmware handler now displays the correct reboot information

## [1.0.0] - 2025-09-19

### Added

- First public release, for Ansible 2.19
