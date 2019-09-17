# region headers
# escript-template v20190611 / stephane.bourdeaud@nutanix.com
# * author:     MITU Bogdan Nicolae (EEAS-EXT) <Bogdan-Nicolae.MITU@ext.eeas.europa.eu>
# * version:    2019/09/17
# task_name:    NewCalmEnvironment
# description:  Create enviroment configuration for Calm. Environment is mandatory to publish the applications into the marketplace. In case while creating a blueprint the VM configuration is not defined then the configuration needs to be defined as part of environment. Also, during the application blueprint launch from marketplace the values are picked from environment. Only one environment per project is applicable in case of different marketplace application blueprints have different VM requirements.
# output vars:  nameuuid,  imageuuid (environment name and environment uuid)
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
os_user= "@@{local1.username}@@"
os_secret= "@@{local1.secret}@@"
rand_num = "@@{calm_unique}@@"
Image_Name = "@@{Image_Name}@@"
#TODO is this still neede it?  Image_Name = "@@{Image_Name}@@"
vm_name = "vml-@" + my_var + "@"+"rand_num"

#TODO move var up here?  envuuid = str(uuid.uuid4())
#TODO move var up here? nameuuid = str(uuid.uuid4())
#TODO move var up here? my_var1="@{platform.status.resources.nic_list[0].ip_endpoint_list[0].ip}@"
# endregion

#region prepare api call
api_server_port = "9440"
api_server_endpoint = "/api/nutanix/v3/images/list"
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
    "filter":"name==@@{Image_Name}@@", 
    "length": 100, "offset": 0
}
#TODO should we use image_name as a filter?
# endregion

#region make the api call

# endregion


#region process the results

# endregion


#! Old Script moved to GetImageUuid.py

url     = "https://@@{PC_IP}@@:9440/api/nutanix/v3/images/list"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

payload = {"filter":"name==@@{Image_Name}@@", "length": 100, "offset": 0}

username =  '@@{pc.username}@@'
username_secret = '@@{pc.secret}@@'

resp = urlreq(url, verb='POST', auth='BASIC', user=username, passwd=username_secret, params=json.dumps(payload), headers=headers)

if resp.ok:
  print json.dumps(json.loads(resp.content), indent=4)
  imageuuid = json.loads(resp.content)['entities'][0]['metadata']['uuid']

else:
  print "Get image uuid failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)
  
print imageuuid

#! Old script

url     = "https://@@{PC_IP}@@:9440/api/nutanix/v3/environments"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

envuuid = str(uuid.uuid4())
nameuuid = str(uuid.uuid4())
project_name= "@{Project_Name}@"
my_var1="@{platform.status.resources.nic_list[0].ip_endpoint_list[0].ip}@"


print "Environment uuid "+ envuuid
print "Name uuid " +nameuuid

payload = {
  "spec": {
    "name": nameuuid,
    "resources": {
      "substrate_definition_list": [
        {
          "uuid": str(uuid.uuid4()),
          "action_list": [],
          "readiness_probe": {
            "connection_type": "SSH",
            "address": "@" + my_var1 + "@",
            "disable_readiness_probe": True,
            "connection_port": 22,
            "retries": "5",
            "login_credential_local_reference": {
              "kind": "app_credential",
              "uuid": nameuuid
            }
          },
          "editables": {
            "create_spec": {
              "resources": {
                "nic_list": {},
                "serial_port_list": {}
              }
            }
          },
          "os_type": "Linux",
          "type": "AHV_VM",
          "create_spec": {
            "resources": {
              "nic_list": [
                {
                  "subnet_reference": {
                    "uuid": "ahv_network_uuid"
                  },
                  "ip_endpoint_list": []
                }
              ],
              "num_vcpus_per_socket": 1,
              "num_sockets": 2,
              "memory_size_mib": 4096,
              "boot_config": {
                "boot_device": {
                  "disk_address": {
                    "device_index": 0,
                    "adapter_type": "SCSI"
                  }
                }
              },
              "disk_list": [
                {
                  "data_source_reference": {
                    "kind": "image",
                    "name": "@@{Image_Name}@@",
                    "uuid": imageuuid
                  },
                  "device_properties": {
                    "disk_address": {
                      "device_index": 0,
                      "adapter_type": "SCSI"
                    },
                    "device_type": "DISK"
                  }
                }
              ]
            },
            "name": "vm_name",
            "categories": {}
          },
          "variable_list": [],
          "name": "Untitled"
        }
      ],
      "credential_definition_list": [
        {
          "name": "root",
          "type": "PASSWORD",
          "username": "os_user",
          "secret": {
            "attrs": {
              "is_secret_modified": "true"
            },
            "value": "os_secret"
          },
          "uuid": nameuuid
        }
      ]
    }
  },
  "api_version": "3.0",
  "metadata": {
    "kind": "environment",
    "uuid": envuuid
  }
}


username =  '@@{pc.username}@@'
username_secret = '@@{pc.secret}@@'


resp = urlreq(url, verb='POST', auth='BASIC', user=username, passwd=username_secret, params=json.dumps(payload), headers=headers)

if resp.ok:
  print json.dumps(json.loads(resp.content), indent=4)
  print "envuuid={0}".format(json.loads(resp.content)['metadata']['uuid'])
  print "nameuuid={0}".format(json.loads(resp.content)['metadata']['name'])
else:
  print "Post create environment failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)