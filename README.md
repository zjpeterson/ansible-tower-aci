# ansible-aci-inventory
Ansible dynamic inventory plugin for use with Cisco ACI
## Overview
When given an APIC target, this plugin builds an Ansible inventory of the physical hardware involved in the associated ACI fabric.

A couple reasons why you may want to use this:

- You use the Settings > License screen in Ansible Tower to determine your usage of managed hosts. However, the physical infrastructure behind your APIC cluster is not accounted for in that data. Including physical infrastructure in a Tower inventory, even if otherwise unused, will account for this discrepency. [More detail here.](https://access.redhat.com/articles/3331481)

- Your organization uses a CMDB, and expects the source of truth to come from your infrastructure's management software (in this case Ansible Tower), rather than the other way around. However, there is not hardware-level data avilable in Ansible Tower to consume in this way. Cached inventory facts can make this information available via the Ansible Tower REST API.

## Inventory Structure

### Groups
The root group name is built from prepending `aci_` to the APIC address specified, replacing `.` characters with `_` characters due to `.` being an invalid character in Ansible group names. For example: `aci_sandboxapicdc_cisco_com`

Example output using `ansible-inventory` and the provided `sandbox_aci.yml`:
```
$ ansible-inventory -i sandbox_aci.yml --playbook-dir=./ --graph
@all:
  |--@aci_sandboxapicdc_cisco_com:
  |  |--@controller:
  |  |  |--apic1
  |  |--@leaf:
  |  |  |--leaf-1
  |  |  |--leaf-2
  |  |--@spine:
  |  |  |--spine-1
  |--@ungrouped:
```

### Host Variables
The plugin currently collects 3 variables about the hardware it finds: `serial`, `model`, `role`, and `address`. These values are provided as host vars.

Example output using `ansible-inventory` and the provided `sandbox_aci.yml`:
```
$ ansible-inventory -i sandbox_aci.yml --playbook-dir=./ --list
{
    "_meta": {
        "hostvars": {
            "apic1": {
                "address": "10.0.0.1",
                "model": "VMware Virtual Platform",
                "role": "controller",
                "serial": "TEP-1-1"
            },
            "leaf-101": {
                "address": "10.0.144.64",
                "model": "N9K-C9396PX",
                "role": "leaf",
                "serial": "TEP-1-101"
            },
            "leaf-102": {
                "address": "10.0.144.66",
                "model": "N9K-C9396PX",
                "role": "leaf",
                "serial": "TEP-1-102"
            },
            "spine-201": {
                "address": "10.0.144.65",
                "model": "N9K-C9508",
                "role": "spine",
                "serial": "TEP-1-103"
            }
        }
    },
[...]
```

## Usage

### Variables

Provide the following information in your inventory:
| Inventory Variable | Environment Variable | Required | Default | Description |
| ------------------ | -------------------- | -------- | ------- | ----------- |
| `host`             | `ACI_HOST`           | yes      | n/a     | IP Address or hostname of APIC resolvable by Ansible control host
| `validate_certs`   | `ACI_VERIFY_SSL`     | no       | `yes`     | If no, SSL certificates will not be validated.
| `username`         | `ACI_USERNAME`       | yes      | n/a     | The username to use for authentication
| `password`         | `ACI_PASSWORD`       | yes      | n/a     | The password to use for authentication
| `flat`             | n/a                  | no       | `no`      | Instruct the plugin not to create child groups.
| `device_roles`     | n/a                  | no       | `['controller', 'leaf', 'spine']` | Instruct the plugin to only get certain device roles.

### Ansible Tower

Recommended Tower usage is to consume the plugin via SCM.

- Create a Credential Type that provides `ACI_USERNAME` and `ACI_PASSWORD` as environment variables
- Create a Credential using the new Credential Type with your APIC login information
- Create a YAML inventory in your SCM that provides `host`, `validate_certs` (optional), and `plugin: aci`
- Consume the YAML inventory in Tower (Inventory > Sources > Create Source > Sourced from a Project > Inventory File), and attach your Credential

#### Credential Type suggestion

Input Configuration
```
fields:
  - id: username
    type: string
    label: APIC Username
    secret: false
  - id: password
    type: string
    label: APIC Password
    secret: true
```

Injector Configuration
```
env:
  ACI_PASSWORD: '{{ password }}'
  ACI_USERNAME: '{{ username }}'
```

## Files
| Name | Description |
| ---- | ----------- |
| `inventory_plugins/aci.py` | The main plugin code. Move to where it makes sense in your envrionment/project.
| `sandbox_aci.yml` | Sample inventory file, using Cisco's always-on public sandbox.
| `tower_api_sample.py` | Sample script which accesses the stored hostvars via the Ansible Tower REST API and prints them to the console.
