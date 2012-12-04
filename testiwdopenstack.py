

print "create dhcp based ip group"

hill_dhcp = {"name":"hill-dhcp","version":"IPv4","protocol":"dhcp" }
hill_dhcp_group = deployer.ipgroups.create(hill_dhcp)
print hill_dhcp_group


print "create static based ip group"

hill_static = { "name":"hill-static","version":"IPv4","subnetaddress":"10.0.3.0","netmask":"255.255.255.0","gateway":"10.0.3.1","primarydns":"10.0.3.1"}
hill_static_group = deployer.ipgroups.create(hill_static)
print hill_static_group



#create cloud group

hill_cloud_data = {"name":"hill_os","address":"http://hillos:5000/v2.0/","userid":"admin","password":"admin_pass","vendor":"OpenStack"}

hill_cloud = deployer.clouds.create(hill_cloud_data)

