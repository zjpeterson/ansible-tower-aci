# aci_aaa_user_security
Creates/maintains an APIC user to use with Ansible, and applies desired security roles.

The user creation sets a generated password. This role can update Ansible Tower with this password. This role can also be run multiple times, and each time will act as a password rotation. *Note that, by default, APIC does not permit more than two password changes within 48 hours*

## Usage

## Role defaults

| Variable                | Description
| ----------------------- | -----------
| `apic_user`             | The APIC user to create/update
| `apic_user_permissions` | Permissions to assign to the APIC user, see below
| `tower_cred_name`       | The Ansible Tower Credential name to create/update with password information
| `tower_cred_org`        | The Tower Organization where `tower_cred_name` belongs
| `tower_cred_type`       | The name of the Credential Type to use; see `aci_tower_credential_type` documentation

### User permissions

The `apic_user_permissions` variable should be a list of dictionaries describing the domain, role, and acccess assignments the managed user should have. The default is:
```
apic_user_permissions:
  - domain: all
    role: aaa
    access: writePriv
```
This results in a user that is suitable for managing the certificates of other users. It can be modified to grant any permission. Reference the [Cisco ACI documentation](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/4-x/basic-configuration/Cisco-APIC-Basic-Configuration-Guide-42x/Cisco-APIC-Basic-Configuration-Guide-42x_chapter_011.html).

### Playbooks
Consider the following example:

```
---
- name: Create user
  hosts: apic
  connection: local
  gather_facts: no

  tasks:
  - include_role:
      name: aci_aaa_user_security
      tasks_from: apic.yml

- name: Create/update Tower credential
  hosts: tower
  connection: local
  gather_facts: no

  tasks:
  - include_role:
      name: aci_aaa_user_security
      tasks_from: tower.yml
```

This assumes two inventory groups, `apic` and `tower`, each having a single target host. You could forego the second play if you don't need the Tower management feature. For example, you may be using an external secrets management system instead.

### Tower

You'll need to apply credentials to the Tower job using your playbook:

* For `tasks/apic.yml`: A Cisco ACI credenital (type created using role `aci_tower_credential_type`)
* For `tasks/tower.yml`: A Tower credential (built-in type "Ansible Tower")
