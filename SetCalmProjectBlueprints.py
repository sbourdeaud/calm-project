url     = "https://@@{PC_IP}@@:9440/api/nutanix/v3/marketplace_items/list"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

payload = {"filter":"app_state==PUBLISHED","length":1000}

pc_user = '@@{Prism_Central.username}@@'
pc_pass = '@@{Prism_Central.secret}@@'

resp = urlreq(url, verb='POST', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(payload), headers=headers)

myresp = json.loads(resp.content)

if resp.ok:
  for i in myresp['entities']:
    print i['metadata']['uuid']
    mp_uuid = i['metadata']['uuid']
    urlitem="https://@@{PC_IP}@@:9440/api/nutanix/v3/calm_marketplace_items/"+str(mp_uuid)
    respitem = urlreq(urlitem, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, headers=headers)
    print respitem.status_code
    payloaditem = json.loads(respitem.content)
    payloaditem['metadata'].pop('owner_reference', None)
    payloaditem.pop('status', None)
    payloaditem['metadata'].pop('create_time', None)
    app_project =  {
        "kind": "project",
        "name": "@@{Project_Name}@@",
        "uuid": "@@{Project_UUID}@@"
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