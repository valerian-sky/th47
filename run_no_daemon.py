#-*- coding: UTF-8 -*-

from cpc import task
import config
import ttwm


task = task.Task(config, ttwm.TTWM)
task.run()
