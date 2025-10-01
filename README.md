# Collection Ansible insa_strasbourg.juniper

## Description

Provides following roles :

- `insa_strasbourg.juniper.ex_config` : to configure Juniper EX switches
- `insa_strasbourg.juniper.ex_firmware` : to deploy firmware on Juniper EX switches

## Requirements

This collection uses [junipernetworks.junos](https://github.com/ansible-collections/junipernetworks.junos) collection, [juniper.device](https://github.com/Juniper/ansible-junos-stdlib) collection and [ansible.utils.ipaddr](https://docs.ansible.com/ansible/latest/collections/ansible/utils/ipaddr_filter.html) filter. Install their requirements using pip:

```bash
pip install -r requirements.txt
```

## Installation

Add the following requirement in your playbook's **requirements.yml**:

```yaml
---
# See available releases for VERSION: https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/releases
collections:
  - name: https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/releases/download/VERSION/insa_strasbourg-juniper-VERSION.tar.gz
```

## Documentation

### Roles

- [`insa_strasbourg.juniper.ex_config`](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_config.md): deploy configuration on Juniper EX switches
- [`insa_strasbourg.juniper.ex_firmware`](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_firmware.md): deploy firmwares on Juniper EX switches

### Playbooks

- [`insa_strasbourg.juniper.ex_config`](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_config.md#deployment): deploy configuration on Juniper EX switches
- [`insa_strasbourg.juniper.ex_firmware`](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_config.md#deployment): deploy firmwares on Juniper EX switches
- `insa_strasbourg.juniper.ex_plan_reboot`: schedule a reboot on Juniper EX switches, or cancel a scheduled reboot
- `insa_strasbourg.juniper.ex_plan_shutdown`: schedule a shutdown on Juniper EX switches, or cancel a scheduled shutdown
- `insa_strasbourg.juniper.ex_show_plan`: print any scheduled reboot or shutdown on Juniper EX switches

## Supported devices

| Device | Support                        |
| ------ | ------------------------------ |
| EX4650 | 🚧 Work in progress            |
| EX4600 | ✅                             |
| EX4300 | ✅                             |
| EX4100 | ✅                             |
| EX3400 | ✅                             |
| EX3300 | ✅                             |
| EX2300 | ⚠️ Not tested, but should work |
| EX2200 | ✅                             |

## Contributing

Contributions are always welcome, but may take some time to be merged.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

## Authors

- [@Boris Lechner](https://github.com/orgs/DSIN-INSA-Strasbourg/people/Boris-INSA)
