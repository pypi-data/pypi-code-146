
import os
import sys
import subprocess
import random
import string
import json
import time
import traceback

class NetWork:
  '''
  Represents all the details needed to make remote calls and read remote responses.
  Provides both a syncronous and an asyncronous API.
  '''

  def gen_job_id(num_chars=8):
    return ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(num_chars)])

  def read_json(json_f):
    with open(json_f, 'r') as fd:
      return json.load(fd)

  def safe_del(file_name):
    if os.path.exists(file_name):
      try:
        os.remove(file_name)
      except:
        traceback.print_exc()

  def __init__(self, shared_work_req_directory, shared_work_return_directory=None, work_req_prefix='call_', work_lock_prefix='lock_', work_return_prefix='return_', fatal_timeout_s=300):
    '''
    :param str shared_work_req_directory: Shared network directory where input requests and files will be written
    :param str shared_work_return_directory: Optional, defaults to shared_work_req_directory if unspecified. Directory where completed work will be written.
    :param str work_req_prefix: Prefix to use for input file names
    :param str work_return_prefix: Prefix to use for output file names
    '''
    self.shared_work_req_directory = shared_work_req_directory

    # If unspecified, out directory is the same as in directory.
    if shared_work_return_directory is None:
      self.shared_work_return_directory = shared_work_req_directory
    else:
      self.shared_work_return_directory = shared_work_return_directory

    if work_req_prefix.lower() == work_return_prefix.lower() or work_req_prefix.lower() == work_lock_prefix.lower():
      raise Exception('Refusing to use identical work_req_prefix, work_lock_prefix, work_return_prefix, please ensure these are different!')

    self.work_req_prefix = work_req_prefix
    self.work_lock_prefix = work_lock_prefix
    self.work_return_prefix = work_return_prefix
    self.fatal_timeout_s = fatal_timeout_s

    for req_d in [self.shared_work_req_directory, self.shared_work_return_directory]:
      if not os.path.exists(req_d):
        os.makedirs(req_d)

  def job_id_from_file_name(self, file_name):
    if self.shared_work_req_directory in file_name:
      file_name = file_name.replace(self.shared_work_req_directory, '').lstrip(os.sep)
    if self.work_req_prefix in file_name:
      file_name = file_name.replace(self.work_req_prefix, '')

    file_name = file_name.replace('.json', '')
    file_name = file_name.replace('.lock', '')

    return file_name

  def work_req_file(self, job_id):
    return os.path.join(
      self.shared_work_req_directory, self.work_req_prefix+job_id+'.json',
    )

  def work_lock_file(self, job_id):
    return os.path.join(
      self.shared_work_req_directory, self.work_lock_prefix+job_id+'.lock',
    )

  def work_return_file(self, job_id):
    return os.path.join(
      self.shared_work_return_directory, self.work_return_prefix+job_id+'.json',
    )
  
  def write_work_req_file(self, job_id, work_req_d):
    work_file = self.work_req_file(job_id)
    with open(work_file, 'w') as fd:
      json.dump(work_req_d, fd)

  def write_work_lock_file(self, job_id):
    if self.shared_work_req_directory in job_id:
      lock_f = job_id
    else:
      lock_f = self.work_lock_file(job_id)
    with open(lock_f, 'w') as fd:
      fd.write('LOCK')

  def write_work_return_file(self, job_id, work_return_d):
    work_file = self.work_return_file(job_id)
    with open(work_file, 'w') as fd:
      json.dump(work_return_d, fd)
    # Also unlock the work
    lock_f = self.work_lock_file(job_id)
    if os.path.exists(lock_f):
      os.remove(lock_f)

  def poll_work_return_file(self, job_id, poll_interval_s=0.25):
    if self.shared_work_return_directory in job_id:
      work_file = job_id # someone mis-passed data, but that's fine & detectable
    else:
      work_file = self.work_return_file(job_id)

    begin_s = int(time.time())
    while not os.path.exists(work_file):
      time.sleep(poll_interval_s)
      if int(time.time()) - begin_s > self.fatal_timeout_s:
        raise Exception('Timeout during poll_work_return_file!')

    with open(work_file, 'r') as fd:
      return json.load(fd)


  def run_cmd_sync(self, cmd_line: list):
    try:
      job_id = NetWork.gen_job_id()
      self.write_work_req_file(job_id, {
        'cmd': cmd_line,
      })
      work_return_d = self.poll_work_return_file(job_id)
      
      NetWork.safe_del( self.work_req_file(job_id) )
      NetWork.safe_del( self.work_lock_file(job_id) )
      NetWork.safe_del( self.work_return_file(job_id) )

      return work_return_d
    except:
      traceback.print_exc()
      return traceback.format_exc()
    return None

  def poll_any_work_req_dicts(self, poll_interval_median_s=0.5, poll_interval_dev=0.4, should_continue_polling_fn=None):
    poll_interval_min_s = max(0, poll_interval_median_s - poll_interval_dev)
    poll_interval_max_s = poll_interval_median_s + poll_interval_dev

    if should_continue_polling_fn is None:
      should_continue_polling_fn = lambda: True

    while should_continue_polling_fn():

      # We sleep for random times to reduce network lock-file race-cases.
      time.sleep(random.uniform(poll_interval_min_s, poll_interval_max_s))

      for file_name in os.listdir(self.shared_work_req_directory):
        if file_name.startswith(self.work_req_prefix):
          json_file_path = os.path.join(self.shared_work_req_directory, file_name)
          # Found one! Is this claimed by another processing node?
          job_id = self.job_id_from_file_name(file_name)
          lock_f = self.work_lock_file(job_id)
          if not os.path.exists(lock_f):
            # We're first, claim it!
            self.write_work_lock_file(lock_f)
            # Return the work dictionary
            work_d = NetWork.read_json(json_file_path)
            work_d['job_id'] = job_id
            return work_d




