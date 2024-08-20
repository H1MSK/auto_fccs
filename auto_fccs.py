from multiprocessing.managers import DictProxy
from typing import Any
import pyautogui
import pydirectinput
import keyboard
import numpy as np
import logging
import multiprocessing
import time

logging.root.setLevel(logging.INFO)

pos = (1441, 303)
color = np.asarray((98, 129, 104))

def screenshot(region=None):
  return np.asarray(pyautogui.screenshot(region=region))

def get_color(pos):
  img = screenshot((pos[0], pos[1], 1, 1))
  return img[0, 0, :]

def calib_pos_cb():
  global pos
  pos = pyautogui.position()
  logging.info(f"Pos updated to {pos}")
  # img = screenshot()
  # colors = np.array(((0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)))
  # for x in range(pos[0] - 4, pos[0] + 5):
  #   for y in range(pos[1] - 4, pos[1] + 5):
  #     if x == 0 and y == 0:
  #       continue
  #     img[y, x] = colors[(abs(x - pos[0]) + abs(y - pos[1])) // 2]
  # cv2.imwrite("calib.png", img)
  
def calib_color_cb():
  global color, pos
  color = get_color(pos)
  logging.info(f"color calib to {color}")
  
def quit_cb():
  logging.info(f"quit")
  quit(0)
  
def runner(share_dict: DictProxy):
  pos = share_dict['pos']
  color: np.ndarray = share_dict['color']
  logging.info(f"Wait till pos {pos} has color {color}...")
  pydirectinput.FAILSAFE = False
  while ((this_color:=get_color(pos)) - color).sum() > 10:
    logging.info(f"Current color: {this_color}")
    pass
  while not share_dict['stop']:
    pos = share_dict['pos']
    color: np.ndarray = share_dict['color']
    c: np.ndarray = get_color(pos)
    diff = np.abs(color.astype(np.int32) - c.astype(np.int32)).sum()
    logging.info(f"color = {c}, diff = {diff}, {'click' if diff > 30 else 'wait'}")
    if diff > 30:
      pydirectinput.press(' ', interval = 0.02)
      time.sleep(0.1)
    
mans = []
share_dict: DictProxy = None
procs = []
  
def run_cb():
  global color, pos, procs
  global share_dict
  if len(mans) == 0:
    m = multiprocessing.Manager()
    mans.append(m)
    share_dict = m.dict()
    share_dict['color'] = color
    share_dict['pos'] = pos
    share_dict['stop'] = True
    

  if len(procs):
    logging.info(f"stop")
    assert share_dict['stop'] == False
    share_dict['stop'] = True
    procs[0].join()
    procs.pop()
  else:
    logging.info(f"start")
    assert share_dict['stop'] == True
    share_dict['color'] = color
    share_dict['pos'] = pos
    share_dict['stop'] = False
    p = multiprocessing.Process(target=runner, args=(share_dict, ))
    p.start()
    procs.append(p)
  
def main():
  logging.info("Started.")
  keyboard.add_hotkey("ctrl+shift+alt+w", calib_pos_cb)
  keyboard.add_hotkey("ctrl+shift+alt+e", calib_color_cb)
  keyboard.add_hotkey("ctrl+shift+alt+s", run_cb)
  keyboard.wait("ctrl+shift+alt+q")
  
if __name__ == '__main__':
  main()
