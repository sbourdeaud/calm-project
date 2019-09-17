# region headers
# escript-template v20190611 / stephane.bourdeaud@nutanix.com
# * author:     MITU Bogdan Nicolae (EEAS-EXT) <Bogdan-Nicolae.MITU@ext.eeas.europa.eu>
# * version:    2019/09/17
# task_name:    GetImageUuid
# description:  Get the UUID of the image that will be published on the new project.
# output vars:  image_uuid
# endregion

#region capture Calm variables
username = "@@{pc.username}@@"
username_secret = "@@{pc.secret}@@"
api_server = "@@{pc_ip}@@"
Image_Name = "@@{Image_Name}@@"


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
  image_uuid = json.loads(resp.content)['entities'][0]['metadata']['uuid']
print "image_uuid={0}".format(json.loads(resp.content)['metadata']['uuid'])

else:
  print "Get image uuid failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)
# endregion


#! Old Script moved to GetImageUuid.py

url     = "https://api_server:9440/api/nutanix/v3/images/list"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

payload = {"filter":"name==@@{Image_Name}@@", "length": 100, "offset": 0}

username =  '@@{pc.username}@@'
username_secret = '@@{pc.secret}@@'

resp = urlreq(url, verb='POST', auth='BASIC', user=username, passwd=username_secret, params=json.dumps(payload), headers=headers)

if resp.ok:
  print json.dumps(json.loads(resp.content), indent=4)
  image_uuid = json.loads(resp.content)['entities'][0]['metadata']['uuid']
print "image_uuid={0}".format(json.loads(resp.content)['metadata']['uuid'])

else:
  print "Get image uuid failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)