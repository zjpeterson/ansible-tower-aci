#!/usr/bin/python3

# Sample code for utilizing Ansible Tower
# hostvars created by Ansible ACI Inventory plugin
# Author: Zach Peterson (@zjpeterson)

import requests
import json

def main():
    # Enter details of Tower environment
    tower_user = 'zach'
    tower_pass = 'M7000p9!'
    tower_host = '10.15.108.156'
    # Enter numeric ID of ACI Inventory
    # Can be found in the URL bar when browsing to the inventory
    # in the web UI after '#/inventories/inventory/'
    tower_inventory_id = 4
    # Session setup
    session = requests.Session()
    session.auth = (tower_user, tower_pass)
    session.verify = False
    # Query hosts in inventory
    url = 'https://{}/api/v2/inventories/{}/hosts/'.format(tower_host, tower_inventory_id)
    response = session.get(url)
    data = response.json()
    output = {'aci_physical': []}
    # Query variable data from discovered hosts
    for host_entry in data['results']:
        url = 'https://{}/api/v2/hosts/{}/variable_data/'.format(tower_host, host_entry['id'])
        host_response = session.get(url)
        host_data = host_response.json()
        host_data.update({'name': host_entry['name']})
        output['aci_physical'].append(host_data)
    # Print queried data
    print(json.dumps(output, indent=1))

if __name__ == "__main__":
    main()
