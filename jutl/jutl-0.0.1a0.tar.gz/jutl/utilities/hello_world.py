def hello_world(name: str = None) -> str:
    """
    Greet the user.

    Returns "Hello, 'user!'" where 'user' is 'name' if passed,
    or "Hello, World!" if 'name' is not passed.

            Parameters:
                    name (str): The user's name
            
            Returns:
                    str: A greeting for the user
    """
    if name:
        return(f"Hello, {name}!")
    else:
        return(f"Hello, World!")
