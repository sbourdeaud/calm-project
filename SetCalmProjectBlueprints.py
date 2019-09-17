
#region headers
# escript-template v20190611 / stephane.bourdeaud@nutanix.com
# * author:     MITU Bogdan Nicolae (EEAS-EXT) <Bogdan-Nicolae.MITU@ext.eeas.europa.eu>
# * version:    2019/09/17
# task_name:    SetCalmProjectBlueprints
# description:  Publish existing CALM Blueprints on the new project created. Blueprints will be added into a list. The list will be populated by Nutanix Admins and stored on a CALM macro.
# endregion

#region capture Calm variables
username = "@@{pc.username}@@"
username_secret = "@@{pc.secret}@@"
api_server = "@@{pc_ip}@@"
project_name = "@@{Project_Name}@@"
project_uuid = "@@{Project_UUID}@@"
# endregion

#region prepare api call
api_server_port = "9440"
api_server_endpoint = "/api/nutanix/v3/marketplace_items/list"
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
    "filter":"app_state==PUBLISHED",
    "length":1000
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
print("Making a {} API call to {}".format(method, url))

myresp = json.loads(resp.content)

if resp.ok:
  for i in myresp['entities']:
    print i['metadata']['uuid']
    mp_uuid = i['metadata']['uuid']
    urlitem="https://api_server:9440/api/nutanix/v3/calm_marketplace_items/"+str(mp_uuid)
    respitem = urlreq(urlitem, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, headers=headers)
    print respitem.status_code
    payloaditem = json.loads(respitem.content)
    payloaditem['metadata'].pop('owner_reference', None)
    payloaditem.pop('status', None)
    payloaditem['metadata'].pop('create_time', None)
    app_project =  {
        "kind": "project",
        "name": "project_name",
        "uuid": "project_uuid"
        }
    payloaditem['spec']['resources']['project_reference_list'].append(app_project)
    print payloaditem['spec']['resources']['project_reference_list']
    respitemput = urlreq(urlitem, verb='PUT', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(payloaditem), headers=headers)
    print json.dumps(json.loads(respitemput.content), indent=4)
    if respitemput.ok:
      print "App with uuid : "+mp_uuid+" is published"
    else:
      print "Can't publish APP with uuid :"+mp_uuid
      exit(1)
else:
  print "Get MP Items list failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)
# endregion




#! Old code

url     = "https://api_server:9440/api/nutanix/v3/marketplace_items/list"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

payload = {"filter":"app_state==PUBLISHED","length":1000}

resp = urlreq(url, verb='POST', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(payload), headers=headers)

myresp = json.loads(resp.content)

if resp.ok:
  for i in myresp['entities']:
    print i['metadata']['uuid']
    mp_uuid = i['metadata']['uuid']
    urlitem="https://api_server:9440/api/nutanix/v3/calm_marketplace_items/"+str(mp_uuid)
    respitem = urlreq(urlitem, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, headers=headers)
    print respitem.status_code
    payloaditem = json.loads(respitem.content)
    payloaditem['metadata'].pop('owner_reference', None)
    payloaditem.pop('status', None)
    payloaditem['metadata'].pop('create_time', None)
    app_project =  {
        "kind": "project",
        "name": "project_name",
        "uuid": "project_uuid"
        }
    payloaditem['spec']['resources']['project_reference_list'].append(app_project)
    print payloaditem['spec']['resources']['project_reference_list']
    respitemput = urlreq(urlitem, verb='PUT', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(payloaditem), headers=headers)
    print json.dumps(json.loads(respitemput.content), indent=4)
    if respitemput.ok:
      print "App with uuid : "+mp_uuid+" is published"
    else:
      print "Can't publish APP with uuid :"+mp_uuid
      exit(1)
else:
  print "Get MP Items list failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)