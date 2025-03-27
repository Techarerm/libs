import os
import sys
import threading
from datetime import datetime

import keyboard

from clientlauncher.platform.universal import universal
from lib import LIB_VERSION

logs = ""

class clientInstance(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        threading.Thread(universal.launch_client("ping 8.8.8.8 -t"))

clientInstance = clientInstance()


class clientLauncher:
    def __init__(self):
        self.thread = None
        self.logs = ""

    @staticmethod
    def init(client_name, command,  info=True, custom_payload=None):
        process_id = os.getpid()
        _locals = locals()
        print("clientLauncher")
        print(f"Process ID {process_id}")
        if info:
            print(f"Version Lib-{LIB_VERSION}")
            print(f"Start date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print("")

        if custom_payload is not None:
            print(custom_payload)

        globals()[client_name] = clientInstance
        return

    @staticmethod
    def start():
        clientInstance.start()

    def start_streaming_output(self, client_name):
        for line in client_name.stdout:
            sys.stdout.write("{line}".format(line=line))
            sys.stdout.flush()
            self.logs += f"{line}\n"
            if keyboard.is_pressed("c"):
                print("Stop streaming output...")
                return

        client_name.stdout.close()
        client_name.wait()

    def kill_client_process(self, client_name):
        try:
            client_name.kill()
        except Exception as e:
            print("An exception occurred: {}".format(e))

    def save_streaming_output(self, output_file_path):
        with open(output_file_path, 'w') as output_file:
            output_file.write(self.logs)

clientLauncher = clientLauncher()
clientLauncher.init("a")
clientLauncher.start()
print("d")