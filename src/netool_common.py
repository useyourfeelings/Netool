# -*- coding: utf-8 -*-

###################################
# Netool
#
# tcp/udp tool
#
# common
###################################

import logging
logging.basicConfig(level=logging.DEBUG)
DBG = logging.debug

import sys


def print_exc_info():
    DBG(type(sys.exc_info()[1]))
    DBG(sys.exc_info()[1])

DBG_TRACE = print_exc_info