import pluggy

store_hookimpl = pluggy.HookimplMarker("hash-store")
resource_hookimpl = pluggy.HookimplMarker("hash-resource")
target_hookimpl = pluggy.HookimplMarker("hash-target")
