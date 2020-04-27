# aci_credential_type

## Overview
Creates an Ansible Tower Credential Type compatible with the other content in this Collection.

This role expects you to use the Ansible Tower built-in credential type to provide access to the Tower install where this Credential Type will be created.

Credentials built using this type will expose the following information:

| Data             | Extra Var         | Envrionment       |
| ---------------- | ----------------- | ----------------- |
| APIC Username    | `aci_username`    | `ACI_USERNAME`    |
| APIC Password    | `aci_password`    | `ACI_PASSWORD`    |
| APIC Private Key | `aci_private_key` | `ACI_PRIVATE_KEY` |

The Environment support is intended to be used with Plugins, such as the `aci_inventory` plugin in this Collection.

The Extra Var support is intended to be used in playbooks where ACI modules require login information. For example:

```
- name: Create Tenant
  cisco.aci.aci_tenant:
    host: "{{ inventory_hostname }}"
    username: "{{ aci_username }}"
    private_key: "{{ aci_private_key }}"
    tenant: mytenant
    state: present
```

## Dependencies

Requires the `awx.awx` collection.

## Variables

If you need the Credenital Type to be called something other than "Cisco ACI", you may set this in `vars/main.yml`.
