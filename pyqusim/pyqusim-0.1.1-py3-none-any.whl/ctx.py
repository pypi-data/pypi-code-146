_ctx_stack = []


class ContextMixin:
    def __enter__(self) -> "ContextMixin":
        _ctx_stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _ctx_stack.pop(-1)


def _get_current_ctx() -> ContextMixin:
    if not _ctx_stack:
        raise RuntimeError("Nothing in context")
    return _ctx_stack[-1]
