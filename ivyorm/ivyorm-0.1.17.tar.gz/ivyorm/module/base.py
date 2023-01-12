import json
from jinja2 import Template, Environment, FileSystemLoader
from .connection import Connection


conn = Connection()


file_loader = FileSystemLoader('template/src')
env = Environment(loader=file_loader)

class base():

    def command (self, command):

        #command = f'{conn.shell_string} {command}'
        #out, err = Shell.run(command)
        out, err = conn.run(command)
        
        if err:
            exit(err)
        return out, err

    def command_cql(self, command):
        script = command
        command = f"cqlsh -e \"{command}\""

        out, err = self.command(command)

        # CQL errors come as a string with 4 sections, seperated by a colon:
        # (0)<stdin> : (1)error number : (2)type or code : (3)description (more on this)
        errStruct = {}
        
        if err == 'h':
            err = None

        if err:
            err = err.split(':')
            errStruct['error'] = err[-1].strip()
            errStruct['code'] = err[2]
           
            if (err[2] == "InvalidRequest"):
                # the description has more values in it, which look like
                # (3)Error from server : (4)code=2200 [something] message=the error
                print(err[4])
                message_location = err[4].find("message") + 9 # the length of the word "message="
                errStruct['code'] = err[4][6:err[4].find("[")].strip()
                errStruct['error'] = err[4][message_location:len(err[4])-2].strip()
                errStruct['script'] = script
            elif(err[2] == "SyntaxException"):
                errStruct['error'] = err[4]
            
            err = errStruct

        return out, errStruct

    def process_shell_result(self, input, seperator=" "):
        """
        Takes the output of a shell command and formats it use in the app
        The input is going to be a wierd shell result, so this may get funky...

        :param input: the shell result to parse and format
        :param seperator: the delimiter to cut up our columns
        """
        l, c = 0, 0
        output = {}
        
        for line in input.split("\n"):
            if (line == ''):
                continue
                
            l, c = l + 1, 0

            output[l] = {}
            
            for col in line.split(seperator):
                if (col == ''):
                    continue

                c = c + 1
                
                output[l][c] = col.strip().lower()

        return output

    def process_cql_result(self, input, key):
        """
        Takes the output of a cqlsh shell command and formats it use in the app
        The input here is already in cqlsh JSON format (SELECT JSON...)

        :param input: the cqlsh result to parse and format
        :param seperator: the delimiter to cut up our columns
        :param key: if specified, will 'key' a row by this value returned in each row
        :return: an array of the original result, parsed
        """

        meta = {}
        output = []
        
        rows = input.split("\n")
        

        # remove any blank rows that get returned from the shell
        rows = list(filter(None, rows))


        # cqlsh tidy up. Remove the header row, the seperator row (------)
        # and the row count at the end. Do this in reverse order so we don't
        # trip over oursevles when doing array deletes
        try:
            del rows[len(rows)-1] # end row
            del rows[1] # the ----- row
            del rows[0] # the header row
        except KeyError:
            pass


        meta['count'] = len(rows)
        if (meta['count'] == 0):
            meta['nodata'] = True
        
        for row in rows:
            if (row == ''):
                continue
            print(row)
            # we create a temp object to store each row in so we don't get 
            # row keys in our output, instead it's just a key-less array
            temp = {}
            temp = row #json.loads(row)

            output.append(temp)

        print(output)
        return output, meta['count'], meta


    def _convertSize(self, col):
        if "KiB" in col:
            temp = col.replace("KiB", '').strip()
            col = float(temp) * 1024
        elif "MiB" in col:
            temp = col.replace("MiB", '').strip()
            col = float(temp) * 1024 * 1024
        elif "NaN" in col:
            temp = col.replace("NaN", '').strip()
            col = ""
        elif "bytes" in col:
            temp = col.replace("bytes", '').strip()
            col = temp
        return col
                    
    def _clean(self, arg):
        return arg.rstrip("\n")
    
    def template(self, template_name, data={}):
        template = env.get_template(f'{template_name}.tpl')
        output = template.render(data=data)
        
        return output


