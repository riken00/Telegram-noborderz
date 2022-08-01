
import subprocess



def run_cmd(cmd, verbose=True):
    """Run shell commands, and return the results

    ``cmd`` should be a string like typing it in shell.
    """
    try:
        if verbose:
            print(f'Command: {cmd}')

        r = subprocess.run(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, shell=True, text=True)
        print(r)
        if verbose:
            if r.returncode == 0:
                print(f'Successful to run the command: {cmd}')
                print(f'Result of the command: {r.stdout}')
            else:
                print(f'Failed to run the command: {cmd}')
                print(f'Result of the command: {r.stdout}')

        return r.returncode, r.stdout
    except Exception as e:
        print(e) 


import threading

import time

file_path = "/media/eu4/49fa581d-6d91-4c0f-886a-2d6d1a2b9857/project/Automation/telegram_avds/office-work/env/bin/python3.8 /media/eu4/49fa581d-6d91-4c0f-886a-2d6d1a2b9857/project/Automation/telegram_avds/office-work/manage.py "

def runserver():
    run_cmd(f'{file_path}runserver')
    ...

def runbot():
    run_cmd(f'{file_path}bot')
    ...

def script():
    print('----11')
    threading.Thread(target=runserver).start()
    threading.Thread(target=runbot).start()
    print('----22')

script()
