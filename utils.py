import logging
import os
import random
import re
import subprocess
import time
import uuid
from datetime import datetime
from pathlib import Path

import requests
from PIL import Image

from home.conf import PRJ_PATH, LOG_DIR, LOG_LEVEL
from log import Log


COMMENT_LI = [

 " You are so impressive!"
," You inspire me!"
," I'm so proud of you!"
," My strong, confident and powerful!"
," Wow, you are the best at driving!"
," You cook like no other!"
," With you I feel like a real lady!"
," Perfect click.. It's superbb..."
," Stunning look with a perfect smile."
," It took my breath away!"
," Really a feast for the eyes!"
," It must be my extreme good luck to"
," I was just staring at the picture"
," You're an awesome friend."
," You're a gift to those around you."
," You're a smart cookie."
," I like your style."
," You have the best laugh."
," I appreciate you."
," You are enough."
," You're strong."
," I'm grateful to know you."
," You light up the room."
," You are strong."
," I'm inspired by you."
,"Hehe. cute monkey."
,"You are the strongest of all!"
,"You are so understanding…"
,"You are my perfect man!"
,"You're all that and a super-size bag of chips."
,"Your kindness is a balm to all who encounter it."
,"Your perspective is refreshing."
,"You are the most perfect you there is."
,"You've got an awesome sense of humor!"
," You're like a ray of sunshine on a really dreary day."
," You have impeccable manners."
," The most stunning thing I've seen today."
," You're more helpful than you realize."
,"That brow game, though."
,"What magazine cover are you posing for today?"
,"Please do my makeup next friend hang."
,"Without makeup, you're gorgeous. With makeup, you're gorgeous. In conclusion, I have a gorgeous bestie no matter what."
,"This look deserves an applause [hand clap emojis]."
,"My bestie is an artist!"
,"Someone hang this selfie up in a museum, because my bestie's makeup lewk is a work of art."
,"If you put out your own makeup line, I'd buy the heck out of it."
,"Some people serve up looks, but you serve up LEWKS."
,"How is it that every color looks amazing on you?"
,"Just so everyone knows, this makeup lewk is even better IRL."
 ,"You are the coolest."
 ,"This outfit deserves applause (Clap emojis)."
 ,"Blessing my Insta feed once again."
 ,"The hottest pal in the town."
 ,"They say love is beautiful, but I say friendship is better."
 ,"Meet my fellow partner in crime."
 ,"You are the only Betty to my Veronica."
 ,"I don’t see any competition here for your gorgeous looks."
 ,"You and strong Wi-Fi are what I only need in my life."
 ,"I am so fortunate that you get to call me your best friend."
 ,"Watch out, world."
 ,"One word for this picture, stunning."
 ,"Besides chocolate, you are my favourite thing."
 ,"Victoria’s Secret Models, my friend is coming for your careers."
 ,"Impressive, I have never seen a nice photo of yours like this."
 ,"Keep shining, pal."
 ,"Very gorgeous; I am falling in love with this snap of you."
 ,"You look gorgeous."
 ,"Wow, you are looking beautiful, pal."
 ,"Your charm is genuinely irresistible."
 ,"Damn, that smile is so dangerous."
 ,"This is the best picture I have come across today."
 ,"Your smile is wow."
 ,"You have a fantastic body figure."
 ,"Beautiful as always."
 ,"Dashing look."
 ,"Hey, you are breaking the internet"
]

_log_name = Path(__file__).stem if __name__ == '__main__' else __name__
if not LOG_DIR:
    _log_file = PRJ_PATH / (Path(__file__).stem + '.log')
else:
    _log_file = PRJ_PATH / LOG_DIR / (Path(__file__).stem + '.log')
LOGGER = Log(log_name=_log_name, log_level=LOG_LEVEL,
             log_file=_log_file).logger


def random_sleep(min_sleep_time=1, max_sleep_time=5):
    sleep_time = random.randint(min_sleep_time, max_sleep_time)
    LOGGER.debug(f'Random sleep: {sleep_time}')
    time.sleep(sleep_time)
    
def log_activity(avd_id, action_type, msg, error):
    try:
        details = {
            "avd_id": avd_id,
            "action_type": action_type,
            "action": msg,
            "error": error,
        }
        LOGGER.debug(f'Log Activity: {details}')
        # TwitterActionLog.objects.create(**details)
    except Exception as e:
        print(e)


