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
# See available releases for VERSION
collections:
  - name: https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/releases/download/VERSION/insa_strasbourg-juniper-VERSION.tar.gz
```

## How-to use

- [insa_strasbourg.juniper.ex_config](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_config.fr.md)
- [insa_strasbourg.juniper.ex_firmware](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_firmware.fr.md)

## Compatibility

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
