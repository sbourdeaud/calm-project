# Set the credentials for Prism
pc_user = '@@{Prism_Central.username}@@'
pc_pass = '@@{Prism_Central.secret}@@'

# Set the headers, url, and payload
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

url     = "https://@@{PC_IP}@@:9440/api/nutanix/v3/user_groups/list"

payload =  {"kind":"user_group", "length":100, "offset":0}

# Make the request
resp = urlreq(url, verb='POST', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(payload), headers=headers)


# If the request went through correctly, print it out.  Otherwise error out, and print the response.

if resp.ok:

    #print json.dumps(json.loads(resp.content), indent=4)
    datafile = json.dumps(json.loads(resp.content), indent=4)
    datafile1 = json.loads(datafile) 

    for a in datafile1['entities']:
        group_name =  a['status']['resources']['display_name'];
        group_nut_uuid= a['metadata']['uuid'];
        group_dn = a['status']['resources']['directory_service_user_group']['distinguished_name']
        #print group_name, group_nut_uuid
        if group_name == "@@{ADGroup_Name}@@":
            print "ADGroup_UUID={0}".format(group_nut_uuid)

    
    exit(0)
    
else:
    print "Post request failed", resp.content
    exit(1)
