from pop.contract import ContractedContext


def pre(hub, ctx: ContractedContext):
    """
    If the endpoint_url wasn't specified in the func_ctx, then supply a default
    """
    func_ctx = ctx.get_argument("ctx")
    if "endpoint_url" not in func_ctx.acct:
        func_ctx.acct.endpoint_url = hub.exec.{{cookiecutter.service_name}}.DEFAULT_ENDPOINT_URL

async def _ret(status:bool, ret=None, comment:str = ""):
    """
    Force the return to be a properly formatted coroutine
    """
    return {
        "comment": comment,
        "ret": ret,
        "status": status,
    }


async def call(hub, ctx: ContractedContext):
    """
    Catch all exceptions and return a False status if there was an error
    """
    try:
        ret = await ctx.func(*ctx.args, **ctx.kwargs)
        return _ret(ret=ret, status=True)
    except Exception as e:
        return _ret(comment=f"{e.__class__}: {e}", status=False)
