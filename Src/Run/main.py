# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

import sys
sys.path.append("Src")

import time
from threading import Thread

from Log import LogManager
from Web import WebManager
from Forward.ForwardManager import ForwardHttp
from Manager.ProxyFetch import ProxyFetch

from Schedule.ProxyVerifySchedule import ProxyVerifySchedule
from Schedule.ProxyFetchSchedule import ProxyFetchSchedule
from Schedule.ProxyCleanSchedule import ProxyCleanSchedule

TASK_LIST = {
    "ProxyVerifySchedule": ProxyVerifySchedule,
    "ProxyFetchSchedule": ProxyFetchSchedule,
    "ProxyCleanSchedule": ProxyCleanSchedule,
    "ForwardHttp": ForwardHttp,
}

def show_time():
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    content = "{newline}{symbol} ProxyPool Start, date:{date} {symbol}{newline}".format(newline="\n", symbol="-"*50, date=date)
    print(content)

def start_fetch():
    ProxyFetch.initQueue()
    t = ProxyFetch()
    t.start()

def start_task():
    start_fetch()

    task_list = []
    for name in TASK_LIST.keys():
        task = TASK_LIST[name]()
        t = Thread(target=task.run, name=name)
        task_list.append(t)

    for t in task_list:
        t.daemon = True
        t.start()

def main(test=False):
    show_time()

    LogManager.init()

    start_task()

    WebManager.run()

if __name__ == '__main__':
    main()