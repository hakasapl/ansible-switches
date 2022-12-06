# Ansible Site for Managing MOC/OCT Switches
Ansible site for MOC/OCT switches

## Supported Switch OSes

* Dell OS9 (FTOS9)

## Site Setup

1. Install newest version of ansible
1. Install required PyPI packages:
    1. `pip install --user ansible-pylibssh`
1. Install the required ansible modules: `ansible-galaxy collection install -r requirements.yaml`
1. Set up AWS CLI and be sure you can access the correct secrets
1. On your client, you may have to enable legacy kex algorithms for some switches:
    ```
    KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
    ```

## Configuration

### System

System configuration is in the file `host_vars/HOST/config.yaml`

An example of this file is below:
```
---
system:
  stp:
    type: "rstp"
    bridge-priority: 4096
  vlt:
    domain: 1
    priority: 10
    peer-address: "10.0.0.1/20"
    port-channel: 50
```

Each section is an individual section in the "system" yaml dictionary.

#### Spanning Tree (`stp`)

| Field Label     | Description                            | Possible Values                            |
|-----------------|----------------------------------------|--------------------------------------------|
| type            | Type of spanning tree to enable        | "rstp", "mstp", or "pvst"                  |
| bridge-priority | Bridge priority of RSTP                | Integer in the range 0-61440 (RSTP Only)   |

#### Virtual Link Trunking - Dell OS9/OS10 ONLY (`vlt`)

| Field Label     | Description                            | Possible Values                               |
|-----------------|----------------------------------------|-----------------------------------------------|
| domain          | VLT Domain                             | Integer in the range 1-1000                   |
| priority        | Priority of the current system         | Integer in the range 1-65535                  |
| peer-address    | IP address of peer VLT switch          | [IP]/[Prefix] formatted string                |
| port-channel    | VLT trunk port-channel number          | Integer port-channel as defined in interfaces |

### Interfaces

Interfaces are configured in the file `host_vars/HOST/interfaces.yaml`

An example of this file is below:

```
interfaces:
  1/1:
    description: "example interface"
    admin: "up"
    mtu: 9216
```

The interface label must be in the format `STACK/PORT` or `STACK/PORT/FANOUT`

The following tables list all available fields for interface configuration. L2 configurations are mutually exclusive with L3 configurations.

#### General Fields

| Field Label   | Description                            | Possible Values                            |
|---------------|----------------------------------------|--------------------------------------------|
| description   | Description of the interface           | Any string                                 |
| admin         | Admin state of interface               | "up" or "down"                             |
| fanout        | Fanout configuration                   | "single", "dual", or "quad"                |
| fanout_speed  | Fanout speed                           | In the format ##G, such as "10G"           |
| mtu           | MTU of interface                       | Integer with range 1-9216                  |
| custom        | Custom fields in switch conf format    | List of strings                            |

#### L2 Fields

| Field Label   | Description                            | Possible Values                            |
|---------------|----------------------------------------|--------------------------------------------|
| untagged      | VLAN to untag on this interface        | Integer with range 1-4096                  |
| tagged        | List of VLANs to tag on this interface | List of integers with range 1-4096         |
| stp-edge      | Set this port to be an edge port       | "true" or "false"                          |

#### L3 Fields

| Field Label   | Description                            | Possible Values                            |
|---------------|----------------------------------------|--------------------------------------------|
| ip4           | IPv4 address for this interface        | [IP]/[Prefix] IPv4 formatted string        |
| ip6           | IPv6 address for this interface        | [IP]/[Prefix] IPv6 formatted string        |
| keepalive     | Keepalive status                       | "true", "false"                            |

### VLAN Interfaces

Example configuration which adds a vlan interface for vlan `100` with an ipv4 address `10.0.80.3/20`:

```
vlan_interfaces:
  100:
    ip4: "10.0.80.3/20"
```

All fields in interface configuration except L2 fields are available

### Port Channel Interfaces

Example configuration which adds a port channel `79` with a description, in lacp mode, with interface `1/1` and `1/2` part of it:

```
port_channels:
  79:
    description: "example port channel"
    mode: "lacp"
    interfaces: ["1/2", "1/1"]
```

All fields in interface configuration are available, with the following additional fields:

| Field Label   | Description                            | Possible Values                            |
|---------------|----------------------------------------|--------------------------------------------|
| mode          | LAG mode (LACP or normal)              | "LACP" or "normal"                         |
| lacp-rate     | LACP rate configuration                | "fast" or "slow"                           |
| interfaces    | Interfaces that are a part of this LAG | ["1/1", "1/2"]                             |

### VLANs

VLANs are defined in the `group_vars/all/vlans.yaml` file. An example of this file is below:

```
vlans:
  100:
    name: "VLAN 100"
    description: "This is the description of example vlan 100"
    switches:
      - oct_tors
  101:
    name: "VLAN 101"
    description: "This is the description of example vlan 101"
    switches:
      - oct_tors
  102:
    name: "VLAN 102"
    description: "hello world"
    switches:
      - oct_tors
```

The following fields are available for each VLAN:

| Field Label   | Description                                          | Possible Values                            |
|---------------|------------------------------------------------------|--------------------------------------------|
| name          | Name of VLAN                                         | Short string                               |
| description   | Description of VLAN                                  | Any string                                 |
| switches      | Switches and groups that the VLAN should be added to | List of ansible groups or switch hostnames |

**NOTE** VLANs are created on each switch defined here, however, they are not assigned to anything. That must be done in the interface configuration.

## Switch Configuration

Switches will need some manual configuration before being able to be set up from this ansible site.
### Dell OS9 Switches

1. On the switch, enter `conf` mode
1. Set the enable password: `enable password <DEFAULT_OS9_PASSWD>`
1. Set the ssh user `username admin password <DEFAULT_OS9_PASSWD>`
1. Enable ssh server `ip ssh server enable`
1. Set the access IP (usually `managementethernet 1/1`)
