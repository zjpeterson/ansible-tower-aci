#!/usr/bin/python3

# Sample code for utilizing Ansible Tower
# hostvars created by Ansible ACI Inventory plugin
# Author: Zach Peterson (@zjpeterson)

import requests
import json

def main():
    tower_user = 'toweruser'
    tower_pass = 'towerpass'
    tower_host = 'tower.example.com'
    tower_inventory_id = 4
    session = requests.Session()
    session.auth = (tower_user, tower_pass)
    session.verify = False
    url = 'https://{}/api/v2/inventories/{}/hosts/'.format(tower_host, tower_inventory_id)
    response = session.get(url)
    data = response.json()
    output = {'aci_physical': []}
    for host_entry in data['results']:
        url = 'https://{}/api/v2/hosts/{}/variable_data/'.format(tower_host, host_entry['id'])
        host_response = session.get(url)
        host_data = host_response.json()
        host_data.update({'name': host_entry['name']})
        output['aci_physical'].append(host_data)
    print(json.dumps(output, indent=1))

if __name__ == "__main__":
    main()
