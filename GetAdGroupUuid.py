#region headers
# escript-template v20190611 / stephane.bourdeaud@nutanix.com
# * author:     Bogdan-Nicolae.MITU@ext.eeas.europa.eu,
# *             stephane.bourdeaud@nutanix.com
# * version:    2019/09/17
# task_name:    GetAdGroupUuid
# description:  Given an AD group, return information from the directory.
# output vars:  ad_group_uuid
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

#region search for group in Active Directory
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
    if len(json_resp['search_result_list']) == 0:
        print("The Active Directory group {} does not exist.".format(ad_group_name))
        exit(1)
    else:
        print("The Active Directory group {} exists. Checking for UUID in Prism Central...".format(ad_group_name))
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
#endregion

#region retrieve group uuid from Prism Central
# region prepare api call
api_server_port = "9440"
api_server_endpoint = "/api/nutanix/v3/user_groups/list"
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
    "kind":"user_group",
    "length":length,
    "offset":0
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
    print("Printing results from {} to {}".format(json_resp['metadata']['offset'], json_resp['metadata']['length']))
    for directory_user in json_resp['entities']:
        if ad_group_name == directory_user['status']['name']:
            ad_group_uuid = directory_user['metadata']['uuid']
            print("ad_group_uuid={}".format(ad_group_uuid))
            exit(0)
    while json_resp['metadata']['length'] is length:
        payload = {
            "kind": "user",
            "length":length,
            "offset": json_resp['metadata']['length'] + json_resp['metadata']['offset'] + 1
        }
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
        if resp.ok:
            json_resp = json.loads(resp.content)
            print("Processing results from {} to {}".format(json_resp['metadata']['offset'], json_resp['metadata']['offset'] + json_resp['metadata']['length']))
            for directory_user in json_resp['entities']:
                if ad_group_name == directory_user['status']['name']:
                    ad_group_uuid = directory_user['metadata']['uuid']
                    print("ad_group_uuid={}".format(ad_group_uuid))
                    exit(0)
        else:
            print("Request failed")
            print("Headers: {}".format(headers))
            print("Payload: {}".format(json.dumps(payload)))
            print('Status code: {}'.format(resp.status_code))
            print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
            exit(1)
    if ad_group_uuid is None:
        print("Group {} does not have a UUID in Prism Central. Creating UUID...".format(ad_group_name))
        #TODO add code here to create uuid in PC
        
    else:
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
#endregion