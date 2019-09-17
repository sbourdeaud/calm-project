
#region headers
# escript-template v20190611 / stephane.bourdeaud@nutanix.com
# * author:     MITU Bogdan Nicolae (EEAS-EXT) <Bogdan-Nicolae.MITU@ext.eeas.europa.eu>
# * version:    2019/09/17
# task_name:    SetCalmProjectEnv
# description:  Set up the enviroment configuration for Calm Project. Environment is mandatory to publish the applications into the marketplace. In case while creating a blueprint the VM configuration is not defined then the configuration needs to be defined as part of environment. Also, during the application blueprint launch from marketplace the values are picked from environment. Only one environment per project is applicable in case of different marketplace application blueprints have different VM requirements.
# endregion

#region capture Calm variables
username = "@@{pc.username}@@"
username_secret = "@@{pc.secret}@@"
api_server = "@@{pc_ip}@@"
project_name = "@@{Project_Name}@@"
project_uuid = "@@{Project_UUID}@@"
project_vlan_id = "@@{project_vlan_id}@@"
ahv_network_uuid = "@@{ahv_network_uuid}@@"
ahv_network_name = "@@{ahv_network_name}@@"
env_uuid = "@@{envuuid}@@"
# endregion

#region prepare api call
api_server_port = "9440"
api_server_endpoint = "/api/nutanix/v3/projects_internal/project_uuid"
length = 100
url = "https://{}:{}{}".format(
    api_server,
    api_server_port,
    api_server_endpoint
)
method = "POST"
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Compose the json payload
payload = {
 "spec": {
    "access_control_policy_list": [
      
    ],
    "project_detail": {
      "name": "project_name",
      "resources": {
        "account_reference_list": [
          
        ],
        "environment_reference_list": [
          {
            "kind": "environment",
            "uuid": "env_uuid"
          }
        ],
        "user_reference_list": [
          
        ],
        "external_user_group_reference_list": [
          
        ],
        "subnet_reference_list": [
          {
            "kind": "subnet",
            "name": "ahv_network_name",
            "uuid": "ahv_network_uuid"
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
      "uuid": "project_uuid"
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
# endregion

#region make the api call
print("Making a {} API call to {}".format(method, url))
resp = urlreq(
    url,
    verb=method,
    auth='BASIC',
    user=username,
    passwd=username_secret,
    params=json.dumps(payload),
    headers=headers,
    verify=False
)
# endregion


#region process the results
if resp.ok:
      print json.dumps(json.loads(resp.content), indent=4)
else:
  print "PUT add env to project failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)
# endregion



#!Old Script

#TODO url     = "https://api_server:9440/api/nutanix/v3/projects_internal/project_uuid"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

payload = {
  "spec": {
    "access_control_policy_list": [
      
    ],
    "project_detail": {
      "name": "project_name",
      "resources": {
        "account_reference_list": [
          
        ],
        "environment_reference_list": [
          {
            "kind": "environment",
            "uuid": "env_uuid"
          }
        ],
        "user_reference_list": [
          
        ],
        "external_user_group_reference_list": [
          
        ],
        "subnet_reference_list": [
          {
            "kind": "subnet",
            "name": "ahv_network_name",
            "uuid": "ahv_network_uuid"
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
      "uuid": "project_uuid"
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

resp = urlreq(url, verb='PUT', auth='BASIC', user=username, passwd=username_secret, params=json.dumps(payload), headers=headers)

if resp.ok:
  print json.dumps(json.loads(resp.content), indent=4)
else:
  print "PUT add env to project failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)