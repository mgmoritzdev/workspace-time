from subprocess import Popen, PIPE
from datetime import datetime, timedelta


def get_output(x):
    return Popen(x, stdout=PIPE).communicate()[0]


class WorkspaceTime:
    """Store the time spent in each workspace"""

    def __init__(self):
        """Assume 4 workspaces, assume compiz"""
        self.last_update_time = None
        self.current_viewport = 0
        self.times = [timedelta(0), timedelta(0), timedelta(0), timedelta(0)]
        self.workspace_active = True

        self.x = 0
        self.y = 0
        self.height = 0
        self.width = 0

    def setup(self):
        """Initialize the size of workspace"""
        self.update_screen_geometry()
        self.update_current_viewport()

    def update(self):
        """Compute and store the times with each workspace"""

        self.update_workspace_state()

        if not self.workspace_active:
            self.last_update_time = datetime.now()
            return

        self.update_current_viewport()

        if self.last_update_time is None:
            self.last_update_time = datetime.now()
        else:
            right_now = datetime.now()
            delta = right_now - self.last_update_time
            self.times[self.current_viewport] += delta
            self.last_update_time = datetime.now()

    def get_display_text(self):
        txt = ('\n' + self.get_pretty_time(0) + '  |  '
               + self.get_pretty_time(1)
               + '\n' + self.get_pretty_time(2) + '  |  '
               + self.get_pretty_time(3)
               + '\n')
        return txt

    def get_pretty_time(self, workspace):
        return str(self.times[workspace]).split(".")[0]

    def update_screen_geometry(self):
        """Get the screen geometry in pixels"""

        geometry = get_output(('xwininfo', '-root', '-stats'))
        geometry = geometry.split('geometry')[1]
        geometry = geometry.split('+')[0]

        size_string = geometry.split('x')
        self.width = int(size_string[0])
        self.height = int(size_string[1])

    def update_current_position(self):
        """Get the workspace offset in pixels"""

        viewport = get_output(('xprop',
                               '-root',
                               '-notype',
                               '_NET_DESKTOP_VIEWPORT'))
        viewport = viewport[24:]
        size_string = viewport.split(',')
        self.x = int(size_string[0])
        self.y = int(size_string[1])

    def update_current_viewport(self):
        self.update_current_position()
        self.current_viewport = (self.x / self.width + 2 *
                                 (self.y / self.height))

    def update_workspace_state(self):
        state_text = get_output(('gnome-screensaver-command', '-q'))
        self.workspace_active = 'inactive' in state_text

    def save_to_file(self):
        text = self.get_display_text()

        f = open('history', 'a')
        f.write(text)
        f.close()
