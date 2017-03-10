from engine import Engine
from workspace_time import WorkspaceTime
from tk_time import TkTime
from time import sleep

e = Engine(0.5)
wt = WorkspaceTime()
e.append_container(wt)
e.start()

tk = TkTime()
tk.setup()

while not tk.stop:
	sleep(1)
	#print wt.get_display_text()
	tk.update(wt.get_display_text())

wt.save_to_file()
tk.destroy()
e.stop()
