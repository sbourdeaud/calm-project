#region headers
# escript-template v20190611 / stephane.bourdeaud@nutanix.com
# * author:     MITU Bogdan Nicolae (EEAS-EXT) <Bogdan-Nicolae.MITU@ext.eeas.europa.eu>
# * version:    2019/09/17
# task_name:    NewCalmProject
# description:  Create a new project in different sizes: small, medium, large, configured with an unique VlanID, with project owner having the "Project Admin role".
# output vars:  project_name, project_uuid
# endregion

#region capture Calm variables
username = "@@{pc.username}@@"
username_secret = "@@{pc.secret}@@"
rand_num = "@@{calm_unique}@@"
ahv_network_uuid = "@@{ahv_network_uuid}@@"
project_vlan_id = "@@{project_vlan_id}@@"
calm_user_uuid = "@@{calm_user_uuid}@@"
calm_user_upn = "@@{calm_username}@@"
ad_group_name = "@@{ad_group_name}@@"
ad_group_uuid = "@@{ad_group_uuid}@@"
project_size = "@@{project_size}@@"
environment_uuid = "@@{environment_uuid}@@"
project_admin_role_uuid = "@@{project_admin_role_uuid}@@"
developer_role_uuid = "@@{developer_role_uuid}@@"
consumer_role_uuid = "@@{consumer_role_uuid}@@"
#input from user
user_project_name = "@@{user_project_name}@@"
#endregion

#region define variables
project_name = "{0}_VPC{1}_{2}".format(user_project_name,project_vlan_id,rand_num)
#TODO check var .eg. POC2_VPC65_09131
max_vcpu = 4
max_memory = 16*1073741824
max_storage = 200*1073741824
medium_multiplier = 2
large_multiplier = 4
if project_size == "medium":
   max_vcpu = max_vcpu*medium_multiplier
   max_mem = max_mem*medium_multiplier
   max_storage = max_storage*medium_multiplier   
if project_size == "large":
   max_vcpu = max_vcpu*large_multiplier
   max_mem = max_mem*large_multiplier
   max_storage = max_storage*large_multiplier 
# endregion

