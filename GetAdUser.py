#region headers
# escript-template v20190611 / stephane.bourdeaud@nutanix.com
# * author:     MITU Bogdan Nicolae (EEAS-EXT) <Bogdan-Nicolae.MITU@ext.eeas.europa.eu>
# * version:    2019/09/16
# task_name:    GetAdUser
# description:  Given an Active Directory user UPN, check that it can be retrieved
#               from Active Directory by Prism Central.
# endregion

#region capture Calm variables
username = '@@{pc.username}@@'
username_secret = "@@{pc.secret}@@"
api_server = "@@{pc_ip}@@"
ad_user_upn = "@@{platform.metadata.owner_reference.uuid}@@"
ad_user_upn = "@@{ad_user_upn}@@"
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
    "query":ad_user_upn,
    "returned_attribute_list":[
        "userPrincipalName",
        "distinguishedName"
    ],
    "searched_attribute_list":[
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

#region process results
if resp.ok:
    print("Request was successfull; processing results...")
    exit(0)
else:
    #api call failed
    print("Request failed")
    print("Headers: {}".format(headers))
    print("Payload: {}".format(json.dumps(payload)))
    print('Status code: {}'.format(resp.status_code))
    print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
    exit(1)
#endregion


# If the request went through correctly, print it out.  Otherwise error out, and print the response.
if resp.ok:

    #print json.dumps(json.loads(resp.content), indent=4)
    datafile = json.dumps(json.loads(resp.content), indent=4)
    datafile1 = json.loads(datafile) 

    for a in datafile1['search_result_list']:
        datafile2 =  a['name'];
        datafile3  = a['attribute_list']
            
    if len(datafile1['search_result_list']) == 0:
        
        print "The username <<"+ADUser+">> does not exist."
    else:
        print "User name <<" , datafile2 , ">> is valid."

    exit(0)
    
else:
    print "Post request failed", resp.content
    exit(1)