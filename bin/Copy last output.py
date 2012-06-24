 #!/usr/bin/python
 2  
 3  from appscript import *
 4  from osax import OSAX
 5  
 6  sa = OSAX()
 7  win = app('/Applications/Utilities/Terminal').windows[1]
 8  title = win.name.get().lower()
 9  
10  if title.find("bash") > -1:
11    inout = win.selected_tab.history.get().split('\n$ ')[-2]
12    sa.set_the_clipboard_to('\n'.join(inout.split('\n')[1:-1]))
13  elif title.find("python") > -1 or title.find("matlab") > -1:
14    inout = win.selected_tab.history.get().split('\n>>> ')[-2]
15    sa.set_the_clipboard_to('\n'.join(inout.split('\n... ')[-1].split('\n')[1:]))