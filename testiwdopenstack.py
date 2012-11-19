


hill_dhcp = {"name":"hill-dhcp","version":"IPv4","protocol":"dhcp" }
hill_dhcp_group = deployer.ipgroups.create(hill_dhcp)
print hill_dhcp_group



hill_static = { "name":"hill-static","version":"IPv4","subnetaddress":"10.0.3.0","netmask":"255.255.255.0","gateway":"10.0.3.1","primarydns":"10.0.3.1"}
hill_static_group = deployer.ipgroups.create(hill_static)
print hill_static_group

