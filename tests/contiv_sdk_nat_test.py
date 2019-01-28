import contiv_sdk

tenant = "tenant2"
c = contiv_sdk.ContivSdk('10.16.1.120', '10000', 'admin', 'admin')

# create a tenant
c.post_tenant(tenant)

# one network for this tenant
c.post_network(tenant, "vxlan", "10.10.10.1", tenant+":"+tenant+"-net",
               tenant+"-net", "data", "10.10.10.1/24")

# create a group
c.post_endpoint_group(tenant, tenant+"-net", tenant+"-group", [])

# create a nat policy
c.post_policy(tenant, "nat-policy")

# rules for nat-policy
# rules to allow internal flow
c.post_rule(tenant, "nat-policy", "r1", 30, "allow", "",
            tenant+"-net", "", "icmp", "out")

c.post_rule(tenant, "nat-policy", "r2", 30, "allow", "",
            tenant+"-net", "", "tcp", "out")

c.post_rule(tenant, "nat-policy", "r3", 30, "allow", "",
            tenant+"-net", "", "udp", "out")

# rules to deny external flow
c.post_rule(tenant, "nat-policy", "r4", 20, "deny", "",
            tenant+"-net", "", "icmp", "out")

c.post_rule(tenant, "nat-policy", "r5", 20, "deny", "",
            tenant+"-net", "", "tcp", "out")

c.post_rule(tenant, "nat-policy", "r6", 20, "deny", "",
            tenant+"-net", "", "udp", "out")


# add policy to group
c.post_endpoint_group(tenant, tenant+"-net", tenant+"-group", ["nat-policy"])

# deletar todas as policies of group
c.post_endpoint_group(tenant, tenant+"-net", tenant+"-group", [])
