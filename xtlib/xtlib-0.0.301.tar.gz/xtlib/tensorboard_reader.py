#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
from asyncore import poll
import os
import sys
import json
import time
import logging
import subprocess

from xtlib import utils
from xtlib import errors
from xtlib import file_utils
from xtlib import store_utils

from .console import console
from xtlib.storage import store

logger = logging.getLogger(__name__)

class TensorboardReader():
    def __init__(self, port, cwd, store_props_dict, ws_name, run_records, browse, interval, detail, snapshot, defer):
        self.port = port
        self.ws_name = ws_name
        self.run_records = run_records
        self.browse = browse
        self.poll_interval = interval
        self.cwd = cwd
        self.detail = detail
        self.started = time.time()
        self.download_count = 0
        self.snapshot = snapshot
        self.defer = defer

        console.set_level("normal")
        os.chdir(cwd)

        # console.print("to rerun reader process for debugging:")
        # console.print("  cd {}\n".format(cwd))
        # console.print("  python run_reader.py")
        # console.print()

        self.store = store.create_from_props_dict(store_props_dict)

    # def create_local_fn_from_template(self, run_record, ws_name, run_name, blob_name):
    #     return path

    def poll_for_tensorboard_files(self, last_changed, blob_path, start_index, tb_path, job_id, run_name):
        # get all blobs in the run's output dir
        #console.print("polling blob: container={}, path={}".format(self.ws_name, blob_path))

        blobs = self.store.list_blobs(self.ws_name, blob_path, return_names=False, recursive=True)
        #console.print("blob_names=", blobs)
        download_count = 0
        byte_count = 0

        for blob in blobs:
            # is this a tensorboard file?
            basename = os.path.basename(blob.name)
            #console.print("polling blob: basename={}, name={}".format(basename, blob.name))

            if not basename.startswith("events.out.tfevents"):
                continue

            # get interesting part of blob's path (after run_name/)
            bn = blob.name[start_index:]
            modified = blob.properties.last_modified

            if not bn in last_changed or last_changed[bn] != modified:
                last_changed[bn] = modified

                # extract parent dir of blob
                test_train_node = os.path.basename(os.path.dirname(blob.name))

                if "{logdir}" in tb_path:
                    # apply to remaining template
                    tb_path_full = tb_path.format( **{"logdir": test_train_node} )
                else:
                    tb_path_full = tb_path

                #console.print("tb_path_full=", tb_path_full)
                local_fn = file_utils.path_join(tb_path_full, basename)

                local_fn = os.path.join("logs", local_fn)

                if self.detail:
                    # console.print("\ntb_path=", tb_path, ", test_train_node=", test_train_node, ", basename=", basename)
                    # console.print("  our local_fn=", local_fn)

                    # if self.snapshot:
                    #     console.print("  downloading SNAPSHOT:")
                    # else:
                    #     console.print("  downloading BLOB:")

                    blob_type = "SNAPSHOT" if self.snapshot else "BLOB"

                    console.print("\n  from {}: {}/jobs/{}/runs/{}/{}".format(blob_type, self.ws_name, job_id, run_name, bn))
                    console.print("  to file: {}".format(local_fn))

                # download the new/changed blob
                try:
                    file_utils.ensure_dir_exists(file=local_fn)
                    self.store.download_file_from_run(self.ws_name, run_name, bn, local_fn, job_id=job_id, use_snapshot=self.snapshot)
                    download_count += 1

                    file_size = os.path.getsize(local_fn)
                    byte_count += file_size

                    if self.detail:
                        console.print("  copied: {:,} bytes".format(file_size))

                except BaseException as ex:
                    logger.exception("Error in download_file_from_run, from tensorboard_reader, ex={}".format(ex))

        return download_count, byte_count

    def run(self):
        console.print("XT Tensorboard Reader process (port={})".format(self.port))

        if not self.run_records:
            errors.internal_error("No runs specified")

        names = [rr["run"] for rr in self.run_records]
        console.print("watching runs: {}".format(", ".join(names)))
        console.print()

        #console.print(self.cwd)

        download_count = 0 
        last_changed = {}
        poll_count = 0

        if not self.defer:
            self.start_tensorboard()

        console.print("pulling down initial log files...")

        while True:
            # monitor storage files by polling them for changes every poll_interval seconds
            started = time.time()
            byte_count = 0

            for r, rr in enumerate(self.run_records):
                run_name = rr["run"]
                tb_path = rr["tb_path"]
                
                #console.print("run_name=", run_name)
                '''
                - the "output" directory is for live (running) jobs writing files to "output" dir
                - the "mirrored" directory is for monitoring a directory in the running job
                - the "after" directory is for jobs that only save their Tensorboard files at end of run (via XT)
                '''
                for root in ["output", "mirrored", "after/output"]:
                    #blob_path = "runs/" + run_name + "/" + root
                    job_id = rr["job"]
                    run_path = store_utils.get_run_path(job_id, run_name)

                    blob_path = run_path + "/" + root
                    start_index = 1 + len(run_path)

                    count, path_byte_count = self.poll_for_tensorboard_files(last_changed, blob_path, start_index, tb_path, job_id, run_name)
                    download_count += count
                    byte_count += path_byte_count

            poll_count += 1

            poll_elapsed = time.time() - started

            if poll_count == 1 or byte_count > 0:
                self.print_stats(poll_elapsed, poll_count, download_count, byte_count)

            if poll_count == 1:
                console.print("finished initial pull, now monitoring for changes every {} secs...".format(self.poll_interval))

                if self.defer:
                    self.start_tensorboard()

            time.sleep(self.poll_interval)

    def start_tensorboard(self):
        # create a tensorboard process as a DEPENDENT child process
        parts = ["tensorboard", "--port", str(self.port), "--logdir=./logs"]

        console.print("\nstarting Tensorboard with cmd: {}".format(" ".join(parts)))
        tb_process = subprocess.Popen(parts, cwd=self.cwd)

        if self.browse:
            self.launch_tensorboard_url()

    def print_stats(self, poll_elapsed, poll_count, file_count, byte_count):
        self.download_count += 1

        console.print("download #{:,} (files: {:,}, bytes: {:,}, elapsed: {:.2f} mins)".format(\
            poll_count, file_count, byte_count, poll_elapsed//60))

    def launch_tensorboard_url(self):
        if self.browse:
            self.browse = False

            # if we open the browser too quickly, it shows a misleading subset of the runs until it refreshes 30 secs later
            # to fix this issue, use a thread so we can delay the browser launch for a few secs

            from threading import Thread

            def set_timer(timeout):
                time.sleep(timeout)

                url = "http://localhost:{}/".format(self.port)
                console.print("\nlaunching browser to url=", url)
                
                import webbrowser
                webbrowser.open(url)

                self.browse = False

            console.print()

            timeout = 6
            thread = Thread(target=set_timer, args=[timeout])
            thread.daemon = True    # mark as background thread
            thread.start()

def main(port, fn_run_records):

    with open(fn_run_records, "rt") as infile:
        json_text = infile.read()

    json_text = json_text.replace("'", "\"")
    pd = json.loads(json_text)

    # pd is a dict of params to pass to TensorboardReader
    reader = TensorboardReader(port=port, **pd)
    reader.run()

if __name__ == "__main__":
    main()
