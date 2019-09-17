#region headers
# escript-template v20190611 / stephane.bourdeaud@nutanix.com
# * author:     stephane.bourdeaud@nutanix.com
# * version:    2019/09/17
# task_name:    GetPcDirectoryServicesUuid
# description:  Returns the UUID of the directory matching the domain of
#               the Calm user.
# output vars:  directory_uuid
# endregion

#region capture Calm variables
username = '@@{pc.username}@@'
username_secret = "@@{pc.secret}@@"
api_server = "@@{pc_ip}@@"
nutanix_calm_user_upn = "@@{calm_username}@@"
# endregion

#region define variables
directory_name = (nutanix_calm_user_upn.split("@"))[1]
#endregion

# region prepare api call
api_server_port = "9440"
api_server_endpoint = "/api/nutanix/v3/directory_services/list"
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
    for directory in json_resp['entities']:
        if directory_name == directory['status']['resources']['domain_name']:
            directory_uuid = directory['metadata']['uuid']
            print("directory_uuid={}".format(directory_uuid))
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

if directory_uuid is None:
    print("Could not find UUID for directory services with name {}".format(directory_name))
    exit(1)
# endregion