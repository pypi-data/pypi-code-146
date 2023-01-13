#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# mirror_worker.py: handles mirroring of files from run box to grok server
import os
import time
import queue
import logging
import threading
import traceback
from fnmatch import fnmatch
import requests
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from xtlib import utils
from xtlib import errors
from xtlib import file_utils
from xtlib.utils import log_info, log_title, log_info_to_text
from .console import console

logger = logging.getLogger(__name__)

class CommonHandler():
    '''
    Shared code to define how to process a file/directory change correctly.
    '''
    def __init__(self, name, store, ws_name, job_id, run_name, node_id, path, dest_folder):
        self.name = name
        self.store = store
        self.ws_name = ws_name
        self.job_id = job_id
        self.run_name = run_name
        self.path = path
        self.file_send_count = 0
        self.dest_folder = dest_folder

        if run_name:
            # we are mirroring to a RUN blob path
            self.blob_helper = store.run_files(ws_name, run_name, job_id=job_id)
        
        elif node_id:
            # we are mirroring to a NODE blob path
            self.blob_helper = store.node_files(ws_name, node_id, job_id=job_id)
        
        else:
            errors.api_error("Mirroring internal error: must specify 'run_name' or 'node_id'")
        
    def process_file_event_now(self, fn_src, fn_dest, src_blob_path, dest_blob_path,
        event_type, is_dir, show_calls):
        '''
        Args:
            fn_src:             the name of the file/dir that the even occurred on
            fn_dest:            the name of the file/dir, after renaming
            src_blob_path:      the path of the associated blob 
            dest_blob_path:     the path of the associated blob, after renaming
            event_type:         the type of file-watcher event being processed ('modified' | 'created' | 'moved' | 'deleted')
            is_dir:             True if this is a directory event
            show_calls          True if event-level logging should be done to the console

        Processing:
            this function does the actual work of updating the blob storage for the file-watch events.
        '''

        if show_calls:
            print("process_file_event_now: fn_src={}, fn_dest={}, src_blob_path={}, dest_blob_path={}, event_type={}, is_dir={}".format(\
                fn_src, fn_dest, src_blob_path, dest_blob_path, event_type, is_dir))

        try:

            if event_type in ["moved", "deleted"]:

                if is_dir:
                    if show_calls:
                        console.print("{}: detected DELETED or RENAMED directory: {}".format(self.name, fn_src))
                        console.print("{}: deleting BLOB directory: {}".format(self.name, src_blob_path))
                    # delete blobs under old folder name
                    #self.store.delete_run_subfolder_and_files(self.ws_name, self.run_name, src_blob_path, job_id=self.job_id)
                    self.blob_helper.delete_files(src_blob_path + "/**")

                else:
                    #if self.store.does_run_file_exist(self.ws_name, self.run_name, src_blob_path, job_id=self.job_id):
                    if self.blob_helper.does_file_exist(src_blob_path):
                        if show_calls:
                            console.print("{}: detected DELETED or RENAMED file: {}".format(self.name, fn_src))
                            console.print("{}: deleting BLOB file: {}".format(self.name, src_blob_path))
                        #self.store.delete_run_file(self.ws_name, self.run_name, src_blob_path, job_id=self.job_id)
                        self.blob_helper.delete_file(src_blob_path)

            if event_type != "deleted":
                # upload file/dir tree
                blob_path = dest_blob_path if event_type == "moved" else src_blob_path
                file_path = fn_dest if event_type == "moved" else fn_src

                if is_dir:
                    # dir moved event
                    if os.path.exists(file_path):
                        if show_calls:
                            console.print("{}: detected NEW or RENAMED directory: {}".format(self.name, file_path))
                            console.print("{}: uploading files to BLOB directory: {}".format(self.name, blob_path))
                        #self.store.upload_files_to_run(self.ws_name, self.run_name, blob_path, fn_dest + "/**", job_id=self.job_id)
                        self.blob_helper.upload_files(blob_path, fn_dest + "/**")

                else:
                    # file create/update/moved event
                    if os.path.exists(file_path):
                        if show_calls:
                            console.print("{}: detected NEW, UPDATED, or RENAMED file: {}".format(self.name, file_path))
                            console.print("{}: uploading file to BLOB: {}".format(self.name, blob_path))
                        #self.store.upload_file_to_run(self.ws_name, self.run_name, blob_path, file_path, job_id=self.job_id)
                        self.blob_helper.upload_files(blob_path, file_path)

        except BaseException as ex:
            # logger.exception("Error in process_file_event_now, ex={}".format(ex))
            # console.print("process_file_event_now EXCEPTION: " + str(ex))
            traceback.print_exc()

