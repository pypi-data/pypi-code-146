NAME_PARAMETER = {
    "default": None,
    "doc": "An Idem name of the resource.",
    "param_type": "Text",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}


RESOURCE_ID_PARAMETER = {
    "default": None,
    "doc": "An identifier of the resource in the provider",
    "param_type": "Text",
    "required": False,
    "target": "hardcoded",
    "target_type": "arg",
}

CREATE_TIMEOUT_PARAMETER = {
    "default": None,
    "doc": """Timeout configuration for resource creation.
            * create (Dict) -- Timeout configuration for resource creation
                * delay -- The amount of time in seconds to wait between attempts. Defaults to 15
                * max_attempts -- Customized timeout configuration containing delay and max attempts. Defaults to 40""",
    "param_type": "Dict",
    "required": False,
    "target": "hardcoded",
    "target_type": "arg",
}

DELETE_TIMEOUT_PARAMETER = {
    "default": None,
    "doc": """Timeout configuration for resource deletion.
            * delete (Dict) -- Timeout configuration for resource deletion
                * delay -- The amount of time in seconds to wait between attempts. Defaults to 15
                * max_attempts -- Customized timeout configuration containing delay and max attempts. Defaults to 40""",
    "param_type": "Dict",
    "required": False,
    "target": "hardcoded",
    "target_type": "arg",
}


PRESENT_REQUEST_FORMAT = r"""result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Get namespace
    namespace = metadata.get("namespace") if "namespace" in metadata else "default"

    # Check for existing {{ function.hardcoded.resource }} by name in namespace
    before = None
    if resource_id:
        {{ function.hardcoded.resource }} = await {{ function.hardcoded.get_function }}(
            ctx, name=resource_id, namespace=namespace
        )
        if not {{ function.hardcoded.resource }}["result"]:
            result["comment"] = {{ function.hardcoded.resource }}["comment"]
            result["result"] = {{ function.hardcoded.resource }}["result"]
            return result
        before = {{ function.hardcoded.resource }}["ret"]

    # Update current state
    # TODO: Implement hub.tool.{{ function.ref }}_utils.convert_raw_{{ function.hardcoded.resource }}_to_present function
    current_state = (
        hub.tool.{{ function.ref }}_utils.convert_raw_{{ function.hardcoded.resource }}_to_present(
            {{ function.hardcoded.resource }}=before
        )
    )
    result["old_state"] = current_state

    # Handle no change behaviour
    # TODO: The parameters of the desired_state should be the same as the present() input parameters.
    desired_state = {{ function.hardcoded.state_parameters }}

    is_change_detected = before is None or bool(
        DeepDiff(current_state, desired_state, ignore_order=True)
    )

    if not is_change_detected:
        result["comment"] = hub.tool.k8s.comment_utils.already_exists_comment(
            resource_type="{{ function.ref }}", name=name
        )
        result["new_state"] = copy.deepcopy(result["old_state"])
        return result

    # Handle test behaviour
    if ctx.get("test", False):
        result["new_state"] = hub.tool.k8s.test_state_utils.generate_test_state(
            enforced_state=current_state,
            desired_state=desired_state,
        )
        result["comment"] = (
            hub.tool.k8s.comment_utils.would_update_comment(
                resource_type="{{ function.ref }}", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="{{ function.ref }}", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="{{ function.hardcoded.payload_type }}"
    )
    if before:
        ret = await {{ function.hardcoded.update_function }}(
            ctx, name=resource_id, namespace=namespace, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
                resource_type="{{ function.ref }}", name=name
        )
    else:
        ret = await {{ function.hardcoded.create_function }}(
            ctx, namespace=namespace, body=body
        )
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
                resource_type="{{ function.ref }}", name=name
        )

    # Custom waiter for create/update
    waiter_config = hub.tool.k8s.waiter_utils.create_waiter_config(
        default_delay=15,
        default_max_attempts=40,
        timeout_config=timeout.get("create") if timeout else None,
    )

    def create_acceptor(status: bool, data: Dict = None, comment: Tuple = None) -> bool:
        # TODO implement wait acceptor method, return true when resource is created/updated
        return True

    arguments = {"name": resource_id, "namespace": namespace}

    # TODO add result arguments passed to create_acceptor
    # TODO format - key : jmes_path
    # TODO eg. result_arguments = { "status" : "status.condition" }
    result_arguments = {}

    {{ function.hardcoded.resource }}_waiter = hub.tool.k8s.waiter_utils.create_waiter(
        api_class_name="{{ function.hardcoded.api_class }}",
        operation="{{ function.hardcoded.waiter_function }}",
        arguments=arguments,
        result_arguments=result_arguments,
        acceptor_function=create_acceptor,
    )
    try:
        await hub.tool.k8s.custom_waiter.wait(
            ctx,
            waiter={{ function.hardcoded.resource }}_waiter,
            waiter_config=waiter_config,
            err_graceful=False
        )
    except Exception as e:
        result["comment"] = result["comment"] + (str(e),)
        result["result"] = False
        return result

    # Fetch the updated resource and update new_state
    {{ function.hardcoded.resource }} = await {{ function.hardcoded.get_function }}(
        ctx, name=resource_id, namespace=namespace
    )
    if not {{ function.hardcoded.resource }}["result"]:
        result["comment"] = result["comment"] + {{ function.hardcoded.resource }}["comment"]
        result["result"] = {{ function.hardcoded.resource }}["result"]
        return result
    after = {{ function.hardcoded.resource }}["ret"]
    result[
        "new_state"
    ] = hub.tool.{{ function.ref }}_utils.convert_raw_{{ function.hardcoded.resource }}_to_present(
        {{ function.hardcoded.resource }}=after
    )
    return result"""

