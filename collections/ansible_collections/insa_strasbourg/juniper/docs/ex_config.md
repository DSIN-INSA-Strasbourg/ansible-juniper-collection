# Ansible - role insa_strasbourg.juniper.ex_config

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_config.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_config.fr.md)

---

## Introduction

This role is used to ensure the day-to-day operation of Juniper switches and to deploy configuration changes.
Each configuration file will be generated locally in a folder on the controller workstation (by default, `$HOME/.juniper-configs/`).

## Main files

Paths are relative to the Ansible folder.

| File | Purpose of this file |
| --- | --- |
| `network` | Network devices inventory file, and assignment of models and configuration type (ELS/non-ELS) |
| `host_vars/*switch_name*.yml` | Switch configuration |
| `group_vars/juniper/*.yml` | Default variables: list of VLANs, users |

## Inventory groups used by the role

Each model family must be assigned its own group. The groups for qualified models are as follows:

- juniper_ex2200
- juniper_ex2300 *(not specifically tested, but should work)*
- juniper_ex3300
- juniper_ex3400
- juniper_ex4100
- juniper_ex4300
- juniper_ex4600
- juniper_ex4650

ELS devices **must** be assigned to the `juniper_els` group, for example:

```yaml
juniper_els:
  children:
    juniper_ex2300:
    juniper_ex3400:
    juniper_ex4100:
    juniper_ex4300:
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

## Global role configuration

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|ex_config_save_dir |$HOME/.juniper-configs |Local folder (on the Ansible controller) where the device configuration files will be generated |No |
|ex_config_commitconfirm_delay |5 |Timeout in **minutes** during which the new configuration must be confirmed. After this timeout, the old configuration will be restored. This should be significantly longer than `ex_config_delay_between_commitconfirm_and_commit` to avoid unnecessary rollbacks when the playbook is executed on multiple devices |No |
|ex_config_delay_between_commitconfirm_and_commit |15 |Timeout in **seconds** between *commit confirm* and its confirmation. This delay should allow for loss of connectivity with the device in the event of a configuration error |No |
|ex_config_ignore_commit_warnings |`["mgd: [0-9]+g config will be applied to ports [0-9]+ to [0-9]+"]` |List of warnings to ignore (regular expressions). Any warning not specified in this variable that will be raised by the device when parsing its configuration will cause the task to fail |No |

## Basic switch configuration

### Network

The role only manages IPv4 network configuration.

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|ex_config_hostname |*N/A* | Hostname (short) |Yes |
|ex_config_location |*N/A* | Location |Yes |
|ex_config_ipaddress |*N/A* | Management interface IP address |Yes |
|ex_config_netmask |*N/A* | Management interface subnet mask |Yes |
|ex_config_mgmtvlan |*N/A* | Management VLAN name |Yes |
|ex_config_toip_vlan |*N/A* | ToIP VLAN name |No |
|ex_config_nameservers |[] |List of DNS server IPs to use |No |
|ex_config_gateway | |Default gateway for the management interface |No |
|ex_config_domainname | |Device domain name |No |
|ex_config_domainsearch |[] |List of search domains |No |

### Password hashing

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|ex_config_password_hashtype |sha256 |Password hashing method to use. Should always be `sha256`, except on firmware prior to version 15 that does not support it, where `md5` should be used |No |
|ex_config_password_salt |CHANGEME |Salt string to use when hashing passwords. If it is too long for the chosen hash method, it will be automatically truncated. |No |

### Login classes

Juniper switches provide the following login classes by default:

- operator
- read-only
- superuser or super-user
- unauthorized

Additional login classes can be defined by specifying them in the `ex_config_user_classes` variable, which should be a list with the following attributes:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|name |*N/A* |Login class name (must be unique) |Yes |
|permissions |*N/A* |List of [permissions](https://www.juniper.net/documentation/us/en/software/junos/user-access-evo/user-access/topics/topic-map/junos-os-login-class.html#id-junos-os-login-classes-overview__d8e136) to grant to the current login class |Yes |

Example:

```yaml
ex_config_user_classes:
  - name: rancid
    permissions:
      - access
      - admin
      - firewall
      - flow-tap
      - interface
      - network
      - routing
      - security
      - snmp
      - storage
      - system
      - trace
      - view
      - view-configuration
```

### User Accounts

The root account is defined through the `ex_config_root_user` variable, which can have the following attributes:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|password |*N/A* | Password | No |
|ssh_pubkeys |*N/A* | Dictionary that can contain one or more of the following three keys: `ssh-ecdsa`, `ssh-ed25519`, `ssh-rsa`, and the associated key as a value | No |

Other user accounts are defined through the `ex_config_users` variable, which must be a list whose each element must have the following attributes:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|login |*N/A* | User login (must be unique) | Yes |
|class |*N/A* |Login class to assign to the user |Yes |
|uid |*N/A* |User's UID (must be unique) |No |
|password |*N/A* |Password |No |
|ssh_pubkeys |*N/A* |Dictionary that can contain one or more of the following three keys: `ssh-ecdsa`, `ssh-ed25519`, `ssh-rsa`, and the associated key as a value |No |

## Interface configuration

### VLAN configuration

| Option | Default Value | Description | Mandatory |
| --- | --- | --- | --- |
|name |*N/A* |VLAN Name (must be unique) |Yes |
|description|*N/A* |VLAN Description |Yes |
|vlanid|*N/A* |Integer identifying the VLAN (must be unique), between 1 and 4094. **Do not assign values ​​1002 to 1005, which are reserved by the standard** |Yes |
|dhcpsnooping|true |Indicates whether to enable DHCP snooping and port security features (Dynamic ARP Inspection and IP Source Guard) on this VLAN |No |
|jumboframes|false |Set to True to enable jumbo frames (Ethernet frames whose MTU increases from 1522 to 9216 bytes) on this VLAN |No |

```yaml
ex_config_vlans:
  - name: employees
    description: Employees
    vlanid: 10
    dhcpsnooping: false
  - name: students
    description: Students
    vlanid: 11
  - name: storage
    description: storage
    vlanid: 12
    jumboframes: true
    dhcpsnooping: false
