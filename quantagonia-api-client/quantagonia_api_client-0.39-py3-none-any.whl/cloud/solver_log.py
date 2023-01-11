class SolverLog:
    
    def __init__(self):
        self.log: str = ""
        self.add_newline = False

    def nextTimeAddNewLine(self):
        self.add_newline = True

    """
    takes as input the updated log. It will make sure that the old log is contained in the new log, and print the
    difference to the screen
    """
    def updateLog(self, new_log: str, add_newline : bool = False) -> None:
        if new_log == "":
            return

        old_log_len = len(self.log)

        if self.log != new_log[:old_log_len]:
            print("WARNING: there was some suspicious discrepancy in the solver log received from the server. "
                  "The solver log might not be printed in the order as the solver generated it.")

        if len(new_log) != old_log_len and self.add_newline:
            print("")
            self.add_newline = False

        print(new_log[old_log_len:], end='', flush=True)
        self.log = new_log
