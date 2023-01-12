import zipfile
import click
import sys, os, re, yaml, shutil
import stat
import subprocess
from glob import glob
from pathlib import Path
from datetime import datetime

from flexmin import flexmin_srv
from flexmin.flexmin_srv import get_config as flexmin_get_config
from flexmin.utils import yamlconfigs
from flexmin.run_checks import checks

from xmlrpc.server import SimpleXMLRPCServer


@click.group()
def cli():
    pass


@cli.command()
def version():
    from flexmin import __version__
    click.echo(__version__)

@cli.command()
@click.argument('apps_folder', default='apps')
#@click.option('-Y', '--yes', is_flag=True, default=False, help='No prompt, assume yes to questions')
@click.option('-H', '--host', default='localhost', help='Host name')
@click.option('-P', '--port', default=8001, type=int, help='Port number')
@click.option('-V', '--verbose', default='', type=str, help='Show activity [debug,display]')
def run(**args):
    #install_args(args)
    apps_folder = args['apps_folder']    
    
    from flexmin import __version__
    click.echo("Flexmin: %s on Python %s\n\n" % (__version__, sys.version))
    
    errors = run_checks(checks)
    if errors:
        for m in errors:
            click.echo("error: " + m)
        exit(1)

    # service
    server = SimpleXMLRPCServer((args['host'],args['port']),allow_none=True)
    if 'verbose' in args and args['verbose']:
        server.register_instance(flexmin_srv.TaskServer(args['verbose']))
    else:
        server.register_instance(flexmin_srv.TaskServer(''))
    server.serve_forever()
    
    
def run_checks(checks={}):
    """
    Carry out some basic checks before trying to run flexmin service
    """
    error_msg = []
    if 'all_of_executables' in checks:
        for executable in checks['all_of_executables']:
            if not shutil.which(executable):
                error_msg.append(f"Application {executable} not found.")
    if 'all_of_files' in checks:
        # Look for any of the files listed, if one found then okay
        for f in checks['all_of_files']:
            if not os.path.isfile(f):
                error_msg.append(f"File {f} not found.")
    if 'all_of_folders' in checks:
        # Look for any of the folders listed, if one found then okay
        for f in checks['all_of_folders']:
            if not os.path.isdir(f):
                error_msg.append(f"Folder {f} not found.")
    if len(error_msg) == 0:
        return error_msg
    elif 'error_threshold' in checks:
        for threshold in checks['error_threshold']:
            if len(error_msg) >= threshold:
                # append message for this threshold
                error_msg.append(checks['error_threshold'][threshold])
    return error_msg


def yamlconfig(yaml_file=''):
    """
    Convert a generic yaml based config file into an app specific config file
    """
    fm_parameters = flexmin_get_config()
    if yaml_file:
        yaml_file = os.path.join(fm_parameters.FM_CONFIGS,yaml_file)
        t = yamlconfigs.Config(yaml_file,fm_parameters.__dict__)
        t.native()
    else:
        return ["Error: no yaml file specified " + str(args)]

    
@cli.command(name='yamlconfig')
@click.argument('yaml_file', default=None)
def yamlconfig_command(**args):
    error_msg = yamlconfig(args['yaml_file'])
    if error_msg:
        print("\n".join(error_msg), file=sys.stderr)


