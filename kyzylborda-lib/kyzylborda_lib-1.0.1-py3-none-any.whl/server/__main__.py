import argparse
import asyncio
import importlib

from . import handlers


async def main():
    parser = argparse.ArgumentParser(prog="kyzylborda_lib.sandbox")
    parser.add_argument("address")
    parser.add_argument("module_name")
    args = parser.parse_args()

    importlib.import_module(args.module_name)

    if handlers._global_handler is None:
        print("Handler is not set. Use @tcp.listen or @http.listen")
        raise SystemExit(1)

    await handlers._global_handler(args.address)


if __name__ == "__main__":
    asyncio.run(main())
    asyncio
