# -*- coding: utf-8 -*-

###################################
# Netool
#
# tcp/udp tool
#
# main
#
# raidercodebear@gmail.com
#
# 20150108 xc v0.01
###################################

from netool_gui import NetoolMainFrame
import wx

import threading
from multiprocessing import Process, freeze_support

import json

from netool_common import DBG, DBG_TRACE

FRAME = None
APP = None


def start_command_server():
    DBG("start_command_server")
    from netool_conn import NetoolCommandServer
    try:
        NetoolCommandServer(':62223').serve_forever()
    except:
        DBG_TRACE()


def start_feeder():
    DBG("start_feeder")
    from netool_conn import NetoolGUIFeeder
    # DBG("start_feeder %d" % threading._get_ident())
    try:
        NetoolGUIFeeder(FRAME, ":62222").serve_forever()
    except:
        DBG_TRACE()

if __name__ == '__main__':
    command_process = None
    feeder = None
    try:
        DBG("~~~~~~~~~~~~~~~~ netool main ~~~~~~~~~~~~~~~")
        freeze_support()
        command_process = Process(target = start_command_server)
        command_process.start()

        APP = wx.App()
        FRAME = NetoolMainFrame()

        feeder = threading.Thread(target = start_feeder)
        feeder.start()

        FRAME.load_status()
        FRAME.Show()

        APP.MainLoop()
        DBG("~~~~~~~~~~~~~~~~~~ die 1 ~~~~~~~~~~~~~~~~~~~")

        command_process.join()
        feeder.join()

        DBG("~~~~~~~~~~~~~~~~~~ die 2 ~~~~~~~~~~~~~~~~~~~")
    except:
        if command_process:
            command_process.join()
        if feeder:
            feeder.join()
        DBG_TRACE()