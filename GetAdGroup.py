# Set the credentials for Prism
pc_user = '@@{Prism_Central.username}@@'
pc_pass = '@@{Prism_Central.secret}@@'

# Set the headers, url, and payload
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
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