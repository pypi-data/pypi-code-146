class Transfer:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.url = kwargs.get("url")
        self.position = kwargs.get("position")
        self.former_school_name = kwargs.get("former_school_name")
        self.former_school_url = kwargs.get("former_school_url")
        self.new_school_name = kwargs.get("new_school_name")
        self.new_school_url = kwargs.get("new_school_url")

    def __repr__(self):
        buffer = "<Transfer("
        buffer += f"name={self.name}, "
        buffer += f"url={self.url}, "
        buffer += f"position={self.position}, "
        buffer += f"former_school_name={self.former_school_name}, "
        buffer += f"former_school_url={self.former_school_url}, "
        buffer += f"new_school_name={self.new_school_name}, "
        buffer += f"new_school_url={self.new_school_url})"

        return buffer
