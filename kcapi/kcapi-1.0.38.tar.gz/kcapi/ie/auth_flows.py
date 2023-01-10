from copy import copy


# def create_flow(flow):
#     alias = flow['displayName']
#     pid = None if not 'provider' in flow else flow['providerId']
#     provider = 'registration-page-flow' if not pid else pid
#     flow_type = 'basic-flow' if not pid else 'form-flow'
#
#     # WARN: The value description is not well validated in Keycloak, it can return 500.
#     return {
#         "alias": alias,
#         "type": flow_type,
#         "description": "empty",
#         "provider": provider,
#     }

# replacement for create_flow()
def create_child_flow_data(flow):
    """
    :param flow: What was stored in json file.
    :return: What needs to be POST-ed to server to create a flow.
    Look at kcfetcher inject_data.py for POST/.create() examples.
    """
    assert 'authenticationFlow' in flow and flow['authenticationFlow'] is True
    assert 'topLevel' not in flow

    # https://172.17.0.3:8443/auth/admin/realms/ci0-realm/authentication/flows
    # description is returned, they are flows, and they are top level flows.
    # topLevel==true
    # Payload to create those top-level flows is NOT computed here.
    #
    # https://172.17.0.3:8443/auth/admin/realms/ci0-realm/authentication/flows/ci0-auth-flow-generic/executions
    # They can be child flows or child executions
    # Payload to create child executions is NOT computed here.
    # Here is computed only payload for child flows.
    #
    # API reponse for child flow
    # - there is no alias, but it has displayName.
    # - no topLevel attribute
    # - has level in index attribute
    #
    # So: for child flows, on POST/.create() we send some alias.
    # On GET/.get() alias attribute is not returned is not returned, but value of alias is in displayName.
    assert "alias" not in flow
    alias = flow['displayName']

    # In .json (API GET response) we have "providerId", to server we send (API POST) "provider".
    pid = flow.get('providerId')

    # Child flows are created with "provider"=="registration-page-form"
    # Child executions have providerId stored in json.
    # provider = pid or 'registration-page-flow'  # orig concept
    assert pid != 'registration-page-flow'  # just want to know if 'registration-page-flow' is ever used.
    provider = pid or 'registration-page-form'  # this will work on ci0-auth-flow-generic-exec-3-generic-alias case

    # flow_type = 'basic-flow' if not pid else 'form-flow'  # orig code
    if pid:
        flow_type = 'form-flow'
    else:
        flow_type = 'basic-flow'

    assert "description" not in flow
    # Real description is not even stored by kcfethcer
    # Seems real description is not even returned by API - is not observable, likely we can just ignore it
    # WARN: The value description is not well validated in Keycloak, it can return 500.
    data = {
        "alias": alias,
        "type": flow_type,
        "description": "empty-description",
        "provider": provider,
    }
    return data


def get_executions(execution):
    provider = execution['providerId']
    return {'provider': provider}


def is_auth_flow(body):
    if 'authenticationFlow' in body:
        assert body['authenticationFlow'] is True
    return 'authenticationFlow' in body


def get_node_level(node):
    return node['level']


def consistent(parent, flow):
    published_flows = parent.all()

    for publishedFlow in published_flows:
        resource_id = False

        if 'providerId' in publishedFlow and 'providerId' in flow:
            resource_id = publishedFlow['providerId'] == flow['providerId']
        else:
            resource_id = publishedFlow['displayName'] == flow['displayName']

        level_is_equal = publishedFlow['level'] == flow['level']
        index_is_equal = publishedFlow['index'] == flow['index']

        if resource_id and level_is_equal and index_is_equal:
            publishedFlow['requirement'] = flow['requirement']
            parent.update(None, publishedFlow).isOk()
            return True

    return False


def get_node_identity_pair(root_node):
    key = 'alias' if 'alias' in root_node else 'displayName'
    unique_identifier = root_node[key]

    return [key, unique_identifier]

