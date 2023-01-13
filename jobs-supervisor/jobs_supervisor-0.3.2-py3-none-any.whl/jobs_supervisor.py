from .FeishuBot import *
import os, time, logging
import argparse

webhook = os.environ.get('JOBS_SUPERVISOR_WEBHOOK')
try: 
    assert webhook is not None
except:
    logging.fatal("Please set JOBS_SUPERVISOR_WEBHOOK in enviornment variables")
    exit(1)

stop_monitor_status = ['fail', 'unknown', 'complete', 'unavailable', 'cancel', 'timeout']
continue_monitor_status = ['running', 'pending']

class Supervisor():
    def __init__(self, jobid_start, jobid_end, show_unavailable=False, show_intermedia=False):
        self.fei = FeishuBot(webhook)
        self.jobid_start, self.jobid_end = jobid_start, jobid_end
        self.jobs = list(range(jobid_start, jobid_end+1))
        self.show_unavailable = show_unavailable
        self.show_intermedia = show_intermedia
        msg = f'Init Supervisor to monitor jobs {min(self.jobs)} to {max(self.jobs)}'
        if self.show_intermedia:
            msg += ' with show_intermedia'
        if self.show_unavailable:
            msg += ' with show_unavailable'
        self.fei.send_msg(msg)
    
    def get_job_name(self, jobid):
        lines = os.popen(cmd=f'sacct -X -j {jobid} -P -o "jobname"').read().strip().split('\n')
        if len(lines) == 1:
            return ''
        jobnames = sorted(list(set(lines[1:])))
        if len(jobnames) == 0:
            return ''
        jobname = jobnames[0]
        return jobname
         
    def parse_job_status(self, jobid):
        lines = os.popen(cmd = f'sacct -X -j {jobid}').read().strip().split('\n')
        print('\n'.join(lines))
        if len(lines) == 2: 
            return 'unavailable'
        for line in lines[2:]:
            if 'fail' in line.lower():
                return 'fail'
            if 'cancel' in line.lower():
                return 'cancel'
            if 'pending' in line.lower():
                return 'pending'
            if 'running' in line.lower():
                return 'running'
            if 'timeout' in line.lower():
                return 'timeout'
            if 'complete' not in line.lower():
                msg = f'unknown job status for jobid {jobid} {self.get_job_name(jobid)}:\n{line}'
                self.fei.send_msg(msg)
                return 'unknown'
        return 'complete'

    def supervise(self, ):
        list_ongoing = self.jobs.copy()
        list_incompete, jobs_status, list_unavaliable = [], [], []
        while len(list_ongoing) > 0:
            list_to_remove = []
            for jobid in list_ongoing:
                status = self.parse_job_status(jobid)
                if status in stop_monitor_status:
                    if self.show_intermedia:
                        if not self.show_unavailable and status=='unavailable':
                            pass
                        else:
                            self.fei.send_msg(f"Stop Monitor {jobid} {self.get_job_name(jobid)} with status {status}")
                    list_to_remove.append(jobid)
                    if status == 'unavailable':
                        list_unavaliable.append((jobid, self.get_job_name(jobid)))
                    elif status != 'complete':
                        list_incompete.append((jobid, self.get_job_name(jobid)))
                    jobs_status.append((jobid, status))
            for jobid in list_to_remove:
                list_ongoing.remove(jobid)
            if len(list_ongoing)>0: 
                print('list_ongoing:', list_ongoing)
                time.sleep(60)
        list_incompete = sorted(list_incompete)
        list_unavaliable = sorted(list_unavaliable)
        msg = f'End to monitor jobids {self.jobid_start} to {self.jobid_end}.\n'
        for jobid, status in jobs_status:
            if not self.show_unavailable and status=='unavailable':
                continue
            msg += f'{jobid} {status} {self.get_job_name(jobid)}\n'
        msg += '='*8+'\n'
        if len(list_incompete) == 0:
            msg += 'No incomplete jobs.\n'
        else:
            msg += f'Incomplete jobs: {list_incompete}\n'
        if len(list_unavaliable) == 0:
            msg += 'No unavaliable jobs.'
        else:
            msg += f'Unavaliable jobs: {list_unavaliable}'
        self.fei.send_msg(msg)

def parse_args():
    parser = argparse.ArgumentParser(description='supervise jobs by ids')
    parser.add_argument('jobid_start', type=int, help='jobid start')
    parser.add_argument('jobid_end', type=int, help='jobid end')
    parser.add_argument('--show_unavailable', action="store_true", help='show unavaliable jobs status')
    parser.add_argument('--show_intermedia', action="store_true", help='ignore intermedia messages')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    jobid_start, jobid_end = args.jobid_start, args.jobid_end
    show_unavailable, show_intermedia = args.show_unavailable, args.show_intermedia
    jobid_start, jobid_end = min([jobid_start, jobid_end]), max([jobid_start, jobid_end])
    
    supervisor = Supervisor(jobid_start, jobid_end, show_unavailable, show_intermedia)
    supervisor.supervise()

if __name__=='__main__':
    main()