```

### Syntactic sugar for trusted interfaces

The role allows you to declare trusted interfaces by adding the `trusted` interface variable set to true.

The behavior of trusted interfaces is fully configurable via a global variable `ex_config_trusted_settings`, whose contents (interface variables and their values) will be merged with those of the trusted interfaces.
During the merge, if interface variables present in `ex_config_trusted_settings` already exist in the interface, the value declared in the interface will be preserved (see example).

| Option | Default Value | Description | Mandatory |
| --- | --- | --- | --- |
|ex_config_trusted_settings |{is_uplink: true, no_maxhosts: true, dhcptrusted: true, stormtrusted: true} |Interface variables that will be added to trusted interfaces if they don't already exist |No |

Interface variables:

| Option | Default value | Description | Required |
| --- | --- | --- | --- |
|trusted |false |If true, interface variables declared in `ex_config_trusted_settings` that don't already exist in the interface will be automatically added |No |

Example, by declaring:

```yaml
ex_config_trusted_settings:
  is_uplink: true
  no_maxhosts: true
  dhcptrusted: true
  stormtrusted: true

ex_config_interfaces:
  - name: ge-0/0/0
    description: host1
    vlans:
      - employees

  - name: ge-0/0/0
    description: host2
    trusted: false
    vlans:
      - employees

  - name: xe-0/1/0
    description: switch1
    trunk: true
    trusted: true
    vlans:
      - all

  - name: xe-0/1/1
    description: switch2
    trunk: true
    trusted: true
    stormtrusted: false
    vlans:
      - all
```

We obtain the following configuration:

```yaml
ex_config_trusted_settings:
  is_uplink: true
  no_maxhosts: true
  dhcptrusted: true
  stormtrusted: true

ex_config_interfaces:
  - name: ge-0/0/0
    description: host1
    vlans:
      - employees
    # No change, since trusted is not specified, and is therefore implicitly false

  - name: ge-0/0/0
    description: host2
    trusted: false
    vlans:
      - employees
    # No change, since trusted is false

  - name: xe-0/1/0
    description: switch1
    trunk: true
    trusted: true
    vlans:
      - all
    # All contents of ex_config_trusted_settings
    is_uplink: true
    no_maxhosts: true
    dhcptrusted: true
    stormtrusted: true

  - name: xe-0/1/1
    description: switch2
    trunk: true
    trusted: true
    stormtrusted: false
    vlans:
      - all
    # All contents of ex_config_trusted_settings except stormtrusted which was already declared in the interface
    is_uplink: true
    no_maxhosts: true
    dhcptrusted: true
```

### Interface Configuration

Interface variables apply to the `ex_config_interfaces` and `ex_config_laggs` elements.

Interface Variables:

| Option | Default Value | Description | Mandatory |
| --- | --- | --- | --- |
|name |*N/A* |Interface name |Yes |
|description| |Interface description |No |
|speed|*Depending on interface and device* |Speed ​​of the interface or interface group (**EX4650 only**) |No |
|disabled|false |Indicates that the interface is disabled |No |
|toip |false |If you want to potentially connect a phone to this interface. The interface must be in *access* mode if this value is true |No |
|native_vlan | |The native VLAN on the interface. The interface must be in trunk mode if this option is set. The VLAN specified here must not be one of the interface's VLANs |No |
|trunk |false |Indicates whether the interface is in trunk or access port mode |No |
|vlans | |The list of VLANs that pass through this interface |Yes |
|used_by_lagg_or_vcport |false |Indicates that the interface should be ignored because it is used elsewhere |No |

Each interface is an element of the `ex_config_interfaces` or `ex_config_laggs` list.
For example:

```yaml
ex_config_interfaces:
  - name: ge-0/0/5
    description: host42
    trusted: true
    vlans:
      - employees

  - name: ge-0/0/34
    description: other_switch
    trunk: true
    trusted: true
    vlans:
      - all
```

> [!IMPORTANT]
> Be careful with SFP+ ports that can be 1Gb/s, 10Gb/s, 25Gb/s, 40Gb/s, and 100Gb/s: their name prefix varies depending on the speed of the plugged module: `ge-` for 1Gb/s, `xe-` for 10Gb/s, and `et-` for 25Gb/s, 40Gb/s, and 100Gb/s.

### PoE

| Option | Default Value | Description | Mandatory |
| --- | --- | --- | --- |
|ex_config_poeenabled |true | Allows you to disable PoE globally on a device by setting this variable to `false`. |No |

Interface Variables:

| Option | Default Value | Description | Mandatory |
| --- | --- | --- | --- |
|poe |false |Whether to enable PoE on this interface. This value is forced to true when *toip* is true |No |

### Configuring a Redundant Trunk Group (RTG)

[Juniper RTG overview](https://www.juniper.net/documentation/en_US/junos/topics/topic-map/redundant-trunk-groups.html)

For each group, you'll need to add a "primary" configuration to one interface, and a "secondary" configuration to another. Making an interface a member of an RTG automatically disables spanning tree on that interface.

Primary Interface Variables:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|name |*N/A* | RTG interface name (must begin with *rtg* followed by a number) |Yes |
|primary |*N/A* | Indicates that the interface is the primary interface of the RTG, set to `true` |Yes |
|wait_before_restore |1 |Once a primary link is back up, the switch will wait this many seconds (max 600) before switching connectivity back to the primary link |No |

Secondary Interface Variables:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|name |*N/A* |RTG interface name (must start with *rtg* followed by a number) |Yes |
|secondary |*N/A* |Indicates that the interface is the secondary of the RTG, set to `true` |Yes |

For example:

```yaml
  - name: xe-0/1/2
    description: Backup link
    trunk: true
    trusted: true
    vlans:
      - all
    rtg:
      name: rtg0
      secondary: true

  - name: xe-0/1/3
    description: Primary link
    trunk: true
    trusted: true
    vlans:
      - all
    rtg:
      name: rtg0
      primary: true
      wait_before_restore: 30
```

### Configuring an aggregate interface (lagg)

There are two types of configurable laggs:

- The standard aggregate, which aims to share multiple links to increase bandwidth. This aggregate is based on the LACP protocol and must be configured on both devices for the link to go up
- The primary/backup aggregate, which aims to fail over to a backup link when the primary link fails. This aggregate is a (less effective) alternative to RTG, but it avoids creating an active loop of control frames in the network

Most interface options apply to a lagg (except for those that don't really make sense, like `toip`, `poe`, and obviously `member_of_lagg` and `used_by_lagg_or_vcport`).

Interface variables specific to a lagg interface `ex_config_laggs`:

| Option | Default value | Description | Required |
| --- | --- | --- | --- |
|name |*N/A* | Interface name (**must** start with *ae* followed by a number) | Yes |
|speed | | Speed ​​of the slowest link in the aggregate: 1G, 10G | Yes |
|periodic |slow | LACP packet transmission rate (`slow\|fast`) |No |

Interface variables specific to a physical interface `ex_config_interfaces`:

| Option | Default value | Description | Required |
| --- | --- | --- | --- |
|member_of_lagg |false | Indicates that the interface is part of the specified aggregate. If this option is true, only *name* and *description* can be defined. The other configuration elements must be defined in the lagg interface |No |
|lagg_link_protection | |If not defined (default), all interfaces in the lagg will be active. Otherwise, this variable allows you to declare an active/backup lagg (see below) and can only take the values ​​`primary` or `backup` |No |

Each interface is an element of the `ex_config_laggs` list.
For example:

```yaml
ex_config_laggs:
  - name: ae35
    speed: 10g
    description: other_switch
    trunk: true
    trusted: true
    vlans:
      - all