def get_matching_flow_from_server(flow, stored_flows):
    [_, flow_id] = get_node_identity_pair(flow)

    for stored_flow in stored_flows:
        [_, id] = get_node_identity_pair(stored_flow)
        if flow_id == id:
            return stored_flow

    raise Exception("Trying to updated a built-in flow, with the wrong flow: " + flow + ". \n Make sure that this flow is defined in the built-in flow.")


def merge_flows(flow_from_server = {}, local_flow={}):
    changed = False
    for key in local_flow.keys():
        if key in flow_from_server and flow_from_server[key] != local_flow[key] and key != 'flowId':
            flow_from_server[key] = local_flow[key]
            changed = True

    return [flow_from_server, changed]

class AuthenticationFlowsImporter():
    def __init__(self, authentication_api):
        self.flowAPI = authentication_api

    def update(self, root_node, flows):
        # flows - child flows (from executors.json) belonging to root_node top-level flow.
        # TODO setup configj for flows/executions that were configured.
        assert root_node["topLevel"] is True

        flow_api = self.flowAPI.flows(root_node)
        executions_api = self.flowAPI.executions(root_node)

        if self.flowAPI.is_built_in(root_node):
            stored_flows = flow_api.all()
            #stored_executions = executions_api.all()

            for flow in flows:
                if is_auth_flow(flow):
                    flow_from_server = get_matching_flow_from_server(flow, stored_flows)
                    [updated_flow, has_change] = merge_flows(flow_from_server, flow)

                    if has_change:
                        flow_api.update(None, updated_flow).isOk()
                else:
                    flow_min = copy(flow)
                    flow_min.pop("authenticationConfigData", {})
                    executions_api.update(None, flow_min).isOk()
        else:
            # Create top-level flow.
            # TODO - remove/create only if change is needed.
            self.remove(root_node)
            self.flowAPI.create(root_node).isOk()
            # Now create child flows.
            self.publish(root_node, flows)

    def remove(self, root_node):
        [key, unique_identifier_value] = get_node_identity_pair(root_node)
        self.flowAPI.removeFirstByKV(key, unique_identifier_value)

    def publish(self, root_node, flows):
        if not isinstance(flows, list):
            raise Exception("Bad Parameters for Authentication Flow: auth_flow parameter should be an array.")

        root_node = root_node
        nodes = {0: root_node}

        root_flow = self.flowAPI.executions(root_node)

        for flow in flows:
            current_level = get_node_level(flow)
            parent = nodes[current_level]

            if is_auth_flow(flow):
                authentication_flow = create_child_flow_data(flow)
                nodes[current_level + 1] = authentication_flow
                self.flowAPI.flows(parent).create(authentication_flow).isOk()
            else:
                execution = get_executions(flow)
                self.flowAPI.executions(parent).create(execution).isOk()

            if not consistent(root_flow, flow):
                raise Exception(
                    'There is an inconsistency problem: Changes are not taking place in the server, latency problems ?.')


"""
debugging
what is created by kcfetcher inject_data.py

1
execution
authenticationFlow missing
"providerId": "direct-grant-validate-username"

2
execution
authenticationFlow missing
"displayName": "Conditional OTP Form",
"providerId": "auth-conditional-otp-form",
"alias": "ci0-auth-flow-generic-exec-20-alias",
    alias was set when config was added

3
flow, "type": "basic-flow",
"authenticationFlow": true,
"displayName": "ci0-auth-flow-generic-exec-3-generic-alias"
    POST - alias was stored into displayName
providerId missing

4
flow, "type": "basic-flow", child of n3
"authenticationFlow": true,
"displayName": "ci0-auth-flow-generic-exec-3-1-flow-alias"
providerId missing

5
flow,  "type": "form-flow",
"authenticationFlow": true,
"displayName": "ci0-auth-flow-generic-exec-4-flow-alias"
"providerId": "registration-page-form",

6
execution, child od 4
authenticationFlow missing
"alias": "ci0-auth-flow-generic-exec-6-alias"
    alias was set when config was added
"displayName": "Recaptcha",
"providerId": "registration-recaptcha-action",

"""
