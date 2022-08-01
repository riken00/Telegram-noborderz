import os
import random
import re
import subprocess
import sys
import time

from appium.webdriver.appium_service import AppiumService

from home.conf import ADB_SERVER_HOST, ADB_SERVER_PORT, ADB_CONSOLE_PORTS
from home.conf import APPIUM_SERVER_HOST, APPIUM_SERVER_PORT
from utils import kill_process_after_waiting, run_cmd_without_exit
from utils import run_cmd, get_listening_pid, get_commands_by_pattern

def get_appium_pids():
    appium_main_script = 'appium/build/lib/main.js'
    appium_cmd_pattern = f"'[n]ode.*bin/appium|[n]ode.*{appium_main_script}'"
    cmd = f'pgrep -f {appium_cmd_pattern}'

    result = run_cmd(cmd)
    if result:
        (returncode, output) = result
        if output:
            # output is the pid
            return tuple(e for e in output.strip().split('\n'))
    return tuple()


def get_listening_appium_pid(host=APPIUM_SERVER_HOST, port=APPIUM_SERVER_PORT):
    print(f'Get pid of appium listening on {host}:{port}')
    pid = get_listening_pid(host=host, port=port)
    pid = pid.strip()
    if pid:
        appium_pids = get_appium_pids()
        if pid in appium_pids:
            print(f'Found the pid of appium: {pid}')
            return pid
        else:
            print(f'Cannot found the pid of appium')
            return ''

    print(f'There is no appium listening on {host}:{port}')
    return ''


def start_appium(host=APPIUM_SERVER_HOST, port=APPIUM_SERVER_PORT,
                 restart=False, **kargs):
    if not restart:
        pid = get_listening_appium_pid(host=host, port=port)
        if pid:
            print(
                f'Appium(pid: {pid}) is listening on {host}:{port}')
            return pid
    else:
        print('Try to restart the appium server')

    if 'args' in kargs:
        args = kargs['args']
    else:
        args = []
    args += ['--address', host, '--port', str(port)]
    #  args += ['--address', host, '--port', str(port), '--session-override']
    kargs['args'] = args
    print(f'Arguments to start appium: {kargs}')

    service = AppiumService()
    process = service.start(**kargs)
    if service.is_running and service.is_listening:
        print(f'Appium server(pid: {process.pid}) is '
                     f'running and listening on {host}:{port}')
        return service
    else:
        print('Appium server is not running or listening')


def find_executable(executable: str):
    path = os.environ['PATH']
    paths = path.split(os.pathsep)
    base, ext = os.path.splitext(executable)
    if sys.platform == 'win32' and not ext:
        executable = executable + '.exe'

    if os.path.isfile(executable):
        return executable

    for p in paths:
        full_path = os.path.join(p, executable)
        if os.path.isfile(full_path):
            return full_path

    return None


def start_appium_without_exit(host=APPIUM_SERVER_HOST, port=APPIUM_SERVER_PORT,
                              restart=False, executable='appium'):
    if not restart:
        pid = get_listening_appium_pid(host=host, port=port)
        if pid:
            print(
                f'Appium(pid: {pid}) is listening on {host}:{port}')
            return pid
    else:
        print('Try to restart the appium server')

    appium_bin = find_executable(executable)
    if not appium_bin:
        print(f'Cannot found appium binary from "{executable}"')
        return None
    cmd = [appium_bin, '--address', host, '--port', str(port), '--log-level', 'error']
    #  cmd_shell = ' '.join(cmd)
    print(f'Command to start appium: {cmd}')

    process = run_cmd_without_exit(cmd)
    return process


def start_avd(cmd='emulator', **kwargs):
    args = []
    args.append(cmd)
    for key, value in kwargs.items():
        args.append(f'-{key}')
        args.append(str(value))

    print(f'AVD command: {" ".join(args)}')
    process = subprocess.Popen(args)
    return process


