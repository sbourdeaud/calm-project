# region headers
# escript-template v20190605 / stephane.bourdeaud@nutanix.com
# * author:     stephane.bourdeaud@nutanix.com
# * version:    2019/09/17
# task_name:    PcGetClusterUuid
# description:  Gets the UUID of the specified cluster.
# output vars:  nutanix_cluster_uuid
# endregion

# region capture Calm variables
username = '@@{pc.username}@@'
username_secret = "@@{pc.secret}@@"
project_type = "@@{project_type}@@"
pc_ip = "@@{pc_ip}@@"
prod_cluster_name = "@@{prod_cluster_name}@@"
dev_cluster_name = "@@{dev_cluster_name}@@"
# endregion

# region define variables
if project_type is "Production":
    nutanix_cluster_name = prod_cluster_name
if project_type is "Dev":
    nutanix_cluster_name = dev_cluster_name
# endregion

# region Get AHV cluster UUID
# region prepare the API call
api_server = pc_ip
api_server_port = "9440"
api_server_endpoint = "/api/nutanix/v3/clusters/list"
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
payload = {
    "kind": "cluster"
}
# endregion

# region make the api call
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

# region process results
if resp.ok:
    print("Request was successful")
    json_resp = json.loads(resp.content)
    for cluster in json_resp['entities']:
        if cluster['spec']['name'] == nutanix_cluster_name:
            print("nutanix_cluster_uuid={}".format(cluster['metadata']['uuid']))
    exit(0)
else:
    print("Request failed")
    print("Headers: {}".format(headers))
    print("Payload: {}".format(json.dumps(payload)))
    print('Status code: {}'.format(resp.status_code))
    print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
    exit(1)
# endregion

# endregion
