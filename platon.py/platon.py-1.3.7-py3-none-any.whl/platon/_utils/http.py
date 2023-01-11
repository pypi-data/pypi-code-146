def construct_user_agent(class_name: str) -> str:
    from platon import __version__ as web3_version

    user_agent = 'platon.py/{version}/{class_name}'.format(
        version=web3_version,
        class_name=class_name,
    )
    return user_agent