```

This lagg will also need to be associated with its physical interfaces in the interfaces configuration:

```yaml
ex_config_interfaces:
  - name: xe-0/0/35
    description: "ae35 : other_switch"
    member_of_lagg: ae35

  - name: xe-1/0/35
    description: "ae35 : other_switch"
    member_of_lagg: ae35
```

#### Special case of the primary/backup aggregate

This aggregate is configured exactly like the standard aggregate, but it must be attached to exactly two physical interfaces, and you must specify which one will be the primary and which one will be the backup:

```yaml
ex_config_interfaces:
  - name: xe-0/0/35
    description: "ae35 : other_switch"
    member_of_lagg: ae35
    lagg_link_protection: primary


  - name: xe-1/0/35
    description: "ae35 : other_switch"
    member_of_lagg: ae35
    lagg_link_protection: backup
```

In the event of a primary link failure, the backup link will activate within a few seconds. Once the primary link is restored, two distinct behaviors must be distinguished depending on the switch generation:

- Legacy switches (Non-ELS): you must manually revert to the primary link using the `request interface revert ae35` command
- ELS switches: the switch will automatically revert to the primary link

#### Removing a Lagg

Unfortunately, removing a lagg must sometimes be done in two steps; otherwise, applying the QoS rules will result in an error, as it appears that the switch is trying to apply them even though its "internal compilation state" indicates that the interfaces are still associated with a lagg.

The first step is to remove the desired `ae*n*` lagg interface and mark the associated physical interfaces as follows:

```yaml
ex_config_interfaces:
  - name: xe-0/0/0
    used_by_lagg_or_vcport: true
    disabled: true

  - name: xe-1/0/0
    used_by_lagg_or_vcport: true
    disabled: true
```

Once this configuration is deployed, the two interfaces can be reconfigured as desired.

### Configuring an Ethernet Ring Protection Switching (ERPS)

> [!WARNING]
> Although the role is designed to support nested or ladder rings, these scenarios have not been tested

Resources:

- [Understanding Ethernet Ring Protection Switching](https://www.juniper.net/documentation/us/en/software/junos/high-availability/topics/topic-map/ethernet-ring-protection-switching-understanding.html)
- [Configuring Ethernet Ring Protection Switching on Switches](https://www.juniper.net/documentation/en_US/junos/topics/task/configuration/ethernet-ring-protection-cli.html)

The global configuration of the rings is done via the variable `ex_config_erps`, a list declaring each ring, and each element of which can have the following parameters:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|ringname |*N/A* | Ring name (must be unique) |Yes |
|control_vlan |*N/A* | Name of the VLAN dedicated to controlling this ring |Yes |
|data_vlans |*N/A* | List of names of data VLANs transiting through the ring |Yes |
|guard_interval |*device default value* | Guard interval, in milliseconds (10-2000). Prevents ring nodes from receiving outdated RAPS messages |No |
|restore_interval |*device default value* |**Applied only to the ring owner node**. Timeout before recovery, in minutes (5-12 or 1-12 depending on the device). Time during which the owner node waits after the last failure has been resolved, to ensure ring stability before restoring ring operation as configured |No|
|compatibility_version |*default value of the equipment* |Version of the ITU-T G.8032/Y.1344 standard to use (1 or 2). Legacy (non-ELS) equipment is *in principle* only compatible with version 1. **Directive used only on ELS switches**. |No|

Once the rings are declared, all that remains is to declare their East/West interfaces (physical or lagg) and indicate which will be the terminating interface.

Interface variables specific to a physical interface `ex_config_interfaces` or a lagg interface `ex_config_laggs`:

| Option (key) | Option for each item in the list | Default value | Description | Required |
| --- | --- | --- | --- | --- |
| erps | | [] | List of rings to which the interface is associated | No |
| | ringname | *N/A* | | Yes |
| | east_interface | False | Marks the interface as the East interface for the ring specified by ringname | No |
| | west_interface | False | Marks the interface as the West interface for the ring specified by ringname | No |
| | ring_protection_link_end | False | Marks the interface as blocked by default during normal operation, and declares the device as the ring owner. **There MUST be one and only one interface with this value set to True in the entire ring, and the role cannot enforce this constraint.** |No |

#### Specifics of the interfaces member of a ring

A ring member interface must be declared as a trunk, as it will carry at least one data VLAN and the ring's control VLAN.

Since ERPS is incompatible with spanning-tree protocols, the role will automatically disable spanning-tree on all ring member interfaces.

The role will automatically configure the interface's VLANs by aggregating:

1. The data VLANs `data_vlans` declared for each ring associated to the interface
2. The control VLANs `control_vlans` declared for each ring associated to the interface
3. Any VLANs declared in the interface's configuration. This is possible, even though in common usage there are probably no VLANs to declare at the interface level

#### Example

```yaml
ex_config_erps:
  - ringname: erps_ring1
    control_vlan: erps-control-ring1
    data_vlans:
      - employees
      - students
      - storage

  - ringname: erps_ring2
    control_vlan: erps-control-ring2
    data_vlans:
      - employees
      - students
```

```yaml
ex_config_interfaces:
  - name: ge-0/0/0
    trunk: true
    trusted: true
    erps:
      - ringname: erps_ring1
        east_interface: true
        ring_protection_link_end: true

  - name: ge-0/0/1
    trunk: true
    trusted: true
    erps:
      - ringname: erps_ring1
        west_interface: true
