from module.shell import Shell

class Conn(Shell):



    def __init__(self, config):
        self.shell_string = '' # this is what our app will use to prefix any commands we send to the database on the shell 

        self.config = config # not used right now as i'm just dealing with local docker

        container_id = self.get_container_id()

        
        
        self.build_shell_string(container_id)


    def build_shell_string(self, container_id):
        self.shell_string = f'docker exec {container_id}'


        

    def get_container_id(self):

        o, r = Shell.run(f'docker ps -f name="cassandra" --format "{{{{.ID}}}}"')

        return o.rstrip("\n")