def get_datetime_str(fmtstr='%Y%m%d-%H%M%S'):
    """Get string of the current time.

    e.g.::

        format: %Y%m%d-%H%M%S
        time example: 20210701-150101
    """

    return datetime.now().strftime(fmtstr)


def get_datetime_date_str(fmtstr='%Y%m%d'):
    return get_datetime_str(fmtstr)


def set_log(prj_path, file_obj, name_obj, log_level=logging.DEBUG,
            log_dir='', log_suffix='.log'):
    _log_name = Path(file_obj).stem if name_obj == '__main__' else name_obj
    if not log_dir:
        _log_file = prj_path / (Path(file_obj).stem + log_suffix)
    else:
        _log_file = prj_path / log_dir / (Path(file_obj).stem + log_suffix)
    logger = Log(log_name=_log_name, log_level=log_level,
                 log_file=_log_file).logger

    return logger


def check_text_present_page_source(driver, text, logger):
    if re.findall(text, driver.page_source, flags=re.IGNORECASE):
        logger.debug(f'Find the text in page source: "{text}"')
        return True
    else:
        logger.debug(f'Cannot find the text in page source: "{text}"')
        return False


def get_random_file_name(min_len=10, max_len=20, suffix=''):
    return ''.join(random.choices(uuid.uuid4().hex,
                                  k=random.randrange(min_len, max_len))) + suffix


def _add_suffix_name(fname, suffix='_small', repeate=False):
    fnames = fname.split('.')
    if len(fnames) == 1:
        if not repeate:
            return fname if fname.endswith(suffix) else (fname + suffix)
        else:
            return fname + suffix

    else:
        if not repeate:
            names = '.'.join(fnames[:-1])
            return fname if names.endswith(suffix) else (
                    names + suffix + '.' + fnames[-1])
        else:
            return '.'.join(fnames[:-1]) + suffix + '.' + fnames[-1]


def resize_img(img_file, reduce_factor=1):
    # reduce the image's size
    img = Image.open(img_file)
    #  LOGGER.debug(f'Original image size: {img.size}')
    #  LOGGER.debug(f'Original file size: {os.path.getsize(img_file)}')
    #  LOGGER.debug(f'Resize factor: {reduce_factor}')

    width = int(img.size[0] / reduce_factor)
    height = int(img.size[1] / reduce_factor)

    if isinstance(img_file, Path):
        img_file_path = str(img_file.absolute())
    else:
        img_file_path = img_file

    small_img_file = _add_suffix_name(img_file_path)

    small_img = img.resize((width, height))
    #  small_img = img.resize(reduce_factor)
    small_img.save(small_img_file)
    #  LOGGER.debug(f'Resized image size: {small_img.size}')
    #  LOGGER.debug(f'Resized file size: {os.path.getsize(small_img_file)}')

    return small_img_file


def restrict_image_size(img_file, reduce_factor, reduce_step, restrict_size):
    """Reduce the image file size to let it be less than restricting size"""
    img_file_size = os.path.getsize(img_file)

    if img_file_size <= restrict_size:
        reduced_img_file = img_file

    times = 0
    while img_file_size > restrict_size:
        reduce_factor += reduce_step
        reduced_img_file = resize_img(img_file, reduce_factor)
        img_file_size = os.path.getsize(reduced_img_file)
        times += 1

    LOGGER.debug(f'Reduced image file: {reduced_img_file}')
    LOGGER.debug(f'After {times} times of reducing, the image file size'
                 f' {img_file_size} is less than {restrict_size}')
    return (reduced_img_file, reduce_factor)


def reduce_img_size(img_file, reduce_factor=1):
    # reduce the image's size
    img = Image.open(img_file)
    LOGGER.info(f'Original image size: {img.size}')
    LOGGER.info(f'Original file size: {os.path.getsize(img_file)}')
    LOGGER.info(f'Reduce factor: {reduce_factor}')

    #  width = int(img.size[0] // reduce_factor)
    #  height = int(img.size[1] // reduce_factor)

    if isinstance(img_file, Path):
        img_file_path = str(img_file.absolute())
    else:
        img_file_path = img_file

    small_img_file = _add_suffix_name(img_file_path)

    #  small_img = img.resize((width, height), Image.ANTIALIAS)
    small_img = img.reduce(reduce_factor)
    small_img.save(small_img_file)
    LOGGER.info(f'Reduced image size: {small_img.size}')
    LOGGER.info(f'Reduced file size: {os.path.getsize(small_img_file)}')

    return small_img_file


