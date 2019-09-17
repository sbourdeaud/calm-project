#region headers
# escript-template v20190611 / stephane.bourdeaud@nutanix.com
# * author:     Bogdan-Nicolae.MITU@ext.eeas.europa.eu,
# *             stephane.bourdeaud@nutanix.com
# * version:    2019/09/17
# task_name:    GetAdGroup
# description:  Given an AD group, return information from the directory.
# endregion

#region capture Calm variables
username = '@@{pc.username}@@'
username_secret = "@@{pc.secret}@@"
api_server = "@@{pc_ip}@@"
project_vlan_id = "@@{project_vlan_id}@@"
directory_uuid = "@@{directory_uuid}@@"
#endregion

#region define variables
ad_group_name = "NUT_EEAS_R_TLAB{}Admins".format(project_vlan_id)
#endregion

# region prepare api call
api_server_port = "9440"
api_server_endpoint = "/api/nutanix/v3/directory_services/{}/search".format(directory_uuid)
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
    "query":ad_group_name,
    "returned_attribute_list":[
        "memberOf",
        "member",
        "userPrincipalName",
        "distinguishedName"
    ],
    "searched_attribute_list":[
        "name",
        "userPrincipalName",
        "distinguishedName"
    ]
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
#endregion

#region process the results
if resp.ok:
    json_resp = json.loads(resp.content)
    #TODO if the search returned something, then we need to check if PC already
    #TODO has a uuid for this object, if not, create one.
    #TODO if the search returned no result, print an error that the group does
    #TODO not exist.
    exit(0)
else:
    # print the content of the response (which should have the error message)
    print("Request failed", json.dumps(
        json.loads(resp.content),
        indent=4
    ))
    print("Headers: {}".format(headers))
    print("Payload: {}".format(payload))
    exit(1)
# endregion

#* Old code 
# If the request went through correctly, print it out.  Otherwise error out, and print the response.

if resp.ok:
    datafile = json.dumps(json.loads(resp.content), indent=4)
    datafile1 = json.loads(datafile) 

    for a in datafile1['search_result_list']:
        datafile2 =  a['name'];
        datafile3  = a['attribute_list']
            
    if len(datafile1['search_result_list']) == 0:
        
        print "The Active Directory Group <<"+ADGroup+">> does not exist."
    else:
        print "Active Directory Group <<" , datafile2 , ">> is valid."

    exit(0)
    
else:
    print "Post request failed", resp.content
    exit(1)