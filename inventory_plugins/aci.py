DOCUMENTATION = '''
    name: aci
    plugin_type: inventory
    author:
        - Zach Peterson (@zjpeterson)
    short_description: ACI dynamic switch inventory for Ansible Tower
    version_added: "n/a"
    description:
        - Reads switch inventory data from the specified APIC
        - Use case: Build an unused inventory for assistance with Ansible Tower licensing
        - Use case: Enable Ansible Tower as a source of hardware information
    options:
        host:
            description: IP Address or hostname of APIC resolvable by Ansible control host.
            type: string
            required: True
            aliases: [ hostname ]
        username:
            description: The username to use for authentication.
            type: string
            required: True
            aliases: [ user ]
        password:
            description: The password to use for authentication.
            type: string
            required: True
        validate_certs:
            description: If no, SSL certificates will not be validated.
            type: bool
            default: True
            required: False
            aliases: [ verify_ssl ]
'''
EXAMPLES = '''
# example aci.yml file
---
plugin: aci
host: sandboxapicdc.cisco.com
username: admin
password: ciscopsdt
validate_certs: no
'''

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.module_utils.urls import Request

import json


class InventoryModule(BaseInventoryPlugin):

    NAME = 'aci'

    def aci_login(self, aci_session, apic, username, password):
        url = 'https://{}/api/aaaLogin.json'.format(apic)
        payload = {'aaaUser': {'attributes': {'name': username, 'pwd': password}}}
        aci_session.post(url, data=json.dumps(payload))

    def aci_get_nodes(self, aci_session, apic):
        url = 'https://{}/api/node/class/fabricNode.json'.format(apic)
        response = aci_session.get(url)
        return json.loads(response.read())

    def verify_file(self, path):
      super(InventoryModule, self).verify_file(path)
      return path.endswith(('aci.yml', 'aci.yaml'))

    def parse(self,inventory,loader,path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path)

        aci_session = Request(validate_certs=self.get_option('validate_certs'))
        self.aci_login(aci_session, self.get_option('host'), self.get_option('username'), self.get_option('password'))
        nodes = self.aci_get_nodes(aci_session, self.get_option('host'))

        root_group_name = self.inventory.add_group('aci_{}'.format(self.get_option('host').replace('.','_')))
        set_vars = ['serial', 'model', 'address']
        for node in nodes['imdata']:
            group_name = self.inventory.add_group(node['fabricNode']['attributes']['role'])
            self.inventory.add_child(root_group_name, group_name)
            host_name = self.inventory.add_host(node['fabricNode']['attributes']['name'])
            self.inventory.add_child(group_name, host_name)
            for var in set_vars:
                self.inventory.set_variable(host_name, var, node['fabricNode']['attributes'][var])
