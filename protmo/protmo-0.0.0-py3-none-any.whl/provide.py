import sys
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional


def use_provided(needle: int) -> Any:
    '''
    The challange is to provide different instances to different
    call-stacks / web-request. To understand this, consider this
    example:
    When a client calls the server, the protmo-frameworks
    server-handler opens the correct database for this client.
    Different clients have different databases. The connection is
    stored in a Db-Object. The same server-handler code with the
    application logic, uses `use_provided` to get the DB-Instance.
    But on one requrest, it sould get one DB-Instance and on the
    other request, the same call should return the other instance.

    The solution is to leverage the call stack. When the middleware
    sets the instance via `provide`, it places it into its own
    private stack of local variables via `locals()[]`. Then it
    continues to call the application code. Every other function
    in the following call tree can now use `use_provided`. This
    function walks up the stack (call-tree) and searches for a
    local variable matching the query. It will find it at the node
    where the middleware set it using `provide`.

    There is one call-tree per web-request, as the same method was
    called multiple times. Every time `provide` is called which
    creates a subtree with a different instance, of DB for example.
    '''
    frame = sys._getframe()
    needle = '__' + (str(id(needle)))
    while frame:
        if needle in frame.f_locals:  # magic happens here
            return frame.f_locals[needle]
        frame = frame.f_back
    return None


def provide(mappings: Dict[Any, Any], callback: Callable,
            *args: Any, **kwargs: Any) -> Optional[Any]:
    for needle, obj in mappings.items():
        locals()['__' + (str(id(needle)))] = obj
    return callback(*args, **kwargs)
