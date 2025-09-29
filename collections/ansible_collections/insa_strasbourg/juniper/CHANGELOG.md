# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Major change in role `insa_strasbourg.juniper.ex_config`: collection [juniper.device](https://galaxy.ansible.com/ui/repo/published/juniper/device/) is now used in replacement of [junipernetworks.junos](https://docs.ansible.com/ansible/latest/collections/junipernetworks/junos/index.html)
  This was motivated by 2 reasons:
    1. Main one, the nasty [issue #535](https://github.com/ansible-collections/junipernetworks.junos/issues/535) was _randomly_ met on EX4650, leading to configuration changes not being deployed to devices, and Ansible erroneously reporting "no changes" to the device config
    2. The whole collection is now only using the juniper.device collection. However, junipernetworks.junos and its requirements are kept to facilitate its eventual use
- Replaced `juniper.device` existing `local` connection used by `juniper.device.pyez`, as some short timeouts were met with the local connection
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