```

### Setting up port mirroring

It is sometimes necessary to implement port mirroring to perform network captures.

Interface variables:

| Option | Default value | Description | Mandatory |
| --- | --- | --- | --- |
|portmirroring | |Dictionary with two sub-elements (see example below): `name`, whose value will be the name of the mirroring rule in the device configuration (must be unique), and `from`, a list of interfaces whose traffic will be mirrored on the current interface. If this option is declared, all other interface variables will be ignored except *name*, *description*, and *disabled*, and the port will therefore have no assigned VLAN, will be removed from the spanning tree, and will be removed from the toip interfaces. **If the port is part of an aggregate, it will also be removed** |No |

#### Example

With the following configuration, traffic from interfaces ge-0/0/25 and ge-0/0/26 will be mirrored to interface ge-0/0/5:

```yaml
ex_config_interfaces:
  - name: ge-0/0/5
    description: Exemple portmirroring
    portmirroring:
      name: mirror-example
      from:
        - ge-0/0/25
        - ge-0/0/26
```

## Services configuration

### Sending logs to Syslog servers

To forward logs to one or more Syslog servers, you can declare the `ex_config_syslogservers` variable, which contains a list of Syslog servers. Each entry must have the following attributes:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|ip |*N/A* |Syslog server IP address |Yes |
|port |*N/A* |Syslog server port |Yes |
|comment |*N/A* |Comment about the Syslog server (e.g., its domain name) |Yes |

For example:

```yaml
ex_config_syslogservers:
  - ip: 192.168.42.1
    port: 514
    comment: syslog1.example.com
```

### NTP client

To synchronize the device's clock, you can declare the `ex_config_ntpservers` variable containing a list of NTP servers, each entry of which must have the following attributes:

| Option | Default Value | Description | Mandatory |
| --- | --- | --- | --- |
|ip |*N/A* | IP address of the NTP server | Yes |
|comment |*N/A* | Comment about the NTP server (e.g., its domain name) | Yes |

For example:

```yaml
ex_config_ntpservers:
  - ip: 192.168.42.1
    comment: ntp1.example.com
  - ip: 192.168.42.2
    comment: ntp2.example.com
```

### SNMP

It is possible to enable the read-only SNMP (v2) service on devices in different communities.

Each community must be an element of the `ex_config_snmpcommunities` list with the following attributes:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|name |*N/A* |Community name (must be unique) |Yes |
|clients |[] |List of authorized clients, each entry of which must include the attributes `ip` (IP address of the authorized network), `netmask` (netmask of the authorized network), and `comment` (comment regarding the authorized entry). If the list is empty, access to the community will be allowed from any client |No |

For example:

```yaml
ex_config_snmpcommunities:
  - name: public
    clients:
      - ip: 192.168.42.42
        netmask: 255.255.255.255
        comment: Monitoring server
      - ip: 192.168.253.0
        netmask: 255.255.255.0
        comment: IT subnet
```

Target groups can also be declared to receive SNMP traps from devices using the `ex_config_snmptrapgroups` variable, each entry of which must contain the following attributes:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|name |*N/A* | SNMP target group name (must be unique) |Yes |
|categories |All except `timing-events` |List of [trap categories](https://www.juniper.net/documentation/us/en/software/junos/cli-reference/topics/ref/statement/categories-edit-snmp.html) to be forwarded to targets |No |
|targets | |List of targets in this group, each entry of which must contain the `ip` (IP address of the authorized network) and `comment` (comment about the declared target) attributes |No |

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|ip |*N/A* | SNMP trap target IP address |Yes |
|targets |*N/A* | SNMP trap target comment |Yes |

For example:

```yaml
ex_config_snmptrapgroups:
  - name: monitoring
    categories:
      - authentication
      - chassis
      - link
      - remote-operations
      - routing
      - rmon-alarm
      - configuration
      - services
    targets:
      - ip: 192.168.42.42
        comment: Monitoring server
```

### Basic filtering rules (firewall)

It is possible to prohibit all communication with the device from a list of networks declared in `ex_config_firewall_denied_ips`, each entry of which must contain the following attributes:

| Option | Default value | Description | Mandatory |
| --- | --- | --- | --- |
|ip |*N/A* |IP address of the filtered network |Yes |
|netmask |*N/A* |Network mask of the filtered network (e.g., 255.255.255.255 to filter only the declared IP address) |Yes |
|comment |*N/A* |Comment regarding the filtered entry |Yes |

For example:

```yaml
ex_config_firewall_denied_ips:
  - ip: 192.168.42.42
    netmask: 255.255.255.255
    comment: filtered_host
  - ip: 192.168.18.0
    netmask: 255.255.255.0
    comment: Students subnet
