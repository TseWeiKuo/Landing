import nidaqmx.system
from nidaqmx.constants import (AcquisitionType, CountDirection, Edge, READ_ALL_AVAILABLE, TaskMode,
                               TriggerType, WAIT_INFINITELY, TerminalConfiguration)
import numpy as np
import time
import matplotlib.pyplot as plt
import sys

channels = ["Dev2/ao1"]  # Add more channels as needed
data = []
fps = int(sys.argv[1])
trial_duration = 300  # was 20 seconds
dac_rate = 50000
trigger_duration = trial_duration + 1
n_samp = int(trigger_duration * dac_rate)
sig = np.zeros(n_samp)
interval_size = int(dac_rate * (1 / fps))
samples_high = round(interval_size / 5)  # duty cycle of 0.5
start_r = samples_high
while start_r < n_samp:
    sig[start_r:start_r + samples_high] = 4
    start_r += interval_size

for i in range(len(channels)):
    data.append(sig)

data = np.asarray(data)
time_tick = list(range(0, len(sig)))
time_tick = [(x / 50000) for x in time_tick]
plt.plot(time_tick, sig)


makePlot = False
if not makePlot:
    # Configure and run the DAQ task
    with nidaqmx.Task() as task:
        try:
            for channel in channels:
                task.ao_channels.add_ao_voltage_chan(channel)
            print("Start writing daq signal")
            task.timing.cfg_samp_clk_timing(dac_rate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
            # Write data to all channels simultaneously
            task.write(data[0], auto_start=True)
            time.sleep(trigger_duration)
            task.stop()
            task.close()
            print("Stop sending signal")
        except KeyboardInterrupt:
            task.stop()
            task.close()
else:
    plt.show()