class DelayQueueWorker(CommonHandler):
    def __init__(self, store, ws_name, job_id, run_name, node_id, path, delay_queue,
        mirror_delay_mins, show_calls, dest_folder):

        super().__init__("BG_WATCHER", store, ws_name, job_id, run_name, node_id, path, 
            dest_folder=dest_folder)

        self.delay_queue = delay_queue
        self.mirror_delay_mins = mirror_delay_mins
        self.show_calls = show_calls
        self.pending_items = []

        if show_calls:
            print("{}: store={}, ws_name={}, job_id={}, run_name={}, path={}, delay_queue={}, mirror_delay_mins={}".format(\
                self.name, store, ws_name, job_id, run_name, path, delay_queue, mirror_delay_mins))

    def process_queue_entry_if_present(self, q, show_calls):
        process_all = False
        stop = False

        if not q.empty():
            item = q.get()
            if item is None:
                process_all = True
                stop = True
            else:
                # add to list of pending_items (if not already present)
                # ready, fn_src, fn_dest, src_blob_path, dest_blob_path, event_type, is_dir = item
                # LOOK for a match of all fields except READY
                fn_src = item[1]
                found = next((x for x in self.pending_items if x[1:] == item[1:]), None)
                if found:
                    # if show_calls:
                    #     console.print("{}: skipping DUP update for fn=", self.name, fn_src)
                    pass
                else:
                    if show_calls:
                        console.print("{}: adding fn={}".format(self.name, fn_src))
                    self.pending_items.append(item)

            q.task_done()

        return process_all, stop

    def run(self):
        self.pending_items = []
        show_calls = self.show_calls

        if show_calls:
            print("{}: is now running".format(self.name))

        while True:
            # process QUEUE
            process_all, stop = self.process_queue_entry_if_present(self.delay_queue, show_calls)

            # process PENDING ITEMS
            last_index = len(self.pending_items)-1

            # process in reverse order since we are deleting selected items
            for i in range(last_index, -1, -1):
                ready, fn_src, fn_dest, src_blob_path, dest_blob_path, event_type, is_dir = self.pending_items[i]

                if process_all or time.time() >= ready:
                    self.process_file_event_now(fn_src, fn_dest, src_blob_path, dest_blob_path, event_type, is_dir, self.show_calls)
                    del self.pending_items[i]

            if stop:
                break

            # sleep
            time.sleep(1)

        if show_calls:
            console.print("{} exiting...".format(self.name))

