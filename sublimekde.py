
import os
import sublime
import sublime_plugin
import subprocess
import threading


class OpenWithKdeCommand(sublime_plugin.WindowCommand):
    def run(self):
        cwd = os.getcwd()
        view = self.window.active_view()
        if view:
            fn = view.file_name()
            if fn:
                cwd = os.path.dirname(fn)

        process = subprocess.Popen(['kdialog', '--getopenfilename', cwd],
                                   stdout=subprocess.PIPE)
        t = DialogThread(process, self.on_open)
        t.start()

    def on_open(self, file_name):
        self.window.open_file(file_name)


class DialogThread(threading.Thread):
    def __init__(self, process, callback):
        self.process = process
        self.callback = callback
        super(DialogThread, self).__init__()

    def run(self):
        stdout_data, stderr_data = self.process.communicate()
        if not self.process.returncode:

            def run_callback():
                self.callback(stdout_data.strip().decode('utf-8'))

            sublime.set_timeout(run_callback, 0)
