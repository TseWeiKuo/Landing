import os

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

from kinematic_object import Group, Trial, Point
import kinematic_utilities as ku
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import math
from scipy.interpolate import interp1d
from scipy.stats import linregress, goodness_of_fit


class PlotCreator:
    def __init__(self, platform_offset, platform_height, radius=0, fps=0):
        self.calculator = ku.SimpleCalculation()
        self.detector = ku.DetectCharacteristics(radius, fps)
        self.analyzer = ku.GroupDataAnalyzer(platform_offset=platform_offset, radius=radius, FPS=fps)
        self.manipulator = ku.FileManipulation()
        self.platform_offset = platform_offset
        self.radius = radius
        self.fps = fps
        self.platform_height = platform_height
        self.key_point_pairs = [["L-wing", "L-wing-hinge"], ["R-wing", "R-wing-hinge"], ["abdomen-tip"],
                                ["platform-tip"], ["L-platform-tip"], ["R-platform-tip"], ["platform-axis"],
                                ["R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT"],
                                ["R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT"],
                                ["R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT"],
                                ["L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT"],
                                ["L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT"],
                                ["L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT"]]
        self.bodyparts = ["R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT",
                           "R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT",
                           "R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT",
                           "L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT",
                           "L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT",
                           "L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT"]
        self.angles = [["R-fBC", "R-fCT", "R-fFT"],
                       ["R-mBC", "R-mCT", "R-mFT"],
                       ["R-mCT", "R-mFT", "R-mTT"],
                       ["R-mFT", "R-mTT", "R-mLT"],
                       ["R-hBC", "R-hCT", "R-hFT"],
                       ["platform-tip", "R-hBC", "R-hTT"],

                       ["L-fBC", "L-fCT", "L-fFT"],
                       ["L-fCT", "L-fFT", "L-fTT"],

                       ["L-mBC", "L-mCT", "L-mFT"],
                       ["L-mCT", "L-mFT", "L-mTT"],
                       ["platform-tip", "L-hBC", "L-hTT"],

                       ["L-hBC", "L-hCT", "L-hFT"],
                       ["L-hCT", "L-hFT", "L-hTT"],
                       ["L-wing", "L-wing-hinge", "R-wing"]]
        self.colors = ["#FF0000", "#008000", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF",
                       "#000000", "#808080", "#A9A9A9", "#D3D3D3", "#FFA500", "#800080",
                       "#A52A2A", "#FFC0CB", "#ADD8E6", "#00FF00", "#4B0082", "#EE82EE",
                       "#FFD700", "#C0C0C0", "#D2B48C", "#FF7F50", "#006400", "#00008B",
                       "#8B0000", "#FF8C00", "#8B008B", "#708090", "#FF6347", "#008080"]
    r""" def plot_flying_posture_over_trial(self, group_info:Group, filename):

        self.analyzer.Determine_all_flying_posture(group_info)

        collected_joint_angle_R = []
        collected_joint_angle_L = []
        for i in range(group_info.total_fly_number):
            ft_angle_r = []
            ft_angle_l = []
            for t in range(20):
                if f"F{i + 1}T{t + 1}" in group_info.fly_kinematic_data:
                    ft_angle_r.append(group_info.fly_kinematic_data[f"F{i + 1}T{t + 1}"].R_stable_FT_angle)
                    ft_angle_l.append(group_info.fly_kinematic_data[f"F{i + 1}T{t + 1}"].L_stable_FT_angle)
            collected_joint_angle_L.append(ft_angle_l)
            collected_joint_angle_R.append(ft_angle_r)

        # print(collected_joint_angle_R)
        fig, ax = plt.subplots()
        # sns.lineplot(collected_joint_angle_R, linestyle="solid", color="grey", legend=False)
        for trace in collected_joint_angle_R:
            # ax.plot(trace, color="grey", alpha=0.3, linewidth=1)
            pass

        collected_joint_angle_R = pd.DataFrame(collected_joint_angle_R)

        mean_values_R = collected_joint_angle_R.mean(axis=0, skipna=True)  # Compute mean for each trial (column)
        sem_values_R = collected_joint_angle_R.sem(axis=0, skipna=True)  # Compute SEM for each trial (column)


        sns.lineplot(x=mean_values_R.index, y=mean_values_R, errorbar=("ci", 0), ax=ax, label="Mean", color="Navy", legend=False, linewidth=2)

        ax.fill_between(mean_values_R.index, mean_values_R - sem_values_R, mean_values_R + sem_values_R, color="navy", alpha=0.25, linewidth=0)

        # Add error bars manually
        # ax.errorbar(mean_values_R.index + 1, mean_values_R, yerr=sem_values_R, fmt='o', color="Navy", capsize=5)

        ax.set_xlabel("Trial", fontsize=25)
        ax.set_ylabel("R-Femur Tibia angle", fontsize=25)
        plt.tick_params(axis="both", width=3, length=10)
        plt.xticks([0, 9, 19], ["1", "10", "20"], fontsize=25)
        plt.yticks([20, 50, 80], fontsize=25)
        for spine in ax.spines.values():
            spine.set_linewidth(2)

        sns.despine(trim=True)
        plt.savefig(f"{filename}.pdf")
        plt.tight_layout()
        plt.show()
        """
    def plot_motion_vector_with_plane(self, kinematic_data:Trial, frame):


        line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
            self.calculator.transform_coords_and_calculate_platform_data(trial_info=kinematic_data,
                                                                         platform_offset=self.platform_offset,
                                                                         platform_height=self.platform_height,
                                                                         radius=self.radius))

        coords = self.detector.ReadCoordsAll(kinematic_data, frame)

        center_points = self.calculator.ReadAndTranspose("platform-tip", kinematic_data)
        platform_ctr_pts_traces = np.array(center_points[200:250])

        # Create color gradient based on the order of the points
        num_points = len(platform_ctr_pts_traces)
        colors = plt.cm.Greys(np.linspace(0, 1, num_points))

        # 3D Plot
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Loop through the connections and plot lines
        for g, group in enumerate(self.key_point_pairs):
            for i in range(len(group) - 1):  # Connect points in the group
                p1 = coords[group[i]]
                p2 = coords[group[i + 1]]

                # Plot a line between p1 and p2
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], linewidth=5, marker='o', color=self.colors[g])
            if len(group) == 1:
                p1 = coords[group[0]]
                # ax.plot([p1[0]], [p1[1]], [p1[2]], marker='o', color=self.colors[g], markersize=8, linestyle='None')  # important: no line

        # ax.quiver(*platform_ctr_pts_traces[-1], *perp_vector1, color='r', arrow_length_ratio=0.1)
        # ax.quiver(*platform_ctr_pts_traces[-1], *perp_vector2, color='r', arrow_length_ratio=0.1)

        # Add the side surface to the plot
        side_surface = Poly3DCollection(verts, alpha=0.3, facecolor='gray', edgecolor='none')
        ax.add_collection3d(side_surface)

        # Plot the trajectory with color gradient
        for i in range(num_points - 1):
            pass
            # ax.plot(platform_ctr_pts_traces[i:i + 2, 0], platform_ctr_pts_traces[i:i + 2, 1], platform_ctr_pts_traces[i:i + 2, 2], color=colors[i], linewidth=6)

        # Plot the best-fit line
        # ax.quiver(*platform_ctr_pts_traces[-1], *direction, color='r', arrow_length_ratio=0.1)
        # Plot the normal plane
        ax.plot_trisurf(plane_points[:, 0], plane_points[:, 1], plane_points[:, 2], color='cyan', alpha=0.5)

        # Labels and legend
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        # ax.set_title("3D Motion with Normal Plane")
        axis_limit = 1.5  # Adjust this value based on your data range
        ax.set_xlim([-axis_limit, axis_limit])
        ax.set_ylim([-axis_limit, axis_limit])
        ax.set_zlim([-axis_limit, axis_limit])

        x_axis = np.array([1, 0, 0])
        y_axis = np.array([0, 1, 0])
        z_axis = np.array([0, 0, 1])
        origin = [-1.5, -1.5, -2]  # shape (3,)
        axis_len = 0.5  # adjust for visibility
        ax.quiver(*origin, *(axis_len * x_axis), color='r', linewidth=2)  # X (red)
        ax.quiver(*origin, *(axis_len * y_axis), color='g', linewidth=2)  # Y (green)
        ax.quiver(*origin, *(axis_len * z_axis), color='b', linewidth=2)  # Z (blue)

        x_tip = origin + 0.9 * np.array([1, 0, 0])
        y_tip = origin + 0.7 * np.array([0, 1, 0])
        z_tip = origin + 0.7 * np.array([0, 0, 1])

        ax.text(*x_tip, 'x', color='r', fontsize=20)
        ax.text(*y_tip, 'y', color='g', fontsize=20)
        ax.text(*z_tip, 'z', color='b', fontsize=20)

        ax.legend()

        # azim = np.arctan2(normal_vector[1], normal_vector[0]) * 180 / np.pi

        # Elevation is calculated based on the z-component of the vector
        plt.gca().set_aspect('equal')
        ax.view_init(elev=0, azim=180)
        ax.grid(True)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))  # Make panes transparent
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.set_axis_off()  # This removes everything including the frame
        plt.savefig("Kinematic.pdf")
        plt.show(block=True)
    def plot_CT_FT_angle_space(self, group_info:Group):
        self.angles = [["L-fBC", "L-fCT", "L-fFT"],
                       ["L-mBC", "L-mCT", "L-mFT"],
                       ["L-hBC", "L-hCT", "L-hFT"],

                       ["L-fCT", "L-fFT", "L-fTT"],
                       ["L-mCT", "L-mFT", "L-mTT"],
                       ["L-hCT", "L-hFT", "L-hTT"]]
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
        for index in group_info.get_targeted_trials(["Landing"]):
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
            start = trial_info.moc
            end = trial_info.mol
            print(f"Fly: {index[0]} Trial: {index[1]}")

            joint = "L-fCT"
            joint2 = "L-fFT"
            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            signal = np.asarray(angs[joint][start:end])
            peaks, troughs = self.detector.detect_peaks_troughs(signal=signal, leg=joint[:3])

            # plt.plot(signal)
            # plt.scatter(peaks, signal[peaks])
            # plt.scatter(troughs, signal[troughs])
            # plt.show()
            # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
            # t = np.asarray(range(len(peaks)))
            print(len(troughs))
            if len(troughs) != 0:
                colors = plt.cm.plasma(np.linspace(0, 1, len(troughs) - 1))
            # norm = Normalize(vmin=t.min(), vmax=int(t.max() - 1))
            # cmap = cm.plasma
            for p in range(len(troughs) - 1):
                sns.lineplot(x=angs[joint][troughs[p] + start:troughs[p + 1] + start], y=angs[joint2][troughs[p] + start:troughs[p + 1] + start], sort=False, color=colors[p], linewidth=2, alpha=0.4)
                """plt.scatter(x=np.mean(angs[joint][troughs[p] + start:troughs[p + 1] + start]),
                            y=np.mean(angs[joint2][troughs[p] + start:troughs[p + 1] + start]),
                            color=colors[p],
                            alpha=0.4, s=100)"""
                """if p == len(troughs) - 2:
                    # sns.lineplot(x=angs[joint][troughs[p + 1] + start:end], y=angs[joint2][troughs[p + 1] + start:end], sort=False, color=colors[p + 1], linewidth=5, alpha=0.4)
                    plt.scatter(x=np.mean(angs[joint][troughs[p + 1] + start:end]),
                                y=np.mean(angs[joint2][troughs[p + 1] + start:end]),
                                color=colors[p + 1],
                                alpha=0.4,
                                s=100)"""


        ax.tick_params(axis="y", labelsize=25)
        ax.tick_params(axis="x", labelsize=25)
        ax.tick_params(width=3, length=20)
        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)
        ax.set_ylabel("L-hFT angle", fontsize=25)
        ax.set_xlabel("L-hCT angle", fontsize=25)
        ax.set_yticks([0, 90, 180])
        ax.set_ylim(-5, 185)
        ax.set_xticks([0, 90, 180])
        ax.set_xlim(-5, 185)
        sns.despine(trim=True)
        plt.tight_layout()
        # plt.savefig(f"Fly{index[0]}AngleSpace")
        plt.show()


    def plot_CTF_MOC(self, group_info:Group):

        index_to_iterate = group_info.get_targeted_trials(["Landing", "Flying"])
        hard_sigs = []
        soft_sigs = []

        FT = False
        CT = True

        hard_color = ""
        soft_color = ""
        if FT:
            hard_color = "orangered"
            soft_color = "deepskyblue"
        if CT:
            hard_color = "orange"
            soft_color = "blue"

        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
        for index in index_to_iterate:
            print(f"Fly {index[0]} Trial {index[1]}")
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            start = trial_info.moc
            end = trial_info.mol

            line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
                self.calculator.transform_coords_and_calculate_platform_data(trial_info=trial_info,
                                                                             platform_offset=self.platform_offset,
                                                                             platform_height=self.platform_height,
                                                                             radius=self.radius))

            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            CT_signal = angs["R-mCT"]
            FT_signal = angs["R-mFT"]
            leg_stuck = self.detector.Detect_hard_touch(trial_info)

            signal_to_use = FT_signal
            signal_to_display = None

            if FT:
                signal_to_display = FT_signal
            if CT:
                signal_to_display = CT_signal

            if start < 0:
                print("Flying trial")
                start = 440
                end = start + trial_info.fps
            seconds = [s / (end - start) for s in range(end - start)]

            if leg_stuck:
                sns.lineplot(x=seconds, y=signal_to_display[start:end], ax=ax[0], color=hard_color, linewidth=1, alpha=0.5)
                hard_sigs.append(signal_to_use[start:end])
            else:
                soft_sigs.append(signal_to_use[start:end])
                sns.lineplot(x=seconds, y=signal_to_display[start:end], ax=ax[1], color=soft_color, linewidth=1, alpha=0.5)

        top_graph_tick_value = [0, 180]
        bottom_graph_tick_value = [0, 180]
        ax[0].tick_params(axis="y", labelsize=15)
        ax[0].tick_params(axis="x", labelsize=15)
        ax[0].tick_params(width=3, length=5)
        ax[0].spines["left"].set_linewidth(2)  # Top border
        ax[0].spines["bottom"].set_linewidth(2)
        ax[0].set_xticks([0, 0.5, 1], labels=["0\nmoc", "0.5", "1\nmol"])
        ax[0].set_xlim(-0.1, 1.1)
        ax[0].set_yticks([top_graph_tick_value[0], (top_graph_tick_value[0] + top_graph_tick_value[1]) / 2, top_graph_tick_value[1]])
        ax[0].set_ylim(top_graph_tick_value[0] - 5, top_graph_tick_value[1] + 5)
        ax[0].set_title("Hard touch", fontsize=15)
        ax[1].set_title("Soft touch", fontsize=15)
        ax[1].tick_params(axis="y", labelsize=15)
        ax[1].tick_params(axis="x", labelsize=15)
        ax[1].tick_params(width=3, length=5)
        ax[1].spines["left"].set_linewidth(2)  # Top border
        ax[1].spines["bottom"].set_linewidth(2)
        ax[1].set_xticks([0, 0.5, 1], labels=["0\nmoc", "0.5", "1\nmol"])
        ax[1].set_xlim(-0.1, 1.1)
        ax[1].set_yticks([bottom_graph_tick_value[0], (bottom_graph_tick_value[0] + bottom_graph_tick_value[1]) / 2, bottom_graph_tick_value[1]])
        ax[1].set_ylim(bottom_graph_tick_value[0] - 5, bottom_graph_tick_value[1] + 5)
        fig.supylabel('FT angle upon moc', fontsize=20)
        plt.xlabel("Standardized landing transition duration", fontsize=20)
        sns.despine(trim=True)
        plt.tight_layout()
        plt.show()

        common_len = group_info.fps[0]  # any length you want
        resampled_hard = []
        resampled_soft = []

        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
        from scipy.interpolate import interp1d

        for s in hard_sigs:
            x_old = np.linspace(0, 1, len(s))
            x_new = np.linspace(0, 1, common_len)
            f = interp1d(x_old, s, kind='linear')
            resampled_hard.append(f(x_new))

        for s in soft_sigs:
            x_old = np.linspace(0, 1, len(s))
            x_new = np.linspace(0, 1, common_len)
            f = interp1d(x_old, s, kind='linear')
            resampled_soft.append(f(x_new))

        resampled_hard = np.array(resampled_hard)
        mean = resampled_hard.mean(axis=0)
        sem = resampled_hard.std(axis=0) / np.sqrt(len(resampled_hard))

        top_graph_tick_value = [40, 100]
        bottom_graph_tick_value = [40, 100]
        # Plot
        x = np.linspace(0, 1, common_len)
        ax[0].plot(x, mean, label='Mean', color=hard_color)
        ax[0].fill_between(x, mean - sem, mean + sem, alpha=0.3, label='SEM', color=hard_color)

        ax[0].tick_params(axis="y", labelsize=15)
        ax[0].tick_params(axis="x", labelsize=15)
        ax[0].tick_params(width=3, length=5)
        ax[0].spines["left"].set_linewidth(2)  # Top border
        ax[0].spines["bottom"].set_linewidth(2)
        ax[0].set_xticks([0, 0.5, 1], labels=["0\nmoc", "0.5", "1\nmol"])
        ax[0].set_xlim(-0.1, 1.1)
        ax[0].set_yticks([top_graph_tick_value[0], (top_graph_tick_value[0] + top_graph_tick_value[1]) / 2, top_graph_tick_value[1]])
        ax[0].set_ylim(top_graph_tick_value[0] - 5, top_graph_tick_value[1] + 5)

        resampled_soft = np.array(resampled_soft)
        mean = resampled_soft.mean(axis=0)
        sem = resampled_soft.std(axis=0) / np.sqrt(len(resampled_soft))

        ax[0].set_title("Hard touch", fontsize=15)
        ax[1].set_title("Soft touch", fontsize=15)

        # Plot
        x = np.linspace(0, 1, common_len)

        ax[1].plot(x, mean, label='Mean', color=soft_color)
        ax[1].fill_between(x, mean - sem, mean + sem, alpha=0.3, label='SEM', color=soft_color)

        ax[1].tick_params(axis="y", labelsize=15)
        ax[1].tick_params(axis="x", labelsize=15)
        ax[1].tick_params(width=3, length=5)
        ax[1].spines["left"].set_linewidth(2)  # Top border
        ax[1].spines["bottom"].set_linewidth(2)
        ax[1].set_xticks([0, 0.5, 1], labels=["0\nmoc", "0.5", "1\nmol"])
        ax[1].set_xlim(-0.1, 1.1)
        ax[1].set_yticks([bottom_graph_tick_value[0], (bottom_graph_tick_value[0] + bottom_graph_tick_value[1]) / 2,
                          bottom_graph_tick_value[1]])
        ax[1].set_ylim(bottom_graph_tick_value[0] - 5, bottom_graph_tick_value[1] + 5)
        fig.supylabel('FT angle average upon moc', fontsize=20)
        plt.xlabel("Standardized landing transition duration", fontsize=20)
        sns.despine(trim=True)
        plt.show()

    def plot_Inidi_Leg_Contact(self, group_info:Group):

        segs = [["L-fFT", "L-fTT", 0.45],
                ["L-fTT", "L-fLT", 0.4],

                ["L-mFT", "L-mTT", 0.5],
                ["L-mTT", "L-mLT", 0.4],

                ["L-hFT", "L-hTT", 0.6],
                ["L-hTT", "L-hLT", 0.5],

                ["R-fFT", "R-fTT", 0.45],
                ["R-fTT", "R-fLT", 0.4],

                ["R-mFT", "R-mTT", 0.5],
                ["R-mTT", "R-mLT", 0.4],

                ["R-hFT", "R-hTT", 0.5],
                ["R-hTT", "R-hLT", 0.4]]

        pts = ["L-fFT", "L-fTT", "L-fLT",
               "L-mFT", "L-mTT", "L-mLT",
               "L-hFT", "L-hTT", "L-hLT",
               "R-fFT", "R-fTT", "R-fLT",
               "R-mFT", "R-mTT", "R-mLT",
               "R-hFT", "R-hTT", "R-hLT"]


        indi_leg_contact_event = dict()
        indi_leg_contact_event_tnorm = dict()
        for j in segs:
            indi_leg_contact_event[j[0]] = []
            indi_leg_contact_event_tnorm[j[0]] = []

        indi_leg_contact_event["Index"] = []
        indi_leg_contact_event["LLBin"] = []

        indi_leg_contact_event_tnorm["Index"] = []
        indi_leg_contact_event_tnorm["LLBin"] = []

        index_to_iterate = group_info.get_targeted_trials(["Landing"])
        for i, index in enumerate(index_to_iterate):
            # print(index, group_info.fly_kinematic_data_path[f"F{index[0]}T{index[1]}"])
            pose_data = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            if "_LO_" in group_info.fly_kinematic_data_path[f"F{index[0]}T{index[1]}"]:
                # print("OFF-trial")
                continue
            else:
                print(group_info.fly_kinematic_data_path[f"F{index[0]}T{index[1]}"])

            start = int(pose_data.moc)
            end = int(pose_data.mol)
            if end == -1:
                end = start + int(0.7 * pose_data.fps)
                indi_leg_contact_event["LLBin"].append("Flying")
                indi_leg_contact_event_tnorm["LLBin"].append("Flying")
            elif (end - start) / pose_data.fps > 0.71:
                end = start + int(0.7 * pose_data.fps)
                indi_leg_contact_event["LLBin"].append("Supra_threshold")
                indi_leg_contact_event_tnorm["LLBin"].append("Supra_threshold")
            elif (end - start) / pose_data.fps <= 0.3:
                indi_leg_contact_event["LLBin"].append("Low_latency")
                indi_leg_contact_event_tnorm["LLBin"].append("Low_latency")
            elif (end - start) / pose_data.fps <= 0.71:
                indi_leg_contact_event["LLBin"].append("High_latency")
                indi_leg_contact_event_tnorm["LLBin"].append("High_latency")
            else:
                print("Unable to categorize!")
            print("data read")

            line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
                self.calculator.transform_coords_and_calculate_platform_data(trial_info=pose_data,
                                                                             platform_offset=self.platform_offset,
                                                                             platform_height=self.platform_height,
                                                                             radius=self.radius))

            Original_points = dict()
            center_points = self.calculator.ReadAndTranspose("platform-tip", pose_data)[start:end]
            for p in pts:
                Original_points[p] = self.calculator.ReadAndTranspose(p, pose_data)[start:end]

            # event_recorder = []
            for point in segs:
                NoContact = True
                distances = []
                stable_contact = 0
                for current_frame in range(end - start):
                    A = Original_points[point[0]][current_frame]
                    B = Original_points[point[1]][current_frame]
                    P1 = center_points[current_frame]

                    d = direction
                    r = point[2]
                    h = self.platform_height

                    intersects_side, pt_side, min_dist = self.calculator.check_cylinder_side_intersection(A, B, P1, d, r, h)
                    intersects_top, pt_top = self.detector.check_leg_platform_intersection(A, B, d, center_points[current_frame], self.platform_offset)
                    distances.append(min_dist)
                    # indi_leg_min_dist[point[0][0:3]].append(min_dist)
                    if intersects_top or intersects_side:
                        stable_contact += 1
                    else:
                        stable_contact = 0
                    if stable_contact >= 1:
                        indi_leg_contact_event[point[0]].append(current_frame / pose_data.fps)
                        indi_leg_contact_event_tnorm[point[0]].append(current_frame / (end - start))
                        NoContact = False
                        break

                if NoContact:
                    indi_leg_contact_event[point[0]].append(10000)
                    indi_leg_contact_event_tnorm[point[0]].append(10000)

            if index not in indi_leg_contact_event["Index"]:
                indi_leg_contact_event["Index"].append(index)
                indi_leg_contact_event_tnorm["Index"].append(index)


        indi_leg_contact_event = pd.DataFrame(indi_leg_contact_event)
        indi_leg_contact_event_tnorm = pd.DataFrame(indi_leg_contact_event_tnorm)
        indi_leg_contact_event.to_csv(f"{group_info.group_name}_SecondaryContact_.csv")
        indi_leg_contact_event_tnorm.to_csv(f"{group_info.group_name}_SecondaryContact_tnorm.csv")
        """n_behaviors = len(indi_leg_contact_event)
        fig, axes = plt.subplots(n_behaviors, 1, sharex=True, figsize=(8, 2 * n_behaviors))

        if n_behaviors == 1:
            axes = [axes]

        c = 0
        for ax, (behavior, trials) in zip(axes, indi_leg_contact_event.items()):
            for trial_idx, frames in enumerate(trials):
                ax.vlines(frames, trial_idx + 0.5, trial_idx + 1.5, color=colors[c])
            c += 1

            ax.set_ylim(0.5, len(trials) + 0.5)
            ax.set_ylabel("Trial")
            ax.set_title(behavior)

        axes[-1].set_xlabel("Frame")
        plt.tight_layout()
        plt.savefig(f"{group_info.group_name}_raster")
        plt.show()"""

    """
    def plot_joint_rhythmicity(self, group_info:Group):
        Joint = "R-fCT"

        for index in group_info.landing_trial_index:
            print(f"F{index[0]}T{index[1]}")
            # trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            trial_info = group_info.fly_kinematic_data[f"F1T6"]
            start = int(trial_info.moc)
            end = int(trial_info.mol)

            line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
                self.calculator.transform_coords_and_calculate_platform_data(trial_info=trial_info,
                                                                             platform_offset=self.platform_offset,
                                                                             platform_height=self.platform_height,
                                                                             radius=self.radius))

            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            R_f_CT = np.asarray(angs[Joint][start:end])
            plt.plot(R_f_CT)
            plt.show()
            rhythmicity_score = self.calculator.calculate_rhythmicity(R_f_CT, trial_info.fps)
            # rhythmicity_score = None
            if not rhythmicity_score:
                plt.title(f"Rhythmicity Score: None")
            else:
                plt.title(f"Rhythmicity Score: {rhythmicity_score}")
    def plot_posture_across_groups(self, groups, filename):
        collected_data = dict()
        collected_data["Group_Name"] = []
        collected_data["RmFTAngle"] = []
        import matplotlib.cm as cm
        # Choose a colormap (e.g., viridis, plasma, coolwarm, etc.)
        cmap = cm.get_cmap('viridis', 10)

        # Generate list of colors
        colors = [cmap(i) for i in range(10)]
        plt.figure(figsize=(len(groups) * 2, 10))
        for group_info in groups:
            current_fly = 1
            posture = []
            print(group_info.group_name)
            for index in group_info.get_targeted_trials(["Landing", "Flying"]):
                if current_fly != index[0] or index == group_info.get_targeted_trials(["Landing", "Flying"])[-1]:
                    current_fly = index[0]
                    collected_data["Group_Name"].append(group_info.group_name)
                    collected_data["RmFTAngle"].append(np.mean(posture))
                    posture = []
                trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
                angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
                data = angs["R-mFT"][:int(1 * trial_info.fps)]
                posture.append(np.mean(data))


        collected_data = pd.DataFrame(collected_data)


        group_stat = collected_data.groupby('Group_Name')['RmFTAngle'].agg(['mean', 'std', 'count']).reset_index()
        group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

        g = sns.stripplot(x="Group_Name", y="RmFTAngle", data=collected_data, alpha=0.4, jitter=0.1, dodge=False, size=30, marker="o", palette=colors, zorder=10)
        sns.pointplot(x='Group_Name', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None, scale=2, zorder=10)
        plt.errorbar(x=group_stat['Group_Name'], y=group_stat['mean'], yerr=group_stat['ci'], fmt="none", color='black', capsize=10, zorder=10)

        plt.ylabel("T2-R femur tibia angle", fontsize=25)
        plt.tick_params(axis="y", labelsize=25)
        plt.tick_params(axis="x", labelsize=25, rotation=45)
        plt.tick_params(width=3, length=10)
        g.spines['left'].set_linewidth(3)
        g.spines['bottom'].set_linewidth(3)

        plt.yticks([10, 40, 70])
        plt.xlim(-1 - 1, len(groups) + 1)
        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"{filename}.pdf", format='pdf', dpi=300, bbox_inches='tight')
        plt.show()
    def plot_PCA_analysis(self, groups):
        # joints = ["R-fCT", "L-fCT", "L-mCT", "R-hCT", "L-hCT"]
        joints = ["L-fCT", "L-mCT", "L-hCT"]
        # joints = ["L-fFT", "L-mFT", "L-hFT"]
        def normalize_length_smooth(data, target_len):
            x = np.linspace(0, 1, len(data))
            f = interp1d(x, data, kind='cubic')  # cubic spline
            x_new = np.linspace(0, 1, target_len)
            return f(x_new)

        collected_joints_data = []
        groups_name = []
        trial_n = 0
        for group_info in groups:
            for index in group_info.get_targeted_trials(["Landing"]):
                trial_n += 1
                trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
                angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
                speeds = self.calculator.calculate_velocity(trial_info, joints)
                start = int(trial_info.moc)
                end = int(trial_info.mol)
                for j in joints:
                    data = angs[j][int(start):int(end)]
                    # data = speeds[j][int(start):int(end)]
                    # data = np.gradient(data)
                    data = normalize_length_smooth(data, 200)
                    from scipy.signal import welch
                    from scipy.signal import butter, filtfilt, welch
                    def highpass_filter(data, cutoff, fs, order=4):
                        nyq = 0.5 * fs
                        normal_cutoff = cutoff / nyq
                        b, a = butter(order, normal_cutoff, btype='high', analog=False)
                        return filtfilt(b, a, data)

                    cutoff = 0.5
                    nperseg = 32
                    nfft = 40
                    # data = data - np.mean(data[:10])
                    # data = highpass_filter(data, cutoff=cutoff, fs=trial_info.fps, order=4)

                    # 2) remove mean
                    # data = data - np.mean(data)

                    # 4) compute Welch PSD with consistent nperseg/nfft
                    # we pass nperseg and nfft so all outputs have same freq vector

                    f, Pxx = welch(data, fs=trial_info.fps, nperseg=nperseg, nfft=nfft)


                    collected_joints_data.append(data)
                    groups_name.append(group_info.group_name + j)

        # print(collected_joints_data)
        collected_joints_data = np.array(collected_joints_data)
        # groups_name = np.array(joints * trial_n)
        groups_name = np.array(groups_name)
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        X_std = scaler.fit_transform(collected_joints_data)

        from sklearn.decomposition import PCA
        from sklearn.decomposition import KernelPCA

        import skfda
        from skfda.preprocessing.smoothing import BasisSmoother
        from skfda.representation.basis import BSplineBasis
        from skfda.exploratory.visualization import FPCAPlot
        from skfda.preprocessing.dim_reduction import FPCA

        n_points = 100  # number of points for functional representation
        fd_list = []

        for trial in collected_joints_data:
            t_original = np.linspace(0, 1, len(trial))
            t_new = np.linspace(0, 1, n_points)
            trial_interp = np.interp(t_new, t_original, trial)
            fd_list.append(trial_interp)
        fd_matrix = np.array(fd_list)  # shape: (n_trials, n_points)

        n_basis = 15  # can tune based on smoothness
        basis = BSplineBasis(n_basis=n_basis)

        fd = skfda.FDataGrid(data_matrix=fd_matrix, grid_points=np.linspace(0, 1, n_points))
        smoother = BasisSmoother(basis=basis)
        fd_smooth = smoother.fit_transform(fd)

        n_components = 5
        fpca = FPCA(n_components=n_components)
        fpca.fit(fd_smooth)
        scores = fpca.transform(fd_smooth)  # shape: (n_trials, n_components)

        # print("FPCA scores shape:", scores.shape)
        from sklearn.metrics.pairwise import euclidean_distances
        distances = euclidean_distances(X_std)
        median_dist2 = np.median(distances ** 2)
        gamma = 1 / median_dist2  # reasonable starting point
        print(gamma)
        kpca = KernelPCA(
            n_components=5,  # number of components to keep
            kernel='poly',  # radial basis function (Gaussian)
            gamma=gamma,  # kernel coefficient; tune for your data
            fit_inverse_transform=False
        )

        # Transform data
        X_kpca = kpca.fit_transform(X_std)

        pca = PCA(n_components=5)  # choose however many you want
        X_pca = pca.fit_transform(X_std)
        # Unique groups and colors
        unique_groups = np.unique(groups_name)
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_groups)))
        colors = plt.cm.viridis(np.linspace(0, 1, len(joints)))
        markers = ["o", "+", ">"]
        # plt.figure(figsize=(8, 6))


        # Create colors for each group
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_groups)))

        from scipy.stats import gaussian_kde


        fig, axes = plt.subplots(nrows=len(joints), ncols=len(groups), figsize=(10, 10), sharex=True, sharey=True)
        # If only one group, axes may not be an array
        if len(unique_groups) == 1:
            axes = [axes]

        g_ind = 0
        j_ind = 0
        c = 0
        for g in unique_groups:
            mask = groups_name == g
            if j_ind % len(joints) == 0:
                j_ind = 0
                g_ind += 1

            tick1 = [-25, 0, 25]
            lim1 = [-30, 30]
            tick2 = [-50, 0, 50]
            lim2 = [-60, 60]
            axes[j_ind, g_ind - 1].scatter(X_pca[mask, 0], X_pca[mask, 1], marker=markers[g_ind - 1], color=colors[j_ind], alpha=0.5, s=50)
            axes[j_ind, g_ind - 1].set_title(f'Group: {g}')
            axes[j_ind, g_ind - 1].set_xlabel("PC1")
            axes[j_ind, g_ind - 1].set_ylabel("PC2")
            axes[j_ind, g_ind - 1].set_xticks(tick2)
            axes[j_ind, g_ind - 1].set_xlim(lim2)
            axes[j_ind, g_ind - 1].set_yticks(tick2)
            axes[j_ind, g_ind - 1].set_ylim(lim2)
            print(j_ind, g_ind - 1)
            j_ind += 1
            c += 1


        sns.despine(trim=True)

        plt.xlabel("PC1")
        plt.ylabel("PC2")
        # plt.legend()
        plt.tight_layout()
        plt.show()"""

    def plot_leg_angle_reaction(self, groups):
        self.angles = [["L-fBC", "L-fCT", "L-fFT"],
                       ["L-mBC", "L-mCT", "L-mFT"],
                       ["L-hBC", "L-hCT", "L-hFT"],

                       ["L-fCT", "L-fFT", "L-fTT"],
                       ["L-mCT", "L-mFT", "L-mTT"],
                       ["L-hCT", "L-hFT", "L-hTT"],

                       ["L-fFT", "L-fTT", "L-fLT"],
                       ["L-mFT", "L-mTT", "L-mLT"],
                       ["L-hFT", "L-hTT", "L-hLT"],


                       ["R-fBC", "R-fCT", "R-fFT"],
                       ["R-mBC", "R-mCT", "R-mFT"],
                       ["R-hBC", "R-hCT", "R-hFT"],

                       ["R-fCT", "R-fFT", "R-fTT"],
                       ["R-mCT", "R-mFT", "R-mTT"],
                       ["R-hCT", "R-hFT", "R-hTT"],

                       ["R-fFT", "R-fTT", "R-fLT"],
                       ["R-mFT", "R-mTT", "R-mLT"],
                       ["R-hFT", "R-hTT", "R-hLT"]]

        start = -0.2
        end = 0.7
        tnorm = False
        threshold = 0.71
        T1_data = self.analyzer.Calculate_angle_traces(groups[0], self.angles, threshold, start, end, tnorm, False)
        T2_data = self.analyzer.Calculate_angle_traces(groups[1], self.angles, threshold, start, end, tnorm, False)
        T3_data = self.analyzer.Calculate_angle_traces(groups[2], self.angles, threshold, start, end, tnorm, False)

        normalization = ""
        if tnorm:
            seconds = [s / 250 for s in range(250)]
            xtick = [0, 1]
            xtick_label = ["MOC", "MOL"]
            normalization = "_tnorm"
        else:
            seconds = [s / 250 for s in range(int(start * 250), int(end * 250))]
            xtick = [start, 0, end]
            xtick_label = [str(start), "MOC", str(end)]

        threshold_bins = [0.34, 0.68, 1, -1]
        # fig, ax = plt.subplots(5, 1, figsize=(5, 15))



        collected_data = [T1_data, T2_data, T3_data]

        Name = "T1"
        joints_to_plot = ["R-fCT", "R-fFT", "R-fTT"]
        color = self.centered_shades("orange", 3)
        style = ["solid", "solid", "solid"]
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        frames = np.arange(-125, 125) / 250

        """for j, joint in enumerate(joints_to_plot):
            all_trials = []
            for fly_data in T1_data:
                signals = [trace for flag, index, fps, trace in fly_data[joint] if flag == threshold]
                all_trials.extend(signals)
            avg = np.nanmean(np.array(all_trials), axis=0)
            std = np.nanstd(np.array(all_trials), axis=0)
            sns.lineplot(x=frames, y=avg, color=color[j], linestyle=style[j], linewidth=4,
                         label=f"T1-{joints_to_plot[j]} (n = {len(all_trials)})")
            ax.fill_between(frames, avg - std, avg + std, color=color[j], alpha=0.2)

        plt.axvline(0, color="black", linestyle="dashed", label="MOC")
        self.formatting(ax, [-0.5, 0, 0.5], [0, 90, 180], xlabel="seconds (s)", ylabel=f"{Name} joint angle")
        sns.despine(trim=True)
        plt.legend()
        plt.savefig(f"{Name}_Contact_angle_change.pdf")
        plt.show()


        Name = "T2"
        joints_to_plot = ["R-mCT", "R-mFT", "R-mTT"]
        color = self.centered_shades("darkgrey", 3)
        style = ["dashed", "dashed", "dashed"]
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        frames = np.arange(-125, 125) / 250

        for j, joint in enumerate(joints_to_plot):
            all_trials = []
            for fly_data in T2_data:
                signals = [trace for flag, index, fps, trace in fly_data[joint] if flag == threshold]
                all_trials.extend(signals)
            avg = np.nanmean(np.array(all_trials), axis=0)
            std = np.nanstd(np.array(all_trials), axis=0)
            sns.lineplot(x=frames, y=avg, color=color[j], linestyle=style[j], linewidth=4,
                         label=f"T2-{joints_to_plot[j]} (n = {len(all_trials)})")
            ax.fill_between(frames, avg - std, avg + std, color=color[j], alpha=0.2)

        plt.axvline(0, color="black", linestyle="dashed", label="MOC")
        self.formatting(ax, [-0.5, 0, 0.5], [0, 90, 180], xlabel="seconds (s)", ylabel=f"{Name} joint angle")
        sns.despine(trim=True)
        plt.legend()
        plt.savefig(f"{Name}_Contact_angle_change.pdf")
        plt.show()


        Name = "T3"
        joints_to_plot = ["R-hCT", "R-hFT", "R-hTT"]
        color = self.centered_shades("brown", 3)
        style = ["dotted", "dotted", "dotted"]
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        frames = np.arange(-125, 125) / 250

        for j, joint in enumerate(joints_to_plot):
            all_trials = []
            for fly_data in T3_data:
                signals = [trace for flag, index, fps, trace in fly_data[joint] if flag == threshold]
                all_trials.extend(signals)
            avg = np.nanmean(np.array(all_trials), axis=0)
            std = np.nanstd(np.array(all_trials), axis=0)
            sns.lineplot(x=frames, y=avg, color=color[j], linestyle=style[j], linewidth=4,
                         label=f"T3-{joints_to_plot[j]} (n = {len(all_trials)})")
            ax.fill_between(frames, avg - std, avg + std, color=color[j], alpha=0.2)

        plt.axvline(0, color="black", linestyle="dashed", label="MOC")
        self.formatting(ax, [-0.5, 0, 0.5], [0, 90, 180], xlabel="seconds (s)", ylabel=f"{Name} joint angle")
        sns.despine(trim=True)
        plt.legend()
        plt.savefig(f"{Name}_Contact_angle_change.pdf")
        plt.show()"""

        Contact_type = "CxTr"

        color = [self.centered_shades("orange", 3)[1],
                 self.centered_shades("grey", 3)[1],
                 self.centered_shades("brown", 3)[1]]
        
        """Name = "CT"
        style = ["solid", "solid", "solid"]
        joints_to_plot = ["R-fCT", "R-mCT", "R-hCT"]
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        frames = np.arange(int(start * 250), int(end * 250)) / 250
        for g, group_data in enumerate(collected_data):
            all_trials = []
            for fly_data in group_data:
                # signals = [trace for flag, index, fps, trace in fly_data[joints_to_plot[g]] if flag == threshold]
                signals = [trace for flag, index, fps, trace in fly_data[joints_to_plot[g]]]
                all_trials.extend(signals)
            avg = np.nanmean(np.array(all_trials), axis=0)
            std = np.nanstd(np.array(all_trials), axis=0)
            # print(len(frames), len(avg))
            sns.lineplot(x=frames, y=avg, color=color[g], linestyle=style[g], linewidth=4,
                         label=f"T{g + 1}-{joints_to_plot[g]} (n = {len(all_trials)})")
            ax.fill_between(frames, avg - std, avg + std, color=color[g], alpha=0.2)
        plt.axvline(0, color="black", linestyle="dashed", label="MOC")
        self.formatting(ax, [start, 0, end], [0, 90, 180], xlabel="seconds (s)", ylabel=f"{Name} joint angle")
        sns.despine(trim=True)
        plt.legend()
        plt.savefig(f"{Contact_type}_Contact_{Name}_change.pdf")
        plt.show()



        color = [self.centered_shades("orange", 3)[1],
                 self.centered_shades("grey", 3)[1],
                 self.centered_shades("brown", 3)[1]]
        Name = "FT"
        joints_to_plot = ["R-fFT", "R-mFT", "R-hFT"]
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        frames = np.arange(int(start * 250), int(end * 250)) / 250
        for g, group_data in enumerate(collected_data):
            all_trials = []
            for fly_data in group_data:
                # signals = [trace for flag, index, fps, trace in fly_data[joints_to_plot[g]] if flag == threshold]
                signals = [trace for flag, index, fps, trace in fly_data[joints_to_plot[g]]]
                all_trials.extend(signals)
            avg = np.nanmean(np.array(all_trials), axis=0)
            std = np.nanstd(np.array(all_trials), axis=0)
            # print(len(frames), len(avg))
            sns.lineplot(x=frames, y=avg, color=color[g], linestyle=style[g], linewidth=4,
                         label=f"T{g + 1}-{joints_to_plot[g]} (n = {len(all_trials)})")
            ax.fill_between(frames, avg - std, avg + std, color=color[g], alpha=0.2)
        plt.axvline(0, color="black", linestyle="dashed", label="MOC")
        self.formatting(ax, [start, 0, end], [0, 90, 180], xlabel="seconds (s)", ylabel=f"{Name} joint angle")
        sns.despine(trim=True)
        plt.legend()
        plt.savefig(f"{Contact_type}_Contact_{Name}_change.pdf")
        plt.show()"""



        color = self.centered_shades("grey", 5)
        Name = "FT"
        joints_to_plot = ["R-mFT"]
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        frames = np.arange(int(start * 250), int(end * 250)) / 250

        failed_trials = []
        successful_trials = []
        for fly_data in T2_data:
            failed_trials.extend([trace for flag, index, fps, trace in fly_data["R-mFT"] if flag != threshold])
            successful_trials.extend([trace for flag, index, fps, trace in fly_data["R-mFT"] if flag == threshold])

        failed_avg = np.nanmean(np.array(failed_trials), axis=0)
        failed_std = np.nanstd(np.array(failed_trials), axis=0)
        successful_avg = np.nanmean(np.array(successful_trials), axis=0)
        successful_std = np.nanstd(np.array(successful_trials), axis=0)
        # print(len(frames), len(avg))
        sns.lineplot(x=frames, y=failed_avg, color=color[4], linestyle="solid", linewidth=4, label=f"Failed landing (n = {len(failed_trials)})")
        ax.fill_between(frames, failed_avg - failed_std, failed_avg + failed_std, color=color[4], alpha=0.2)

        sns.lineplot(x=frames, y=successful_avg, color=color[2], linestyle="solid", linewidth=4, label=f"Successful landing (n = {len(successful_trials)})")
        ax.fill_between(frames, successful_avg - successful_std, successful_avg + successful_std, color=color[2], alpha=0.2)

        plt.axvline(0, color="black", linestyle="dashed", label="MOC")
        self.formatting(ax, [start, 0, end], [0, 90, 180], xlabel="seconds (s)", ylabel=f"T2-R-FT joint angle")
        sns.despine(trim=True)
        plt.legend()
        plt.savefig(f"Failed_vs_successful_FT_change.pdf")
        plt.show()

        """color = [self.centered_shades("orange", 3)[0],
                 self.centered_shades("grey", 3)[0],
                 self.centered_shades("brown", 3)[0]]
        Name = "TT"
        joints_to_plot = ["R-fTT", "R-mTT", "R-hTT"]
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        frames = np.arange(int(start * 250), int(end * 250)) / 250
        for g, group_data in enumerate(collected_data):
            all_trials = []
            for fly_data in group_data:
                signals = [trace for flag, index, fps, trace in fly_data[joints_to_plot[g]] if flag == threshold]
                all_trials.extend(signals)
            avg = np.nanmean(np.array(all_trials), axis=0)
            std = np.nanstd(np.array(all_trials), axis=0)
            # print(len(frames), len(avg))
            sns.lineplot(x=frames, y=avg, color=color[g], linestyle=style[g], linewidth=4,
                         label=f"T{g + 1}-{joints_to_plot[g]} (n = {len(all_trials)})")
            ax.fill_between(frames, avg - std, avg + std, color=color[g], alpha=0.2)
        plt.axvline(0, color="black", linestyle="dashed", label="MOC")
        self.formatting(ax, [-0.5, 0, 0.5], [0, 90, 180], xlabel="seconds (s)", ylabel=f"{Name} joint angle")
        sns.despine(trim=True)
        plt.legend()
        plt.savefig(f"{Contact_type}_Contact_{Name}_change.pdf")
        plt.show()"""


    def formatting(self, ax, xticks=None, yticks=None, xlabel=None, ylabel=None, yticklabel=None, xticklabel=None, ylabel_size=10, xlabel_size=10, spine_width=3, tick_width=3):
        """
        Format matplotlib axes consistently.

        Parameters
        ----------
        ax : matplotlib axis or iterable of axes
            Single axis or list/array of axes.
        xticks : list or array, optional
        yticks : list or array, optional
        xlabel : str, optional
        ylabel : str, optional
        spine_width : int or float
        tick_width : int or float
        """

        # Make sure ax is iterable
        if not isinstance(ax, (list, tuple, np.ndarray)):
            axes = [ax]
        else:
            axes = ax.flatten() if isinstance(ax, np.ndarray) else ax

        for a in axes:

            # --- Remove top and right spines ---
            # a.spines["top"].set_visible(False)
            # a.spines["right"].set_visible(False)

            # --- Set spine thickness ---
            a.spines["left"].set_linewidth(spine_width)
            a.spines["bottom"].set_linewidth(spine_width)


            # --- Set tick thickness ---
            a.tick_params(
                axis='both',
                width=tick_width,
                length=6
            )

            # --- Set ticks ---
            if xticks is not None:
                a.set_xticks(xticks)
            if yticks is not None:
                a.set_yticks(yticks)

            # --- Set labels ---
            if xlabel is not None:
                a.set_xlabel(xlabel, fontsize=xlabel_size)
            if ylabel is not None:
                a.set_ylabel(ylabel, fontsize=ylabel_size)

            if yticklabel is not None:
                a.set_ticklabel(yticklabel, axis="y")

    def centered_shades(self, color, n_shades=5, spread=0.6):
        import matplotlib.colors as mcolors
        """
        Generate shades centered on the input color.

        Parameters:
            color (str or tuple): any matplotlib-valid color
            n_shades (int): must be odd to perfectly center
            spread (float): how far to move toward white/black (0–1)

        Returns:
            List of RGB tuples
        """
        if n_shades % 2 == 0:
            raise ValueError("n_shades should be odd to center on base color.")

        base_rgb = np.array(mcolors.to_rgb(color))

        # symmetric factors around 0
        factors = np.linspace(-spread, spread, n_shades)

        shades = []
        for f in factors:
            if f < 0:
                # darken (toward black)
                new_color = base_rgb * (1 + f)
            else:
                # lighten (toward white)
                new_color = base_rgb + (1 - base_rgb) * f
            shades.append(tuple(new_color))

        return shades

    def plot_latency_bin(self, group_info:Group):
        self.angles = [["L-fBC", "L-fCT", "L-fFT"],
                       ["L-mBC", "L-mCT", "L-mFT"],
                       ["L-hBC", "L-hCT", "L-hFT"],

                       ["L-fCT", "L-fFT", "L-fTT"],
                       ["L-mCT", "L-mFT", "L-mTT"],
                       ["L-hCT", "L-hFT", "L-hTT"],

                       ["L-fFT", "L-fTT", "L-fLT"],
                       ["L-mFT", "L-mTT", "L-mLT"],
                       ["L-hFT", "L-hTT", "L-hLT"],

                       ["R-fBC", "R-fCT", "R-fFT"],
                       ["R-mBC", "R-mCT", "R-mFT"],
                       ["R-hBC", "R-hCT", "R-hFT"],

                       ["R-fCT", "R-fFT", "R-fTT"],
                       ["R-mCT", "R-mFT", "R-mTT"],
                       ["R-hCT", "R-hFT", "R-hTT"],

                       ["R-fFT", "R-fTT", "R-fLT"],
                       ["R-mFT", "R-mTT", "R-mLT"],
                       ["R-hFT", "R-hTT", "R-hLT"]]

        start = -0.1
        end = 0.7
        tnorm = False
        threshold = None
        group_data = self.analyzer.Calculate_angle_traces(group_info, self.angles, threshold, start, end, tnorm, False)

        normalization = ""
        if tnorm:
            seconds = [s / 250 for s in range(250)]
            xtick = [0, 1]
            xtick_label = ["MOC", "MOL"]
            normalization = "_tnorm"
        else:
            seconds = [s / 250 for s in range(int(start * 250), int(end * 250))]
            xtick = [start, 0, end]
            xtick_label = [str(start), "MOC", str(end)]

        threshold_bins = [0.3, 0.68, 1, -1]
        # fig, ax = plt.subplots(5, 1, figsize=(5, 15))
        """colors = self.centered_shades("red", 5)
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        indi = True
        joints_to_plot = ["L-fCT"]
        for j, joint in enumerate(joints_to_plot):
            for th, ll_threshold in enumerate(threshold_bins):
                if not indi:
                    signal_info = [(fps, trace) for fly_data in T1_data for ll, fps, trace in fly_data[joint] if ll == ll_threshold]
                    stacked = [trace for fly_data in T1_data for ll, fps, trace in fly_data[joint] if ll == ll_threshold]
                    for sig in signal_info:
                        sns.lineplot(x=seconds, y=sig[1], ax=ax[th], linewidth=1, color="lightgrey")
                    sns.lineplot(x=seconds, y=np.array(stacked).mean(axis=0), ax=ax[th], linewidth=4, color=colors[th], label=f"latency < {ll_threshold} (n = {len(stacked)})")
                    ax[th].set_xticklabels(xtick_label)
                    if tnorm:
                        self.formatting(ax[th], xticks=xtick, yticks=[0, 90, 180], ylabel=f"{joint} angle", xlabel_size=10, ylabel_size=10)
                    else:
                        ax[th].axvline(0, color="black", linestyle="dashed")
                        self.formatting(ax[th], xticks=xtick, xlabel="second (s)", yticks=[0, 90, 180], ylabel=f"{joint} angle", xlabel_size=10, ylabel_size=10)
                else:
                    stacked = [trace for fly_data in T1_data for ll, fps, trace in fly_data[joint] if ll == ll_threshold]
                    sns.lineplot(x=seconds, y=np.array(stacked).mean(axis=0), ax=ax, linewidth=4, color=colors[th], label=f"latency < {ll_threshold} (n = {len(stacked)})")
                    ax.set_xticklabels(xtick_label)
                    if tnorm:
                        self.formatting(ax, xticks=xtick, yticks=[0, 90, 180], ylabel=f"{joint} angle",
                                        xlabel_size=10, ylabel_size=10)
                    else:
                        ax.axvline(0, color="black", linestyle="dashed")
                        self.formatting(ax, xticks=xtick, xlabel="second (s)", yticks=[0, 90, 180],
                                        ylabel=f"{joint} angle", xlabel_size=10, ylabel_size=10)
            sns.despine(trim=True)
            plt.tight_layout()
            plt.savefig(f"{joint}_tnorm_ALL_bins.pdf")
            plt.show()
            plt.close()"""

        joints_groups = [["L-fCT", "L-mCT", "L-hCT", "R-fCT", "R-mCT", "R-hCT"],
                         ["L-fFT", "L-mFT", "L-hFT", "R-fFT", "R-mFT", "R-hFT"]]
        for jg in joints_groups:
            colors = ["red", "green", "blue", "orange", "grey", "brown"]
            fig, ax = plt.subplots(3, 2, figsize=(10, 15))
            ax = ax.flatten(order="F")
            for j, joint in enumerate(jg):
                color_shades = self.centered_shades(colors[j], len(threshold_bins) + 1)
                for l, ll_threshold in enumerate(threshold_bins):
                    stacked = [trace for fly_data in group_data for ll, index, fps, trace in fly_data[joint] if ll == ll_threshold]
                    if len(stacked) == 0:
                        continue

                    mean = np.array(stacked).mean(axis=0)
                    if j == 0:
                        sns.lineplot(x=seconds, y=mean, ax=ax[j], linewidth=4,
                                     color=color_shades[l], label=f"n = {len(stacked)}")
                    else:
                        sns.lineplot(x=seconds, y=mean, ax=ax[j], linewidth=4,
                                     color=color_shades[l])
                    ax[j].set_xticklabels(xtick_label)
                    if tnorm:
                        self.formatting(ax[j], xticks=xtick, yticks=[0, 90, 180], ylabel=f"{joint} angle")
                    else:
                        # print(joint)
                        ax[j].axvline(0, color="black", linestyle="dashed")
                        self.formatting(ax[j], xticks=xtick, xlabel="second (s)", yticks=[0, 90, 180],
                                        ylabel=f"{joint} angle")
            ax[0].legend(
                fontsize=20,
                borderpad=0.1,  # padding inside box
                labelspacing=0.2,  # vertical spacing between entries
                handlelength=2,  # line length in legend
                handletextpad=1.5  # space between marker and text
            )
            sns.despine(trim=True)
            plt.tight_layout()
            plt.savefig(f"T2_{jg[0][3:]}_{group_info.group_name}_LL_bins.pdf")
            # plt.show()
            plt.close()
    def plot_landing_profile(self, group_info:Group, leg_contact, leg_extension, leg_searches, secondary_contact):
        if leg_contact:
            os.chdir(r"C:\Users\agrawal-admin\Desktop\Landing\Landing Profile\Leg contact")
            self.plot_contact_leg(group_info)
        if leg_extension:
            os.chdir(r"C:\Users\agrawal-admin\Desktop\Landing\Landing Profile\Leg extension")
            self.plot_leg_extension(group_info)
        if leg_searches:
            os.chdir(r"C:\Users\agrawal-admin\Desktop\Landing\Landing Profile\Leg searches")
            self.plot_leg_searches(group_info)
        if secondary_contact:
            os.chdir(r"C:\Users\agrawal-admin\Desktop\Landing\Landing Profile\Secondary contact")
            self.plot_Inidi_Leg_Contact(group_info)
    def plot_IT_vs_OT(self, group_info=None):
        inward_touch_ll = pd.read_excel(r"C:\Users\agrawal-admin\Desktop\LandingDataSummary\Others\WT-T2-TiTa_new_OT_filtered.xlsx")
        outward_touch_ll = pd.read_excel(r"C:\Users\agrawal-admin\Desktop\LandingDataSummary\Others\WT-T2-TiTa_new_IT_filtered.xlsx")
        ot_index = []
        it_index = []
        for row, values in outward_touch_ll.iterrows():
            for t in range(4, 21):
                if (isinstance(values[t], float) or isinstance(values[t], int)):
                    if values[t] >= -1 and row + 1 in group_info.good_fly_index:
                        ot_index.append((row + 1, t))

        for row, values in inward_touch_ll.iterrows():
            for t in range(4, 21):
                if (isinstance(values[t], float) or isinstance(values[t], int)):
                    if values[t] >= -1 and row + 1 in group_info.good_fly_index:
                        it_index.append((row + 1, t))
        print(len(it_index), len(ot_index))
        indi_legs = ["L-f", "L-m", "L-h"]
        contact_leg_angle = [["R-mCT", "R-mFT", "R-mTT"]]
        color = ["red", "green", "blue", "orange", "brown"]
        threshold = 0.71
        stat = dict()
        stat["Group"] = []
        stat["mean"] = []
        stat["std"] = []


        IT_LS_data, OT_LS_data, Success_LS_data, Failed_LS_data, IT_Success_LS, IT_Failed_LS, OT_Success_LS, OT_Failed_LS = self.analyzer.combine_data(group_info, "LS", True, it_index, ot_index)
        IT_SC_data, OT_SC_data, Success_SC_data, Failed_SC_data, IT_Success_SC, IT_Failed_SC, OT_Success_SC, OT_Failed_SC = self.analyzer.combine_data(group_info, "SC", True, it_index, ot_index)

        fig, ax = plt.subplots(1, 1, figsize=(7, 7))
        sns.histplot(IT_LS_data["sum"], ax=ax, color="deepskyblue", stat="probability", kde=True, binwidth=1, label=f"IT (n = {len(IT_LS_data['sum'])})")
        sns.histplot(OT_LS_data["sum"], ax=ax, color="orangered", stat="probability", kde=True, binwidth=1, label=f"OT (n = {len(OT_LS_data['sum'])})")
        self.formatting(ax, xticks=[0, 5, 10, 15, 20], xlabel="time (s)", yticks=[0, 0.5])
        stat["Group"].append("IT-LS")
        stat["Group"].append("OT-LS")
        stat["mean"].append(np.mean(IT_LS_data["sum"]))
        stat["mean"].append(np.mean(OT_LS_data["sum"]))
        stat["std"].append(np.std(IT_LS_data["sum"]))
        stat["std"].append(np.std(OT_LS_data["sum"]))
        print("LS IT vs OT", self.calculator.Bootstrapping_test(IT_LS_data["sum"], OT_LS_data["sum"], 30000))
        ax.legend()
        sns.despine(trim=True, offset=5)
        plt.savefig(f"ITvsOT-LegSearch.pdf")
        plt.close()

        fig, ax = plt.subplots(1, 1, figsize=(7, 7))
        sns.histplot(Success_LS_data["sum"], ax=ax, color="dimgrey", stat="probability", kde=True, binwidth=1, label=f"Success (n = {len(Success_LS_data['sum'])})")
        sns.histplot(Failed_LS_data["sum"], ax=ax, color="lightgrey", stat="probability", kde=True, binwidth=1, label=f"Failed (n = {len(Failed_LS_data['sum'])})")
        self.formatting(ax, xticks=[0, 5, 10, 15, 20], xlabel="time (s)", yticks=[0, 0.5])
        print("LS S vs F", self.calculator.Bootstrapping_test(Success_LS_data["sum"], Failed_LS_data["sum"], 30000))
        stat["Group"].append("Success-LS")
        stat["Group"].append("Failed-LS")
        stat["mean"].append(np.mean(Success_LS_data["sum"]))
        stat["mean"].append(np.mean(Failed_LS_data["sum"]))
        stat["std"].append(np.std(Success_LS_data["sum"]))
        stat["std"].append(np.std(Failed_LS_data["sum"]))
        ax.legend()
        sns.despine(trim=True, offset=5)
        plt.savefig(f"SvsF-LegSearch.pdf")
        plt.close()


        fig, ax = plt.subplots(1, 1, figsize=(7, 7))
        sns.histplot(IT_SC_data["SC"], ax=ax, color="deepskyblue", stat="probability", kde=True, bins=np.arange(0, 0.75, 0.05), label=f"IT (n = {len(IT_SC_data['SC'])})")
        sns.histplot(OT_SC_data["SC"], ax=ax, color="orangered", stat="probability", kde=True, bins=np.arange(0, 0.75, 0.05), label=f"OT (n = {len(OT_SC_data['SC'])})")
        self.formatting(ax, xticks=[0, 0.7], xlabel="time (s)", yticks=[0, 0.5])
        print("SC IT vs OT", self.calculator.Bootstrapping_test(IT_SC_data["SC"], OT_SC_data["SC"], 30000))
        stat["Group"].append("IT-SC")
        stat["Group"].append("OT-SC")
        stat["mean"].append(np.mean(IT_SC_data["SC"]))
        stat["mean"].append(np.mean(OT_SC_data["SC"]))
        stat["std"].append(np.std(IT_SC_data["SC"]))
        stat["std"].append(np.std(OT_SC_data["SC"]))
        sns.despine(trim=True, offset=5)
        ax.legend()
        plt.savefig(f"ITvsOT-SecondaryContact.pdf")
        plt.close()

        fig, ax = plt.subplots(1, 1, figsize=(7, 7))
        sns.histplot(Success_SC_data["SC"], ax=ax, color="dimgrey", stat="probability", kde=True, bins=np.arange(0, 0.75, 0.05), label=f"Success (n = {len(Success_SC_data['SC'])})")
        sns.histplot(Failed_SC_data["SC"], ax=ax, color="lightgrey", stat="probability", kde=True, bins=np.arange(0, 0.75, 0.05), label=f"Failed (n = {len(Failed_SC_data['SC'])})")
        self.formatting(ax, xticks=[0, 0.7], xlabel="time (s)", yticks=[0, 0.5])
        print("SC S vs F", self.calculator.Bootstrapping_test(IT_SC_data["SC"], OT_SC_data["SC"], 30000))
        sns.despine(trim=True, offset=5)
        stat["Group"].append("Success-SC")
        stat["Group"].append("Failed-SC")
        stat["mean"].append(np.mean(Success_SC_data["SC"]))
        stat["mean"].append(np.mean(Failed_SC_data["SC"]))
        stat["std"].append(np.std(Success_SC_data["SC"]))
        stat["std"].append(np.std(Failed_SC_data["SC"]))
        ax.legend()
        plt.savefig(f"SvF-SecondaryContact.pdf")
        plt.close()

        color1 = self.centered_shades("green", 5)[4]
        color2 = self.centered_shades("red", 5)[4]
        color3 = self.centered_shades("purple", 5)[4]
        color4 = self.centered_shades("blue", 5)[4]
        fig, ax = plt.subplots(1, 1, figsize=(7, 7))
        sns.histplot(IT_Success_LS["sum"], ax=ax, color=color1, stat="probability", kde=True, binwidth=1, label=f"IT Success (n = {len(IT_Success_LS['sum'])})")
        sns.histplot(IT_Failed_LS["sum"], ax=ax, color=color2, stat="probability", kde=True, binwidth=1, label=f"IT Failed (n = {len(IT_Failed_LS['sum'])})")
        sns.histplot(OT_Success_LS["sum"], ax=ax, color=color3, stat="probability", kde=True, binwidth=1, label=f"OT Success (n = {len(OT_Success_LS['sum'])})")
        sns.histplot(OT_Failed_LS["sum"], ax=ax, color=color4, stat="probability", kde=True, binwidth=1, label=f"OT Failed (n = {len(OT_Failed_LS['sum'])})")
        self.formatting(ax, xticks=[0, 5, 10, 15, 20], xlabel="time (s)", yticks=[0, 0.5])
        stat["Group"].append("SU-IT-LS")
        stat["Group"].append("FA-IT-LS")
        stat["Group"].append("SU-OT-LS")
        stat["Group"].append("FA-OT-LS")
        stat["mean"].append(np.mean(IT_Success_LS["sum"]))
        stat["mean"].append(np.mean(IT_Failed_LS["sum"]))
        stat["mean"].append(np.mean(OT_Success_LS["sum"]))
        stat["mean"].append(np.mean(OT_Failed_LS["sum"]))
        stat["std"].append(np.std(IT_Success_LS["sum"]))
        stat["std"].append(np.std(IT_Failed_LS["sum"]))
        stat["std"].append(np.std(OT_Success_LS["sum"]))
        stat["std"].append(np.std(OT_Failed_LS["sum"]))
        ax.legend()
        sns.despine(trim=True, offset=5)
        plt.savefig(f"S-F_vs_IT-OT-LegSearch.pdf")
        plt.close()

        fig, ax = plt.subplots(1, 1, figsize=(7, 7))
        sns.histplot(IT_Success_SC["SC"], ax=ax, color=color1, stat="probability", kde=True, bins=np.arange(0, 0.75, 0.05), label=f"IT Success (n = {len(IT_Success_SC['SC'])})")
        sns.histplot(IT_Failed_SC["SC"], ax=ax, color=color2, stat="probability", kde=True, bins=np.arange(0, 0.75, 0.05), label=f"IT Failed (n = {len(IT_Failed_SC['SC'])})")
        sns.histplot(OT_Success_SC["SC"], ax=ax, color=color3, stat="probability", kde=True, bins=np.arange(0, 0.75, 0.05), label=f"OT Success (n = {len(OT_Success_SC['SC'])})")
        sns.histplot(OT_Failed_SC["SC"], ax=ax, color=color4, stat="probability", kde=True, bins=np.arange(0, 0.75, 0.05), label=f"OT Failed (n = {len(OT_Failed_SC['SC'])})")
        self.formatting(ax, xticks=[0, 0.7], xlabel="time (s)", yticks=[0, 0.5])
        sns.despine(trim=True, offset=5)
        ax.legend()
        plt.savefig(f"S-F_vs_IT-OT-SecondaryContact.pdf")
        plt.close()
        stat["Group"].append("SU-IT-SC")
        stat["Group"].append("FA-IT-SC")
        stat["Group"].append("SU-OT-SC")
        stat["Group"].append("FA-OT-SC")
        stat["mean"].append(np.mean(IT_Success_SC["SC"]))
        stat["mean"].append(np.mean(IT_Failed_SC["SC"]))
        stat["mean"].append(np.mean(OT_Success_SC["SC"]))
        stat["mean"].append(np.mean(OT_Failed_SC["SC"]))
        stat["std"].append(np.std(IT_Success_SC["SC"]))
        stat["std"].append(np.std(IT_Failed_SC["SC"]))
        stat["std"].append(np.std(OT_Success_SC["SC"]))
        stat["std"].append(np.std(OT_Failed_SC["SC"]))
        pd.DataFrame(stat).to_csv("IT vs OT-stat.csv")
        """success_ot, failed_ot = self.manipulator.read_leg_search_data(self.analyzer.Analyze_leg_search(group_info, ot_index, "OT", 0.71), indi_legs)
        success_it, failed_it = self.manipulator.read_leg_search_data(self.analyzer.Analyze_leg_search(group_info, it_index, "IT", 0.71), indi_legs)
        self.plot_ON_OFF_LS_and_SC(success_ot, failed_ot, success_it, failed_it, group_info.group_name, "OT", "IT", [0, 5, 10, 15], "Number of searches", "LegSearch")
        self.plot_SvF_LS_and_SC(pd.concat([success_ot, success_it]), pd.concat([failed_ot, failed_it]), group_info.group_name, [0, 5, 10, 15], "Number of searches", "LegSearch")
        print("Leg search done")
        success_ot, failed_ot = self.manipulator.read_secondary_contact_data(self.analyzer.AnalyzeSecondaryContact(ot_index, group_info, 0.71, "OT"), indi_legs)
        success_it, failed_it = self.manipulator.read_secondary_contact_data(self.analyzer.AnalyzeSecondaryContact(it_index, group_info, 0.71, "IT"), indi_legs)
        self.plot_ON_OFF_LS_and_SC(success_ot, failed_ot, success_it, failed_it, group_info.group_name, "OT", "IT", [0, 0.7], "Time (s)", "SecondaryContact")
        self.plot_SvF_LS_and_SC(pd.concat([success_ot, success_it]), pd.concat([failed_ot, failed_it]), group_info.group_name, [0, 0.7], "Time (s)", "SecondaryContact")
        print("Secondary done")"""
        """success_ot_ang_v, success_ot_ft_ang, success_ot_proj_ang, failed_ot_ang_v, failed_ot_ft_ang, failed_ot_proj_ang = self.analyzer.Calculate_contact_leg_metrices(group_info, ot_index, contact_leg_angle, threshold)
        success_it_ang_v, success_it_ft_ang, success_it_proj_ang, failed_it_ang_v, failed_it_ft_ang, failed_it_proj_ang = self.analyzer.Calculate_contact_leg_metrices(group_info, it_index, contact_leg_angle, threshold)
        print("Angular done")
        self.plot_posture_metrics_multi_groups([success_ot_ang_v, failed_ot_ang_v, success_it_ang_v, failed_it_ang_v],
                                               ["OT-Success", "OT-Failed", "IT-Success", "IT-Failed"],
                                               [-300, -200, -100, 0, 100, 200, 300, 400, 500],
                                               "T2-R-mFT angular velocity (degree°/s)",
                                               group_info.group_name, "ang_v-OTvIT-SvF")


        self.plot_posture_metrics(success_ot_ang_v + failed_ot_ang_v, success_it_ang_v + failed_it_ang_v,
                                  "OT", "IT",
                                  [-300, -200, -100, 0, 100, 200, 300, 400, 500],
                                  "T2-R-mFT angular velocity (degree°/s)",
                                  group_info.group_name, "ang_v-OTvIT", ["orangered", "deepskyblue"])

        su_color = self.centered_shades("grey", 5)[1]
        fa_color = self.centered_shades("grey", 5)[3]
        self.plot_posture_metrics(success_ot_ang_v + success_it_ang_v, failed_ot_ang_v + failed_it_ang_v,
                                  "Success", "Failed",
                                  [-300, -200, -100, 0, 100, 200, 300, 400, 500],
                                  "T2-R-mFT angular velocity (degree°/s)",
                                  group_info.group_name, "ang_v-SvF", [su_color, fa_color])

        self.plot_posture_metrics(success_ot_ft_ang + success_it_ft_ang, failed_ot_ft_ang + failed_it_ft_ang,
                                  "Success", "Failed",
                                  [0, 90, 180],
                                  "T2-R-mFT angle (degree°)",
                                  group_info.group_name, "ang_ft-SvF", [su_color, fa_color])

        self.plot_posture_metrics(success_ot_ft_ang + failed_ot_ft_ang, success_it_ft_ang + failed_it_ft_ang,
                                  "OT", "IT",
                                  [0, 90, 180],
                                  "T2-R-mFT angle (degree°)",
                                  group_info.group_name, "ang_ft-OTvIT", ["orangered", "deepskyblue"])"""

    def plot_Opto_data(self, group_info:Group):
        print(group_info.group_name)
        indi_legs = ["L-f", "L-m", "L-h"]
        contact_leg_angle = [["R-mCT", "R-mFT", "R-mTT"]]
        threshold = 0.71
        index_to_iterate = group_info.get_targeted_trials(["Landing", "Flying"])
        LO_index = []
        NL_index = []
        for index in index_to_iterate:
            if "_NL_" in group_info.fly_kinematic_data_path[f"F{index[0]}T{index[1]}"]:
                NL_index.append(index)
            else:
                LO_index.append(index)
        """ON_success, ON_failed = self.manipulator.read_leg_search_data(self.analyzer.Analyze_leg_search(group_info, LO_index, "ON"), indi_legs)
        OFF_success, OFF_failed = self.manipulator.read_leg_search_data(self.analyzer.Analyze_leg_search(group_info, NL_index, "OFF"), indi_legs)
        self.plot_SvF_LS_and_SC(pd.concat([ON_success, ON_failed]), pd.concat([OFF_success, OFF_failed]), group_info.group_name, [0, 5, 10, 15], "Number of searches", "LegSearch")

        ON_success, ON_failed = self.manipulator.read_secondary_contact_data(self.analyzer.AnalyzeSecondaryContact(LO_index, group_info, 0.71, "ON"), indi_legs)
        OFF_success, OFF_failed = self.manipulator.read_secondary_contact_data(self.analyzer.AnalyzeSecondaryContact(NL_index, group_info, 0.71, "OFF"), indi_legs)
        self.plot_SvF_LS_and_SC(pd.concat([ON_success, ON_failed]), pd.concat([OFF_success, OFF_failed]), group_info.group_name, [0, 0.7], "Time (s)", "SecondaryContact")"""

        """ON_success, ON_failed = self.manipulator.read_leg_search_data(self.analyzer.Analyze_leg_search(group_info, LO_index, "ON"), indi_legs)
        OFF_success, OFF_failed = self.manipulator.read_leg_search_data(self.analyzer.Analyze_leg_search(group_info, NL_index, "OFF"), indi_legs)
        self.plot_ON_OFF_LS_and_SC(ON_success, ON_failed, OFF_success, OFF_failed, group_info.group_name, "ON", "OFF", [0, 5, 10, 15], "Number of searches", "LegSearch")

        ON_success, ON_failed = self.manipulator.read_secondary_contact_data(self.analyzer.AnalyzeSecondaryContact(LO_index, group_info, 0.71, "ON"), indi_legs)
        OFF_success, OFF_failed = self.manipulator.read_secondary_contact_data(self.analyzer.AnalyzeSecondaryContact(NL_index, group_info, 0.71, "OFF"), indi_legs)
        self.plot_ON_OFF_LS_and_SC(ON_success, ON_failed, OFF_success, OFF_failed, group_info.group_name, "ON", "OFF", [0, 0.7], "Time (s)", "SecondaryContact")
        """
        success_off_ang_v, success_off_ft_ang, success_off_proj_ang, failed_off_ang_v, failed_off_ft_ang, failed_off_proj_ang = self.analyzer.Calculate_contact_leg_metrices(group_info, NL_index, contact_leg_angle, threshold)
        success_on_ang_v, success_on_ft_ang, success_on_proj_ang, failed_on_ang_v, failed_on_ft_ang, failed_on_proj_ang = self.analyzer.Calculate_contact_leg_metrices(group_info, LO_index, contact_leg_angle, threshold)
        print(len(success_off_ang_v), len(success_on_ang_v), len(failed_off_ang_v), len(failed_on_ang_v))

        self.plot_posture_metrics_multi_groups([success_on_ang_v, failed_on_ang_v, success_off_ang_v, failed_off_ang_v],
                                               ["ON-Success", "ON-Failed", "OFF-Success", "OFF-Failed"],
                                               [-300, -200, -100, 0, 100, 200, 300, 400, 500],
                                               "T2-R-mFT angular velocity (degree°/s)",
                                               group_info.group_name, "ang_v-ONvOFF-SvF")

        self.plot_posture_metrics(success_on_ang_v + failed_on_ang_v, success_off_ang_v + failed_off_ang_v,
                                  "ON", "OFF",
                                  [-300, -200, -100, 0, 100, 200, 300, 400, 500],
                                  "T2-R-mFT angular velocity (degree°/s)",
                                  group_info.group_name, "ang_v-ONvOFF")


    def plot_posture_metrics_multi_groups(self, data_groups, names, y_tick, y_label, group_name, type):
        import itertools
        color = ["blue", "deepskyblue", "red", "orangered"]

        fig, ax = plt.subplots(1, 1, figsize=(6, 6))
        ax.set_title(f"{group_name}-{type}")

        # ----- build dataframe -----
        Group = []
        Val = []

        cleaned_groups = []
        cleaned_names = []
        stat = dict()
        stat["mean"] = []
        stat["std"] = []
        stat["group"] = []

        for d in range(len(data_groups)):
            vals = pd.to_numeric(pd.Series(data_groups[d]), errors="coerce").dropna().tolist()

            # skip completely empty groups
            if len(vals) == 0:
                continue

            cleaned_groups.append(vals)
            cleaned_names.append(names[d])

            Group.extend([names[d]] * len(vals))
            Val.extend(vals)
            stat["mean"].append(np.mean(vals))
            stat["std"].append(np.std(vals))
            stat["group"].append(vals)
        pd.DataFrame(stat).to_csv(f"{group_name}-{type}-stat.csv")
        if len(cleaned_groups) < 2:
            print(f"Not enough valid groups to compare in {group_name}-{type}")
            return

        df = pd.DataFrame({"Group": Group, "Values": Val})

        # preserve plotting order
        order = cleaned_names

        group_stat = (
            df.groupby("Group")["Values"]
            .agg(["mean", "std", "count"])
            .reindex(order)
            .reset_index()
        )

        # ----- plot raw data + mean/std -----
        sns.stripplot(
            data=df,
            ax=ax,
            x="Group",
            y="Values",
            order=order,
            palette=color[:len(order)],
            size=12,
            alpha=0.3
        )

        sns.pointplot(
            data=group_stat,
            ax=ax,
            x="Group",
            y="mean",
            order=order,
            color="black",
            linestyles=" ",
            markers="s",
            errorbar=None,
            markersize=10,
            zorder=10
        )

        ax.errorbar(
            x=np.arange(len(order)),
            y=group_stat["mean"],
            yerr=group_stat["std"],
            fmt="none",
            color="black",
            capsize=10,
            zorder=10
        )

        # ----- pairwise comparisons -----
        def p_to_stars(p):
            if p < 0.0001:
                return "****"
            elif p < 0.001:
                return "***"
            elif p < 0.01:
                return "**"
            elif p < 0.05:
                return "*"
            else:
                return "ns"

        pairs = list(itertools.combinations(range(len(cleaned_groups)), 2))

        y_data_max = max(
            df["Values"].max(),
            (group_stat["mean"] + group_stat["std"].fillna(0)).max()
        )
        y_data_min = df["Values"].min()
        y_range = y_data_max - y_data_min

        if y_range == 0:
            y_range = 1

        bar_h = 0.05 * y_range
        text_offset = 0.01 * y_range
        current_y = y_data_max + bar_h

        for i, j in pairs:
            data1 = cleaned_groups[i]
            data2 = cleaned_groups[j]

            # skip if either group is empty
            if len(data1) == 0 or len(data2) == 0:
                continue

            p = self.calculator.Bootstrapping_test(data1, data2, 20000)
            stars = p_to_stars(p)

            x1, x2 = i, j

            ax.plot(
                [x1, x1, x2, x2],
                [current_y, current_y + bar_h, current_y + bar_h, current_y],
                lw=1.5,
                c="black"
            )
            ax.text(
                (x1 + x2) / 2,
                current_y + bar_h + text_offset,
                stars,
                ha="center",
                va="bottom",
                fontsize=12
            )

            current_y += 2 * bar_h

        self.formatting(ax, yticks=y_tick, ylabel=y_label)

        ax.set_xlim(-0.5, len(order) - 0.5)
        ax.set_ylim(top=current_y + bar_h)

        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"{group_name}-{type}.pdf")
        plt.close()
    def plot_posture_metrics(self, data1, data2, name1, name2, y_tick, y_label, group_name, type, color=None):
        if color is None:
            color = ["blue", "red"]
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        plt.title(f"{group_name}-{type}")
        df = pd.DataFrame({"Group": [name1] * len(data1) + [name2] * len(data2), "Values": data1 + data2})

        group_stat = df.groupby('Group')["Values"].agg(['mean', 'std', 'count']).reset_index()

        sns.stripplot(data=df, ax=ax, x="Group", y="Values", palette=color, size=15, alpha=0.3)
        sns.pointplot(x='Group', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None,
                      scale=2, zorder=10)
        plt.errorbar(x=group_stat['Group'], y=group_stat['mean'], yerr=group_stat['std'], fmt="none", color='black',
                     capsize=10, zorder=10)
        stat = dict()
        stat["mean"] = []
        stat["std"] = []
        stat["group"] = []
        stat["mean"].append(np.mean(data1))
        stat["std"].append(np.std(data1))
        stat["group"].append(name1)
        stat["mean"].append(np.mean(data2))
        stat["std"].append(np.std(data2))
        stat["group"].append(name2)
        pd.DataFrame(stat).to_csv(f"{group_name}-{type}-stat.csv")
        p = self.calculator.Bootstrapping_test(data1, data2, 20000)

        if p < 0.0001:
            stars = "****"
        elif p < 0.001:
            stars = "***"
        elif p < 0.01:
            stars = "**"
        elif p < 0.05:
            stars = "*"
        else:
            stars = "ns"

        # ----- draw significance bar -----
        x1, x2 = 0, 1

        # top of plotted data
        y_max = max(
            df["Values"].max(),
            (group_stat["mean"] + group_stat["std"]).max()
        )

        h = 0.05 * (df["Values"].max() - df["Values"].min())  # bar height
        if h == 0:
            h = 0.1

        y = y_max + h

        ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, c='black')
        ax.text((x1 + x2) / 2, y + h, stars, ha='center', va='bottom', fontsize=14)

        self.formatting(ax, yticks=y_tick, ylabel=y_label)
        ax.set_xlim(-1, 2)

        # make sure the star is not cut off
        ax.set_ylim(top=y + 3 * h)

        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"{group_name}-{type}.pdf")
        # plt.show()
        plt.close()

    def plot_ON_OFF_LS_and_SC(self, ONSdata, ONFdata, OFFSdata, OFFFdata, group_name, name1, name2, xtick, xlabel, type):
        indi_legs = ["L-f", "L-m", "L-h"]
        colors = ["red", "green", "blue", "orangered", "lime", "deepskyblue"]
        fig, ax = plt.subplots(6, 2, figsize=(8, 12))
        for l, leg in enumerate(indi_legs):

            ONS_vals = ONSdata[leg].dropna()
            ONF_vals = ONFdata[leg].dropna()
            OFFS_vals = OFFSdata[leg].dropna()
            OFFF_vals = OFFFdata[leg].dropna()
            if max(xtick) > 1:
                bins = np.arange(0, 16, 1)
            else:
                bins = np.arange(0, 0.75, 0.05)  # 0, 0.05, 0.10, ..., 0.70

            if len(ONS_vals) > 0:
                sns.histplot(
                    ONS_vals,
                    ax=ax[l * 2][0],
                    bins=bins,
                    color=colors[l],
                    stat="probability",
                    kde=False,
                    label=f"{name1}-Successful (n = {len(ONS_vals)})"
                )

            if len(ONF_vals) > 0:
                sns.histplot(
                    ONF_vals,
                    ax=ax[l * 2 + 1][0],
                    bins=bins,
                    color=colors[l + 3],
                    stat="probability",
                    kde=False,
                    label=f"{name1}-Failed (n = {len(ONF_vals)})"
                )

            if len(OFFS_vals) > 0:
                sns.histplot(
                    OFFS_vals,
                    ax=ax[l * 2][1],
                    bins=bins,
                    color=colors[l],
                    stat="probability",
                    kde=False,
                    label=f"{name2}-Successful (n = {len(OFFS_vals)})"
                )

            if len(OFFF_vals) > 0:
                sns.histplot(
                    OFFF_vals,
                    ax=ax[l * 2 + 1][1],
                    bins=bins,
                    color=colors[l + 3],
                    stat="probability",
                    kde=False,
                    label=f"{name2}-Failed (n = {len(OFFF_vals)})"
                )

        ax[0][0].set_title(f"{name1} trials")
        ax[0][1].set_title(f"{name2} trials")

        for a in ax.flatten(order="F"):
            a.legend()

        self.formatting(ax, yticks=[0, 0.5, 1], xticks=xtick, xlabel=xlabel)
        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"{group_name}-{type}-{name1}v{name2}.pdf")
        # plt.show()
        plt.close()
    def plot_SvF_LS_and_SC(self, data1, data2, group_name, xtick, xlabel, type):
        indi_legs = ["L-f", "L-m", "L-h"]
        colors = ["red", "green", "blue", "orangered", "lime", "deepskyblue"]
        fig, ax = plt.subplots(3,2, figsize=(8, 12))
        for l, leg in enumerate(indi_legs):
            if max(xtick) > 1:
                bins = np.arange(0, 16, 1)
            else:
                bins = np.arange(0, 0.75, 0.05)
            Successful_vals = data1[leg].dropna()
            Failed_vals = data2[leg].dropna()

            if len(Successful_vals) > 0:
                sns.histplot(
                    Successful_vals,
                    ax=ax[l][0],
                    bins=bins,
                    color=colors[l],
                    stat="probability",
                    kde=False,
                    label=f"{leg}-ON (n = {len(Successful_vals)})"
                )

            if len(Failed_vals) > 0:
                sns.histplot(
                    Failed_vals,
                    ax=ax[l][1],
                    bins=bins,
                    color=colors[l + 3],
                    stat="probability",
                    kde=False,
                    label=f"{leg}-OFF (n = {len(Failed_vals)})"
                )

        for a in ax.flatten(order="F"):
            a.legend()

        self.formatting(ax, yticks=[0, 0.5, 1], xticks=xtick, xlabel=xlabel)
        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"{group_name}-{type}-SvF.pdf")
        # plt.show()
        plt.close()
    def plot_conv_data(self, group_info:Group):
        """indi_legs = ["L-f", "L-m", "L-h"]
        index_to_iterate = group_info.get_targeted_trials(["Landing"])
        Success, Failed = self.manipulator.read_leg_search_data(self.analyzer.Analyze_leg_search(group_info, index_to_iterate, group_info.group_name), indi_legs)
        self.plot_SvF_LS_and_SC(Success, Failed, group_info.group_name, [0, 5, 10, 15], "Number of searches", "LegSearch")

        Success, Failed = self.manipulator.read_secondary_contact_data(self.analyzer.AnalyzeSecondaryContact(index_to_iterate, group_info,  0.71), indi_legs)
        self.plot_SvF_LS_and_SC(Success, Failed, group_info.group_name, [0, 0.7], "Time (s)", "SecondaryContact")"""
        index_to_iterate = group_info.get_targeted_trials(["Landing"])
        threshold = 0.71
        (success_ang_v, success_ang_ft, success_ang_proj,
         failed_ang_v, failed_ang_ft, failed_ang_proj) = (self.analyzer.Calculate_contact_leg_metrices(group_info, index_to_iterate, [["R-mCT", "R-mFT", "R-mTT"]], threshold))

        self.plot_posture_metrics(success_ang_v, failed_ang_v,
                                  "Success", "Failed",
                                  [-300, -200, -100, 0, 100, 200, 300, 400, 500],
                                  "T2-R-mFT angular velocity (degree°/s)",
                                  group_info.group_name, "angular_v")

        """self.plot_posture_metrics(success_ang_ft, failed_ang_ft,
                                  "Success", "Failed",
                                  [0, 90, 180],
                                  "Flight posture (T2-R-mFT angle°)",
                                  group_info.group_name, "FT angle")

        self.plot_posture_metrics(success_ang_proj, failed_ang_proj,
                                  "Success", "Failed",
                                  [0, 180, 360],
                                  "Tarsus direction (°)",
                                  group_info.group_name, "Projection")"""

    def plot_chrimson_data(self, group_info:Group, color):
        index_to_iterate = group_info.get_targeted_trials(["Landing", "Flying"])
        indi_legs = ["L-f", "L-m", "L-h"]
        ON_index = []
        OFF_index = []

        for index in index_to_iterate:
            path = group_info.fly_kinematic_data_path[f"F{index[0]}T{index[1]}"]
            if "ON" in path or "LO" in path:
                ON_index.append(index)
            if "OFF" in path or "NL" in path:
                OFF_index.append(index)


        ON_success, ON_failed = self.manipulator.read_leg_search_data(self.analyzer.Analyze_leg_search_CHR(group_info, ON_index, "ON"), indi_legs)
        LS_data_ON = pd.concat([ON_success, ON_failed])
        combined = LS_data_ON.sum(axis=1).to_frame(name="sum")

        fig, ax = plt.subplots(1, 1, figsize=(7, 7))
        sns.histplot(combined["sum"], ax=ax, color=color, stat="probability", kde=True, binwidth=1, label=f"ON (n = {len(LS_data_ON['sum'])})")
        self.formatting(ax, xticks=[0, 5, 10, 15, 20], xlabel="time (s)", yticks=[0, 0.5])
        ax.legend()
        sns.despine(trim=True, offset=5)
        plt.savefig(f"{group_info.group_name}-LegSearch.pdf")
        plt.close()
    def plot_chrimson_LP(self, groups):
        angs = [["L-wing", "L-wing-hinge", "R-wing"]]
        collected_data = dict()
        collected_data["GroupName"] = []
        collected_data["Values"] = []
        collected_LP = dict()
        collected_LP["GroupName"] = []
        collected_LP["Values"] = []
        for group_info in groups:
            ON_index = []
            OFF_index = []
            index_to_iterate = group_info.get_targeted_trials(["Landing", "Flying"])
            for index in index_to_iterate:
                path = group_info.fly_kinematic_data_path[f"F{index[0]}T{index[1]}"]
                if "ON" in path or "LO" in path:
                    ON_index.append(index)
                if "OFF" in path or "NL" in path:
                    OFF_index.append(index)

            last_fly = ON_index[0][0]
            flying_num = 0
            landing_num = 0
            for index in ON_index:
                trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
                wing_angle = self.calculator.Calculate_joint_angle(trial_info, angs)["L-wing-hinge"][750:1250]
                MOL = self.detector.detect_landing(wing_angle)

                if MOL == -1 or (MOL / 250) > 0.71:
                    flying_num += 1
                else:
                    landing_num += 1
                    collected_data["GroupName"].append(group_info.group_name)
                    collected_data["Values"].append(MOL / 250)
                if last_fly != index[0] or index == ON_index[-1]:
                    collected_LP["GroupName"].append(group_info.group_name)
                    collected_LP["Values"].append(landing_num / (landing_num + flying_num))
                    flying_num = 0
                    landing_num = 0
                    last_fly = index[0]


        color = ["magenta", "green", "red", "orange", "brown", "blue"]
        dim_color = []
        for c in color:
            dim_color.append(self.centered_shades(c, 5)[3])
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        collected_data = pd.DataFrame(collected_data)
        group_order_LL = [g.group_name for g in groups if g.group_name in collected_data["GroupName"].unique()]
        sns.stripplot(data=collected_data, x="GroupName", y="Values", ax=ax, alpha=0.5, size=15, palette=color)
        group_stat = collected_data.groupby('GroupName')["Values"].agg(['mean', 'std', 'count']).reset_index()
        sns.pointplot(x='GroupName', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None, scale=2, zorder=10)
        plt.errorbar(x=group_stat['GroupName'], y=group_stat['mean'], yerr=group_stat['std'], fmt="none", color='black', capsize=10, zorder=10)
        self.formatting(ax, yticks=[0, 1], ylabel="Landing latency (s)")
        sns.despine(trim=True, offset=5)
        plt.savefig(f"Chr-LL.pdf")

        # p-value table for landing latency
        LL_p_table = self.pairwise_bootstrap_table(
            df=collected_data,
            group_col="GroupName",
            value_col="Values",
            group_order=group_order_LL)
        print(LL_p_table)
        # plt.show()

        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        collected_LP = pd.DataFrame(collected_LP)
        group_order_LP = [g.group_name for g in groups if g.group_name in collected_LP["GroupName"].unique()]
        sns.stripplot(data=collected_LP, x="GroupName", y="Values", ax=ax, alpha=0.5, palette=color, size=15)
        group_stat = collected_LP.groupby('GroupName')["Values"].agg(['mean', 'std', 'count']).reset_index()
        sns.pointplot(x='GroupName', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None, scale=2, zorder=10)
        plt.errorbar(x=group_stat['GroupName'], y=group_stat['mean'], yerr=group_stat['std'], fmt="none", color='black', capsize=10, zorder=10)
        self.formatting(ax, yticks=[0, 1], ylabel="Landing probability")
        sns.despine(trim=True, offset=5)
        plt.savefig(f"Chr-LP.pdf")

        LP_p_table = self.pairwise_bootstrap_table(
            df=collected_LP,
            group_col="GroupName",
            value_col="Values",
            group_order=group_order_LP
        )

        # optional save
        LL_p_table.to_csv("Chr-LL-pvalues.csv")
        LP_p_table.to_csv("Chr-LP-pvalues.csv")

        # plt.show()

    def plot_ft_ang_over_trials(self, groups):
        import matplotlib.cm as cm
        cmap = cm.get_cmap('viridis', len(groups))
        colors = [cmap(i) for i in range(len(groups))]
        fig, ax = plt.subplots(3, 3, figsize=(12, 12))
        trials = [t + 1 for t in range(20)]
        ax = ax.flatten(order="F")
        for g, group_info in enumerate(groups):
            index_to_iterate = group_info.get_targeted_trials(["Landing", "Flying"])
            collected_data = []
            for t in range(group_info.trial_num):
                trials_data = []
                for f in group_info.good_fly_index:
                    if (f, t + 1) in index_to_iterate:
                        trial_info = group_info.fly_kinematic_data[f"F{f}T{t + 1}"]
                        ft_ang = np.mean(self.calculator.Calculate_joint_angle(trial_info, [["R-mCT", "R-mFT", "R-mTT"]])["R-mFT"][:200])
                        trials_data.append(ft_ang)
                    else:
                        trials_data.append(np.nan)
                collected_data.append(trials_data)

            trials_mean = np.nanmean(np.array(collected_data), axis=1)
            trials_std = np.nanstd(np.array(collected_data), axis=1)

            sns.lineplot(x=trials, y=trials_mean, ax=ax[g], color=colors[g], linewidth=5)
            ax[g].fill_between(trials, trials_mean - trials_std, trials_mean + trials_std, color=colors[g], alpha=0.3)
            ax[g].set_title(f"{group_info.group_name}")

        self.formatting(ax, xticks=[1, 10, 20], xlabel="trials", yticks=[0, 45, 90], ylabel="R-mFT angle")
        sns.despine(trim=True, offset=5)
        plt.tight_layout()
        plt.savefig("FT-change through trials.pdf")
        plt.show()
    def plot_ON_OFF_angle_change(self, group_info:Group):

        self.angles = [["R-mCT", "R-mFT", "R-mTT"]]

        start = -0.2
        end = 0.7
        tnorm = False
        threshold = 0.71

        index_to_iterate = group_info.get_targeted_trials(["Landing", "Flying"])

        ON_index = []
        OFF_index = []
        for index in index_to_iterate:
            path = group_info.fly_kinematic_data_path[f"F{index[0]}T{index[1]}"]
            if "ON" in path or "LO" in path:
                ON_index.append(index)
            if "OFF" in path or "NL" in path:
                OFF_index.append(index)

        ON_data = self.analyzer.Calculate_angle_traces(group_info, ON_index, self.angles, threshold, start, end, tnorm, False)
        OFF_data = self.analyzer.Calculate_angle_traces(group_info, OFF_index, self.angles, threshold, start, end, tnorm, False)

        color = self.centered_shades("grey", 5)

        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        frames = np.arange(int(start * 250), int(end * 250)) / 250

        ON_trials = []
        OFF_trials = []
        for fly_data in ON_data:
            ON_trials.extend([trace for flag, index, fps, trace in fly_data["R-mFT"]])

        for fly_data in OFF_data:
            OFF_trials.extend([trace for flag, index, fps, trace in fly_data["R-mFT"]])


        ON_avg = np.nanmean(np.array(ON_trials), axis=0)
        ON_std = np.nanstd(np.array(ON_trials), axis=0)
        OFF_avg = np.nanmean(np.array(OFF_trials), axis=0)
        OFF_std = np.nanstd(np.array(OFF_trials), axis=0)

        sns.lineplot(x=frames, y=ON_avg, color=color[3], linestyle="solid", linewidth=4, label=f"light on(n = {len(ON_trials)})")
        ax.fill_between(frames, ON_avg - ON_std, ON_avg + ON_std, color=color[3], alpha=0.2)

        sns.lineplot(x=frames, y=OFF_avg, color=color[1], linestyle="solid", linewidth=4, label=f"light off (n = {len(OFF_trials)})")
        ax.fill_between(frames, OFF_avg - OFF_std, OFF_avg + OFF_std, color=color[1], alpha=0.2)

        plt.axvline(0, color="black", linestyle="dashed", label="MOC")
        self.formatting(ax, [start, 0, end], [0, 90, 180], xlabel="seconds (s)", ylabel=f"T2-R-FT joint angle")
        sns.despine(trim=True)
        plt.legend()
        plt.savefig(f"{group_info.group_name}_ONvOFF_FT_change.pdf")
        plt.show()

    def plot_combined_LS_and_SC(self, groups, Opto, color):
        color1 = self.centered_shades(color, 5)[1]
        color2 = self.centered_shades(color, 5)[4]

        if not Opto:
            color = ["orange", "grey", "brown"]
            datas_to_compare = []
            stat = dict()
            stat["Group"] = []
            stat["mean"] = []
            stat["std"] = []
            fig, ax = plt.subplots(1, 1, figsize=(7, 7))
            for g, group_info in enumerate(groups):
                LS_data = self.analyzer.combine_data(group_info, "LS", False)
                datas_to_compare.append(LS_data["sum"])
                sns.histplot(LS_data["sum"], ax=ax, color=color[g], stat="probability", kde=True, binwidth=1, label=f"{group_info.group_name} (n = {len(LS_data['sum'])})")

                stat["Group"].append(group_info.group_name)
                stat["mean"].append(np.mean(LS_data["sum"]))
                stat["std"].append(np.std(LS_data["sum"]))
                print(f"Group: {group_info.group_name} Mean:{np.mean(LS_data['sum'])} STD: {np.std(LS_data['sum'])}")
            self.formatting(ax, xticks=[0, 5, 10, 15, 20, 25], xlabel="time (s)", yticks=[0, 0.5])
            ax.legend()
            sns.despine(trim=True, offset=5)
            plt.savefig(f"WT-LegSearch.pdf")
            plt.close()
            pd.DataFrame(stat).to_csv(f"WT-LS.csv")
            print("WT LS")
            print(self.calculator.Bootstrapping_test(datas_to_compare[0], datas_to_compare[1], 30000))
            print(self.calculator.Bootstrapping_test(datas_to_compare[0], datas_to_compare[2], 30000))
            print(self.calculator.Bootstrapping_test(datas_to_compare[1], datas_to_compare[2], 30000))


            datas_to_compare = []
            fig, ax = plt.subplots(1, 1, figsize=(7, 7))
            stat = dict()
            stat["Group"] = []
            stat["mean"] = []
            stat["std"] = []
            for g, group_info in enumerate(groups):

                SC_data = self.analyzer.combine_data(group_info, "SC", False)
                datas_to_compare.append(SC_data["SC"])
                sns.histplot(SC_data["SC"], ax=ax, color=color[g], stat="probability", kde=True, bins=np.arange(0, 0.75, 0.05), label=f"{group_info.group_name} (n = {len(SC_data['SC'])})")
                stat["Group"].append(group_info.group_name)
                stat["mean"].append(np.mean(SC_data['SC']))
                stat["std"].append(np.std(SC_data['SC']))
                print(f"Group: {group_info.group_name} Mean:{np.mean(SC_data['SC'])} STD: {np.std(SC_data['SC'])}")
            self.formatting(ax, xticks=[0, 0.7], xlabel="time (s)", yticks=[0, 0.5])
            sns.despine(trim=True, offset=5)
            ax.legend()
            plt.savefig(f"WT-SecondaryContact.pdf")
            plt.close()
            pd.DataFrame(stat).to_csv(f"WT-SC.csv")
            print("WT SC")
            print(self.calculator.Bootstrapping_test(datas_to_compare[0], datas_to_compare[1], 30000))
            print(self.calculator.Bootstrapping_test(datas_to_compare[0], datas_to_compare[2], 30000))
            print(self.calculator.Bootstrapping_test(datas_to_compare[1], datas_to_compare[2], 30000))
        else:
            stat = dict()
            stat["Group"] = []
            stat["mean"] = []
            stat["std"] = []

            fig, ax = plt.subplots(1, 1, figsize=(7, 7))
            for g, group_info in enumerate(groups):

                LS_data_ON, LS_data_OFF = self.analyzer.combine_data(group_info, "LS", True)
                sns.histplot(LS_data_ON["sum"], ax=ax, color=color2, stat="probability", kde=True, binwidth=1, label=f"ON (n = {len(LS_data_ON['sum'])})")
                sns.histplot(LS_data_OFF["sum"], ax=ax, color=color1, stat="probability", kde=True, binwidth=1, label=f"OFF (n = {len(LS_data_OFF['sum'])})")

                stat["Group"].append(group_info.group_name + "ON")
                stat["mean"].append(np.mean(LS_data_ON["sum"]))
                stat["std"].append(np.std(LS_data_ON["sum"]))

                stat["Group"].append(group_info.group_name + "OFF")
                stat["mean"].append(np.mean(LS_data_OFF["sum"]))
                stat["std"].append(np.std(LS_data_OFF["sum"]))
                pd.DataFrame(stat).to_csv(f"{group_info.group_name}-LS.csv")
                print(group_info.group_name, self.calculator.Bootstrapping_test(LS_data_ON["sum"], LS_data_OFF["sum"], 30000))
            self.formatting(ax, xticks=[0, 5, 10, 15, 20], xlabel="time (s)", yticks=[0, 0.5])
            ax.legend()
            sns.despine(trim=True, offset=5)
            plt.savefig(f"{groups[0].group_name}-LegSearch.pdf")
            plt.close()


            stat = dict()
            stat["Group"] = []
            stat["mean"] = []
            stat["std"] = []
            fig, ax = plt.subplots(1, 1, figsize=(7, 7))
            for g, group_info in enumerate(groups):

                SC_data_ON, SC_data_OFF = self.analyzer.combine_data(group_info, "SC", True)
                sns.histplot(SC_data_ON["SC"], ax=ax, color=color2, stat="probability", kde=True, bins=np.arange(0, 0.75, 0.05), label=f"ON (n = {len(SC_data_ON['SC'])})")
                sns.histplot(SC_data_OFF["SC"], ax=ax, color=color1, stat="probability", kde=True, bins=np.arange(0, 0.75, 0.05), label=f"OFF (n = {len(SC_data_OFF['SC'])})")

                stat["Group"].append(group_info.group_name + "ON")
                stat["mean"].append(np.mean(SC_data_ON['SC']))
                stat["std"].append(np.std(SC_data_ON['SC']))

                stat["Group"].append(group_info.group_name + "OFF")
                stat["mean"].append(np.mean(SC_data_OFF['SC']))
                stat["std"].append(np.std(SC_data_OFF['SC']))
                pd.DataFrame(stat).to_csv(f"{group_info.group_name}-SC.csv")
                print(group_info.group_name, self.calculator.Bootstrapping_test(SC_data_ON["SC"], SC_data_OFF["SC"], 30000))
            self.formatting(ax, xticks=[0, 0.7], xlabel="time (s)", yticks=[0, 0.5])
            sns.despine(trim=True, offset=5)
            ax.legend()
            plt.savefig(f"{groups[0].group_name}-SecondaryContact.pdf")
            plt.close()

    def plot_LS_vs_LL(self, group_info:Group, Opto=False, SC_path=None, LS_path=None):
        index_to_iterate = group_info.get_targeted_trials(["Landing", "Flying"])

        if Opto:
            ON_index = []
            for index in index_to_iterate:
                path = group_info.fly_kinematic_data_path[f"F{index[0]}T{index[1]}"]
                if "ON" in path or "LO" in path:
                    ON_index.append(index)

            data = self.analyzer.AnalyzeSecondaryContact(ON_index, group_info, 0.71, "ON")
            cols = data.filter(regex=r'^L-[fmh]').columns
            new_df = data[['Index']].copy()
            new_df['min_val'] = data[cols].replace(10000, np.nan).min(axis=1)
            new_df = new_df.dropna(subset=['min_val']).reset_index(drop=True)

            LL = []
            SC = []
            for i in range(len(new_df["Index"])):
                trial_info = group_info.fly_kinematic_data[f"F{new_df['Index'][i][0]}T{new_df['Index'][i][1]}"]
                if trial_info.mol != -1:
                    LL.append((trial_info.mol - trial_info.moc) / trial_info.fps)
                    SC.append(new_df['min_val'][i])

            sns.scatterplot(x=SC, y=LL)
            plt.show()

            Success, Failed = self.manipulator.read_leg_search_data(self.analyzer.Analyze_leg_search(group_info, ON_index, "ON"), ["L-f", "L-m", "L-h", "Index"])
            combined = pd.concat([Success, Failed])
            new_df = combined[['Index']].copy()
            new_df['sum'] = combined[['L-f', 'L-m', 'L-h']].sum(axis=1)
            LL = []
            LS = []
            for i in range(len(new_df["Index"])):
                trial_info = group_info.fly_kinematic_data[f"F{new_df['Index'][i][0]}T{new_df['Index'][i][1]}"]
                if trial_info.mol != -1:
                    LL.append((trial_info.mol - trial_info.moc) / trial_info.fps)
                    LS.append(new_df['sum'][i])

            sns.scatterplot(x=LS, y=LL)
            plt.show()









            OFF_index = []
            for index in index_to_iterate:
                path = group_info.fly_kinematic_data_path[f"F{index[0]}T{index[1]}"]
                if "OFF" in path or "NL" in path:
                    OFF_index.append(index)

            data = self.analyzer.AnalyzeSecondaryContact(OFF_index, group_info, 0.71, "OFF")
            cols = data.filter(regex=r'^L-[fmh]').columns
            new_df = data[['Index']].copy()
            new_df['min_val'] = data[cols].replace(10000, np.nan).min(axis=1)
            new_df = new_df.dropna(subset=['min_val']).reset_index(drop=True)

            LL = []
            SC = []
            for i in range(len(new_df["Index"])):
                trial_info = group_info.fly_kinematic_data[f"F{new_df['Index'][i][0]}T{new_df['Index'][i][1]}"]
                if trial_info.mol != -1:
                    LL.append((trial_info.mol - trial_info.moc) / trial_info.fps)
                    SC.append(new_df['min_val'][i])

            sns.scatterplot(x=SC, y=LL)
            plt.show()

            Success, Failed = self.manipulator.read_leg_search_data(self.analyzer.Analyze_leg_search(group_info, OFF_index, "OFF"), ["L-f", "L-m", "L-h", "Index"])
            combined = pd.concat([Success, Failed])
            new_df = combined[['Index']].copy()
            new_df['sum'] = combined[['L-f', 'L-m', 'L-h']].sum(axis=1)
            LL = []
            LS = []
            for i in range(len(new_df["Index"])):
                trial_info = group_info.fly_kinematic_data[f"F{new_df['Index'][i][0]}T{new_df['Index'][i][1]}"]
                if trial_info.mol != -1:
                    LL.append((trial_info.mol - trial_info.moc) / trial_info.fps)
                    LS.append(new_df['sum'][i])

            sns.scatterplot(x=LS, y=LL)
            plt.show()
        else:
            if SC_path is not None:
                import ast
                data = pd.read_csv(SC_path)
                data["Index"] = data["Index"].apply(ast.literal_eval)
            else:
                data = self.analyzer.AnalyzeSecondaryContact(index_to_iterate, group_info, 0.71)
            cols = data.filter(regex=r'^L-[fmh]').columns
            new_df = data[['Index']].copy()
            new_df['min_val'] = data[cols].replace(10000, np.nan).min(axis=1)
            new_df = new_df.dropna(subset=['min_val']).reset_index(drop=True)

            LL = []
            SC = []
            for i in range(len(new_df["Index"])):
                trial_info = group_info.fly_kinematic_data[f"F{new_df['Index'][i][0]}T{new_df['Index'][i][1]}"]
                if trial_info.mol != -1:
                    LL.append((trial_info.mol - trial_info.moc) / trial_info.fps)
                    SC.append(new_df['min_val'][i])

            sns.scatterplot(x=SC, y=LL)
            plt.show()



            if LS_path is not None:
                import ast
                combined = pd.read_csv(LS_path)
                combined["Index"] = combined["Index"].apply(ast.literal_eval)
            else:
                Success, Failed = self.manipulator.read_leg_search_data(self.analyzer.Analyze_leg_search(group_info, index_to_iterate, group_info.group_name),["L-f", "L-m", "L-h", "Index"])
                combined = pd.concat([Success, Failed])

            print(combined.columns.tolist())
            new_df = combined[['Index']].copy()
            new_df['sum'] = combined[['L-f', 'L-m', 'L-h']].sum(axis=1)
            LL = []
            LS = []
            for i in range(len(new_df["Index"])):
                trial_info = group_info.fly_kinematic_data[f"F{new_df['Index'][i][0]}T{new_df['Index'][i][1]}"]
                if trial_info.mol != -1:
                    LL.append((trial_info.mol - trial_info.moc) / trial_info.fps)
                    LS.append(new_df['sum'][i])

            sns.scatterplot(x=LS, y=LL)
            plt.show()
    def plot_LS_SC(self, group_info, Opto=False):
        ls_cols = ["L-f", "L-m", "L-h"]

        if not Opto:
            ls_df = pd.read_csv(r"C:\Users\agrawal-admin\Desktop\Landing\WT-T3-TiTa-WT-T3-TiTa-LS_data_.csv")
            sc_df = pd.read_csv(r"C:\Users\agrawal-admin\Desktop\Landing\WT-T3-TiTa--0.71.csv")
            ls_out = ls_df[["Index", "Result"]].copy()
            ls_out["LS_sum"] = ls_df[ls_cols].sum(axis=1)

            # ---------------------------------------------------
            # 2) Build SC from all columns containing:
            #    L-f, L-m, or L-h
            #    Treat 10000 as NaN before taking row-wise min
            # ---------------------------------------------------
            sc_cols = sc_df.filter(regex=r"L-f|L-m|L-h").columns

            sc_out = sc_df[["Index", "Result"]].copy()
            sc_out["SC"] = (
                sc_df[sc_cols]
                .replace(10000, np.nan)
                .min(axis=1)
            )

            # Optional:
            # drop rows where SC is NaN (meaning all relevant values were 10000)
            # sc_out = sc_out.dropna(subset=["SC"])

            # ---------------------------------------------------
            # 3) Merge them together using Index and Result
            # ---------------------------------------------------
            result_df = pd.merge(ls_out, sc_out, on=["Index", "Result"], how="inner")

            # Reorder columns
            result_df = result_df[["Index", "Result", "LS_sum", "SC"]]


            # Save if needed
            result_df.to_csv("filtered_LS_SC_data.csv", index=False)
            final_df = result_df.dropna(subset=["SC"])
            n_dropped = result_df["SC"].isna()
            print(n_dropped)

            success_color = self.centered_shades("blue", 5)[3]
            failed_color = self.centered_shades("green", 5)[3]
            fig, ax = plt.subplots(1, 1, figsize=(7, 7))
            success = final_df[final_df["Result"] == "Success"]
            failed = final_df[final_df["Result"] == "Failed"]
            sns.scatterplot(x=success["SC"], y=success["LS_sum"], s=100, alpha=0.5, color=success_color, label=f"Success")
            sns.scatterplot(x=failed["SC"], y=failed["LS_sum"], s=100, alpha=0.5, color=failed_color, label="Failed")
            self.formatting(ax, xticks=[0, 0.5, 1, 1.5, 2], yticks=[0, 5, 10, 15, 20, 25], xlabel="moment of first secondary contact", ylabel="number of leg searches")
            sns.despine(trim=True, offset=5)
            plt.savefig(f"{group_info.group_name} LS vs SC.pdf")
            plt.show()
        else:
            ls_df_on = pd.read_csv(os.path.join(r"C:\Users\agrawal-admin\Desktop\Landing",  f"{group_info.group_name}-ON-LS_data_.csv"))
            ls_df_off = pd.read_csv(os.path.join(r"C:\Users\agrawal-admin\Desktop\Landing", f"{group_info.group_name}-OFF-LS_data_.csv"))

            sc_df_on = pd.read_csv(os.path.join(r"C:\Users\agrawal-admin\Desktop\Landing", f"{group_info.group_name}-ON-0.71.csv"))
            sc_df_off = pd.read_csv(os.path.join(r"C:\Users\agrawal-admin\Desktop\Landing", f"{group_info.group_name}-OFF-0.71.csv"))

            ls_out_on = ls_df_on[["Index", "Result"]].copy()
            ls_out_on["LS_sum"] = ls_df_on[ls_cols].sum(axis=1)
            ls_out_off = ls_df_off[["Index", "Result"]].copy()
            ls_out_off["LS_sum"] = ls_df_off[ls_cols].sum(axis=1)

            # ---------------------------------------------------
            # 2) Build SC from all columns containing:
            #    L-f, L-m, or L-h
            #    Treat 10000 as NaN before taking row-wise min
            # ---------------------------------------------------
            sc_cols = sc_df_on.filter(regex=r"L-f|L-m|L-h").columns
            sc_out_on = sc_df_on[["Index", "Result"]].copy()
            sc_out_on["SC"] = (sc_df_on[sc_cols].replace(10000, np.nan).min(axis=1))

            sc_cols = sc_df_off.filter(regex=r"L-f|L-m|L-h").columns
            sc_out_off = sc_df_off[["Index", "Result"]].copy()
            sc_out_off["SC"] = (sc_df_off[sc_cols].replace(10000, np.nan).min(axis=1))

            # Optional:
            # drop rows where SC is NaN (meaning all relevant values were 10000)
            # sc_out = sc_out.dropna(subset=["SC"])

            # ---------------------------------------------------
            # 3) Merge them together using Index and Result
            # ---------------------------------------------------

            # Reorder columns

            # Save if needed
            # result_df_on.to_csv("filtered_LS_SC_data.csv", index=False)
            fig, ax = plt.subplots(2, 1, figsize=(5, 10))

            result_df_on = pd.merge(ls_out_on, sc_out_on, on=["Index", "Result"], how="inner")
            result_df_on = result_df_on[["Index", "Result", "LS_sum", "SC"]]
            final_df_on = result_df_on.dropna(subset=["SC"])
            success_color = self.centered_shades("blue", 5)[3]
            failed_color = self.centered_shades("green", 5)[3]
            success = final_df_on[final_df_on["Result"] == "Success"]
            failed = final_df_on[final_df_on["Result"] == "Failed"]
            sns.scatterplot(x=success["SC"], y=success["LS_sum"], s=100, alpha=0.5, color=success_color, ax=ax[0], label=f"Success")
            sns.scatterplot(x=failed["SC"], y=failed["LS_sum"], s=100, alpha=0.5, color=failed_color, ax=ax[0], label="Failed")

            result_df_off = pd.merge(ls_out_off, sc_out_off, on=["Index", "Result"], how="inner")
            result_df_off = result_df_off[["Index", "Result", "LS_sum", "SC"]]
            final_df_off = result_df_off.dropna(subset=["SC"])
            success_color = self.centered_shades("blue", 5)[3]
            failed_color = self.centered_shades("green", 5)[3]
            success = final_df_off[final_df_off["Result"] == "Success"]
            failed = final_df_off[final_df_off["Result"] == "Failed"]
            sns.scatterplot(x=success["SC"], y=success["LS_sum"], s=100, alpha=0.5, color=success_color, ax=ax[1],label=f"Success")
            sns.scatterplot(x=failed["SC"], y=failed["LS_sum"], s=100, alpha=0.5, color=failed_color, ax=ax[1], label="Failed")



            ax[0].set_title("ON")
            ax[1].set_title("OFF")
            self.formatting(ax, xticks=[0, 0.5, 1, 1.5, 2], yticks=[0, 5, 10, 15, 20, 25, 30], xlabel="moment of first secondary contact", ylabel="number of leg searches")
            sns.despine(trim=True, offset=5)
            plt.tight_layout()
            plt.savefig(f"{group_info.group_name}-LS vs SC.pdf")
            plt.show()
    def plot_Chrimson_ang_change(self, groups):
        angs = [["L-wing", "L-wing-hinge", "R-wing"]]
        color = ["magenta", "green", "red", "orange", "brown", "blue"]
        fig, ax = plt.subplots(2, 1, figsize=(7, 14))
        for g, group_info in enumerate(groups):
            index_to_iter = group_info.get_targeted_trials(["Landing", "Flying"])
            ON_index = []
            traces = []
            for index in index_to_iter:
                path = group_info.fly_kinematic_data_path[f"F{index[0]}T{index[1]}"]
                if "ON" in path or "LO" in path:
                    trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
                    ON_index.append(index)
                    wing_ag = self.calculator.Calculate_joint_angle(trial_info, angs)
                    traces.append(wing_ag["L-wing-hinge"][500:1250])
            avg = np.nanmean(traces, axis=0)
            std = np.nanstd(traces, axis=0)
            seconds = [s / 250 for s in range(-250, 500)]
            sns.lineplot(x=seconds, y=avg, color=color[g], linewidth=1, ax=ax[g // 3], label=f"{group_info.group_name} (n = {len(traces)})")
            ax[g // 3].fill_between(x=seconds, y1=avg - std, y2=avg + std, alpha=0.3, color=color[g])
        ax[0].axvline(0, color="black", linestyle="dashed")
        ax[1].axvline(0, color="black", linestyle="dashed")
        ax[0].legend()
        ax[1].legend()
        self.formatting(ax, xticks=[-1, 0, 1, 2], yticks=[0, 90, 180], xlabel="Time (s)", ylabel="Wing angle")
        sns.despine(trim=True, offset=5)
        plt.savefig("Chrimson-angle_change.pdf")
        plt.show()

    def pairwise_bootstrap_table(self, df, group_col, value_col, group_order=None):
        """
        Perform all pairwise bootstrap comparisons and return a symmetric p-value table.

        Parameters
        ----------
        df : pandas.DataFrame
        group_col : str
            Column containing group labels
        value_col : str
            Column containing numeric values
        bootstrap_func : callable
            Function like bootstrap_func(data1, data2) -> p_value
        group_order : list or None
            Order of groups in the output table

        Returns
        -------
        p_table : pandas.DataFrame
            Symmetric table of p-values
        """
        import itertools
        if group_order is None:
            group_order = list(df[group_col].dropna().unique())

        p_table = pd.DataFrame(np.nan, index=group_order, columns=group_order)

        for g in group_order:
            p_table.loc[g, g] = 0

        for g1, g2 in itertools.combinations(group_order, 2):
            data1 = df.loc[df[group_col] == g1, value_col].dropna().to_numpy(dtype=float)
            data2 = df.loc[df[group_col] == g2, value_col].dropna().to_numpy(dtype=float)

            if len(data1) == 0 or len(data2) == 0:
                p = np.nan
            else:
                p = self.calculator.Bootstrapping_test(data1, data2, 30000)

            p_table.loc[g1, g2] = p
            p_table.loc[g2, g1] = p

        return p_table
    def plot_secondary_contact_probability(self, groups):
        collected_data = dict()
        collected_data["Group"] = []
        collected_data["Value"] = []
        stat = dict()
        stat["mean"] = []
        stat["std"] = []
        stat["group"] = []
        fig, ax = plt.subplots(1, 1, figsize=(len(groups) * 2, 7))
        for group_info in groups:
            index_to_iterate = group_info.get_targeted_trials(["Flying", "Landing"])
            data = self.analyzer.AnalyzeSecondaryContact(index_to_iterate, group_info, 0.71)
            cols = data.filter(regex=r'^L-[fmh]').columns
            new_df = data[['Index']].copy()
            new_df['min_val'] = data[cols].replace(10000, np.nan).min(axis=1)
            new_df = new_df.dropna(subset=['min_val']).reset_index(drop=True)

            sc_probability = []
            for f in range(group_info.total_fly_number):
                if f + 1 in group_info.good_fly_index:
                    valid_trial_num = len([ind for ind in index_to_iterate if ind[0] == f + 1])
                    sc_count = 0
                    for index in new_df["Index"]:
                        if index[0] == f + 1:
                            sc_count += 1

                    sc_probability.append(sc_count / valid_trial_num)
                    collected_data["Group"].append(group_info.group_name)
                    collected_data["Value"].append(sc_count / valid_trial_num)
            stat["mean"].append(np.mean(sc_probability))
            stat["std"].append(np.std(sc_probability))
            stat["group"].append(group_info.group_name)


        sns.stripplot(data=collected_data, x="Group", y="Value")
        self.formatting(ax, yticks=[0, 0.5, 1], ylabel="secondary contact probability")
        sns.despine(trim=True, offset=5)
        pd.DataFrame(stat).to_csv("WT-SC-probability-stat.csv")
        plt.savefig(f"WT-SC-probability.pdf")
        plt.show()
    """def plot_secondary_contact_probability_OPTO(self, group_info:Group):
        index_to_iterate = group_info.get_targeted_trials(["Flying", "Landing"])
        ON = []
        OFF = []
        for index in index_to_iterate:
            path = group_info.fly_kinematic_data_path[f"F{index[0]}T{index[1]}"]
            if "ON" in path or "LO" in path:
                ON.append(index)
            if "OFF" in path or "NL" in path:
                OFF.append(index)
        on_data = self.analyzer.AnalyzeSecondaryContact(ON, group_info, 0.71)
        off_data = self.analyzer.AnalyzeSecondaryContact(OFF, group_info, 0.71)
        def read_data(data):
            cols = data.filter(regex=r'^L-[fmh]').columns
            new_df = data[['Index']].copy()
            new_df['min_val'] = data[cols].replace(10000, np.nan).min(axis=1)
            new_df = new_df.dropna(subset=['min_val']).reset_index(drop=True)
            sc_probability = []
            for f in range(group_info.total_fly_number):
                if f + 1 in group_info.good_fly_index:
                    valid_trial_num = len([ind for ind in index_to_iterate if ind[0] == f + 1])
                    sc_count = 0
                    for index in on_data["Index"]:
                        if index[0] == f + 1:
                            sc_count += 1
                    sc_probability.append((f, sc_count / valid_trial_num))

            return sc_probability
        sc_probability_on = read_data(on_data)
        sc_probability_off = read_data(off_data)

        # sns.stripplot(data=collected_data, x="Group", y="Value")
        plt.show()"""

    def plot_secondary_contact_probability_OPTO(self, group_info: Group):
        index_to_iterate = group_info.get_targeted_trials(["Flying", "Landing"])

        ON = []
        OFF = []
        for index in index_to_iterate:
            path = group_info.fly_kinematic_data_path[f"F{index[0]}T{index[1]}"]
            if "ON" in path or "LO" in path:
                ON.append(index)
            if "OFF" in path or "NL" in path:
                OFF.append(index)

        on_data = self.analyzer.AnalyzeSecondaryContact(ON, group_info, 0.71)
        off_data = self.analyzer.AnalyzeSecondaryContact(OFF, group_info, 0.71)

        def read_data(data, trial_pool, group_name):
            cols = data.filter(regex=r'^L-[fmh]').columns
            new_df = data[['Index']].copy()
            new_df['min_val'] = data[cols].replace(10000, np.nan).min(axis=1)
            new_df = new_df.dropna(subset=['min_val']).reset_index(drop=True)

            sc_probability = []
            for f in range(group_info.total_fly_number):
                fly_id = f + 1
                if fly_id in group_info.good_fly_index:
                    valid_trial_num = len([ind for ind in trial_pool if ind[0] == fly_id])

                    if valid_trial_num == 0:
                        continue

                    sc_count = 0
                    for index in new_df["Index"]:
                        if index[0] == fly_id:
                            sc_count += 1

                    sc_probability.append({
                        "Fly#": fly_id,
                        "Group_Name": group_name,
                        "SCProb": sc_count / valid_trial_num
                    })

            return pd.DataFrame(sc_probability)

        sc_probability_on = read_data(on_data, ON, "ON")
        sc_probability_off = read_data(off_data, OFF, "OFF")

        combined_df = pd.concat([sc_probability_off, sc_probability_on], ignore_index=True)

        # keep only flies that exist in both ON and OFF, so connection lines make sense
        valid_flies = (
            combined_df.groupby("Fly#")["Group_Name"]
            .nunique()
        )
        valid_flies = valid_flies[valid_flies == 2].index
        combined_df = combined_df[combined_df["Fly#"].isin(valid_flies)].copy()

        # sort so OFF and ON are always in the same order for each fly
        combined_df["Group_Name"] = pd.Categorical(
            combined_df["Group_Name"],
            categories=["OFF", "ON"],
            ordered=True
        )
        combined_df = combined_df.sort_values(by=["Fly#", "Group_Name"])

        plt.figure(figsize=(6, 10))

        g = sns.pointplot(data=combined_df, x="Group_Name", y="SCProb", ci=None, dodge=True, color="black", join=False)

        # connect same flies across OFF vs ON
        for fly_id, group in combined_df.groupby("Fly#"):
            plt.plot(group["Group_Name"], group["SCProb"], marker="o", markersize=20, color="lightgrey", linewidth=5)

        # mean and std
        group_stat = combined_df.groupby("Group_Name")["SCProb"].agg(['mean', 'std', 'count']).reset_index()
        sns.pointplot(x="Group_Name", y="mean", data=group_stat, color="black", linestyles=" ", markers="s", errorbar=None, scale=2,  zorder=10)
        plt.errorbar(x=group_stat["Group_Name"], y=group_stat["mean"], yerr=group_stat["std"], fmt="none", color="black", capsize=10, zorder=10)

        mean_df = combined_df.groupby("Group_Name", as_index=False)["SCProb"].mean()
        plt.plot(mean_df["Group_Name"], mean_df["SCProb"], color="black", marker="o", markersize=20, linewidth=5, label="Mean")

        pd.DataFrame(group_stat).to_csv(f"{group_info.group_name}-SC-stat.csv")

        plt.title("Secondary Contact Probability")
        plt.xlabel("Group")
        plt.ylabel("Secondary Contact Probability", fontsize=25)

        g.spines['left'].set_linewidth(3)
        g.spines['bottom'].set_linewidth(3)

        plt.tick_params(axis="y", labelsize=25)
        plt.tick_params(axis="x", labelsize=25, rotation=45)
        plt.tick_params(width=3, length=10)
        plt.yticks([0, 0.5, 1])
        plt.ylim(-0.1, 1.1)
        plt.xlim(-0.5, 1.5)

        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"{group_info.group_name}-SC-Prob.pdf")
        # plt.show()
        plt.close()
    def plot_LP(self, groups):
        Color_blind_palette = ["blue", "red", "green", "dodgerblue", "orange", "lawngreen", "orange"]
        collected_LP = dict()
        collected_LP["GroupName"] = []
        collected_LP["Values"] = []
        for g, group_info in enumerate(groups):
            LP = group_info.get_LP()
            print(LP)
            collected_LP["GroupName"].extend([group_info.group_name] * len(LP))
            collected_LP["Values"].extend(LP)

        fig, ax = plt.subplots(1,1, figsize=(len(groups) * 2, 10))
        sns.stripplot(x="GroupName", y="Values", data=collected_LP, alpha=0.4, jitter=0.2, dodge=False, size=20, marker="o", palette=Color_blind_palette)
        self.formatting(ax)
        sns.despine(trim=True, offset=5)
        plt.show()
    def plot_LL(self, groups):
        from matplotlib.lines import Line2D
        legend_handles = []  # List to store legend handles
        legend_labels = []
        Color_blind_palette = ["blue", "red", "green", "dodgerblue", "orange", "lawngreen", "orange"]
        collected_LP = dict()
        groups_data = []
        legend_handles = []
        legend_labels = []
        collected_LP["GroupName"] = []
        collected_LP["Values"] = []
        for g, group_info in enumerate(groups):
            MLL, TLL = group_info.get_LL()
            collected_LP["GroupName"].extend([group_info.group_name] * len(TLL))
            collected_LP["Values"].extend(TLL)
            groups_data.append(TLL)
            legend_labels.append(group_info.group_name)

        fig, ax = plt.subplots(1,1, figsize=(7, 7))
        for g in range(len(groups)):

            sns.ecdfplot(groups_data[g], alpha=0.8, color=Color_blind_palette[g], ax=ax, linestyle="solid", linewidth=2)
            legend_handles.append(Line2D([0], [0], color=Color_blind_palette[g], linestyle="solid", lw=2))
        ax.legend(legend_handles, legend_labels, fontsize=20, loc="lower right", frameon=True)
        # plt.savefig(f"{filename}.pdf")

        plt.tick_params(axis="y", labelsize=25)
        plt.tick_params(axis="x", labelsize=25)
        plt.tick_params(width=3, length=10)
        self.formatting(ax=ax,
                        xlabel="Landing latency (s)",
                        xlabel_size=25,
                        ylabel="Percentage",
                        ylabel_size=25,
                        xticks=[0, 0.71],
                        yticks=[0, 0.5, 1])
        sns.despine(trim=True, offset=5)
        plt.tight_layout()
        plt.show()