class MirrorWorker():
    def __init__(self, store, run_dir, mirror_dest, wildcard_path, grok_url, ws_name, run_name, node_id,
        job_id=None, mirror_delay_mins=0, show_calls=False, dest_folder=None):
        # path = '.'
        # wildcard = "*.tfevents.*" 

        self.run_dir = run_dir
        self.job_id = job_id
        self.mirror_delay_mins = mirror_delay_mins

        # some paths may contain environment variables that need to be expanded
        wildcard_path = os.path.expandvars(wildcard_path)
        wildcard_path = wildcard_path.replace("\\", "/")

        # adjust things when user specified a specific file (no "*")
        if show_calls:
            console.print("MirrorWorker: run_dir: {}, wildcard_path: {}, blob run_name: {}, blob node_id: {}".format( \
                run_dir, wildcard_path, run_name, node_id))
        else:
            log_info("MirrorWorker, wildcard_path", wildcard_path)

        if not wildcard_path.startswith("/"):
            wildcard_path = os.path.join(run_dir, wildcard_path)

        # our rule is a directory must be followed by "*", "**", or a name with a "*" within in
        # otherwise, we will assume a specific file has been specified
        if not "*" in wildcard_path:
            # a specific file has been specified
            path = os.path.dirname(wildcard_path)
            wildcard = os.path.basename(wildcard_path)

        else:
            path = os.path.dirname(wildcard_path)
            wildcard = os.path.basename(wildcard_path)

        path = file_utils.fix_slashes(path)
        if show_calls:
            console.print("MirrorWorker: path={}, wildcard={}".format(path, wildcard))

        # in case program will create dir, but it hasn't yet been created
        file_utils.ensure_dir_exists(path)

        self.event_handler = MyHandler(store, mirror_dest, grok_url, ws_name, run_name, node_id, path, wildcard, 
            job_id, mirror_delay_mins, show_calls, dest_folder=dest_folder)

        self.observer = Observer()
        self.observer.schedule(self.event_handler, path, recursive=True)

    def get_status(self):
        status = self.event_handler.get_status()
        status["run_dir"] = self.run_dir
        return status

    def start(self):
        # start observer on his OWN THREAD
        self.observer.start()

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer = None

        if self.event_handler:
            self.event_handler.stop()
            self.event_handler = None

