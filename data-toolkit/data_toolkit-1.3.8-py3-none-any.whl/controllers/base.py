from regex import E
from dt.ext.aws_s3 import get_lastest_file
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from pprint import pprint as pp
import os

VERSION_BANNER = """
ML & data helper code! %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'ML & data helper code!'

        # text displayed at the bottom of --help output
        epilog = 'Usage: dt command [args] [kwargs]'

        # controller level arguments. ex: 'dt --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        # TODO: implement `--home` for setting up home address
        help='AWS Security Groups helper functions',
        arguments=[
            (['action'],{
                "help" : "One of {update, show, ls}",
                "action": "store"
            }),
            (['-n','--name'],{
                "help" : "Name of the SG to act on",
                "action": "store"
            }),
            (['-ip'],{
                "help" : "IP to add to security group",
                "action": "store"
            }),
            (['-p','--profile'],{
                "help" : "Which AWS profile should boto3 use",
                "action" : "store"
            }),
            (['-P','--ports'],{
                "help" : "Which ports should AWS SG set",
                "action" : "store"
            }),
            (['-m','--messages'],{
                "help" : "Message to add to SG description, WARNing will not use default ports if used "
                         "Accepts port:messages pairs separated by commas. E.g. 42:answer to life, 22:memes",
                "action" : "store"
            }),
            (['-r','--region'],{
                "help": "Which AWS region should boto3 use",
                "action": "store"
            }),
            (['-i','--id'],{
                "help" : "ID of the SG to act on from the ls DataFrame",
                "action" : "store"
            }),
        ]
    )
    def sg(self):
        from ..ext.aws_sg import get_sg, update_sg_to_ip
        profile = self.app.pargs.__dict__.get('profile') or self.app.pargs.__dict__.get('p') or 'default'
        name = self.app.pargs.__dict__.get('name') or self.app.pargs.__dict__.get('n')
        region = self.app.pargs.__dict__.get('region') or self.app.pargs.__dict__.get('r') or 'eu-west-1'

        # which ports to change
        ports = self.app.pargs.__dict__.get('ports') or self.app.pargs.__dict__.get('P')
        if ports: ports = [ int(p) for p in ports.split(',') ]
        else: ports = [22, 8888, 8501, 8889, 5432]

        # which messages to assign to which ports
        messages = self.app.pargs.__dict__.get('messages') or self.app.pargs.__dict__.get('m') or ''

        # if any id is given, use that one
        sid = self.app.pargs.__dict__.get('id') or self.app.pargs.__dict__.get('i')
        if sid: sid = int(sid)

        if self.app.pargs.action=='show':
            pp(get_sg(profile, sid = sid, region=region))

        elif self.app.pargs.action=='update':
            if not self.app.pargs.name: sg_name = get_sg(profile, sid = sid)[0]['GroupName']
            else: sg_name = self.app.pargs.name
            update_sg_to_ip(sg_name=sg_name, profile=profile,
                            ports=ports, messages=messages, region=region)

        elif self.app.pargs.action=='ls':
            from ..ext.aws_sg import list_security_groups
            df = list_security_groups(region, profile)
            print(df)

        else:
            raise NotImplementedError('As action, chose one of {update, show}')

    @ex(
        help="GCP VM Instances helper commands."
        "These are currently in alpha and some may not work",
        arguments=[
            (['action'],{
                    "help" : "To show one of {ls, scp}.",
                    "action" : "store"
                }),
            (['--rpath'],{
                "help" : "What is the location on the remote server",
                "action": "store"
            }),
            (['-f','--filter'],{
                "help" : "One of {live, all}. Default: live",
                "action": "store"
            }),
            (['-id'],{
                "help": "InstanceId to be passed to ec2 start/stop",
                "action": "store"
            })
        ]
    )
    def gcp(self):
        from ..ext.gcp import gcp_ls, scp

        # profile = self.app.pargs.profile or 'default'
        # filt = self.app.pargs.filter or "live"

        if self.app.pargs.action=='ls':
            print(gcp_ls())

        # elif self.app.pargs.action=='update':
        #     print(update_ec2_ssh(profile))

        # elif self.app.pargs.action=='start':
        #     start_ec2(self.app.pargs.id, profile)

        elif self.app.pargs.action=='scp':
            scp(int(self.app.pargs.id), self.app.pargs.rpath)
            # stop_ec2(self.app.pargs.id, profile)

        else:
            raise NotImplementedError("Choose one of {ls, update, start, stop}")

    @ex(
        help='Tree helper/replacement functions',
        arguments= [
            (['loc'], {
                "help": "Location of the tree to act on",
                "action": "store"
            }),
            (['-n'],{
                "help": "Depth of the tree to print",
                "action": "store"
            }),
            (['-f'],{
                "help": "Print out full path",
                "action": "store"  
            })
        ]
    )
    def tree(self):
        from ..ext.tree import tree
        
        level = int(self.app.pargs.n or 2)
        full_path = int(self.app.pargs.f or 0)
        
        tree(self.app.pargs.loc, level, full_path)
        

    @ex(
        help="AWS EC2 helper commands.",
        arguments=[
            (['action'],{
                    "help" : "To show one of {ls, update}.",
                    "action" : "store"
                }),
            (['-p','--profile'],{
                "help" : "Which AWS profile should boto3 use.",
                "action": "store"
            }),
            (['-f','--filter'],{
                "help" : "One of {live, all}. Default: live",
                "action": "store"
            }),
            (['-id'],{
                "help": "InstanceId to be passed to ec2 start/stop",
                "action": "store"
            }),
            (['-r','--region'],{
                "help": "Which region to use",
                "action": "store"
            }),
        ]
    )
    def ec2(self):
        from ..ext.aws_ec2 import get_ec2, start_ec2, stop_ec2, update_ec2_ssh

        profile = self.app.pargs.profile or 'default'
        filt = self.app.pargs.filter or "live"
        region = self.app.pargs.region or "eu-west-1"

        if self.app.pargs.action=='ls':
            print(get_ec2('live', profile, filt, region))

        elif self.app.pargs.action=='update':
            print(update_ec2_ssh(profile))

        elif self.app.pargs.action=='start':
            start_ec2(self.app.pargs.id, profile)

        elif self.app.pargs.action=='stop':
            stop_ec2(self.app.pargs.id, profile)

        else:
            raise NotImplementedError("Choose one of {ls, update, start, stop}")

    @ex(
        help="Operations to easily work with remote servers / devices",
        arguments=[
            # TODO: maybe make grabable from ec2 ls
            (['ip'],{
                "help" : "IP of the target server",
                "action" : "store"
            }),
            (['-r','--remote'],{
                "help" : "Remote path on the target server",
                "action": "store"
            }),
            (['-u','--user'],{
                "help" : "Which user to ssh with.",
                "action" : "store"
            }),
            (['--server_name','-sn'],{
                "help" : "To give the SFTP server a name.",
                "action" : "store"
            }),
            (['-i', '--identity'],{
                "help" : "Path to the identity file to use for ssh.",
                "action" : "store"
            }),
            (['-p','--port'],{
                "help" : "Port over which to run SFTP.",
                "action" : "store"
            })
        ]
    )
    def sftp(self):
        ip = self.app.pargs.ip
        remote = self.app.pargs.__dict__.get('remote') or self.app.pargs.__dict__.get('r') or '/data/openpilot'
        port = self.app.pargs.__dict__.get('port') or self.app.pargs.__dict__.get('p') or 8022
        user = self.app.pargs.__dict__.get('user') or self.app.pargs.__dict__.get('u') or 'comma'
        server_name = self.app.pargs.__dict__.get('server_name') or self.app.pargs.__dict__.get('sn') or 'C3'
        identity = self.app.pargs.__dict__.get('identity') or self.app.pargs.__dict__.get('i') or os.path.expanduser("~/openpilot/tools/ssh/CL-key")

        from ..ext.sftp_conf import write_sftp
        
        write_sftp(name=server_name, ip=ip, port=port, user=user,
                    remote=remote, key_path=identity)

    @ex(
        help="Ops with Codex AI from OpenAI.",
        arguments=[
            (['text'],{
                "help" : "Text to be suggested",
                "action": "store"
            }),
            (['-n','--n_suggestions'],{
                "help" : "Number of suggestions to return",
                "action": "store",
                "default": 5
            }),
            (['-f','--file'],{
                "help" : "File to be suggested from as context",
                "action": "store"
            }),
            (['-m','--model'],{
                "help": "which model to use",
                "action": "store",
            })
        ]
    )
    def cai(self):
        from ..ext.codex import get_cai_suggestions, list_models
        import pprint as pp

        if self.app.pargs.text=='ls':
            list_models(self)
                
        else:
            if self.app.pargs.model is None: model = 'code-davinci-002' 
            else: model = self.app.pargs.model
            suggestions = get_cai_suggestions(self.app.pargs.text, 
                                              self.app.pargs.n_suggestions, 
                                              model,
                                              self.app.pargs.file)
            try:
                text = suggestions['choices'][0]['text']
                pp.pprint(suggestions)
                print('Suggestion: \n', text)
            except:
                print('Exception: ', suggestions)

    @ex(
        help='Monitor lack of GPU activity. When there is none, runs -job',
        arguments=[
            (['-job'],{
                "help" : "Text of the command to run after no GPU activity",
                "action" : "store"
            }),
            (['-n'], {
                "help" : "Number of processes before 'no activity'.",
                "action" : "store"
            })
        ]
    )
    def monitor(self):
        from ..ext.monitor import submit
        submit(self.app.pargs.job)


    # number of files
    @ex(
        help='Displays the number of files',
        arguments=[
            (['-d'], {
            "help" : "which directory to show",
            "action" : "store" } )
        ]
    )
    def nf(self):
        loc = self.app.pargs.d or '.'
        os.system(f'ls {loc} | wc -l')

    @ex(
        help="Appends defaults: from zshrc.txt to ~/.bashrc or ~/.zshrc or tmux conf",
        arguments = [
            (['shell'], {
                "help" : "One of {sh, zsh, tmux}. Imports a DT version of zshrc into bashrc or zshrc. or tmux .conf into ~/",
                "action": "store"
            })
        ]
    )
    def load(self):
        # TODO: reload the file after.
        # TODO: load git aliases
        zshrc = os.path.abspath(__file__).split('/')[:-2] + ['ext', 'zshrc.txt']
        tmux = os.path.abspath(__file__).split('/')[:-2] + ['ext', 'tmux.conf']

        zshrc_path = os.path.join('/'.join(zshrc))
        tmux_path = os.path.join('/'.join(tmux))
        if self.app.pargs.shell == 'sh':
            os.system(f'cat {zshrc_path} >> ~/.bashrc ')
        elif self.app.pargs.shell == 'zsh':
            os.system(f'cat {zshrc_path} >> ~/.zshrc ')
        elif self.app.pargs.shell == 'tmux':
            os.system(f'cat {tmux_path} >> ~/.tmux.conf ')
        else:
            raise NotImplementedError("Try one of {sh, zsh, tmux}")


    @ex(
        help='Operations on CLI hist',
        arguments=[
            (['-s'],{
                "help" : "Which lines to save separated by commas",
                "action" : "store"
            }),
            (['-n'],{
                # TODO: probably better as mandatory
                "help" : "Which lines from the selected history to show/save",
                "action" : "store"
            }),
            (['-e'],{
                "help": "Which terns to exclude separated by commas",
                "action": "store"
            }),
            (['-a','--alias'],{
                "help": "Name for the snippet.",
                "action" : "store"
            })
        ]
    )
    def hist(self):
        if not self.app.pargs.s:
            from ..ext.hist import hist_tail
            import pprint as pp
            n_lines = int(self.app.pargs.n or 20)
            excluded_terms = self.app.pargs.e or []
            if isinstance(excluded_terms, str): excluded_terms = excluded_terms.split(',')
            pp.pprint(hist_tail(n_lines, excluded_terms))
        else:
            from ..ext.hist import hist_save
            import uuid
            
            n_lines = int(self.app.pargs.n or 20)
            lines_to_save = [int(x) for x in str(self.app.pargs.s).split(',')]
            snippet_name = self.app.pargs.__dict__.get('a') or self.app.pargs.__dict__.get('alias') or str(uuid.uuid4())
            print(f'Saving {lines_to_save} lines from history to snippet {snippet_name}')
            
            hist_save(lines_to_save, snippet_name, n_lines=n_lines)
            
    # function fd (fake data) to generate fake data based on a template or clipboard
    @ex(
        help='Generate fake data',
        arguments=[
            (['-n'],{
                "help" : "Number of lines to generate",
                "action" : "store"
            }),
            (['-t','--template'],{
                "help" : "Path to template for data generation",
                "action" : "store"
            }),
            (['-c','--columns'],{
                "help" : "Whether column names are present",
                "action" : "store_true"
            }),
            (['--csv'],{
                'help' : "Whether to generate csv", 
                "action" : "store_true"
            }),
            (['-pk','--primary-key'],{
                "help" : "Primary key column name (-1 crate a new column)",
                "action" : "store"
            }),
            (['-d'],{
                "help" : "Delimiter for the generated data",
                "action" : "store"
            })
        ]
    )
    def fd(self):
        from ..ext.faker import generate_fake_data
        n_lines = int(self.app.pargs.__dict__.get('n') or 10)
        template = self.app.pargs.__dict__.get('t') or self.app.pargs.__dict__.get('template')
        columns = self.app.pargs.__dict__.get('c') or self.app.pargs.__dict__.get('columns')
        csv = self.app.pargs.__dict__.get('csv')
        primary_key = self.app.pargs.__dict__.get('pk') or self.app.pargs.__dict__.get('primary_key')
        delimiter = self.app.pargs.__dict__.get('d') or ','
        
        generate_fake_data(n_lines, template, columns, csv, primary_key, delimiter)
        

    @ex(
        help='Operations with snippets',
        arguments=[
            (['-n','--n_lines'],{
                "help" : "Which snippet to run/create. Using commas to seperate ids"
                "e.g. `dt run 13,23`",
                "action" : "store"
            }),
            (['-ssh'],{
                "help" : "Whether the command (includes?)/is? an SSH command",
                "action": "store"
            }),
            (['-c'],{
                # TODO: probably better as mandatory
                "help" : "Which lines from the selected history to show/save",
                "action" : "store"
            }),
            # TODO: what if non-default n lines has been pased to hist
            (['--save'],{
                "help" : "Whether to save the snippet to the history",
                # TODO: figure out if bool
                "action" : "store"   
            }),
            (['-a','--alias'],{
                "help": "Name of the alias to run",
                "action" : "store"
            })
        ]
    )
    def run(self):
        is_alias = self.app.pargs.__dict__.get('a') or self.app.pargs.__dict__.get('alias') or False
        
        if is_alias:
            from ..ext.run import run_command_from_alias
            run_command_from_alias(is_alias)
        else:
            from ..ext.run import run_command
            n_lines = [int(x) for x in str(self.app.pargs.n_lines).split(',')]
            run_command(n_lines)
            
    @ex(
        help='Operations with s3 buckets',
        arguments=[
            (['action'],{
                "help" : "One of {ls, link}",
                "action" : "store"
            }),
            (['target'],{
                "help" : "The target of the action. Can be {dongle_id, -1}",
                "action" : "store"
            }),
            (['--num_segments'],{
                "help" : "Number of recent files to show",
                "action" : "store",
                "default" : 10
            }),
            (['-n','--show_n'],{
                "help" : "Number of recent files to show",
                "action" : "store",
                "default" : 50
            }),
            (['-f','--filter'],{
                "help" : "Filter the files by this int",
                "action" : "store",
                "default" : 0
            }),
            (['-F','--file'],{
                "help": "File containing metadata",
                "action": "store",
                "default": "/home/jakub/data/devices.csv"
            })
        ]
    )
    def s3(self):
        if self.app.pargs.action == 'link':
            from ..ext.aws_s3 import get_lastest_file
            print(get_lastest_file(self.app.pargs.target))

        # ls actions for all dongle ids
        if self.app.pargs.action == 'ls':
            filter = self.app.pargs.__dict__.get('filter') or self.app.pargs.__dict__.get('f') or 0
            metadata_file = self.app.pargs.__dict__.get('file') or self.app.pargs.__dict__.get('F')
            
            from ..ext.aws_s3 import get_drives
            show_n = int(self.app.pargs.__dict__.get('show_n') or self.app.pargs.__dict__.get('n'))

            if self.app.pargs.target == '-1':
                get_drives(self.app.pargs.target, show_n=show_n, metadata_file=metadata_file, filter=filter)
            else:
                # TODO: potentially removed
                # num_segments = self.app.pargs.__dict__.get('n') or self.app.pargs.__dict__.get('num_segments')
                get_drives(self.app.pargs.target, show_n=show_n, metadata_file=metadata_file, 
                            filter=int(filter))

        if self.app.pargs.action == 'pull':
            from ..ext.aws_s3 import pull_latest
            pull_latest(self.app.pargs.target)

    @ex(
        help='Operations on the SSH config',
        arguments=[
            (['action'],{
                "help" : "To show one of {set, ls, update}. Set is for new remote value, update is to grab from AWS",
                "action" : "store"
            }),
            (['-host'],{
            "help" : "Which SSH config host to SET",
            "action": "store"
            }),
            (['-ip'],{
                "help" : "The IP to SET in the ssh config as HostName",
                "action" : "store"
            })
        ]
    )
    def ssh(self):
        from ..ext.sshconf import read_ssh_config
        from ..ext.sshconf import print_ls
        ssh_config_path = os.path.expanduser('~/.ssh/config')

        if self.app.pargs.action=='set':
            ssh_config_obj = read_ssh_config(ssh_config_path)
            ssh_config_obj.set(self.app.pargs.host, HostName=self.app.pargs.ip)
            ssh_config_obj.write(ssh_config_path)
            print_ls(ssh_config_obj)
            

        elif self.app.pargs.action=='update':
            from ..ext.aws_ec2 import update_ec2_ssh
            profile ='default' # or  self.app.pargs
            # print(update_ec2_ssh(profile))
            update_ec2_ssh(profile)
            ssh_config_obj = read_ssh_config(ssh_config_path)
            print_ls(ssh_config_obj)

        elif self.app.pargs.action=='ls':
            ssh_config_obj = read_ssh_config(ssh_config_path)
            print_ls(ssh_config_obj)

        else:
            # raise NotImplementedError()
            print('Arg out of {set, update} provided assuming an SSH command.')
            ssh_config_obj = read_ssh_config(ssh_config_path)
            target = self.app.pargs.action
            if not target in ssh_config_obj.hosts_: raise Exception(f'Host {target} not in configured hosts.')
            else:
                os.system('dt sg update')
                os.system(f'ssh {target}')

    @ex(
        help='Basic viz using streamlit for image comparisons',
        arguments = [
            (['images'], {
                'help' : 'Location of target images',
                'action' : "store"
            }),
            (['labels'], {
                'help' : 'Location of target labels',
                "action" : 'store'
            }),
            (['adapted'], {
                'help' : 'Location of domain adapted images',
                "action" : "store"
            })
            #     'action' : "store",
            #     "images" : '/efs/public_data/gta5/images',
            #     "labels" : '/efs/public_data/gta5/labels',
            #     "adapted" : '/efs/public_data/images'
            # })
        ]
    )
    def viz(self):
        args = self.app.pargs
        print(args.images)
        from ..ext.firelit import create_viz
        create_viz(args.images, args.labels, args.adapted)

    @ex(
        help="Download file from Google Drive",
        arguments=[
            (["file_id"], {
                "help" : "The file id of the file to download",
                "action" : "store"
            }),
            (["destination"], {
                "help": "The destination to download the file to",
                "action" : "store"
            })
        ]
    )
    def gdrive(self):
        from ..ext.gdrive_dl import download_file_from_google_drive
        download_file_from_google_drive(self.app.pargs.file_id, self.app.pargs.destination)


    @ex(
        help='Operations with config.',
        arguments = [
            (['action'], {
                "help" : "One of {show, set, loc}: \
                *show*: show configs Sentry DNS etc. \
                *set*: Resets the config from CLI. \
                *loc*: shows the location of the config",
                'action' : "store",
            })
        ]
    )
    def config(self):
        # TODO: setup Data-toolkit specific config
        # shows config
        
        if self.app.pargs.action=='show' or self.app.pargs.action=='ls':
            from ..ext.config import show_config
            show_config()

        # shows the path of the config
        if self.app.pargs.action=='loc':
            config_path = os.path.join(os.path.expanduser('~'), 'dt_config.json')
            print(config_path)

        # resets the config
        # TODO this config method needs programmatic acces for spot instances
        if self.app.pargs.action=='set':
            from ..ext.tracking import initialize
            initialize(overwrite=True)

        elif self.app.pargs.action not in ['set','loc', 'show','ls']:
            raise NotImplementedError("Try one of {show, set, loc}")


    @ex(
        help='All Github related operations',
        arguments=[
             (['action'],{
                "help" : """To show one of {ff, fs, contrib, diff, branches}. \r\n
                ff: Finds the forks of a repo.  \r\n
                fs: Finds the last commit of a repo by fork. \r\n 
                contrib: Finds the contributors of a repo. \r\n
                diff: Finds the all the diffs in directories below. """,
                "action" : "store"
            }),
            (['-url'],{
                # TODO: what if there's no forks to give?
                "help" : "Github URL to search for forks."
            }),
            (['--remote'],{
                "help" : "Remove remote branches.",
                "action" : "store"
            }),
            (['-r','--remove'],{
                "help" : "Remove remote branches.",
                "action" : "store"
            }),
        ]
    )
    def gh(self):
        if self.app.pargs.action=='ff':
            from ..ext.github import find_forks
            print(find_forks(self.app.pargs.url))
        elif self.app.pargs.action=='fs':
            from ..ext.github import fork_status
            print(fork_status(self.app.pargs.url))
        elif self.app.pargs.action=='contrib':
            from ..ext.github import find_contributors
            print(find_contributors(self.app.pargs.url))
        elif self.app.pargs.action=='diff':
            from ..ext.github import dir_diff
            pp(dir_diff(self.app.pargs.url))
        elif self.app.pargs.action=='branches':
            from ..ext.github import find_branches
            
            if self.app.pargs.remote is None: remote = True
            else: remote = self.app.pargs.remote == 'True'
            
            
            remove = self.app.pargs.__dict__.get('remove', True)
            print(find_branches(self.app.pargs.url, remote, remove))
            
    # create notes that are organized into project folders and are stored in md files
    @ex(
        help='Create notes that are organized into project folders and are stored in md files',
        arguments=[
            (['action'],{
                "help" : "One of {add (screenshot), ls (notes), mk (project), rm (project), fin (note)}",
                "action": "store"
            }),
            (['-t'],{
                "help": "Text of the note",
                "action": "store"
            }),
            (['-p'],{
                "help" : "Project id. If not given, grabs the first one.",
                "action" : 'store'
            }),
            (['-i'],{
                "help" : "Id of the finished note",
                "action": "store"
            }),
            (['-ws'],{
                "help": "Workspace name (e.g. Daily) otherwiwise grabs the first one",
                "action": "store"
            })
        ]
    )
    def nt(self):
        from ..ext.notes import Note
        note = Note(self.app.pargs.p, )
        if self.app.pargs.action=='add':
            note.add_attachment(self.app.pargs.p)
        elif self.app.pargs.action=='ls':
            note.ls(self.app.pargs.p, self.app.pargs.ws)
        elif self.app.pargs.action=='mk':
            note.create_project(self.app.pargs.p, self.app.pargs.t)
        elif self.app.pargs.action=='up':
            note.up(self.app.pargs.i, self.app.pargs.t, self.app.pargs.ws)
        else:
            print("Try one of {add, ls, dn}")

    # create notes that are organized into project folders and are stored in md files
    

    @ex(
        help='Manage TODOs using Asana',
        arguments=[
            (['action'],{
                "help" : "One of {add, ls, dn}",
                "action": "store"
            }),
            (['-t'],{
                "help": "Text of the TODO",
                "action": "store"
            }),
            (['-l'],{
                "help": "Length of time in days this is expected to take",
                "action": "store"
            }),
            (['-p'],{
                "help" : "Project id. Daily is 0",
                "action" : 'store'
            }),
            (['-i'],{
                "help" : "Id of the finished task",
                "action": "store"
            }),
            (['-ws'],{
                "help": "Workspace name (e.g. Daily) otherwiwise grabs the first one",
                "action": "store"
            }),
            (['-f'],{
                "help" : "Filter TODOs for ls",
                "action": "store"
            })
        ]
    )
    def td(self):
        from ..ext.asana import add_todo, asana_list_todos, done_todo, fix_past_due
        project = self.app.pargs.p or "Daily"

        if self.app.pargs.action=='add':
            add_todo(self.app.pargs.t, self.app.pargs.l, self.app.pargs.ws, project)
        elif self.app.pargs.action=='ls':
            asana_list_todos(
                self.app.pargs.p,
                self.app.pargs.f,)
        elif self.app.pargs.action=='dn':
            done_todo(self.app.pargs.i)
        elif self.app.pargs.action=='fix':
            fix_past_due(self.app.pargs.p)

        else:
            raise NotImplemented("Action must be one of {add, ls, dn}")

    @ex(
        help='(Deprecated) Manage TODOs using Google Keep',
        arguments=[
            (['action'],{
                "help" : "One of {add, ls, dn}",
                "action": "store"
            }),
            (['-t'],{
                "help": "Text of the TODO",
                "action": "store"
            }),
            (['-l'],{
                "help": "Length of time in hours this is expected to take",
                "action": "store"
            }),
            (['-p'],{
                "help" : "Project name. One of {DA, SL}",
                "action" : 'store'
            }),
            (['-i'],{
                "help" : "Id of the finished task",
                "action": "store"
            }),
            (['-f'],{
                "help" : "Filter TODOs for ls",
                "action": "store"
            })
        ]
    )
    def gkeep(self):
        from ..ext.gkeep import add_todo, list_todos, done_todo
        project = self.app.pargs.p or 'SL'

        if self.app.pargs.action=='add':
            add_todo(self.app.pargs.t, self.app.pargs.l, self.app.pargs.p)
        elif self.app.pargs.action=='ls':
            list_todos(self.app.pargs.f or True,
                       self.app.pargs.p)
        elif self.app.pargs.action=='dn':
            done_todo(self.app.pargs.i)

        else:
            raise NotImplemented("Action must be one of {add, ls, dn}")
        
    @ex(
        help="Manage outlook calendar",
        arguments=[
            (['action'],{
                "help" : "One of {add, ls, del}",
                "action": "store"
            }),
            (['-t'],{
                "help": "Title of the event",
                "action": "store"
            }),
            (['-i','--invite'],{
                "help": "Invitee email(s) separated by commas",
                "action": "store"
            }),
            (['-s','--start'],{
                "help": "Start time of the event",
                "action": "store"
            }),
            (['-d','--duration'],{
                "help": "Duration of the event in minutes",
                "action": "store"
            })
        ]
    )
    def ms(self):
        from ..ext.ms_outlook import add_event, list_events, delete_event
        if self.app.pargs.action=='add':
            add_event(self.app.pargs.t, self.app.pargs.i, self.app.pargs.s, self.app.pargs.d)
        elif self.app.pargs.action=='ls':
            list_events()
        elif self.app.pargs.action=='del':
            delete_event(self.app.pargs.i)
        else:
            raise NotImplemented("Action must be one of {add, ls, del}")
    
         
    # TODO: implement this as command
    # likely easiest as just alias dt='python -m dt.main'
    # echo "alias dt='python -m dt.main'" > ~/.bashrc; source ~/.basshrc
    # local / mac version and EC2 / remote version

    @ex(
        help='(WIP/Pre-Alpha) Execute a Python command across all files in current dir.',
        arguments=[
            (['command'],{
                "help": "what python command to run",
                "action": "store"
            }),
            (['-f'],{
                "help" : "filter all files in in this directory and below by this expression.",
                "action" : "store"
            })
        ]
    )
    def py(self):
        from ..ext.python_exec import execute
        execute(self.app.pargs.command, self.app.pargs.f)