#-*- coding: UTF-8 -*-

from cpc import taskd
from cpc import task
from cpc.VClient import *
import ttwm
import config


taskd.run(task.Task, config, ttwm.TTWM)
