# region headers
# escript-template v20190611 / stephane.bourdeaud@nutanix.com
# * author:     Bogdan-Nicolae.MITU@ext.eeas.europa.eu
# *             stephane.bourdeaud@nutanix.com
# * version:    2019/09/18
# task_name:    Readme
# description:  Prints information about the project that was just created. 
# endregion

#region capture Calm variables
ahv_network_name = "@@{ahv_network_name}@@"
username = "@@{calm_username}@@"
ad_group_name = "@@{ad_group_name}@@"
project_name = "@@{project_name}@@"
project_size = "@@{project_size}@@"
#endregion

#region processing
print("********** Your Project Information **********\n")
print("   Project Name: {}".format(project_name))
print("   Project Size: {}".format(project_size))
print("   Project Owner: {}".format(username))
print("   Active Directory Group for Consumers: {}".format(ad_group_name))
print("   Network Name: {}".format(ahv_network_name))
print("\n**********************************************")
#endregion
