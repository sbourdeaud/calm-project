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
ad_group_name = "@@{ad_group_name}@@"
# endregion

# region prepare api call
api_server_port = "9440"
api_server_endpoint = "/api/nutanix/v3/directory_services/396b243b-cd9c-4668-849e-4fa40ea37bcd/search"
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
    "kind":"user",
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
    #TODO: see if user matches here
    for directory_user in json_resp['entities']:
        #print("Comparing {} with {}".format(nutanix_calm_user_upn,directory_user['status']['name']))
        if nutanix_calm_user_upn == directory_user['status']['name']:
            nutanix_calm_user_uuid = directory_user['metadata']['uuid']
            print("calm_user_uuid={}".format(nutanix_calm_user_uuid))
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
            #TODO: see if user matches here
            for directory_user in json_resp['entities']:
                if calm_user_upn == directory_user['status']['name']:
                    calm_user_uuid = directory_user['metadata']['uuid']
                    print("calm_user_uuid={}".format(calm_user_uuid))
                    exit(0)
        else:
            print("Request failed")
            print("Headers: {}".format(headers))
            print("Payload: {}".format(json.dumps(payload)))
            print('Status code: {}'.format(resp.status_code))
            print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
            exit(1)
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
# Set the headers, url, and payload
url     = "https://@@{PC_IP}@@:9440/api/nutanix/v3/directory_services/396b243b-cd9c-4668-849e-4fa40ea37bcd/search"


payload =  {"query":"@@{ADGroup_Name}@@","returned_attribute_list":["memberOf","member","userPrincipalName","distinguishedName"],"searched_attribute_list":["name","userPrincipalName","distinguishedName"]}

# Make the request
  
resp = urlreq(url, verb='POST', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(payload), headers=headers)


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