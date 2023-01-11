import os
os.environ["Z_LEVEL"] = "warn"
import wcap
import numpy
import win32gui

def get_hwnd(title_prefix):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title.startswith(title_prefix):
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    if hwnds:
        return hwnds[0]
    else:
        raise ValueError(f"No window with title prefix '{title_prefix}' was found.")

  
def get_potplayer_handle():
  hwnd = get_hwnd("Mr.")
  title = win32gui.GetWindowText(hwnd)
  print(f"hwnd: {hwnd}, {title}")
  return hwnd
  

def test_audio():
  import win32gui
  import time
  # cur_handle = win32gui.GetForegroundWindow()
  cur_handle = get_potplayer_handle()
  print("before init_audio")
  Audio = wcap.WCAP(cur_handle, wcap.WAVE_FORMAT.WAVE_FORMAT_IEEE_FLOAT)
  print("after init_audio")
  # time.sleep(2)
  while True:
    # print("before get_audio")
    # arr = wrap.get_audio(cur_handle)
    arr = Audio.get_audio()
    # print(arr)
    print(arr[10], arr[11])
    # for v in arr:
    #   assert -3 < v < 3
    # print(arr.size)
    assert arr.size==160
    # print("after get_audio")
  time.sleep(5)

if __name__ == "__main__":
  test_audio()