#region prepare api call
api_server_port = "9440"
api_server_endpoint = "/api/nutanix/v3/projects_internal"
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
   "api_version":"3.1.0",
   "metadata":{
      "kind":"project"
   },
   "spec":{
      "project_detail":{
         "name":project_name,
         "description":"Created for {}".format(calm_user_upn),
         "resources":{
            "subnet_reference_list":[
               {
                  "kind":"subnet",
                  "uuid":ahv_network_uuid
               }
            ],
            "resource_domain":{
               "resources":[
                  {
                     "limit":max_vcpu,
                     "resource_type":"VCPUS"
                  },
                  {
                     "limit":max_storage,
                     "resource_type":"STORAGE"
                  },
                  {
                     "limit":max_memory,
                     "resource_type":"MEMORY"
                  }
               ]
            },
            "user_reference_list":[
               {
                  "kind":"user",
                  "uuid":calm_user_uuid,
                  "name":calm_user_upn
               }
            ],
            "external_user_group_reference_list":[
               {
                  "kind":"user_group",
                  "uuid":ad_group_uuid,
                  "name":ad_group_name
               }
            ],
            "environment_reference_list": [
               {
                  "kind": "environment",
                  "uuid": environment_uuid
               }
            ],
         }
      },
      "access_control_policy_list":[
         {
            "operation":"ADD",
            "metadata":{
               "kind":"access_control_policy"
            },
            "acp":{
               "name":"prismui-name-428e618abe71",
               "description":"prismui-desc-ad5dd335dd14",
               "resources":{
                  "role_reference":{
                     "kind":"role",
                     "name":"Project Admin",
                     "uuid":project_admin_role_uuid
                  },
                  "user_reference_list":[
                     {
                        "kind":"user",
                        "uuid":calm_user_uuid,
                        "name":calm_user_upn
                     }
                  ] 
               }
            }
         },
         {
            "operation":"ADD",
            "metadata":{
               "kind":"access_control_policy"
            },
            "acp":{
               "name":"prismui-name-22b4b5a2b5fd",
               "description":"prismui-desc-225d2f0c16d5",
               "resources":{
                  "role_reference":{
                     "kind":"role",
                     "name":"Developer",
                     "uuid":developer_role_uuid
                  },
                  "user_group_reference_list":[
                     {
                        "kind":"user_group",
                        "uuid":ad_group_uuid,
                        "name":ad_group_name
                     }
                  ]
                                
               }
            }
         }
      ]
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
   print "######Project details######"
   print "Vlan ID for this project is {}".format(project_vlan_id)
   print "User Name for this project is {}".format(calm_user_upn)
   print "Group Name for this project is {}".format(ad_group_name)
   
   print "project_name={0}".format(json.loads(resp.content)['spec']['project_detail']['name'])
   print "project_uuid={0}".format(json.loads(resp.content)['metadata']['uuid'])

   exit(0)
else:
    #api call failed
    print("Request failed")
    print("Headers: {}".format(headers))
    print("Payload: {}".format(json.dumps(payload)))
    print('Status code: {}'.format(resp.status_code))
    print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
    exit(1)
# endregion







#! Old script


# Set the credentials for Prism
username = '@@{Prism_Central.username}@@'
username_secret = '@@{Prism_Central.secret}@@'


# Set the headers, url, and payload
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url     = "https://@@{PC_IP}@@:9440/api/nutanix/v3/projects_internal"

payload = {
   "api_version":"3.1.0",
   "metadata":{
      "kind":"project"
   },
   "spec":{
      "project_detail":{
         "name":"project_name",
         "description":"User VPC Project Small size: \n4 vCPUs \n16 GB RAM \n200 GB Storage",
         "resources":{
            "subnet_reference_list":[
               {
                  "kind":"subnet",
                  "uuid":"ahv_network_uuid"
               }
            ],
            "resource_domain":{
               "resources":[
                  {
                     "limit":"p_vcpu",
                     "resource_type":"VCPUS"
                  },
                  {
                     "limit":"p_storage",
                     "resource_type":"STORAGE"
                  },
                  {
                     "limit":"p_mem",
                     "resource_type":"MEMORY"
                  }
               ]
            },
            "user_reference_list":[
               {
                  "kind":"user",
                  "uuid":"calm_user_uuid",
                  "name":"calm_user_upn"
               }
            ],
            "external_user_group_reference_list":[
               {
                  "kind":"user_group",
                  "uuid":"ad_group_uuid,
                  "name":"ad_group_name"
               }
            ]
         }
      },
      "access_control_policy_list":[
         {
            "operation":"ADD",
            "metadata":{
               "kind":"access_control_policy"
            },
            "acp":{
               "name":"prismui-name-428e618abe71",
               "description":"prismui-desc-ad5dd335dd14",
               "resources":{
                  "role_reference":{
                     "kind":"role",
                     "name":"Project Admin",
                     "uuid":"75488899-853f-4a88-a9a5-20f388d141de"
                  },
                  "user_reference_list":[
                     {
                        "kind":"user",
                        "uuid":"calm_user_uuid",
                        "name":"calm_user_upn"
                     }
                  ] 
               }
            }
         },
         {
            "operation":"ADD",
            "metadata":{
               "kind":"access_control_policy"
            },
            "acp":{
               "name":"prismui-name-22b4b5a2b5fd",
               "description":"prismui-desc-225d2f0c16d5",
               "resources":{
                  "role_reference":{
                     "kind":"role",
                     "name":"Developer",
                     "uuid":"2676bf44-45b2-4a85-806c-948296665c0b"
                  },
                  "user_group_reference_list":[
                     {
                        "kind":"user_group",
                        "uuid":"ad_group_uuid",
                        "name":"ad_group_name
                     }
                  ]
                                
               }
            }
         }
      ]
   }
}



# Make the request
resp = urlreq(url, verb='POST', auth='BASIC', user=username, passwd=username_secret, params=json.dumps(payload), headers=headers)

# If the request went through correctly, print it out.  Otherwise error out, and print the response.
if resp.ok:
   print json.dumps(json.loads(resp.content), indent=4)
   print "######Project details######"
   print "ahv_network_uuid=" , "@@{ahv_network_uuid}@@"
   print "VlanID=" , "@@{project_vlan_id}@@"
   print "User Name= " , "calm_user_upn"
   print "Group Name=" , "ad_group_name"
   
   print "project_name={0}".format(json.loads(resp.content)['spec']['project_detail']['name'])
   print "project_uuid={0}".format(json.loads(resp.content)['metadata']['uuid'])

   exit(0)
else:
    print "Post request failed", resp.content
    exit(1)