```

### Storm control protection

Storm control is enabled by default on all switches. Its behavior can be configured using the following variables:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|ex_config_enable_stormcontrol |true | Allows you to completely disable storm control by setting the value to `false` |No |
|ex_config_stormtrusted_default |false | Default value that will be applied if the `stormtrusted` interface variable is not set |No |
|ex_config_stormcontrol_bandwidthlevel |4000 | Bandwidth threshold in kbps of the combined monitored traffic beyond which storm control will raise an alert |No |
|ex_config_stormcontrol_shutdown |false |If true, the alert will disable the interface for the duration defined in ex_config_stormcontrol_disable_timeout |No |
|ex_config_stormcontrol_disable_timeout |60 |Time in seconds a triggered interface will be disabled |No |
|ex_config_stormcontrol_monitor_broadcast |true |If true, broadcast traffic will be monitored |No |
|ex_config_stormcontrol_monitor_multicast |false |If true, multicast traffic will be monitored |No |
|ex_config_stormcontrol_monitor_registered_multicast |false |If true, only registered multicast traffic (multicast MAC addresses between 01-00-5E-00-00-00-00 and 01-00-5E-7F-FF) will be monitored. **Directive only used on ELS switches**. |No |
|ex_config_stormcontrol_monitor_unregistered_multicast |false |If true, unregistered multicast traffic (multicast MAC addresses not in the range 01-00-5E-00-00-00-00 to 01-00-5E-7F-FF) will be monitored. **Directive only used on ELS switches**. |No |
|ex_config_stormcontrol_monitor_unknown_unicast |false |If true, unknown unicast traffic will be monitored |No |

See [Understanding Storm Control](https://www.juniper.net/documentation/en/en/software/junos/security-services/topics/concept/rate-limiting-storm-control-understanding.html) for more details.

Interface Variables:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|stormtrusted |{{ ex_config_stormtrusted_default }} |Disables storm detection on the interface, if set to `true`. |No |

### DHCP snooping, dynamic arp inspection and IP source guard

| Options | Default | Description | Mandatory |
| --- | --- | --- | --- |
|ex_config_portsecurity_enable_dhcpsnooping |false |Enables [DHCP snooping](https://www.juniper.net/documentation/en_US/junos/topics/concept/port-security-dhcp-snooping.html) |No |
|ex_config_portsecurity_enable_dynamic_arp_inspection |false |Enables [Dynamic ARP inspection](https://www.juniper.net/documentation/en_US/junos/topics/task/configuration/understanding-and-using-dai.html#id-understanding-arp-spoofing-and-inspection). The *ex_config_portsecurity_enable_dhcpsnooping* option must also be set to `true` for the feature to be active |No |
|ex_config_portsecurity_enable_ip_source_guard |false |Activates [IP Source Guard](https://www.juniper.net/documentation/en_US/junos/topics/concept/port-security-ip-source-guard.html). The *ex_config_portsecurity_enable_dhcpsnooping* option must also be set to `true` for the feature to be active |No |
|ex_config_dhcptrusted_default | |Defines the default value that will be applied to the `dhcptrusted` interface variable when it is not set. By default, when `ex_config_dhcptrusted_default` is not set, it will be set to `true` for trunk mode interfaces, and `false` for access mode interfaces. If `ex_config_dhcptrusted_default` is set, its value will be applied regardless of the interface mode. |No |

Interface Variables:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|dhcptrusted |Variable according to {{ ex_config_dhcptrusted_default }} |Valid only if the switch has the `ex_config_portsecurity_enable_dhcpsnooping` option enabled. <br/> <br/> Indicates whether to trust and therefore ignore DHCP snooping, Dynamic ARP Inspection, and IP Source Guard rules on this interface. <br/> <br/> By default (if `dhcptrusted` and `ex_config_dhcptrusted_default` are not set), an access port interface has this option set to `false`, and an interface in trunk mode has this option set to `true`. If `ex_config_dhcptrusted_default` is set, its value will be the default. |No |
|macstatic | |Only valid if the switch has the `ex_config_portsecurity_enable_dhcpsnooping` option enabled. <br/> <br/> Allows you to declare IP/MAC/VLAN address associations for devices with static addressing, or with erratic DHCP lease renewal. This does not prevent devices that have obtained a DHCP lease from using the interface. See configuration example below. |No |

#### Example `macstatic` configuration

```yaml
ex_config_interfaces:
  - name: ge-0/0/5
    description: Exemple macstatic
    toip: true
    vlans:
      - employees
    macstatic:
      employees:
        192.168.0.1: 00:d3:ad:be:ef:01
        192.168.0.2: 00:d3:ad:be:ef:02
      toip:
        192.168.1.1: 00:d3:ad:be:ef:11
      students:
        # The entry below will be ignored since the vlan is not assigned to the interface
        192.168.2.1: 00:d3:ad:be:ef:21
```

### Restrictions on the number of devices connected to interfaces

It is possible to set a limit on the number of active MAC addresses on an interface, for example to prevent undeclared use of a switch.
This feature is only enabled on interfaces whose `is_uplink` and `no_maxhosts` interface variables are not defined or set to `false`.

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|ex_config_defaultmaxhosts | |Limits the number of devices (MAC addresses) allowed to connect to an access port on all enabled interfaces and whose `no_maxhosts` interface variable is not defined or set to `false`. This value is automatically incremented by one if ToIP is enabled to count the number of phones. If the limit is exceeded, packets from new devices will be rejected by the switch. By default, no limit is active. This value can be fine-tuned or overridden via the `maxhosts` interface parameter | No |

Interface Variables:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|maxhosts | | Limits the number of devices (mac addresses) allowed to connect via this interface. This value is automatically incremented by one if ToIP is enabled to account for the telephone. If the limit is exceeded, packets from new devices will be rejected by the switch. By default, no limit is active, unless the global parameter `ex_config_defaultmaxhosts` is set. This parameter is only taken into account on enabled interfaces, as access ports, and whose interface variable `no_maxhosts` is not defined or set to `false` | No |
|no_maxhosts |false |Disables restrictions on the interface, even when the `maxhosts` or `ex_config_defaultmaxhosts` directives are declared |No |
|is_uplink |false |If `true`, indicates that the interface is used to connect another switch/network device. Its value influences the behavior of COS/QoS, spanning tree, restrictions on the number of devices connected to interfaces, and 802.1X |No |

### Multicast Querier

| Option | Default Value | Description | Mandatory |
| --- | --- | --- | --- |
|ex_config_igmpquerier |{} | Dictionary whose keys are the VLANs on which the switch should act as an IGMP querier, and whose values ​​(if any) are the source IP (v4) that the querier will use to send IGMP messages on this VLAN. This source IP (v4) has no purpose other than to elect the default querier when there is more than one on the network. If the value is not set (`None`), the IP (v4) defined in `ex_config_ipaddress` will be used. A specific VLAN `all` can be declared: its configuration will then apply to all VLANs not explicitly specified. **Directive used only on ELS switches** |No |
|ex_config_mldquerier |{} |Dictionary whose keys are the VLANs on which the switch must act as an MLD querier, and whose values ​​(if any) are the source IP (v6) that the querier will use to send MLD messages on this VLAN. This source IP (v6) has no other purpose than to elect the default querier when there is more than one on the network. A particular VLAN `all` can be declared: its configuration will then apply to all VLANs not explicitly specified. **Directive used only on ELS switches** |No |

### Provisioning virtual chassis members

The configuration of a virtual chassis (VC) is not handled by this role. However, it is possible to provision the list of VC members in `ex_config_virtual_chassis`, each entry of which must contain the following attributes:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|memberid |*N/A* | VC member ID (first starting at 0) | Yes |
|serial |*N/A* | Device serial number | Yes |

For example:

```yaml
ex_config_virtual_chassis:
  - memberid: 0
    serial: AB123456789001
  - memberid: 1
    serial: AB123456789002
