
from http import server
import os
import sys
import subprocess
import time
import traceback
import threading

try:
  import wx
except:
  traceback.print_exc()
  subprocess.run([
    sys.executable, *('-m pip install --user wxPython'.split())
  ])
  import wx
import wx.adv


import net_work

def maybe(callback):
  try:
    return callback()
  except:
    return traceback.format_exc()

def first_existing_file(*files):
  for f in files:
    if os.path.exists(f):
      return f
  return None

app = None
frame = None
server_t = None
server_t_exit_flag = False
server_work_req_folder = ""
server_work_return_folder = ""

class TaskBarGuiIcon(wx.adv.TaskBarIcon):
  
  def __init__(self, parent_frame):
    wx.adv.TaskBarIcon.__init__(self)

    self.parent_frame = parent_frame

    icon_file = first_existing_file(
      r'S:\Users\jmcateer\ToolResources\net_work_tray_icon.ico',
      r'C:\Temp\net_work_tray_icon.ico',
      '/tmp/net_work_tray_icon.ico',
    )
    if icon_file is not None:
      self.SetIcon(wx.Icon(icon_file, wx.BITMAP_TYPE_ICO))
    

  
  def CreatePopupMenu(self):
    global server_t_exit_flag, server_work_req_folder, server_work_return_folder
    m = wx.Menu()

    m.Append(wx.ID_NEW, "net-work server running", "net-work server running")
    m.AppendSeparator()

    m.Append(wx.ID_NEW, "Working tasks sent to {}".format(server_work_req_folder), "Working tasks sent to {}".format(server_work_req_folder))
    m.Append(wx.ID_NEW, "Returning tasks to {}".format(server_work_return_folder), "Returning tasks to {}".format(server_work_return_folder))
    m.AppendSeparator()

    m.Append(wx.ID_ANY, "Quit net-work server", "Quit net-work server")

    def on_quit_clicked(event):
      global server_t_exit_flag, frame

      # print('Exiting... (event={}, id={})'.format(event, event.GetId() ))
      
      try:
        if event.GetId() == wx.ID_NEW:
          return # Not an exit event
      except:
        traceback.print_exc()
      
      try:
        server_t_exit_flag = True
        time.sleep(3)
      except:
        traceback.print_exc()
      try:
        frame.onClose(event)
      except:
        traceback.print_exc()
      # sys.exit(0)

    self.Bind(wx.EVT_MENU, on_quit_clicked)

    return m

class DummyGuiFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, wx.ID_ANY, "", size=(1,1))
    panel = wx.Panel(self)
    self.tray_icon = TaskBarGuiIcon(self)
    self.Bind(wx.EVT_CLOSE, self.onClose)
  
  def onClose(self, evt):
    global server_t_exit_flag
    server_t_exit_flag = True
    self.tray_icon.RemoveIcon()
    self.tray_icon.Destroy()
    self.Destroy()


class ServerGuiApp(wx.App):
  def OnInit(self):
    global frame
    frame = DummyGuiFrame()
    self.SetTopWindow(frame)
    #frame.Center(wx.BOTH)
    #frame.Show(False)
    return True

def run_gui_server(args: list):
  global app, server_t

  app = ServerGuiApp(0)

  server_t = threading.Thread(target=run_server, args=(args, ))
  server_t.start()

  time.sleep(0.75) # Wait for run_server to possibly die b/c of bad arguments, if it does we also die.
  if not server_t.is_alive():
    return
  
  print('App constructed, running GUI loop...')
  app.MainLoop()

def run_server(args: list):
  global server_t_exit_flag, server_work_req_folder, server_work_return_folder
  # remove args until we hit the first one beginning with '-'
  while len(args) > 0 and not args[0].startswith('-'):
    args.pop(0)
  # Now turn args (which we assume to be like ['-req', '/path/to/a/dir', '-return', '/path/to/another/dir',])
  # into a dictionary
  args_d = {}
  for arg_flag, arg_value in zip(args[0::2], args[1::2]):
    arg_flag = arg_flag.replace('-', '') # --req and -req both turn into "req" in our argument dictionary.
    args_d[arg_flag] = arg_value

  work_req_dir = args_d['req']
  work_return_dir = work_req_dir
  if 'return' in args_d:
    work_return_dir = args_d['return']

  # TODO parse all other arguments

  # Save globals in case GUI is running
  server_work_req_folder = work_req_dir
  server_work_return_folder = work_return_dir

  nw = net_work.NetWork(work_req_dir, work_return_dir)
  # Poll for incoming work, run, return, etc.
  files_we_must_delete = []
  while not server_t_exit_flag:
    if len(files_we_must_delete) > 0:
      try:
        for file_name in files_we_must_delete:
          net_work.NetWork.safe_del(file_name)
        files_we_must_delete = [] # clear list
      except:
        traceback.print_exc()
    
    try:
      work_d = nw.poll_any_work_req_dicts(should_continue_polling_fn=lambda: not server_t_exit_flag)
      if work_d is None:
        continue # should_continue_polling_fn said to exit
      
      files_we_must_delete.append(
        nw.work_req_file(work_d['job_id']),
      )
      files_we_must_delete.append(
        nw.work_lock_file(work_d['job_id']),
      )

      if 'cmd' in work_d:
        cmd_args = work_d['cmd']
        proc = subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        nw.write_work_return_file(work_d['job_id'], {
          'returncode': proc.returncode,
          'stdout': maybe(lambda: proc.stdout.decode()),
          'stderr': maybe(lambda: proc.stderr.decode()),
        })
        
      else:
        raise Exception(f'Unknown work dictionary={work_d}')
    except:
      traceback.print_exc()
      time.sleep(1)
  print('Server thread exiting...')





