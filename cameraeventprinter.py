# Contains a Camera Event Handler that prints a message for each event method call.
import numpy as np
import random
import subprocess
from subprocess import Popen
import json
import time
import sys

nums = random.sample(range(0, 29), 15)

Send_signal_process = Popen(['python', 'DeblurImages.py', json.dumps(nums)], stdin=subprocess.PIPE, text=True)

time.sleep(3)