```

### Tags for Netmagis

This role automatically adds the tags required by the [Netmagis](http://netmagis.org/config-topo.html) *topo* module.

Activating the feature:

| Option | Default value | Description | Required |
| --- | --- | --- | --- |
|ex_config_enable_netmagis_descriptions |false | Adds tags specific to the Netmagis topo module to the end of interface descriptions |No |

Declare link numbers on the appropriate interfaces with interface variables:

| Option | Default value | Description | Required |
| --- | --- | --- | --- |
|linknumber | |The link number for Netmagis, to be entered only if the interface is connected to another switch. The same number must be declared on the interface of the other switch. This number must be unique and declared in netmagis (`Topo > Link number`). **Parameter taken into account only if `ex_config_enable_netmagis_descriptions` is set to `true`** |No |

### 802.1X (incomplete)

> [!CAUTION]
> **Feature under development**

To configure one or more Radius servers, you can declare the `ex_config_radiusservers` variable, which contains a list of Radius servers. Each entry must have the following attributes:

| Option | Default Value | Description | Mandatory |
| --- | --- | --- | --- |
|ip |*N/A* |Radius server IP address |Yes |
|port |*N/A* |Radius server port |Yes |
|password |*N/A* |Secret key to connect to the Radius server |Yes |

For example:

```yaml
ex_config_radiusservers:
  - ip: 192.168.42.1
    port: 1812
    password: SeCr3t_p4s5w0rD
```

For 802.1X, everything is declared on the interface.

Interface Variables:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|dot1x | |If set, enables 802.1X on the interface. Possible values ​​for this option are <br/> - `dot1x`: Enables only standard 802.1X on the port <br/> - `macradius`: Enables only macradius authentication on the port <br/> - `both`: Enables both 802.1X and macradius authentication on the port |No |

## Spanning tree protocol configuration

[Juniper Comparison of Spanning Tree Protocols](https://www.juniper.net/documentation/us/en/software/junos/stp-l2/topics/topic-map/spanning-tree-configuring-mstp.html#id-understanding-mstp__d6613e107)

The following spanning tree protocols are supported by the role:

- [rstp](https://www.juniper.net/documentation/en_US/junos/topics/topic-map/spanning-tree-configuring-rstp.html)
  - Fast
  - Low CPU overhead
  - Only handles physical loops and does not consider VLANs: therefore, care must be taken to ensure that all VLANs pass through all redundant links,   otherwise there is a risk of VLAN discontinuity
- [mstp](https://www.juniper.net/documentation/en_US/junos/topics/topic-map/spanning-tree-configuring-mstp.html)
  - Fast
  - Low CPU overhead
  - Manages VLAN groups (mstp)
  - Allows for active/active switching with appropriate configuration
  - Interoperable with RSTP

### Root protection

Regardless of the active spanning-tree protocol, this role allows the root protection mechanism to be enabled.
If a BPDU arrives on an interface with this mechanism enabled, and this BPDU would modify the root switch in place, the switch will disable the interface in question to preserve the root and the spanning-tree topology.

This feature is therefore only enabled on edge interfaces, when the `is_uplink` interface variable is not defined or is set to `false`.

| Option | Default Value | Description | Mandatory |
| --- | --- | --- | --- |
|ex_config_enable_rootprotection |false |If `true`, enables the spanning-tree root protection feature |No |

Interface Variables:

| Option | Default Value | Description | Mandatory |
| --- | --- | --- | --- |
|is_uplink |false |If true, indicates that the interface is used to connect another switch/network device. Its value influences the behavior of COS/QoS, spanning tree, restrictions on the number of devices connected to interfaces, and 802.1X |No |

- [Root Protection](https://www.juniper.net/documentation/en_US/junos/topics/topic-map/spanning-tree-root-protection.html#id-understanding-root-protection-for-spanning-tree-instance-interfaces-in-a-layer-2-switched-network).

### BPDU filtering

This role also allows you to enable BPDU filtering on interfaces, to avoid incompatibility and topology change issues more gracefully than with root protection, simply by ignoring BPDUs.

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|ex_config_bpdu_block_default |false | Allows you to set the default value that will be applied to the `bpdu_block` interface variable when it is not defined |No |

This feature will not be enabled if the `stp_link_cost` interface variable is defined on the interface.

Interface Variables:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|bpdu_block |{{ ex_config_bpdu_block_default }} |If `true`, enables filtering of BPDUs arriving on this interface |No |

- [BPDU Protection for Spanning-Tree Protocols](https://www.juniper.net/documentation/us/en/software/junos/stp-l2/topics/topic-map/spanning-tree-bpdu-protection.html).

### Disabling spanning tree

#### Global configuration

To disable spanning tree, simply declare an unrecognized protocol.

Example:

```yaml
# STP configuration
ex_config_stp:
  protocol: None
```

| Option (key) | Possible subkeys | Description | Mandatory |
| --- | --- | --- | --- |
|ex_config_stp | |Global spanning tree configuration |Yes |
| |protocol |The STP protocol to use. `rstp` or `mstp`. Any other value will disable spanning tree on switches |Yes |

### RSTP

The RSTP protocol only handles physical loops and does not take VLANs into account: therefore, care must be taken to ensure that all VLANs pass through all redundant links, otherwise there is a risk of VLAN discontinuity.

#### Global Configuration

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|ex_config_stp_default_bridge_priority |32k |Sets the default spanning tree priority for all devices when `ex_config_stp_bridge_priority` is not set |No |
|ex_config_stp_default_edge_link_cost |200000000 |Sets the default spanning tree cost for an edge interface |No |
|ex_config_stp_bridge_priority |{{ ex_config_stp_default_bridge_priority }} |Overrides the switch's spanning tree priority: the one with the lowest value will be elected root |No |

Sample stp configuration:

```yaml
# STP configuration
ex_config_stp:
  protocol: rstp
```

| Option (key) | Possible subkeys | Description | Required |
| --- | --- | --- | --- |
|ex_config_stp | |Global spanning tree configuration |Yes |
| |protocol |The STP protocol to use. `rstp` or `mstp`. Any other value will disable spanning tree on switches |Yes |

#### Interface Configuration

Interface Variables:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|stp_link_cost |[Automatically determined by the device based on the interface type](https://kb.juniper.net/InfoCenter/index?page=content&id=KB31861) |Link cost for spanning tree. For MSTP, this will only apply to CIST. If this value is not set, the switch will choose a cost based on the link speed |No |
|disable_stp |false |If true, disables spanning tree on this interface |No |
|is_uplink |false |If true, indicates that the interface is being used to connect another switch/network device. Its value influences the behavior of COS/QoS, spanning tree, restrictions on the number of devices connected to interfaces, and 802.1X |No|

If `is_uplink` is not defined or is set to `false`, the interface will be declared as `edge`, and its default cost will be `ex_config_stp_default_edge_link_cost`.

Example of interface configuration:

```yaml
ex_config_laggs:
  - name: ae10
    stp_link_cost: "2000"
