# ansible-aci
Ansible Collection for use with [Cisco ACI](https://www.cisco.com/c/en/us/solutions/data-center-virtualization/application-centric-infrastructure/index.html)

Available on Ansible Galaxy as a Collection: [zjpeterson.aci](https://galaxy.ansible.com/zjpeterson/aci)

## Contents

### Plugins

| Name            | Description                                                                                                              |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `aci_inventory` | Builds an Ansible inventory of the physical hardware involved in the associated ACI fabric. See: `docs/aci_inventory.md` |

### Roles

| Name                  | Description                                                                                                                       |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `aci_credential_type` | Creates an Ansible Tower Credential Type compatible with the other content in this Collection. See: `docs/aci_credential_type.md` |
