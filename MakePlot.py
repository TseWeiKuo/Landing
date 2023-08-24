import json
import math

import simplejson
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import statistics as st
import pickle
FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)

def grabJSON(s):
    """Takes the largest bite of JSON from the string.
       Returns (object_parsed, remaining_string)
    """
    decoder = simplejson.JSONDecoder()
    obj, end = decoder.raw_decode(s)
    end = WHITESPACE.match(s, end).end()
    return obj, s[end:]
def ExtractData(FileDirectory):
    data_map = list(dict())
    with open(FileDirectory) as f:
        Data = f.read()
    while True:
        obj, remaining = grabJSON(Data)
        Data = remaining
        data_map.append(obj)
        if not remaining.strip():
            break
    return data_map
def PlotVoltageDifference(Data_map, FigName, FigTitle):
    legend_label = []
    fig = plt.figure(figsize=(16, 12))
    i = 0
    for plot_data in Data_map:
        i += 1
        plt.subplot(2, 2, i).set_title(Title[i - 1])
        for key in plot_data.keys():
            for data_point in plot_data[key]:
                print(key)
                print(data_point)
                plt.scatter(float(key), float(data_point), color=color[i])
        plt.xlabel("Stop voltage", fontsize=15)
        plt.ylabel("Voltage difference", fontsize=15)
        plt.xticks([2, 2.5, 3, 3.5])
    plt.legend(handles=legend_label, fontsize=15, loc='upper right',
               bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=4)
    plt.suptitle(FigTitle, fontsize=25)
    plt.savefig(FigName)
    plt.show()
def PlotVoltageDiffErrorBar(Data_map, FigName, FigTitle):
    legend_label = []
    fig = plt.figure(figsize=(16, 12))
    i = 0
    for plot_data in Data_map:
        i += 1
        std = []
        average = []
        N = 0
        for key in plot_data.keys():
            N = len(list(plot_data[key]))
            std.append(st.stdev(np.asarray(plot_data[key])))
            average.append(np.mean(np.asarray(plot_data[key])))
        plt.plot(list(plot_data.keys()), average, color[i])
        plt.errorbar(list(plot_data.keys()), average, linestyle='-', marker='.', capsize=5, markersize=15,
                     yerr=(std[len(std) - 1] / math.sqrt(N)), color=color[i])
        legend_label.append(mpatches.Patch(color=color[i], label=Title[i - 1]))
        plt.xlabel("Stop voltage", fontsize=15)
        plt.ylabel("Voltage difference", fontsize=15)
    plt.legend(handles=legend_label, fontsize=15, loc='upper right',
               bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=4)
    plt.suptitle(FigTitle, fontsize=25)
    plt.savefig(FigName)
    plt.show()

Title = ["Velocity: 0.15", "Velocity: 0.2", "Velocity: 0.25", "Velocity: 0.3"]
FigName = ["AccuracyData_@Stop1", "AverageErrorBar_@Stop1", "TraceGraph"]
Target_Voltage = ["Target V: 2", "Target V: 2.5", "Target V: 3", "Target V: 3.5"]

FigureName = ""
FileDirectory = ""
color = "bgrcmy"
ImmediateStopDirectory = r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\OneSecDelayVTrace.txt"
OneSecDelayVDirectory = r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\OneSecDelayV.txt"
OneSecDelayVTraceDirectory = r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\OneSecDelayVTrace.txt"

Immediate_data_map = ExtractData(ImmediateStopDirectory)
OneSDelay_data_map = ExtractData(OneSecDelayVDirectory)
OneSDelayTrace_data_map = ExtractData(OneSecDelayVTraceDirectory)

ImmediateStop = True
OneSecDelayStop = True

Voltage_difference = True
Voltage_Error_bar = True
TraceGraph = True

if ImmediateStop:
    if Voltage_difference:
        PlotVoltageDifference(Immediate_data_map, r"ImmediateStopVoltageDiff", "Immediate stop at target voltage")
    if Voltage_Error_bar:
        PlotVoltageDiffErrorBar(Immediate_data_map, r"ImmediateStopVoltageDiffErr", "Immediate stop at target voltage average")
if OneSecDelayStop:
    if Voltage_difference:
        PlotVoltageDifference(OneSDelay_data_map, r"OneSecDelayVoltageDiff", "1s delay at target voltage")
    if Voltage_Error_bar:
        PlotVoltageDiffErrorBar(OneSDelay_data_map, r"OneSecDelayVoltageDiffErr", "1s delay at target voltage average")





"""
legend_label = []
fig = plt.figure(figsize=(16, 12))
i = 0
for plot_data in Immediate_data_map:
    i += 1
    if Voltage_difference:
        plt.subplot(2, 2, i).set_title(Title[i-1])
        for key in plot_data.keys():
            for data_point in plot_data[key]:
                plt.scatter(float(key), float(data_point), color=color[i])
        plt.xlabel("Stop voltage", fontsize=15)
        plt.ylabel("Voltage difference", fontsize=15)
        plt.xticks([2, 2.5, 3, 3.5])
    if Voltage_Error_bar:
        std = []
        average = []
        N = 0
        for key in plot_data.keys():
            N = len(list(plot_data[key]))
            std.append(st.stdev(np.asarray(plot_data[key])))
            average.append(np.mean(np.asarray(plot_data[key])))
        plt.plot(list(plot_data.keys()), average, color[i])
        plt.errorbar(list(plot_data.keys()), average, linestyle='-', marker='.', capsize=5, markersize=15,
                     yerr=(std[len(std) - 1] / math.sqrt(N)), color=color[i])
        legend_label.append(mpatches.Patch(color=color[i], label=Title[i - 1]))
        plt.xlabel("Stop voltage", fontsize=15)
        plt.ylabel("Voltage difference", fontsize=15)
    if TraceGraph:
        plt.subplot(2, 2, i).set_title(Title[i-1])
        j = 0
        for key in plot_data.keys():
            for traces in plot_data[key]:
                TimeTrace = []
                VoltageTrace = []
                for t in traces:
                    TimeTrace.append(t[0])
                    VoltageTrace.append(t[1])
                plt.plot(TimeTrace, VoltageTrace, color[j], linestyle='-', marker='.')
            j += 1
        legend_label.append(mpatches.Patch(color=color[i - 1], label=Target_Voltage[i - 1]))
        plt.xlabel("Time (s)", fontsize=15)
        plt.ylabel("Voltage (v)", fontsize=15)

plt.legend(handles=legend_label, fontsize=15,loc='upper right',
           bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=4)
plt.suptitle("1s delay voltage drift trace", fontsize=25)
plt.savefig("1s delay voltage drift")
plt.show()
"""