def get_absolute_path_str(path):
    if isinstance(path, Path):
        absolute_path = str(path.absolute())
    elif isinstance(path, str):
        absolute_path = os.path.abspath(path)
    else:
        LOGGER.debug(f'Other type of path: {type(path)}')
        absolute_path = path

    #  LOGGER.debug(f'Absolute path: "{absolute_path}" from "{path}"')
    return absolute_path


def get_random_records(records, model, max_records=10):
    ids = [e.id for e in records]
    all_number = len(ids)
    max_select_number = min(max_records, all_number)
    select_number = random.randint(1, max_select_number)
    random_ids = random.choices(ids, k=select_number)
    return model.objects.filter(id__in=random_ids)



def run_cmd(cmd, verbose=True):
    """Run shell commands, and return the results

    ``cmd`` should be a string like typing it in shell.
    """
    try:
        if verbose:
            LOGGER.debug(f'Command: {cmd}')

        r = subprocess.run(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, shell=True, text=True)
        
        if verbose:
            if r.returncode == 0:
                LOGGER.debug(f'Successful to run the command: {cmd}')
                LOGGER.debug(f'Result of the command: {r.stdout}')
            else:
                LOGGER.warning(f'Failed to run the command: {cmd}')
                LOGGER.debug(f'Result of the command: {r.stdout}')

        return r.returncode, r.stdout
    except Exception as e:
        LOGGER.error(e)


def run_cmd_without_exit(cmd, verbose=True, shell=False):
    """Run shell commands, and return the results

    ``cmd`` should be a string like typing it in shell.
    """
    try:
        if verbose:
            LOGGER.debug(f'Command: {cmd}')

        process = subprocess.Popen(cmd, shell=shell)
        return process
    except Exception as e:
        LOGGER.error(e)


def run_cmd_loop(cmd, success_code=0, retry_times=3, sleep_time=2,
                 verbose=True):
    """Run the command until beyond the retry times or successfully"""
    times = 0
    while times <= retry_times:
        result = run_cmd(cmd, verbose=verbose)
        if result:
            (status, output) = result
        else:
            times += 1
            if sleep_time > 0:
                time.sleep(sleep_time)
            LOGGER.debug(f'Retry to run the command: {cmd}')
            continue

        if status == success_code:
            return True
        else:
            times += 1
            if sleep_time > 0:
                time.sleep(sleep_time)
            LOGGER.debug(f'Retry to run the command: {cmd}')
            continue

    return False


def kill_process_after_waiting(pid, success_code=0, retry_times=3,
                               sleep_time=2, verbose=True):
    """Using process ID to kill a process"""
    # if the process exits normally, then kill it forcely
    search_pid_cmd = f'ps --pid {pid}'
    if not run_cmd_loop(search_pid_cmd, success_code=success_code,
                        verbose=verbose):
        kill_cmd = f'kill -9 {pid}'
        LOGGER.debug(f'Kill the process forcely: {pid}')
        run_cmd(kill_cmd, verbose=verbose)


def pkill_process_after_waiting(pname, success_code=0, retry_times=3,
                                sleep_time=2, verbose=True):
    """Using process name to kill a process"""
    # if the process exits normally, then kill it forcely
    search_pid_cmd = f'pgrep {pname}'
    if not run_cmd_loop(search_pid_cmd, success_code=success_code,
                        verbose=verbose):
        kill_cmd = f'pkill -9 {pname}'
        LOGGER.debug(f'Kill the process forcely: {pname}')
        run_cmd(kill_cmd, verbose=verbose)


def get_listening_pid(host, port):
    cmd = f'lsof -i tcp@{host}:{port} -sTCP:LISTEN -t'
    result = run_cmd(cmd)
    if result:
        (returncode, output) = result
        if output:
            # output is the pid
            return output
    return ''


def get_commands_by_pattern(pattern, verbose=False):
    #  cmd = f'pgrep -f {pattern}'
    cmd = f'pgrep -a -f {pattern}'
    result = run_cmd(cmd)

    if verbose:
        LOGGER.debug(f'Result: {result}')

    if result:
        (returncode, output) = result
        if output:
            # output is the pid
            return tuple(e for e in output.strip().split('\n'))
    return tuple()


def get_installed_packages():
    cmd = 'sdkmanager --list_installed'
    result = run_cmd(cmd, False)
    if result:
        (returncode, output) = result
        if output:
            return output
    return ''
