url     = "https://@@{PC_IP}@@:9440/api/nutanix/v3/projects_internal/@@{Project_UUID}@@"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

payload = {
  "spec": {
    "access_control_policy_list": [
      
    ],
    "project_detail": {
      "name": "@@{Project_Name}@@",
      "resources": {
        "account_reference_list": [
          
        ],
        "environment_reference_list": [
          {
            "kind": "environment",
            "uuid": "@@{envuuid}@@"
          }
        ],
        "user_reference_list": [
          
        ],
        "external_user_group_reference_list": [
          
        ],
        "subnet_reference_list": [
          {
            "kind": "subnet",
            "name": "belbru-nut-vlan@@{VlanID}@@test",
            "uuid": "@@{Subnet_UUID}@@"
          }
        ]
      }
    },
    "user_list": [
      
    ],
    "user_group_list": [
      
    ]
  },
  "api_version": "3.1",
  "metadata": {
    "project_reference": {
      "kind": "project",
      "name": "",
      "uuid": "@@{Project_UUID}@@"
    },
    "kind": "project",
    "spec_version": 0,
    "categories_mapping": {
      
    },
    "owner_reference": {
      "kind": "user",
      "name": "admin",
      "uuid": "00000000-0000-0000-0000-000000000000"
    }
  }
}

pc_user = '@@{Prism_Central.username}@@'
pc_pass = '@@{Prism_Central.secret}@@'

resp = urlreq(url, verb='PUT', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(payload), headers=headers)

if resp.ok:
  print json.dumps(json.loads(resp.content), indent=4)
else:
  print "PUT add env to project failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)