ABSENT_REQUEST_FORMAT = r"""result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    namespace = metadata.get("namespace") if "namespace" in metadata else "default"

    before = None
    if resource_id:
        {{ function.hardcoded.resource }} = await {{ function.hardcoded.get_function }}(
            ctx, name=resource_id, namespace=namespace
        )
        if {{ function.hardcoded.resource }} and {{ function.hardcoded.resource }}["result"]:
            before = {{ function.hardcoded.resource }}["ret"]
            result[
                "old_state"
            ] = hub.tool.{{ function.ref }}_utils.convert_raw_{{ function.hardcoded.resource }}_to_present(
                {{ function.hardcoded.resource }}=before
            )

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="{{ function.ref }}", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
            resource_type="{{ function.ref }}", name=name
        )
    else:
        ret = await {{ function.hardcoded.delete_function }}(
            ctx, name=resource_id, namespace=namespace
        )
        if not ret["result"]:
            result["result"] = ret["result"]
            result["comment"] = ret["comment"]
            return result

        # Custom waiter for delete
        waiter_config = hub.tool.k8s.waiter_utils.create_waiter_config(
            default_delay=15,
            default_max_attempts=40,
            timeout_config=timeout.get("delete") if timeout else None,
        )

        def delete_acceptor(status: bool, data: Dict = None, comment: Tuple = None) -> bool:
            # TODO implement wait acceptor method, return true when resource is deleted
            return True

        arguments = {"name": name, "namespace": namespace}

        # TODO add result arguments passed to delete_acceptor
        # TODO format - key : jmes_path
        # TODO eg. result_arguments = { "status" : "status.condition" }
        result_arguments = {}

        {{ function.hardcoded.resource }}_waiter = hub.tool.k8s.waiter_utils.create_waiter(
            api_class_name="{{ function.hardcoded.api_class }}",
            operation="{{ function.hardcoded.waiter_function }}",
            arguments=arguments,
            result_arguments=result_arguments,
            acceptor_function=delete_acceptor,
        )
        try:
            await hub.tool.k8s.custom_waiter.wait(
                ctx,
                waiter={{ function.hardcoded.resource }}_waiter,
                waiter_config=waiter_config,
                err_graceful=True
            )
        except Exception as e:
            result["comment"] = result["comment"] + (str(e),)
            result["result"] = False
            return result

        result["comment"] = hub.tool.k8s.comment_utils.delete_comment(
                resource_type="{{ function.ref }}", name=name
        )
    return result"""

DESCRIBE_REQUEST_FORMAT = r"""ret = await {{ function.hardcoded.list_function }}(
        ctx,
    )
    if not ret["result"]:
        hub.log.debug(f"Could not describe {{ function.hardcoded.resource }} {ret['comment']}")
        return {}

    result = {}
    for {{ function.hardcoded.resource }} in ret["ret"].items:
        {{ function.hardcoded.resource }}_resource = (
            hub.tool.{{ function.ref }}_utils.convert_raw_{{ function.hardcoded.resource }}_to_present(
                {{ function.hardcoded.resource }}={{ function.hardcoded.resource }}
            )
        )
        result[{{ function.hardcoded.resource }}.metadata.name] = {
            "{{ function.ref }}.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in {{ function.hardcoded.resource }}_resource.items()
            ]
        }
    return result"""
