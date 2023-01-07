class CoachingChange:
    def __init__(self, **kwargs):
        self.program = kwargs.get("program")
        self.program_url = kwargs.get("program_url")
        self.old_coach = kwargs.get("old_coach")
        self.old_coach_url = kwargs.get("old_coach_url")
        self.new_coach = kwargs.get("new_coach")
        self.new_coach_url = kwargs.get("new_coach_url")
        self.clgid = kwargs.get("clgid")

    def __repr__(self):
        buffer = "<CoachingChange("
        buffer += f"program='{self.program}', "
        buffer += f"program_url='{self.program_url}', "
        buffer += f"old_coach='{self.old_coach}', "
        buffer += f"old_coach_url='{self.old_coach_url}', "
        buffer += f"new_coach='{self.new_coach}', "
        buffer += f"new_coach_url='{self.new_coach_url}', "
        buffer += f"clgid='{self.clgid}')>"

        return buffer
