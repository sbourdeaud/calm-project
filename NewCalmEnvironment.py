url     = "https://@@{PC_IP}@@:9440/api/nutanix/v3/images/list"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

payload = {"filter":"name==@@{Image_Name}@@", "length": 100, "offset": 0,}

pc_user =  '@@{Prism_Central.username}@@'
pc_pass = '@@{Prism_Central.secret}@@'

resp = urlreq(url, verb='POST', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(payload), headers=headers)

if resp.ok:
  print json.dumps(json.loads(resp.content), indent=4)
  imageuuid = json.loads(resp.content)['entities'][0]['metadata']['uuid']

else:
  print "Get image uuid failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)
  
print imageuuid

url     = "https://@@{PC_IP}@@:9440/api/nutanix/v3/environments"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

envuuid = str(uuid.uuid4())
nameuuid = str(uuid.uuid4())
my_var= "@{Project_Name}@"
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
                    "uuid": "@@{Subnet_UUID}@@"
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
            "name": "vml-@" + my_var + "@"+"@@{calm_unique}@@",
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
          "username": "@@{local.username}@@",
          "secret": {
            "attrs": {
              "is_secret_modified": "true"
            },
            "value": "@@{local.secret}@@"
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


pc_user =  '@@{Prism_Central.username}@@'
pc_pass = '@@{Prism_Central.secret}@@'


resp = urlreq(url, verb='POST', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(payload), headers=headers)

if resp.ok:
  print json.dumps(json.loads(resp.content), indent=4)
  print "envuuid={0}".format(json.loads(resp.content)['metadata']['uuid'])
  print "nameuuid={0}".format(json.loads(resp.content)['metadata']['name'])
else:
  print "Post create environment failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)