```

### MSTP

The MSTP protocol divides its region's network into several spanning tree topologies.

- Each user-defined MSTI is a topology, which contains the VLANs assigned by the user. MSTIs are optional, but not creating one is equivalent to using RSTP.
- The CIST (which must be present) is a topology, which will contain all VLANs not assigned to an MSTI.

When operating with redundant links, it is possible to have a configuration where a backup link for the CIST will be a primary link for an MSTI and vice versa, thus allowing network traffic to be distributed.

#### Global Configuration

| Option | Default Value | Description | Mandatory |
| --- | --- | --- | --- |
|ex_config_stp_default_bridge_priority |32k |Sets the default spanning tree priority for all devices when `ex_config_stp_bridge_priority` or `ex_config_msti_bridge_priority` are not set |No |
|ex_config_stp_default_edge_link_cost |200000000 |Sets the default spanning tree cost for an edge interface |No |
|ex_config_stp_bridge_priority |{{ ex_config_stp_default_bridge_priority }} |Overrides the switch's spanning tree priority: the one with the lowest value will be elected root. For MSTP, this will only apply to the CIST |No |
|ex_config_msti_bridge_priority |{{ ex_config_stp.msti.*mstiID*.bridge_priority }} and otherwise {{ ex_config_stp_default_bridge_priority }} | **Only used for MSTP protocol.** Dictionary where the key is the mstiID and the value is the spanning tree priority of this MSTI. Allows you to override the spanning tree priority of this MSTI on the switch: the one with the lowest value will be elected root |No |
|ex_config_mstp_all_vlans |[] | **Only used for MSTP protocol.** List of all VLANs used in the MSTP configuration - even those not declared on the device. The format is identical to that of the `ex_config_vlans` variable |No |

Example stp configuration:

```yaml
# STP configuration
ex_config_mstp_all_vlans: "{{ ex_config_vlans }}"
ex_config_stp:
  protocol: mstp
  mstp_settings:
    configname: whatever_you_want
    revlevel: 1
    mstis:
      # storage vlan only
      - id: 1
        vlans:
          - storage
      # Some other vlans
      - id: 2
        vlans:
          - employees
          - students
      # All others vlans
      - id: 3
        vlans:
          - -REMAINING-
          - -UNDEFINED-
```

| Option (key) | Possible subkeys | Description | Required |
| --- | --- | --- | --- |
|ex_config_stp | |Global spanning tree configuration |Yes |
| |protocol |The STP protocol to use. `rstp` or `mstp`. Any other value will disable spanning tree on switches |Yes |
| |mstp_settings |The MSTP protocol-specific settings |Yes, if `protocol` is `mstp` |

##### mstp_settings

| Option (key) | Possible subkeys | Description | Required |
| --- | --- | --- | --- |
|configname | |MSTP configuration name |Yes |
|revlevel | |MSTP configuration version |Yes |
|mstis | |List of MSTPs to declare |Yes |
| |id |The MSTI ID (1..4094) |Yes |
| |vlans |The list of VLAN names to be attached to this MSTI. A VLAN can only be attached to one MSTI. It is also possible to specify the `-REMAINING-` keyword, which will be replaced by all VLANs declared on the network and not assigned to another MSTI, and the `-UNDEFINED-` keyword, which will be replaced by all VLANs not declared on the network and not assigned to another MSTI |Yes |

#### Interface Configuration

Interface Variables:

| Option | Default Value | Description | Required |
| --- | --- | --- | --- |
|stp_link_cost |[Automatically determined by the device based on the interface type](https://kb.juniper.net/InfoCenter/index?page=content&id=KB31861) | Spanning tree link cost on the CIST |No |
|msti_link_cost | |Dictionary where the key is the mstiID and the link cost value for this MSTI |No |
|disable_stp |false |If `true`, disables spanning tree on this interface |No |
|is_uplink |false |If `true`, indicates that the interface is used to connect another switch/network device. Its value influences the behavior of COS/QoS, spanning tree, restrictions on the number of devices connected to interfaces, and 802.1X |No |

If `is_uplink` is not defined or is `false`, the interface will be declared as an `edge`, and its default cost will be `ex_config_stp_default_edge_link_cost`.

Example of an interface configuration:

```yaml
ex_config_laggs:
  - name: ae10
    stp_link_cost: "200000"
    msti_link_cost:
      1: "2000"
      2: "200000"
      3: "200000"
```

## QoS / CoS

> [!IMPORTANT]
> Since CoS settings vary depending on the device type (yes, the EX4600/EX4650, I'm talking about you), and the possible settings are infinite, it is impossible to guarantee that this part of the role will be able to apply the CoS policy of your dreams. As the role currently stands, the defined policy is applied to all active interfaces.

> [!WARNING]
> Given the complexity of CoS rules and the large number of possible values ​​for the many variables, the Ansible role does not perform any prior verification. It is therefore advisable to validate the configuration on the different device families **before** deploying it in production.

It is possible to define very fine-grained priority levels based on network flows. In Juniper, this is called CoS (Class of Service). For example, on [Renater](https://services.renater.fr/services_ip/classes_de_services), QoS is based on the DSCP (Differentiated Service Code Point) field.

We will need to distinguish between two types of network interfaces and apply separate CoS rules to them:

1. Interconnect interfaces: These interfaces should only need to apply CoS according to the DSCP field **already included in the IP packet**. In our Ansible role, we distinguish them by the presence of an `is_uplink` variable with a value of *true*.
2. Other interfaces: These interfaces must respect a DSCP field, but also check the type of network traffic passing through, in order to write the appropriate DSCP value if necessary. This is based on firewall-type rules (source IP, destination IP, TCP/UDP protocol, port number, etc.). In our Ansible role, we distinguish them by the presence of an `is_uplink` variable or its value of *false*.

Here is the basic structure of the CoS configuration via Ansible.

```yaml
ex_config_qos:
  qos_company:
    enabled: true
    ip_prefixes:
      hosts_toip:
        - "192.168.250.0/24"
      hosts_backup:
        - "192.168.30.3/32"
        - "192.168.30.42/32"
    classes:
      - (...)
    policers:
      - (...)
