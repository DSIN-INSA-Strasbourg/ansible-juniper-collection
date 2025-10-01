# Ansible - insa_strasbourg.juniper.ex_firmware role

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_firmware.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_firmware.fr.md)

---

## Introduction

This role is used to update the firmware of Juniper switches, as well as their backup images (system snapshots).
For most switches, they will be updated only when necessary and rebooted according to the setting of the `ex_firmware_reboot_at` variable. There are two special cases that are not updated by this role by default:

- Virtual chassis, which will only be updated if the playbook is launched with the `install_on_virtual_chassis_only` tag, and whose update sequence depends on the value of the `ex_firmware_use_nssu_on_vc` variable.
- Switches declared as critical, which will only be updated if the playbook is launched with the `install_on_critical` tag.

## Inventory groups used by the role

Each model family must be assigned its own group. The groups for qualified models are as follows:

- juniper_ex2200
- juniper_ex2300 *(not specifically tested, but should work)*
- juniper_ex3300
- juniper_ex3400
- juniper_ex4100
- juniper_ex4300
- juniper_ex4600
- juniper_ex4650 *(work in progress)*

Critical devices, whose firmware updates require confirmation, must be assigned to the `juniper_critical_devices` group, for example:

```yaml
juniper_critical_devices:
  children:
    juniper_ex4600:
    juniper_ex4650:

juniper_ex2200:
  hosts:
    my_ex2200:

juniper_ex2300:
  hosts:
    my_ex2230:

juniper_ex3400:
  hosts:
    my_ex3400:

juniper_ex4100:
  hosts:
    my_ex4100:

juniper_ex4300:
  hosts:
    my_ex4300:

juniper_ex4600:
  hosts:
    my_ex4600:

juniper_ex4650:
  hosts:
    my_ex4650:
```

## Operating logic

Without any specific tags, the playbook will perform the following tasks:

1. Firmware installation (if necessary): If the firmware has been updated, a reboot is scheduled according to the `ex_firmware_reboot_at` variable setting, and the playbook stops
2. Snapshot creation (if necessary)

This means that if the firmware is updated, the playbook will need to be restarted after the reboot to update the snapshot.

## Building the firmware URL

The firmware download URL is built with three variables, the last two of which must be defined by model : `{{ ex_firmware_baseurl }}/{{ ex_firmware_dir }}/{{ ex_firmware }}`. For example:

| Variable | Value | Resulting URL |
| --- | --- | --- |
|ex_firmware_baseurl  |[https://www.example.com/PLEASE/SET/ME](https://www.example.com/PLEASE/SET/ME)  |  |
|ex_firmware_dir  |EX4600  |[https://www.example.com/PLEASE/SET/ME/EX4600/jinstall-host-ex-4600-18.1R3-S11.3-signed.tgz](https://www.example.com/PLEASE/SET/ME/EX4600/jinstall-host-ex-4600-18.1R3-S11.3-signed.tgz)  |
|ex_firmware  |jinstall-host-ex-4600-18.1R3-S11.3-signed.tgz  |  |

## Main files

Paths are relative to the Ansible folder

| File | Purpose of this file |
| --- | --- |
|`network` | Network devices inventory file, and assignment of models and critical or non-critical status |
|`host_vars/*switch_name*.yml` | Switch configuration |
|`group_vars/juniper_ex*XXXX*.yml` | Model-family-specific configuration: firmware version and any specifics |

## Global configuration

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|ex_firmware_baseurl |[https://www.example.com/PLEASE/SET/ME](https://www.example.com/PLEASE/SET/ME) |The firmware download URL prefix, e.g. [https://www.example.com/PLEASE/SET/ME](https://www.example.com/PLEASE/SET/ME) |Yes |
|ex_firmware_reboot_at |"{{ '%y%m%d0100' \| strftime(ansible_date_time.epoch \| int + 86400) }}" (*next day at 01:00*) |Indicates when to reboot the switch after an update. Possible values ​​are: <br/> - "now": Reboot immediately <br/> - "+minutes": Reboot after the specified number of minutes <br/> - "yymmddhhmm": Reboot at the specified date and time |No |
|ex_firmware_use_nssu_on_vc |false |Indicates whether the firmware of a virtual chassis should be installed using *NSSU*, in which case the virtual chassis will not be rebooted according to `ex_firmware_reboot_at`, since its members will have been rebooted individually one after the other. **Since NSSU deployment is more of a source of problems than benefits, its use is discouraged, although possible**. If this variable is `false`, the virtual chassis firmware will be deployed to all members, which will reboot according to the instructions of `ex_firmware_reboot_at` |No |

## Switch model configuration

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|ex_firmware_dir |*N/A* |Subfolder containing the firmware for this model on the remote server, i.e., `EX4600` |Yes |
|ex_firmware |*N/A* |Firmware to deploy for this model. The version number will be deduced from the name, so it's best to preserve the original names, i.e., `junos-arm-32-18.2R3-S6.5.tgz` |Yes |
|ex_firmware_validate |true |By default, the switch is asked to validate the compatibility of its configuration with the new firmware. However, recent models (ELS) do this by default and no longer recognize the `validate` option. For these, this variable must be set to `false` |No |
|ex_firmware_snapshot_cmd |*N/A* |The command to generate a new system snapshot. Specify an empty string `""` for switches without this feature, such as the EX4600 |Yes |
|ex_firmware_snapshot_version_format |text |Leave the default value on older models (those whose snapshot is taken with a `request system snapshot media internal slice alternate`), and use `json` for newer models using the `request system snapshot recovery` command |No |

## Switch configuration

The switch must be associated with a properly configured model group (i.e., `juniper_ex4600`).

## Deployment

### On a single device (excluding virtual chassis)

Deployment on all non-critical switches that are not part of a virtual chassis (stack):

```bash
ansible-playbook -i network insa_strasbourg.juniper.ex_firmware
```

Deployment on a list of switches, here *juniper1*, *juniper2* and *juniper3*. If some are declared critical or are part of a virtual chassis, they will be ignored (errorized):

```bash
ansible-playbook -i network -l juniper1,juniper2,juniper3 insa_strasbourg.juniper.ex_firmware
```

Checking for the need to update the firmware or snapshot (without doing so):

```bash
ansible-playbook -i network insa_strasbourg.juniper.ex_firmware --tags check
```

Deployment command on all switches, including critical ones, and not part of a virtual chassis (stack):

```bash
ansible-playbook -i network insa_strasbourg.juniper.ex_firmware --tags install_on_critical
```

### On virtual chassis

> [!WARNING]
> Tests performed on nonstop software upgrades (NSSUs) of virtual chassis - when `ex_firmware_use_nssu_on_vc` is set to `true` - have yielded relatively disappointing results.
> Even when the playbook runs without errors, it will fail because it will lose its connection to the [*primary routing engine RE when it switches to secondary for updating](https://github.com/Juniper/ansible-junos-stdlib/issues/431)
> **This feature is retained in principle, but its use is discouraged.**

Deployment command on all non-critical switches in a virtual chassis (stack):

```bash
ansible-playbook -i network insa_strasbourg.juniper.ex_firmware --tags install_on_virtual_chassis_only
```

Deployment command on all switches, including critical switches, in a virtual chassis (stack):

```bash
ansible-playbook -i network insa_strasbourg.juniper.ex_firmware --tags install_on_critical,install_on_virtual_chassis_only
```
