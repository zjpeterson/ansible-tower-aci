# aci_aaa_certificate_rotate
Generates a new x509 certificate + RSA key pair, then applies the certificate to an APIC user. This role can update Ansible Tower with the private key.

## Usage

### Role defaults

| Variable            | Description
|-------------------- | -----------
| `apic_user`         | The APIC user to apply the certificate to
| `key_type`          | The type of key to generate
| `key_size`          | The bit size of the key
| `cert_days`         | How many days the certificate is valid for
| `cert_organization` | Organization name on the certificate
| `cert_country`      | Country name on the certificate
| `tower_cred_name`   | The Ansible Tower Credential name to create/update with private key information
| `tower_cred_org`    | The Tower Organization where `tower_cred_name` belongs
| `tower_cred_type`   | The name of the Credential Type to use; see `aci_tower_credential_type` documentation

### Playbooks
Consider the following example:

```
---
- name: Apply certificate to APIC
  hosts: apic
  connection: local
  gather_facts: no

  tasks:
  - include_role:
      name: aci_aaa_certificate_rotate
      tasks_from: generate.yml
  - include_role:
      name: aci_aaa_certificate_rotate
      tasks_from: apic.yml

- name: Apply key and passphrase to Tower
  hosts: tower
  connection: local
  gather_facts: no

  tasks:
  - include_role:
      name: aci_aaa_certificate_rotate
      tasks_from: tower.yml
  - include_role:
      name: aci_aaa_certificate_rotate
      tasks_from: cleanup.yml
```

This assumes two inventory groups, `apic` and `tower`, each having a single target host. You could forego `tower.yml` task, and move the `cleanup.yml` task to the `apic` play, if you don't need the Tower management feature. For example, you may be using an external secrets management system instead.

### Tower

You'll need to apply credentials to the Tower job using your playbook:

* For `apic` play: A Cisco ACI credenital (type created using role `aci_tower_credential_type`)
* For `tower` play: A Tower credential (built-in type "Ansible Tower")
