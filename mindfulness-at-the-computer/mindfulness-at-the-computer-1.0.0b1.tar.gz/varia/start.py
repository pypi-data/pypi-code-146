#!/usr/bin/env python3
import matc.__main__

# import trace
# import sys
# import os

if __name__ == '__main__':
    """
    tracer = trace.Trace(
        ignoredirs=[sys.prefix, sys.exec_prefix],
        ignoremods=["posixpath", "types"]
    )
    tracer.run("matc.main.main()")
    tracer_results = tracer.results()
    tracer_results.write_results()
    """

    matc.main.main()