@cli.command()
@click.argument('apps_folder', default='apps')
#@click.option('-Y', '--yes', is_flag=True, default=False, help='No prompt, assume yes to questions')
@click.option('-F', '--folder', default='', help='Install folder')
@click.option('-L', '--log', default='/var/log/flexmin_setup.log.md')
def install(**args):
    # get configuration via the flexmin server method
    fm = flexmin_get_config(silent=True)
    
    if 'folder' in args and args['folder']:
        fm.FM_HOME = args['folder']   # set FM_HOME to explicity defined folder
    elif not 'FM_HOME' in fm:
        fm.FM_HOME = '/home/flexmin'   # default if not 
        
    if 'FM_UPGRADE_BLOCK' in fm:
        reBlock = re.compile('^(' + fm.FM_UPGRADE_BLOCK + ')$')
    else:
        reBlock = None
    
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    assets_cfg = os.path.join(assets_dir, "assets.txt")
    
    # open log file ready for writing, zero buffer to ensure all output logged in case of crash
    log = open(args['log'],'w')  
    print("Flexmin installation")
    print("====================")
    log.write("Flexmin installation\n")
    log.write("====================\n")
    
    if os.path.exists(assets_cfg):
        with open(assets_cfg,'r') as af:
            y_src = af.read()
            # create regex, enclosing parameters in {}
            params = dict((re.escape('{'+k+'}'), v) for k, v in fm.__dict__.items()) 
            # compile regexes
            pattern = re.compile("|".join(params.keys()))
            # substitute parameters in yaml source file
            y_mod = pattern.sub(lambda m: params[re.escape(m.group(0))], y_src)
            # get data from modified yaml config
            assets = yaml.load(y_mod, Loader=yaml.SafeLoader)
            if 'files' in assets:
                files = assets['files']
            else:
                files = {}
    else:
        click.echo(f"Error: File {assets_cfg} not found.")
        log.write(f"Error: File {assets_cfg} not found.  \n")
        sys.exit(1)  # exit with error code 1
    
    # Carry out prerequisite checks
    pr_errors = []
    for pr in assets['prerequisites']:
        if re.match('^[^' + os.sep + ']+$',pr['check']):
            # no path check for executable
            if not shutil.which(pr['check']):
                if 'fail_msg' in pr:
                    pr_errors.append(pr['fail_msg'])
                else:
                    pr_errors.append(f"{pr['check']} not found")
        elif not os.path.exists(pr):
            if 'fail_msg' in pr:
                pr_errors.append(pr['fail_msg'])
            else:
                pr_errors.append(f"{pr['check']} not found")
            
    if len(pr_errors) > 0:
        log.write("\n")
        click.echo("")
        click.echo("Failed prerequisites check:")
        log.write("Failed prerequisites check:  \n")
        for msg in pr_errors:
            click.echo(msg)
            log.write(msg + "  \n")
        sys.exit(1)  # exit with error code 1
            
    for asset in assets['assets']:
        zip_filename = os.path.join(assets_dir, asset['source'])
        target_dir = asset['destination']
        if 'preserve' in asset:
            preserve = asset['preserve']
        else:
            preserve = None

        if os.path.exists(zip_filename):
            click.echo("")
            log.write("\n")
            if not os.path.exists(target_dir):
                if click.confirm('Create folder %s?' % target_dir, default=True):
                    #log.write("Creating folder %  \n" % target_dir)
                    do_unzip = True
                else:
                    do_unzip = False # no unzip possible if folder not created
            else:  
                # folder already exists, do some checks
                if reBlock and reBlock.match(os.path.basename(target_dir)):
                    do_unzip = False  # block names specified, and this is in the list
                elif reBlock:
                    do_unzip = True   # block names specified, but no match implies permission to overwrite
                elif click.confirm('Replace folder %s (delete and replace with new contents)?' % target_dir, default=True):
                    do_unzip = True
                else:
                    do_unzip = False  # no unzip if not replacing folder

            if do_unzip:
                
                # Delete the folder, preserving existing files if specified
                if not preserve:
                    if os.path.isdir(target_dir):
                        shutil.rmtree(target_dir)
                    #log.write("Removing folder %  \n" % target_dir)
                else:
                    #log.write("Clearing out folder % but keeping files and folders known to store persistent data  \n" % target_dir)
                    if os.path.isdir(target_dir):
                        result = clear_and_preserve(target_dir, preserve)
                        log.write("  \n".join(result) + "  \n")
                    
                # (Re)create the folder
                if not os.path.exists(target_dir):
                    #log.write("Creating folder %  \n" % target_dir)
                    os.makedirs(target_dir)
                    
                # Extract replacement files into folder
                log.write("Unzipping asset %s to %s - " % (asset['source'], target_dir) )
                click.echo("[ ] Unzipping asset %s to %s" % (asset['source'], target_dir) )
                zip_file = zipfile.ZipFile(zip_filename, "r")
                zip_file.extractall(target_dir)
                zip_file.close()
                click.echo("\x1b[A[X]")
                log.write("Done  \n")
            else:
                log.write(f"**Not** replacing {target_dir} - declined or blocked\n")
                click.echo(f"Not replacing {target_dir} - declined or blocked")
        else:
            click.echo("Error: Specified asset file %s not found." % asset['source'])
            log.write("Error: Specified asset file %s not found.  \n" % asset['source'])
            
        # Check if folder has files that should be distributed elsewhere
        folder_name = os.path.basename(target_dir)
        if folder_name in files:
            for f in files[folder_name]:
                copied = False
                if f['destination'][-1] == os.sep:  # is a folder, add filename
                    file_dest = f['destination'] + f['name']
                else:  # is file path
                    file_dest = f['destination'] 
                if 'check_existing' in f and f['check_existing'] and os.path.isfile(file_dest):
                    if f['user_confirm']:
                        if ( ( reBlock and not reBlock.match(f['name']) ) or
                                click.confirm(f"Replace existing {file_dest}?", default=True) 
                            ):
                            log.write(f"Replacing {file_dest} with a copy from {folder_name}  \n")
                            shutil.copyfile(target_dir + os.sep + f['name'], file_dest)
                            copied = True
                            click.echo(f"{file_dest} replaced")
                        else:
                            click.echo(f"You can copy the {f['name']} file from {folder_name} to {file_dest} later if you wish")
                else:
                    log.write(f"Copying {f['name']} to {file_dest}  \n")
                    # ensure destination directory exists
                    Path(os.path.dirname(file_dest)).mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(target_dir + os.sep + f['name'], file_dest)
                    copied = True
                if copied and 'yamlconfig' in f:
                    yamlconfig(yaml_file=file_dest)  # process yaml file to generate native configuration

                
        # Check for scripts in system folder and ensure it has execute permissions
        if os.path.basename(target_dir) == 'system':
            setup_script = os.path.join(target_dir, 'setup.sh')
            script_list = glob(os.path.join(target_dir,'*.sh'))
            #log.write("\n")
            for script in script_list:
                try:
                    log.write(f"Found system script: {script}, making executable  \n")
                    os.chmod(script, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXGRP | stat.S_IRGRP | stat.S_IWGRP)
                    click.echo(f"Set execute permission for {script}")
                    if script == setup_script:
                        setup_ready = True
                    #click.echo("Please run " + setup_script + " to complete the installation or upgrade")
                    #click.echo("On initial installation specify a flexmin password: setup.sh <flexmin_password>")
                except:
                    click.echo(f"Error: Failed to set execute permission for {script}")
                    log.write(f"Error: Failed to set execute permission for {script}  \n")

    click.echo("")
    click.echo("Running set up script: " + setup_script)
    click.echo("")
    log.write("\nRunning setup.sh script  \n\n")
    log.close()
    done = runscript(script=setup_script, log=args['log'], folder=fm.FM_HOME)

    if os.path.isfile(os.path.join(fm.FM_CONFIGS,'installed')):
        log_type = 'upgrade'  # already installed so this is an upgrade
    else:
        log_type = 'install'  # is first install
        
    # On install parameters will not be defined, make assumption about log root
    if not 'FM_LOGROOT' in fm and os.path.isdir('/var/log/flexmin'):
        fm.FM_LOGROOT = '/var/log/flexmin'

    # Move log file into FM_LOGROOT if exists
    if done and os.path.isfile(args['log']):
        if 'FM_LOGROOT' in fm and os.path.isdir(fm.FM_LOGROOT):
            timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
            log_dest = os.path.join(fm.FM_LOGROOT,f"flexmin_{log_type}_log_{timestamp}.md")
            shutil.copyfile(args['log'], log_dest)
            click.echo(f"A log of this {log_type} is at {log_dest}")
        else:
            click.echo(f"A log of this {log_type} is at {args['log']}")
    else:
        click.echo(f"Something may have gone wrong, check output above or at {args['log']}")


