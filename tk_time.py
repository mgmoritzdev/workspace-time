from Tkinter import Tk, Label
from datetime import timedelta


class TkTime:
    def setup(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.time_label = Label(self.root, text=self.get_empty_workspace_time)
        self.stop = False
        self.root.update()
        # self.root.mainloop()

    def get_empty_workspace_time(self):
        empty_timedelta = str(timedelta(0))
        return ('\n' + empty_timedelta + '  |  '
                + empty_timedelta + '\n' + empty_timedelta + '  |  '
                + empty_timedelta)

    def update(self, text):
        self.time_label['text'] = text
        self.time_label.pack()
        self.root.update()

    def on_closing(self):
        self.stop = True

    def destroy(self):
        self.root.destroy()