def stop_avd(process=None, name='', port='', verbose=True):
    if process:
        pid = process.pid
    else:
        pid = get_avd_pid(name=name, port=port)

    if not pid:
        print('Cannot find the pid of the avd')
        return
    #  kill_cmd = f"kill --signal TERM {pid}"
    kill_cmd = f"kill -s TERM {pid}"
    run_cmd(kill_cmd, verbose=verbose)
    kill_process_after_waiting(pid, success_code=1, verbose=verbose)
    time.sleep(random.randint(5, 10))


def get_avd_command(name='', port='', verbose=False):
    if not name and not port:
        print('Please sepcify name or port')
        return

    if name and port:
        pattern = fr"'emulator.*-avd\s+{name}.*(-port\s+{port})?'"
    elif name and not port:
        pattern = fr"'emulator.*-avd\s+{name}.*'"
    else:
        pattern = fr"'emulator.*-port\s+{port}'"
    result = get_commands_by_pattern(pattern=pattern, verbose=verbose)
    return result


def get_avd_pid(name='', port=''):
    result = get_avd_command(name, port)
    print(f'AVD command: {result}')
    if result:
        pattern = fr'(\d+)\s+.*emulator.*-avd\s+{name}.*(-port\s+{port})?'
        m = re.search(pattern, result[0])
        if m:
            return m.group(1)


def get_all_avd_commands(verbose=False):
    pattern = r"'emulator.*-avd\s+.*(-port\s+[0-9]+)?'"
    result = get_commands_by_pattern(pattern=pattern, verbose=verbose)
    return result


def get_running_adb_console_ports():
    pattern = r'emulator.*-avd\s+(\w+).*-port\s+([0-9]+)'
    ports = []
    commands = get_all_avd_commands()
    for cmd in commands:
        m = re.search(pattern, cmd)
        if m:
            print(f'Avd name: {m.group(1)}')
            print(f'ADB console port: {m.group(2)}')
            ports.append(m.group(2))
    return ports


def get_available_adb_console_ports():
    used_ports = get_running_adb_console_ports()
    all_ports = list(ADB_CONSOLE_PORTS)
    for p in used_ports:
        port = int(p)
        if port in all_ports:
            all_ports.remove(port)

    print(f'Number of available adb console ports: {len(all_ports)}')
    return all_ports


def get_one_available_adb_console_port():
    available_ports = get_available_adb_console_ports()
    if available_ports:
        return random.choice(available_ports)
    print('Cannot get one available adb console port')


def get_listening_adb_pid(host=ADB_SERVER_HOST, port=ADB_SERVER_PORT):
    print(f'Get pid ADB adb listening on {host}:{port}')
    pid = get_listening_pid(host=host, port=port)
    pid = pid.strip()
    if pid:
        appium_pids = get_adb_pids()
        if pid in appium_pids:
            print(f'Found the pid of ADB: {pid}')
            return pid
        else:
            print(f'Cannot found the pid of ADB')
            return ''

    print(f'There is no ADB listening on {host}:{port}')
    return ''


def get_adb_pids(port=ADB_SERVER_PORT):
    cmd_pattern = f"'adb -L tcp:{ADB_SERVER_PORT} fork-server server'"
    cmd = f'pgrep -f {cmd_pattern}'

    result = run_cmd(cmd)
    if result:
        (returncode, output) = result
        if output:
            # output is the pid
            return tuple(e for e in output.strip().split('\n'))
    return tuple()


def get_serial_number_of_device(port):
    return f'emulator-{port}'


def get_one_available_appium_port(availables):
    while True:
        appium_port = availables[0]
        if get_listening_pid(APPIUM_SERVER_HOST, appium_port):
            availables.remove(appium_port)
            continue
        print(f'Appium server port: {appium_port}')
        availables.remove(appium_port)
        return appium_port


def get_one_available_system_port(adb_console_port):
    port = adb_console_port + 2646
    print(f'System port: {port}')
    return port