def runscript(script='', log='', folder=''):
    """
    Run shell script to complete installation
    """
    if script and log:
        sub = subprocess.Popen(script + " '" + folder + "'", 
                        shell=True,
                        universal_newlines=True,
                        bufsize=0,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT
                        )
    else:
        prnt("Error: No script or log file specified")
        return False
    
    with open(log,'a') as log_file:
        while True:
            response = sub.stdout.readline()  # decode to convert from bytestring to strings
            if response:
                if response[0:9].lower() == 'password:':
                    log_file.write("(password not sent to log)  \n")
                else:
                    log_file.write(response.rstrip() + "  \n")
                print(response.rstrip())  # output each line with two extra spaces to ensure markdown uses separate lines
            else:
                break
            
    print("\nSetup.sh script completed")
    return True


@cli.command(name="runscript")
@click.option('-S', '--script', default='/home/flexmin/system/setup.sh')
@click.option('-F', '--folder', default='/home/flexmin', help='Folder for flexmin files')
@click.option('-L', '--log', default='/var/log/flexmin_setup.log.md')
def runscript_command(**args):
    runscript(args['script'], args['log'], args['password'])

                

def clear_and_preserve(target_dir, preserve):
    """
    Clear out the specified target_dir, but keep any files matching the globs specified in preserve (list)
    e.g.
    target_dir = '/my/folder/path'
    preserve = [ '**/database/*', 'keepfile.txt']
    """
    result = []  # list of text lines to return
    result.append("Clearing out " + str(target_dir) + " preserving " + str(preserve))
    print(result[-1])
    
    # Generate list of all files and folders
    del_list = glob(os.path.join(target_dir,'**/*'),recursive=True)
    # add hidden files to the list (*nix)
    del_list = del_list + glob(os.path.join(target_dir,'**/.*'),recursive=True)
    # add hidden folders and contents to the list (*nix)
    del_list = del_list + glob(os.path.join(target_dir,'**/.*/**/*'),recursive=True)
    
    # Generate list of all files and folders to keep 
    keep_list = []
    del_dir_list = []
    for p in preserve:
        keep_list = keep_list + ( glob(os.path.join(target_dir,p)) )
    print("Keeping: " + str(keep_list))
    for k in keep_list:
        result.append("Keeping:  " + str(k))
        

    # delete all files not in keep_list, add folders to separate del_dir_list
    for del_item in del_list:
        if not del_item in keep_list:
            if os.path.isfile(del_item):
                os.remove(del_item)
            elif os.path.isdir(del_item):
                del_dir_list.append(del_item)

    # delete all directories from original del_list
    del_dir_list.sort(key=len, reverse=True)  # get into length order, deal with longest paths first
    for del_dir in del_dir_list:
        try:
            os.rmdir(del_dir)
        except Exception as ex:
            #print(ex)  # if dir not empty the command should fail, list those not deleted
            result.append("Folder not deleted " + str(del_dir))
            print(result[-1])
    
    return result


if __name__ == '__main__':
    cli()
