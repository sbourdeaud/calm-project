# Set the credentials for Prism
pc_user = '@@{Prism_Central.username}@@'
pc_pass = '@@{Prism_Central.secret}@@'


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
         "name":"@@{UserProject_Name}@@_VPC@@{VlanID}@@_@@{calm_unique}@@",
         "description":"User VPC Project Small size: \n4 vCPUs \n16 GB RAM\n200 GB Storage",
         "resources":{
            "subnet_reference_list":[
               {
                  "kind":"subnet",
                  "uuid":"@@{Subnet_UUID}@@"
               }
            ],
            "resource_domain":{
               "resources":[
                  {
                     "limit":4,
                     "resource_type":"VCPUS"
                  },
                  {
                     "limit":214748364800,
                     "resource_type":"STORAGE"
                  },
                  {
                     "limit":17179869184,
                     "resource_type":"MEMORY"
                  }
               ]
            },
            "user_reference_list":[
               {
                  "kind":"user",
                  "uuid":"@@{ADUser_UUID}@@",
                  "name":"@@{ADUser_UPN}@@"
               }
            ],
            "external_user_group_reference_list":[
               {
                  "kind":"user_group",
                  "uuid":"@@{ADGroup_UUID}@@",
                  "name":"@@{ADGroup_Name}@@"
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
                        "uuid":"@@{ADUser_UUID}@@",
                        "name":"@@{ADUser_UPN}@@"
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
                        "uuid":"@@{ADGroup_UUID}@@",
                        "name":"@@{ADGroup_Name}@@"
                     }
                  ]
                                
               }
            }
         }
      ]
   }
}



# Make the request
resp = urlreq(url, verb='POST', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(payload), headers=headers)

# If the request went through correctly, print it out.  Otherwise error out, and print the response.
if resp.ok:
   print json.dumps(json.loads(resp.content), indent=4)
   print "######Project details######"
   print "Subnet_UUID=" , "@@{Subnet_UUID}@@"
   print "VlanID=" , "@@{VlanID}@@"
   print "User Name= " , "@@{ADUser_UPN}@@"
   print "Group Name=" , "@@{ADGroup_Name}@@"
   
   print "Project_Name={0}".format(json.loads(resp.content)['spec']['project_detail']['name'])
   print "Project_UUID={0}".format(json.loads(resp.content)['metadata']['uuid'])

   exit(0)
else:
    print "Post request failed", resp.content
    exit(1)