import json
import os

import requests
import urllib3
import logging

urllib3.disable_warnings()


class ContivSdk:

    @staticmethod
    def get_instance():
        """ Static access method.
        :rtype: ContivSdk
        :return: ContivSdk instance
        """
        return ContivSdk(host=os.environ.get('SW4IOT_CONTIV_HOST', 'contiv'),
                         port=os.environ.get('SW4IOT_CONTIV_PORT', '10000'),
                         user=os.environ.get('SW4IOT_CONTIV_USER', 'admin'),
                         password=os.environ.get('SW4IOT_CONTIV_PASSWORD',
                                                 'admin'))

    def __init__(self, host, port, user, password):
        self.base_url = 'https://{}:{}/api/v1'.format(host, port)
        self.user = user
        self.password = password
        #
        self.token = None
        self.login()

    def __headers(self, token=True):
        headers = {
            'Content-Type': 'application/json',
        }
        if token:
            headers['X-Auth-Token'] = self.token
        return headers

    def __post_request(self, url, data, token=True):
        """
        Post request

        :param url:
        :param data:
        :param token:
        :return:
        """
        return requests.post('{}/{}/'.format(self.base_url, url), json=data,
                             headers=self.__headers(token), verify=False)

    def __put_request(self, url, data, token=True):
        """
        Put request

        :param url:
        :param data:
        :param token:
        :return:
        """
        return requests.put('{}/{}/'.format(self.base_url, url), json=data,
                            headers=self.__headers(token), verify=False)

    def __delete_request(self, url):
        """
        Delete request

        :param url:
        :return:
        """
        return requests.delete('{}/{}/'.format(self.base_url, url),
                               headers=self.__headers(True), verify=False)

    def login(self):
        """
        Contiv login
        """
        r = self.__post_request('auth_proxy/login', data={
            "username": self.user,
            "password": self.password
        }, token=False)
        if r.status_code == requests.codes.ok:
            self.token = json.loads(r.content)['token']

    def post_tenant(self, tenant_name):
        """
        Create tenant

        :param tenant_name:
        :return:
        """
        r = self.__post_request('tenants/{}'.format(tenant_name), data={
            "key": tenant_name,
            "tenantName": tenant_name
        })

        if r.status_code == requests.codes.ok:
            return json.loads(r.content)
        else:
            logging.warning(r.content)
            return None

    def delete_tenant(self, tenant_name):
        """
        Delete tenant

        :param tenant_name:
        :return:
        """
        r = self.__delete_request('tenants/{}'.format(tenant_name))
        return True if r.status_code == requests.codes.ok else None

    def post_network(self, tenant_name, encap, gateway, key, network_name,
                     nw_type, subnet):
        """
        Create network

        :param tenant_name:
        :param encap:
        :param gateway:
        :param key:
        :param network_name:
        :param nw_type:
        :param subnet:
        :return:
        """
        r = self.__post_request(
            'networks/{}:{}-net'.format(tenant_name, tenant_name),
            data={
                'encap': encap,
                'gateway': gateway,
                'key': key,
                'networkName': network_name,
                'nwType': nw_type,
                'subnet': subnet,
                'tenantName': tenant_name
            })

        if r.status_code == requests.codes.ok:
            return json.loads(r.content)
        else:
            logging.warning(r.content)
            return None

    def delete_network(self, tenant_name):
        """
        Delete network

        :param tenant_name:
        :return:
        """
        r = self.__delete_request('networks/{}:{}-net'.format(tenant_name,
                                                              tenant_name))

        if r.status_code == requests.codes.ok:
            return True
        else:
            logging.warning(r.content)
            return None

    def post_policy(self, tenant_name, policy_name):
        """
        Create network policy

        :param tenant_name:
        :param policy_name:
        :return:
        """

        key = '{}:{}'.format(tenant_name, policy_name)
        r = self.__post_request(
            'policys/{}:{}'.format(tenant_name, policy_name),
            data={
                'key': key,
                'policyName': policy_name,
                'tenantName': tenant_name
            })

        if r.status_code == requests.codes.ok:
            return json.loads(r.content)
        else:
            logging.warning(r.content)
            return None

    def delete_policy(self, policy_key):
        """
        Delete a network policy with all rules

        :param policy_key: "%s:%s" (tenant_name, policy_name)
        :return:
        """

        r = self.__delete_request('policys/{}'.format(policy_key))

        if r.status_code == requests.codes.ok:
            return True
        else:
            logging.warning(r.content)
            return None

    def post_rule(self, tenant_name, policy_name, rule_id, rule_priority,
                  rule_action, rule_to_epg, rule_to_net, rule_to_addr,
                  rule_protocol, rule_direction, rule_port=0):
        """
        Create network rule to compose a policy

        :param policy_name:
        :param tenant_name:
        :param rule_action: "allow or deny"
        :param rule_direction: "out or in"
        :param rule_port: int
        :param rule_priority: int
        :param rule_protocol: "tcp, udp or icmp"
        :param rule_id:
        :param rule_to_epg: "toEndpontGroup"
        :param rule_to_addr: "toIpAddress"
        :param rule_to_net: "toNetwork"
        :return:
        """

        key = '{}:{}:{}'.format(tenant_name, policy_name, rule_id)
        r = self.__post_request(
            'rules/{}'.format(key),
            data={
                'tenantName': tenant_name,
                'policyName': policy_name,
                'key': key,
                'ruleId': rule_id,
                'priority': rule_priority,
                'action': rule_action,
                'toEndpointGroup': rule_to_epg,
                'toNetwork': rule_to_net,
                'toIpAddress': rule_to_addr,
                'protocol': rule_protocol,
                'port': rule_port,
                'direction': rule_direction
            })

        if r.status_code == requests.codes.ok:
            return json.loads(r.content)
        else:
            logging.warning(r.content)
            return None

    def delete_rule(self, rule_key):
        """
        Delete a network rule

        :param rule_key
        :return:
        """

        r = self.__delete_request('rules/{}'.format(rule_key))

        if r.status_code == requests.codes.ok:
            return True
        else:
            logging.warning(r.content)
            return None

    def post_endpoint_group(self, tenant_name, tenant_net, group_name,
                            group_policies):
        """
        Create endpoint group with policys to apply

        :param group_name:
        :param tenant_name:
        :param tenant_net:
        :param group_policies: []
        :return:
        """

        key = '{}:{}'.format(tenant_name, group_name)
        r = self.__post_request(
            'endpointGroups/{}'.format(key),
            data={
                'groupName': group_name,
                'networkName': tenant_net,
                'policies': group_policies,
                'netProfile': '',
                'extContractsGrps': [],
                'tenantName': tenant_name,
                'key': key
            })

        if r.status_code == requests.codes.ok:
            return json.loads(r.content)
        else:
            logging.warning(r.content)
            return None

    def put_endpoint_group(self, tenant_name, tenant_net, group_name,
                           group_policies):
        """
        Add or delete one policy or more to a endpoint group
        :param group_name:
        :param tenant_name:
        :param tenant_net:
        :param group_policies: []
        :return:
        """

        key = '{}:{}'.format(tenant_name, group_name)
        r = self.__put_request(
            'endpointGroups/{}'.format(key),
            data={
                'groupName': group_name,
                'networkName': tenant_net,
                'policies': group_policies,
                'netProfile': '',
                'networkName': tenant_net,
                'links-sets': {},
                'links': {'AppProfile': {}, 'NetProfile': {},
                          'Network': {'type': 'network',
                                      'key': '{}:{}'.format(tenant_name,
                                                            tenant_net)},
                          'Tenant': {'type': 'tenant', 'key': tenant_name}},
                'tenantName': tenant_name,
                'key': key
            })

        if r.status_code == requests.codes.ok:
            return json.loads(r.content)
        else:
            logging.warning(r.content)
            return None

    def delete_endpoint_group(self, group_key):
        """
        Delete a endpoint group with all your policies

        :param group_key
        :return:
        """

        r = self.__delete_request('endpointGroups/{}'.format(group_key))

        if r.status_code == requests.codes.ok:
            return True
        else:
            logging.warning(r.content)
            return None
