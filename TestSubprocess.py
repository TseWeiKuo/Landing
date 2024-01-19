import pypylon.pylon as py
import numpy as np
import time
from matplotlib import pyplot as plt
from imageio import get_writer
from subprocess import Popen
import os
import concurrent.futures
import datetime
import scipy
import threading
import nidaqmx.system
from nidaqmx.constants import (AcquisitionType, CountDirection, Edge, READ_ALL_AVAILABLE, TaskMode,
                               TriggerType, WAIT_INFINITELY, TerminalConfiguration)

print("Subprocess Start")
time.sleep(3)