from typing import List, Tuple, Union

# Tags allow you to scope requests within an
# environment. Both tags and environment need
# to match for a resolver to be a candidate to
# execute.
Tags = Union[List[str], Tuple[str, ...], str]

# Environments are used to trigger behavior
# in different deployments such as staging,
# production, and local development.
# For example, you may wish to interact with
# a vendor via an API call in the production
# environment, and opt to return a constant
# value in a staging environment.
#
# Environment can take one of three types:
#   - None (default) - candidate to run in every environment
#   - str - run only in this environment
#   - list[str] - run in any of the specified environment and no others
Environments = Union[List[str], Tuple[str, ...], str]
