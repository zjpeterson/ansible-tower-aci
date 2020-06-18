# aci_tower_credential_type
Creates a Credential Type in Ansible Tower that will be compatible with the other roles in this Collection, as well as the `cisco.aci` collection.

## Usage (this role)

### Credential
It's expected that this will be run in AWX/Tower itself, using a Credential of the built-in type "Ansible Tower". If you do *not* want to do that, you'll need to emulate the environment provided in that scenario by setting appropriate environment variables: `TOWER_HOST`, `TOWER_USERNAME`, `TOWER_PASSWORD`, `TOWER_VERIFY_SSL`, and/or `TOWER_OAUTH_TOKEN`.

### Inventory
Since the built-in Credential Type "Ansible Tower" stores hostname information, the only inventory consideration is to use a single target, such as `localhost`, or the name of a single server in your Tower cluster.

### Playbook
The playbook for invoking this role should be very simple, using `connection: local`, an inventory as described above, and specifying this role.

### Variables
The only variable in the role is the name of the Credential Type, `tower_cred_type`. It is set to "Cisco ACI" at the Role Variable level and can be overridden.

## Usage (user credentials)

### Variable outputs
The injector configuration outputs the following:

| Extra variable       | Environment variable | Required | Encrypted |
| -------------------- | -------------------- | -------- | --------- |
| `aci_host`           | `ACI_HOST`           | yes      | no        |
| `aci_validate_certs` | `ACI_VERIFY_SSL`     | no       | n/a       |
| `aci_username`       | `ACI_USERNAME`       | yes      | no        |
| `aci_password`       | `ACI_PASSWORD`       | no       | yes       |
| `aci_private_key`    | `ACI_PRIVATE_KEY`    | no       | yes       |

The environment variables, as well as the host/SSL data, are primarily meant for use with the `aci_inventory` plugin in this Collection, but are nevertheless available if you have another use for them. The extra variables are meant for use with tasks.

You have to provide *either* `aci_password` or `aci_private_key` for the credential to be useful, but the Credential Type does not enforce this, nor does it prevent setting of both.

### Playbooks
If you go on to use Credentials built from this Credential Type with playbooks that use the modules in `cisco.aci`, consider the following example:

```
---
- name: Example ACI playbook
  hosts: apic
  connection: local
  gather_facts: no

  tasks:
  - name: Query tenants
    cisco.aci.aci_tenant:
      host: "{{ ansible_host }}"
      username: "{{ aci_username }}"
      password: "{{ aci_password }}"
      # optionally, instead of password:
      # private_key: "{{ aci_private_key }}"
      state: query
```
The above assumes an inventory with group `apic` that has a single enabled APIC target. You could also use `hosts: localhost` at play level and `host: "{{ aci_host }}"` as module input, however, your task output will be less clear if you do this.
