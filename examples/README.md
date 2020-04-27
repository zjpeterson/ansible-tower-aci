# Examples

Some example code for using this Collection

## aci_inventory

| File                           | Description                                                                               |
| ------------------------------ | ----------------------------------------------------------------------------------------- |
| `tower_api_sample.py`          | Sample script to access the stored hostvars via the Ansible Tower REST API.               |
| `collections/requirements.yml` | Example `requirements.yml` file to resolve Collection dependencies.                       |
| `sandbox_aci.yml`              | Sample inventory file, using Cisco's always-on public sandbox.                            |
| `leaf_only_sandbox_aci.yml`    | Same as above, but uses optional parameters to produce a flat list of only leaf switches. |

## aci_credential_type

| File                           | Description                                                         |
| ------------------------------ | ------------------------------------------------------------------- |
| `collections/requirements.yml` | Example `requirements.yml` file to resolve Collection dependencies. |
| `create_credential_type.yml`   | Sample playbook to invoke `aci_credential_type`                     |