```

Everything is done through an `ex_config_qos` dictionary, which itself contains one (or more, although this isn't necessarily a good idea) dictionary whose key is the name of the CoS configuration, and whose value is a dictionary containing the configuration. This configuration is divided into four parts:

| Option (key) | Default value | Description | Mandatory |
| --- | --- | --- | --- |
|enabled |false |Indicates whether this configuration will be active or not on the device |No |
|ip_prefixes |{} |Dictionary containing the name of an IP address/network range alias as the key, and a list of subnets in CIDR notation (192.168.42.0/24) as the value. These aliases can be used in network traffic filtering rules |No |
|classes |N/A |List of class of service configurations, see below for details |Yes |
|policers |[] |List of flow limiting rules. If I had to translate *policer* in this context, it would be "limiter." See below for details. These rules are not mandatory, as the limiter's role is to prevent a flow from exceeding certain limits (e.g., throughput), but they should be used only in moderation because they can be quite harsh when exceeded. |No |

### classes

Example class:

```yaml
    classes:
      - name: voice
        codepoints: "ef" # Expedited-forwarding traffic
        loss_priority: low
        queuenum: 1
        scheduler:
          buffer_size: "10%"
          priority: "strict-high"
        mf_classifier_rules:
          - name: voip
            from:
              source_prefix_list:
                - hosts_toip
              destination_prefix_list:
                - hosts_toip
            then:
              forwarding_class: true
              loss_priority: low
              policer: voip_limit
```

| Option (key) | Possible subkeys | Description | Required |
| --- | --- | --- | --- |
|name | |Unique name (in the entire configuration) of the class |Yes |
|codepoints | |[DSCP value](https://www.juniper.net/documentation/en_US/junos/topics/task/configuration/cos-classifiers-cli.html) associated with this class |Yes |
|loss_priority | |Sets the packet drop priority in case of congestion. Possible values: `high` and `low` |Yes |
|queuenum | |ID of the queue associated with this [class](https://www.juniper.net/documentation/en_US/junos/topics/concept/forwarding-classes-default-cos-config-guide.html) |Yes |
|scheduler | |Reservation values ​​and (soft) limits for this class for the packet scheduler. Limits may be exceeded if there is remaining bandwidth. |Yes |
| |buffer_size |Reservation of a portion of the output buffer (as a percentage), or `remainder` indicating to make do with what is available. |No |
| |transmit_rate |Bandwidth reservation (guaranteed minimum). The value can be an integer (3200..6400000000000) in bits per second, or a percentage (must end with '%'). |No |
| |shaping_rate |Bandwidth limit for the class. The value can be an integer (3200..6400000000000) in bits per second, or a percentage (must end with '%'). |No |
| |priority |Priority of this class (`low` or `strict-high`) |No |
|mf_classifier_rules | |Packet classification rules (firewall type). See below for details. These rules are not mandatory: if there are none, packets will be classified as *best-effort* by default. Furthermore, the switch already includes some classification rules. It is therefore advisable to define these rules for specific network flows (TOIP, backup, video, etc.) |No |

#### mf_classifier_rules

| Option (key) | Possible subkeys | Description | Mandatory |
| --- | --- | --- | --- |
|name | |Unique name (in the entire configuration) of the classification rule |Yes |
|if | |Conditions that a packet must meet to be classified by this rule |Yes |
| |source_prefix_list |(List) The packet must have a source IP address matching one of those declared in one of the specified *ip_prefixes*. |No |
| |source_address |(List) The packet must have a source IP address matching one of those specified. |No |
| |source_port |(List) The packet must have a source port matching one of those specified. It is possible to specify a port range such as `10000-20000` |No |
| |destination_prefix_list |(List) The packet must have a destination IP address matching one of those declared in one of the specified *ip_prefixes*. |No |
| |destination_address |(List) The packet must have a destination IP address matching one of those specified. |No |
| |destination_port |(List) The packet must have a destination port matching one of those specified. It is possible to specify a port range such as `10000-20000`. |No |
| |protocol |(List) The packet must have one of the specified IP protocols: tcp, udp, etc. |No |
| |vlan_id |(List) The packet must come from one of the specified VLAN IDs. |No |
|then | |Classification Actions |Yes |
| |forwarding_class |If true, applies the rules of the current class of service. Should always be `true`... |No |
| |loss_priority |Sets the priority for discarding incoming packets in case of congestion. Possible values ​​are `high` and `low` |No |
| |policer |Applies the specified policer (limiter) |No |

### policers

Example policer:

```yaml
    policers:
      - name: voip_limit
        if_exceeding:
            bandwidth_limit: 1000000
            burst_size_limit: 15000
        then:
          discard: true
```

| Option (key) | Possible subkeys | Description | Mandatory |
| --- | --- | --- | --- |
|name | |Unique name (in the entire configuration) of the policer |Yes |
|if_exceeding | |Sets the limit thresholds |Yes |
| |bandwidth_limit |Bandwidth limit in bits per second. Allowed value range 32000..50000000000 |No |
| |burst_size_limit |Burst size limit in bytes. Allowed value range 1..2147450880 |No |
|then | |Action to take when thresholds are exceeded |Yes |
| |discard |Silently discard packets if the value is `true` |No |
| |loss_priority |Mark packets as the first to be discarded in case of congestion. The only allowed value is `high` |No |

## Deployment

Deployment to all switches:

```bash
ansible-playbook -i network insa_strasbourg.juniper.ex_config
```

On a list of switches, here *juniper1*, *juniper2*, and *juniper3*:

```bash
ansible-playbook -i network -l juniper1,juniper2,juniper3 insa_strasbourg.juniper.ex_config
```

### Tag list

By default (without tags), the playbook will:

1. Run a significant number of checks, which will stop execution if they fail
2. Generate a configuration file locally
3. Push this configuration to the device
4. Validate this configuration with a commit confirm, which must be confirmed within 5 minutes
5. Wait 15 seconds to allow for any connectivity issues
6. Confirm the validation of the new configuration with a *commit*
7. Save the new configuration as a backup configuration: *request system configuration rescue save*

With the `offline` tag, the playbook will:

1. Generate a configuration file locally

With the `check` tag, the playbook will:

1. Generate a configuration file locally
2. Push this configuration to the device
3. Validate this configuration with a commit check, which will determine whether the new configuration is unchanged, different, or invalid

With the tag `quick`, the playbook:

1. Generate a configuration file locally
2. Push this configuration to the device
3. Validate this configuration with a commit confirm, which must be confirmed within 5 minutes
4. Wait 15 seconds to allow for any connectivity issues to occur
5. Confirm the validation of the new configuration with a *commit*
6. Save the new configuration as a rescue configuration: *request system configuration rescue save*

## References

- [Ansible for Junos OS](https://www.juniper.net/documentation/product/us/en/ansible-for-junos-os)
- [Ansible for Junos OS Developer Guide](https://www.juniper.net/documentation/us/en/software/junos-ansible/ansible/topics/concept/junos-ansible-overview.html )
