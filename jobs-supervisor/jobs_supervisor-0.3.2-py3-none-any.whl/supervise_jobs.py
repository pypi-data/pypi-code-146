from .jobs_supervisor import *

python_path = 'python'

logdir = os.environ.get('JOBS_SUPERVISOR_LOGDIR')
try: 
    assert logdir is not None
except:
    logging.fatal("Please set JOBS_SUPERVISOR_LOGDIR in enviornment variables")
    exit(1)


def submit(batch, wait, dryrun=False):
    from subprocess import Popen, PIPE, STDOUT
    import re
    """Submit an batch file
    Parameters
    ----------
    batch : str
        the batch string to submig, it could be str or utf8 bytes
    wait: bool
        When True, wait the submitted jobs to exit
    dryrun : bool
        When True, print the batches to stdout instead of submit them
    """
    if dryrun:
        print(batch)
    else:
        if wait:
            cmd = ['sbatch', '-W']
        else:
            cmd = ['sbatch']
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        if type(batch) is str:
            batch = batch.encode()
        try:
            out, _ = p.communicate(input=batch)
        except:
            print(out.decode(), end='')
        return re.search("\d+", out.decode()).group(0), p.returncode

def get_sbatch(jobid_start, jobid_end, show_unavailable, show_intermedia):
    jobname = f'supervise_jobs_{jobid_start}_{jobid_end}'
    python_cmd = 'from jobs_supervisor import Supervisor;'
    python_cmd += f'Supervisor({jobid_start}, {jobid_end}, show_unavailable={show_unavailable}, show_intermedia={show_intermedia}).supervise()'
    os.makedirs(logdir, exist_ok=True)
    batch = f'''#! /bin/bash -l
#SBATCH --job-name={jobname}
#SBATCH --chdir={logdir}
#SBATCH --output={logdir}/%A-%a-%x.out
#SBATCH --export=none
#SBATCH --time=3-0
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=4G
#SBATCH --cpus-per-task=1
#SBATCH --partition=cpu
srun --export=all {python_path} -c "{python_cmd}"
'''
    return batch

def main():
    args = parse_args()
    jobid_start, jobid_end = args.jobid_start, args.jobid_end
    show_unavailable, show_intermedia = args.show_unavailable, args.show_intermedia
    jobid_start, jobid_end = min([jobid_start, jobid_end]), max([jobid_start, jobid_end])
    
    sbatch = get_sbatch(jobid_start, jobid_end, show_unavailable, show_intermedia)
    jobid, returncode = submit(sbatch, wait=False)
    print('Submitted', jobid)

if __name__=='__main__':
    main()