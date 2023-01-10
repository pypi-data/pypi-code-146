
# static class, no self here
class Shell:
    @staticmethod
    def run(arg):
        import subprocess

        result = subprocess.Popen(arg,
                        shell=True,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        universal_newlines=True) 
        stdout, stderr = result.communicate()

        if stderr:
            print(stderr)

        if (result.returncode != 0):
            print(f'Shell command failed "{arg}"')
            #exit()

        return stdout, stderr