class MyHandler(FileSystemEventHandler):

    def __init__(self, store, mirror_dest, grok_url, ws_name, run_name, node_id, path, wildcard, job_id=None, 
        mirror_delay_mins=0, show_calls=False, dest_folder=None):

        super(MyHandler, self).__init__()

        self.store = store
        self.mirror_dest = mirror_dest
        self.grok_url = grok_url
        self.ws_name = ws_name
        self.run_name = run_name
        self.path = os.path.realpath(path)
        self.wildcard = wildcard
        self.last_modified = {}    # used to ignore duplicate msgs
        self.started = time.time()
        self.file_send_count = 0
        self.file_check_count = 0
        self.job_id = job_id
        self.mirror_delay_mins = mirror_delay_mins
        self.common_handler = CommonHandler("FG WATCHER", self.store, ws_name, job_id, 
            run_name, node_id, self.path, dest_folder=dest_folder)

        self.show_calls = show_calls

        self.delay_queue = None
        self.delay_worker = None

        # use dest_folder if provided, otherwise fall back on last folder name in path being mirrored
        self.dest_folder = dest_folder if dest_folder else os.path.basename(self.path)

        if mirror_delay_mins:
            self.delay_queue = queue.Queue()

            # start worker thread
            ww = DelayQueueWorker(store, ws_name, job_id, run_name, node_id, path, 
                self.delay_queue, mirror_delay_mins, self.show_calls, dest_folder=dest_folder)

            self.delay_worker = threading.Thread(target=ww.run, daemon=True, args=[])

            self.delay_worker.start()

    def get_status(self):
        elapsed = time.time() - self.started
        status = {"ws_name": self.ws_name, "run_name": self.run_name, "elapsed": elapsed, 
            "check_count": self.file_check_count, "send_count": self.file_send_count}
        return status

    def send_file_to_grok(self, fn):
        if self.show_calls:
            console.print("mirror: send_file_to_grok: fn=", fn)

        fin = open(fn, 'rb')
        files = {'file': fin}
        append = False

        # build relative path
        plen = 1 + len(self.path)
        rel_path = os.path.dirname(fn)[plen:]
        rel_path = rel_path.replace("\\", "/")

        payload = {"ws_name": self.ws_name, "run_name": self.run_name, "append": append, "rel_path": rel_path}
        console.print("mirror: payload=", payload)

        try:
            result = requests.post(url="http://" + self.grok_url + "/write_file", files=files, params=payload)
            if self.show_calls:
                console.print("mirror: POST result=", result)
            self.file_send_count += 1
        except BaseException as ex:
            logger.exception("Error in send_file_to_grok, ex={}".format(ex))
            console.print("send_file_to_grok EXCEPTION: " + str(ex))

    def stop(self):
        # write any pending calls that have been scheduled
        if self.delay_queue:
            self.delay_queue.put( None )

            # wait for all files to be processed
            utils.log_info("mirror_worker.stop", "waiting for queue to be processed at end of run")
            self.delay_queue.join()
            utils.log_info("mirror_worker.stop", "queue processing completed")
    
    def build_blob_path(self, fn, event_type, is_dir):
                        
        if fn:
            # build dest_blob_path each time an event occurs
            plen = 1 + len(self.path)
            fn_rel = fn[plen:]
            fn_rel = fn_rel.replace("\\", "/")

            # if self.show_calls:
            #     console.print("on_any_event BEFORE: fn: {}, fn_rel: {}".format(fn, fn_rel))

            if "/" in fn_rel:
                # it is a multi-dir path; use all but last folder of fn_rel
                blob_path = "mirrored/" + self.dest_folder + "/" + os.path.dirname(fn_rel)
            else:
                # its a simple name; just write it to the base blob path
                blob_path = "mirrored/" + self.dest_folder
        else:
            blob_path = None

        return blob_path

    def on_any_event(self, event):
        fn_src = event.src_path
        fn_dest = event.dest_path if hasattr(event, "dest_path") else None
        event_type = event.event_type    # 'modified' | 'created' | 'moved' | 'deleted'
        is_dir = event.is_directory

        # if self.show_calls:
        #     console.print("event: ", event)

        # process any FILE event and DIR delete/moved events
        if not is_dir or event_type in ["deleted", "moved"]:
            basename = os.path.basename(fn_src)
            
            if not self.wildcard or fnmatch(basename, self.wildcard):

                self.file_check_count += 1

                # NOTE: watch out for multiple notifications for single change
                process_event = True

                if os.path.exists(fn_src):
                    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fn_src)
                    process_event = (not fn_src in self.last_modified) or mtime != self.last_modified[fn_src]
                    self.last_modified[fn_src] = mtime
                    #console.print("last modified: %s" % time.ctime(mtime))

                if process_event:

                    # to make it simpler, can we check last modified time of file?
                    elapsed = time.time() - self.started

                    if self.mirror_dest == "grok":
                        if self.show_calls:
                            console.print("CHANGED: fn_src={}, et={}, is_dir={}, elapsed={:.2f}".format(fn_src, event_type, is_dir, elapsed))
                        # write file to grok server
                        self.send_file_to_grok(fn_src)

                    else:

                        # build blob paths carefully 
                        src_blob_path = self.build_blob_path(fn_src, event_type, is_dir)
                        dest_blob_path = self.build_blob_path(fn_dest, event_type, is_dir)

                        # if self.show_calls:
                        #     console.print("on_any_event AFTER: fn_src: {}, fn_dest: {}, src_blob_path: {}, dest_blob_path: {}, event_type: {}, is_dir: {}".format( \
                        #         fn_src, fn_dest, src_blob_path, dest_blob_path, event_type, is_dir))

                        if self.delay_queue:
                            # BUFFERING CHANGES; send the change to the bg worker via our queue
                            ready = time.time() + self.mirror_delay_mins*60

                            item = [ready, fn_src, fn_dest, src_blob_path, dest_blob_path, event_type, is_dir]
                            self.delay_queue.put(item)

                        else:
                            # handle event immediately
                            self.common_handler.process_file_event_now(fn_src, fn_dest, src_blob_path, dest_blob_path, event_type, is_dir, self.show_calls)
