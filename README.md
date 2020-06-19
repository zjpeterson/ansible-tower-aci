# ansible-tower-aci
Ansible Collection for use with [Cisco ACI](https://www.cisco.com/c/en/us/solutions/data-center-virtualization/application-centric-infrastructure/index.html), focused on the use of Ansible Tower.

Available on Ansible Galaxy as a Collection: [zjpeterson.aci](https://galaxy.ansible.com/zjpeterson/aci)

For best experience, read this documentation on [GitHub Pages](https://zjpeterson.github.io/ansible-tower-aci/).

A walkthrough of `aci_inventory` can be found on the [Ansible Blog](https://www.ansible.com/blog/using-cisco-aci-as-inventory-for-ansible-tower).

## Contents

### Plugins

Please reference the full documentation under `docs/` and the examples under `examples/`.

| Plugin | Description |
| --- | --- |
| [aci_inventory](./docs/aci_inventory) | Builds an Ansible inventory of the physical hardware involved in the associated ACI fabric. |

### Roles

Please reference the full documentation under `docs/` and the example playbooks under `playbooks/`.

| Role | Description |
| --- | --- |
| [aci_tower_credential_type](./roles/aci_tower_credential_type) | Creates an Ansible Tower Credential Type for Cisco ACI. |
| [aci_aaa_user_security](./roles/aci_aaa_user_security) | Creates/maintains an APIC user to use with Ansible, applies desired security roles, updates Tower. |
| [aci_aaa_certificate_rotate](./roles/aci_aaa_certificate_rotate) | Generates a new x509 certificate + RSA key pair, applies it to an APIC user, updates Tower. |

## Integration

These pieces fit together. You can, for instance:

1. Use `aci_tower_credential_type` to define a Cisco ACI credential type in Tower
2. Use `aci_aaa_user_security` to create an APIC user to manage other APIC users, and store the password in Tower
3. Use `aci_aaa_user_security` on a schedule to keep the password rotated, if that's a requirement for your organization
4. Use `aci_aaa_user_security` again to create an APIC admin user with wider permission to make changes
5. Use `aci_aaa_certificate_rotate` to convert the APIC admin user to certificate-based authentication (a best practice)
6. Use `aci_aaa_certificate_rotate` on a schedule to keep the certificate rotated, if that's a requirement for your organization
7. Use `aci_inventory` with the APIC admin credential to keep Tower current with the physical inventory of your ACI fabric
8. Use the APIC admin credential to reliably provide `cisco.aci` modules with login information
