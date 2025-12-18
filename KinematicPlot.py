import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from kinematic_object import Group, Trial, Point
import kinematic_utilities as ku
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.signal import find_peaks
import math
from scipy.interpolate import interp1d
from scipy.stats import linregress

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
        """self.angles = [["L-fBC", "L-fCT", "L-fFT"],
                       ["L-fCT", "L-fFT", "L-fTT"],
                       ["R-fBC", "R-fCT", "R-fFT"],
                       ["R-fCT", "R-fFT", "R-fTT"],

                       ["L-mBC", "L-mCT", "L-mFT"],
                       ["L-mCT", "L-mFT", "L-mTT"],
                       ["R-mBC", "R-mCT", "R-mFT"],
                       ["R-mCT", "R-mFT", "R-mTT"],
                       ["R-mFT", "R-mTT", "R-mLT"],

                       ["L-hBC", "L-hCT", "L-hFT"],
                       ["L-hCT", "L-hFT", "L-hTT"],
                       ["R-hBC", "R-hCT", "R-hFT"],
                       ["R-hCT", "R-hFT", "R-hTT"],

                       ["R-hLT", "R-hBC", "platform-axis"],
                       ["L-hLT", "L-hBC", "platform-axis"],

                       ["L-wing", "L-wing-hinge", "R-wing"]]"""
        self.angles = [["R-fBC", "R-fCT", "R-fFT"],
                       ["R-mFT", "R-mTT", "R-mLT"],
                       ["R-hBC", "R-hCT", "R-hFT"],

                       ["L-fBC", "L-fCT", "L-fFT"],
                       ["L-fCT", "L-fFT", "L-fTT"],

                       ["L-mBC", "L-mCT", "L-mFT"],
                       ["L-mCT", "L-mFT", "L-mTT"],

                       ["L-hBC", "L-hCT", "L-hFT"],
                       ["L-hCT", "L-hFT", "L-hTT"]]
        self.colors = ["#FF0000", "#008000", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF",
                       "#000000", "#808080", "#A9A9A9", "#D3D3D3", "#FFA500", "#800080",
                       "#A52A2A", "#FFC0CB", "#ADD8E6", "#00FF00", "#4B0082", "#EE82EE",
                       "#FFD700", "#C0C0C0", "#D2B48C", "#FF7F50", "#006400", "#00008B",
                       "#8B0000", "#FF8C00", "#8B008B", "#708090", "#FF6347", "#008080"]
    def plot_flying_posture_over_trial(self, group_info:Group):

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


        fig, ax = plt.subplots()
        sns.lineplot(collected_joint_angle_R, legend=False)
        ax.set_xlabel("Trial", fontsize=25)
        ax.set_ylabel("R FT joint angle", fontsize=25)
        plt.tick_params(axis="both", width=3, length=10)
        plt.xticks([0, 9, 19], ["1", "10", "20"], fontsize=25)
        plt.yticks([0, 45, 90], fontsize=25)
        for spine in ax.spines.values():
            spine.set_linewidth(2)
        sns.despine(trim=True)
        plt.savefig("FT angle R")
        plt.tight_layout()
        plt.show()

        fig, ax = plt.subplots()
        sns.lineplot(collected_joint_angle_L, legend=False)
        ax.set_xlabel("Trial", fontsize=25)
        ax.set_ylabel("L FT joint angle", fontsize=25)
        plt.tick_params(axis="both", width=3, length=10)
        plt.xticks([0, 9, 19], ["1", "10", "20"], fontsize=25)
        plt.yticks([0, 45, 90], fontsize=25)
        sns.despine(trim=True)
        for spine in ax.spines.values():
            spine.set_linewidth(2)
        plt.savefig("FT angle L")
        plt.tight_layout()
        plt.show()

        collected_joint_angle_L = pd.DataFrame(collected_joint_angle_L)
        collected_joint_angle_R = pd.DataFrame(collected_joint_angle_R)

        mean_values_R = collected_joint_angle_R.mean(axis=0, skipna=True)  # Compute mean for each trial (column)
        sem_values_R = collected_joint_angle_R.sem(axis=0, skipna=True)  # Compute SEM for each trial (column)

        mean_values_L = collected_joint_angle_L.mean(axis=0, skipna=True)  # Compute mean for each trial (column)
        sem_values_L = collected_joint_angle_L.sem(axis=0, skipna=True)

        fig, ax = plt.subplots()

        sns.lineplot(x=mean_values_R.index + 1, y=mean_values_R,
                     errorbar=("ci", 0),  # Disables default CI
                     ax=ax, label="Mean", color="Navy")

        sns.lineplot(x=mean_values_L.index + 1, y=mean_values_L,
                     errorbar=("ci", 0),  # Disables default CI
                     ax=ax, label="Mean", color="skyblue")

        # Add error bars manually
        ax.errorbar(mean_values_R.index + 1, mean_values_R, yerr=sem_values_R, fmt='o', color="Navy", capsize=5)
        ax.errorbar(mean_values_L.index + 1, mean_values_L, yerr=sem_values_L, fmt='o', color="skyblue", capsize=5)

        ax.set_xlabel("Trial", fontsize=25)
        ax.set_ylabel("FT joint angle", fontsize=25)
        plt.xticks([1, 10, 20], fontsize=25)
        plt.yticks([0, 45, 90], fontsize=25)
        plt.tick_params(axis="both", width=3, length=10)
        for spine in ax.spines.values():
            spine.set_linewidth(2)
        plt.savefig("FT angle mean")
        plt.tight_layout()
        plt.show()
    def plot_tarsus_contact_vs_latency(self, group_info:Group):

        Contact_relative_position, Latency = self.analyzer.TiTa_relative_contact(group_info=group_info)

        df = {
            "ContactPoints": Contact_relative_position,
            "Latency": Latency
        }
        df = pd.DataFrame(df)
        fig, ax = plt.subplots()

        sns.scatterplot(x="ContactPoints", y="Latency", data=df, markers="o", s=100, alpha=0.8, legend=False)

        ax.set_xlabel("Ti-Ta relative contact point", fontsize=25)
        ax.set_ylabel("Latency (s)", fontsize=25)
        plt.xticks([0, 1], fontsize=25)
        plt.yticks([0, 1], fontsize=25)
        for spine in ax.spines.values():
            spine.set_linewidth(2)
        plt.tick_params(axis="both", width=3, length=10)
        plt.title(f"{group_info.group_name}", fontsize=25)
        plt.ylim([-0.1, 1.1])
        plt.xlim([-0.1, 1.1])
        plt.tight_layout()
        plt.show()
    def MakePlot(self, group_info:Group):
        start = 0
        end = int(group_info.video_duration * group_info.fps)

        for fly in range(group_info.total_fly_number):
            fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(20, 16))
            i = 0
            j = 0
            t = 0
            for trial in range(20):
                if f"F{fly + 1}T{trial + 1}" not in group_info.fly_kinematic_data:
                    plt.tight_layout()  # Adjust subplot layout
                    plt.savefig(f"{group_info.group_name} Fly {fly + 1}.png")
                    break
                Data = group_info.fly_kinematic_data[f"F{fly + 1}T{trial + 1}"]
                if i % 5 == 0:
                    j += 1
                    i = 1
                else:
                    i += 1

                trial_type, MOL = self.analyzer.CategorizeTrial(Data)
                WingAbTipAngle = self.calculator.Calculate_joint_angle(Data, [["R-wing", "R-wing-hinge", "abdomen-tip"], ["L-wing", "L-wing-hinge", "abdomen-tip"]])
                WingAbTipAngle["R-wing-hinge"] = list(WingAbTipAngle["R-wing-hinge"])
                WingAbTipAngle["L-wing-hinge"] = list(WingAbTipAngle["L-wing-hinge"])
                R_mol, RL = self.detector.detect_moment_of_landing_WingAngle(WingAbTipAngle["R-wing-hinge"], 50, 4, 2)
                L_mol, LL = self.detector.detect_moment_of_landing_WingAngle(WingAbTipAngle["L-wing-hinge"], 50, 4, 2)

                print(f"Fly {fly + 1} Trial {trial + 1}")
                seconds = [f for f in range(end - start)]

                plot_df = pd.DataFrame({
                    "seconds": seconds,
                    "R": list(WingAbTipAngle["R-wing-hinge"]),
                    "L": list(WingAbTipAngle["L-wing-hinge"])
                })
                try:
                    if trial_type == 0:
                        print("NF")
                        sns.lineplot(x=seconds, y=WingAbTipAngle["R-wing-hinge"][start:end], ax=axs[i - 1, j - 1], color="blue")
                        sns.lineplot(x=seconds, y=WingAbTipAngle["L-wing-hinge"][start:end], ax=axs[i - 1, j - 1], color="navy")
                    elif trial_type == 1:
                        moc, leg, contact_point = self.analyzer.DetermineTiTaMOC(Data)
                        if contact_point == "NoContact" or contact_point == "L":
                            print("N/A")
                            sns.lineplot(x=seconds, y=WingAbTipAngle["R-wing-hinge"][start:end], ax=axs[i - 1, j - 1], color="red")
                            sns.lineplot(x=seconds, y=WingAbTipAngle["L-wing-hinge"][start:end], ax=axs[i - 1, j - 1], color="maroon")
                        else:
                            print("Landing")
                            sns.lineplot(x=seconds, y=WingAbTipAngle["R-wing-hinge"][start:end], ax=axs[i - 1, j - 1], color="yellow")
                            sns.lineplot(x=seconds, y=WingAbTipAngle["L-wing-hinge"][start:end], ax=axs[i - 1, j - 1], color="gold")
                            axs[i - 1, j - 1].axvline(R_mol - start, color="black")
                            axs[i - 1, j - 1].axvline(L_mol - start, color="grey")
                            axs[i - 1, j - 1].axvline(moc - start, color="red")
                    elif trial_type == -1:
                        moc, leg, contact_point = self.analyzer.DetermineTiTaMOC(Data)
                        if contact_point == "NoContact" or contact_point == "L":
                            print("N/A")
                            sns.lineplot(x=seconds, y=WingAbTipAngle["R-wing-hinge"][start:end], ax=axs[i - 1, j - 1], color="red")
                            sns.lineplot(x=seconds, y=WingAbTipAngle["L-wing-hinge"][start:end], ax=axs[i - 1, j - 1], color="maroon")
                        else:
                            print("Flying")
                            nan_count = sum(math.isnan(x) for x in WingAbTipAngle["R-wing-hinge"][start:end])
                            print(nan_count)
                            sns.lineplot(x=seconds, y=WingAbTipAngle["R-wing-hinge"][start:end], ax=axs[i - 1, j - 1], color="darkorange")
                            sns.lineplot(x=seconds, y=WingAbTipAngle["L-wing-hinge"][start:end], ax=axs[i - 1, j - 1], color="orange")
                except:
                    continue

                axs[i - 1, j - 1].set_xlabel("Frames")
                axs[i - 1, j - 1].set_yticks([0, 90, 180])
                axs[i - 1, j - 1].set_ylim(-5, 185)
                axs[i - 1, j - 1].set_ylabel("Distance (mm)")
                axs[i - 1, j - 1].set_title(f"Trial {t + 1}")
                t += 1
            print(f"Plotting {fly + 1}'s data")
            plt.suptitle(str(fly + 1), fontsize=20)
            plt.tight_layout()  # Adjust subplot layout
            # plt.show()
            plt.savefig(f"{group_info.group_name} Fly {fly + 1}.png")  # Save the figure
            # plt.close()
    def plot_motion_vector_with_plane(self, kinematic_data:Trial, frame):


        line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
            self.calculator.transform_coords_and_calculate_platform_data(trial_info=kinematic_data,
                                                                         platform_offset=self.platform_offset,
                                                                         platform_height=self.platform_height,
                                                                         radius=self.radius))

        coords = self.detector.ReadCoordsAll(kinematic_data, frame)

        center_points = self.calculator.ReadAndTranspose("platform-tip", kinematic_data)
        platform_ctr_pts_traces = np.array(center_points[300:350])

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

        # ax.quiver(*platform_ctr_pts_traces[-1], *perp_vector1, color='r', arrow_length_ratio=0.1)
        # ax.quiver(*platform_ctr_pts_traces[-1], *perp_vector2, color='r', arrow_length_ratio=0.1)

        # Add the side surface to the plot
        side_surface = Poly3DCollection(verts, alpha=0.3, facecolor='gray', edgecolor='none')
        # ax.add_collection3d(side_surface)

        # Plot the trajectory with color gradient
        for i in range(num_points - 1):
            pass
            # ax.plot(platform_ctr_pts_traces[i:i + 2, 0], platform_ctr_pts_traces[i:i + 2, 1], platform_ctr_pts_traces[i:i + 2, 2], color=colors[i], linewidth=6)

        # Plot the best-fit line
        # ax.quiver(*platform_ctr_pts_traces[-1], *direction, color='r', arrow_length_ratio=0.1)
        # Plot the normal plane
        # ax.plot_trisurf(plane_points[:, 0], plane_points[:, 1], plane_points[:, 2], color='cyan', alpha=0.5)

        # Labels and legend
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("3D Motion with Normal Plane")
        axis_limit = 1.5  # Adjust this value based on your data range
        ax.set_xlim([-axis_limit, axis_limit])
        ax.set_ylim([-axis_limit, axis_limit])
        ax.set_zlim([-axis_limit, axis_limit])
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
        # plt.show(block=True)
        plt.savefig("Kinematic.pdf")
    def plot_posture_angle_change(self, trial_info:Trial):
        angles = [["L-fBC", "L-fCT", "L-fFT"], ["L-fCT", "L-fFT", "L-fTT"], ["R-fBC", "R-fCT", "R-fFT"], ["R-fCT", "R-fFT", "R-fTT"],
                  ["L-mBC", "L-mCT", "L-mFT"], ["L-mCT", "L-mFT", "L-mTT"], ["R-mBC", "R-mCT", "R-mFT"], ["R-mCT", "R-mFT", "R-mTT"],
                  ["L-hBC", "L-hCT", "L-hFT"], ["L-hCT", "L-hFT", "L-hTT"], ["R-hBC", "R-hCT", "R-hFT"], ["R-hCT", "R-hFT", "R-hTT"]]
        Angles = self.calculator.Calculate_joint_angle(trial_info, angles)

        duration = 7
        alpha = 1
        fig, ax = plt.subplots(figsize=(10, 8))
        ax1 = ax.twinx()

        for k in Angles.keys():
            postureData = self.calculator.exponential_moving_average(Angles[k][:duration * self.fps], alpha)
            x = np.asarray(range(len(postureData))) / self.fps
            sns.lineplot(x=x, y=postureData, ax=ax)
            sns.lineplot(x=x[1:], y=self.calculator.Calculate_derivative(postureData), ax=ax1)
        ax.set_ylim(-5, 200)
        ax.set_xlim(-0.1, duration + 0.1)
        ax1.set_ylim(-0.5, 21)
        ax.set_xlabel("Second (s)", fontsize=25)
        ax.set_ylabel("Joints angle", fontsize=25)
        ax1.set_ylabel("Change of angle", fontsize=25)
        ax.set_xticks([0, duration / 2 , duration])
        ax.set_yticks([0, 90, 180])
        ax1.set_yticks([0, 10, 20])
        ax.tick_params(axis='x', labelsize=25)
        ax.tick_params(axis='y', labelsize=25)
        ax.tick_params(axis="both", width=3, length=10)
        ax1.tick_params(axis='y', width=3, length=10, labelsize=25)
        for spine in ax.spines.values():
            spine.set_linewidth(2)
        plt.tight_layout()
        plt.show()
    def plot_FT_ang_ll(self, group_info:Group, mean=False):
        ft_angle = []
        trial_latency = []
        self.analyzer.Determine_all_flying_posture(group_info)
        for index, r in group_info.ll_data.iloc[:group_info.total_fly_number].iterrows():
            fly_ft = []
            fly_trial_latency = []
            na = 0
            nf = 0
            for i, ll in enumerate(r):
                # low latency landing trial
                if not isinstance(ll, str) and ll > -1 and not pd.isna(ll) and (ll / self.fps) < 1:
                    fly_ft.append(group_info.fly_kinematic_data[f"F{index + 1}T{i + 1}"].R_stable_FT_angle)
                    fly_trial_latency.append(ll / self.fps)
                # nan trial
                elif pd.isna(ll):
                    na += 1
                # not flying trial
                elif isinstance(ll, str):
                    nf += 1
            if na + nf <= 10:
                if mean:
                    ft_angle.append(np.mean(fly_ft))
                    trial_latency.append(np.mean(fly_trial_latency))
                else:
                    ft_angle.extend(fly_ft)
                    trial_latency.extend(fly_trial_latency)
        # return ft_angle
        # print(trial_latency, ft_angle)
        ax = sns.scatterplot(x=trial_latency, y=ft_angle, s=200, alpha=0.3, color="blue")
        ax.set_xlabel("Landing latency", fontsize=25)
        ax.set_ylabel("R-mFT angle", fontsize=25)
        plt.xticks([0, 1], fontsize=25)
        plt.yticks([0, 90, 180], fontsize=25)
        for spine in ax.spines.values():
            spine.set_linewidth(2)
        sns.despine(trim=True)
        plt.tick_params(axis="both", width=3, length=10)
        plt.title(f"{group_info.group_name}", fontsize=25)
        plt.ylim([-5, 185])
        plt.xlim([-0.1, 1.1])
        plt.tight_layout()
        plt.show()
    def plot_CT_FT_angle_space(self, group_info:Group):
        for i in range(group_info.total_fly_number):
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
            for t in range(20):
                if f"F{i + 1}T{t + 1}" in group_info.fly_kinematic_data:
                    if not isinstance(group_info.mol_data.iloc[i][t], str) and not pd.isna(group_info.mol_data.iloc[i][t]) and not group_info.mol_data.iloc[i][t] < 0:
                        start = int(group_info.moc_data.iloc[i][t])
                        end = int(group_info.mol_data.iloc[i][t])
                        print(f"Fly: {i + 1} Trial: {t + 1}")
                        kinematic_data = group_info.fly_kinematic_data[f"F{i + 1}T{t + 1}"]

                        joint = "L-fCT"
                        joint2 = "L-fFT"
                        angs = self.calculator.Calculate_joint_angle(kinematic_data, self.angles)
                        signal = np.asarray(angs[joint][start:end])
                        peaks, troughs = self.detector.detect_peaks_troughs(signal=signal, leg=joint[:3])

                        t = np.asarray(range(len(peaks)))
                        norm = Normalize(vmin=t.min(), vmax=int(t.max() - 1))
                        cmap = cm.plasma
                        for p in range(len(peaks) - 1):
                            sns.lineplot(x=angs[joint][troughs[p]:peaks[p] + 1], y=angs[joint2][troughs[p]:peaks[p] + 1], color=cmap(norm(p)), linewidth=5, alpha=0.4)
                            sns.lineplot(x=angs[joint][peaks[p]:troughs[p + 1]], y=angs[joint2][peaks[p]:troughs[p + 1]], color=cmap(norm(p)), linewidth=5, alpha=0.4)

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
            plt.savefig(f"Fly{i}AngleSpace")
            plt.show()
    def plot_IndiLegContactPointWithPlatform(self, kinematic_data:Trial, frame):

        center_points = self.calculator.ReadAndTranspose("platform-tip", kinematic_data)
        platform_ctr_pts_traces = np.array(center_points[300:350])

        line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
            self.calculator.calculate_platform_surfaces(platform_traces=platform_ctr_pts_traces,
                                                        platform_center=center_points[frame],
                                                        platform_offset=self.platform_offset,
                                                        radius=self.radius, height=self.platform_height))

        segs = [["R-fTT", "R-fLT"], ["L-fTT", "L-fLT"], ["L-mTT", "L-mLT"], ["R-hTT", "R-hLT"], ["L-hTT", "L-hLT"]]



        start = kinematic_data.moc
        end = kinematic_data.mol
        print(start, end)

        for point in segs:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_trisurf(plane_points[:, 0], plane_points[:, 1], plane_points[:, 2], color='cyan', alpha=0.5)
            for f in range(start, end):
                A = [kinematic_data.trial_data[f"{point[0]}"].x_coord[f],
                     kinematic_data.trial_data[f"{point[0]}"].y_coord[f],
                     kinematic_data.trial_data[f"{point[0]}"].z_coord[f]]
                B = [kinematic_data.trial_data[f"{point[1]}"].x_coord[f],
                     kinematic_data.trial_data[f"{point[1]}"].y_coord[f],
                     kinematic_data.trial_data[f"{point[1]}"].z_coord[f]]
                P0 = cylinder_bottom
                d = direction
                r = self.radius
                h = self.platform_height
                intersects, pt = self.calculator.check_cylinder_side_intersection(A, B, P0, d, r, h)
                print(intersects)
                if intersects:
                    coords = self.detector.ReadCoordsAll(kinematic_data, f)
                    ax.scatter(*pt, color='magenta', s=50, label='Side Contact')

                    Colors = ["#FF0000", "#008000", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#000000",
                              "#808080", "#A9A9A9", "#D3D3D3", "#FFA500", "#800080", "#A52A2A", "#FFC0CB",
                              "#ADD8E6", "#00FF00", "#4B0082", "#EE82EE", "#FFD700", "#C0C0C0", "#D2B48C",
                              "#FF7F50", "#006400", "#00008B", "#8B0000", "#FF8C00", "#8B008B", "#708090",
                              "#FF6347", "#008080"]

                    for g, group in enumerate(self.key_point_pairs):
                        for i in range(len(group) - 1):  # Connect points in the group
                            p1 = coords[group[i]]
                            p2 = coords[group[i + 1]]
                            # Plot a line between p1 and p2
                            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], marker='o', color=Colors[g])

                    # ax.plot(line_points[:, 0], line_points[:, 1], line_points[:, 2], 'r--', label="Best-Fit Line")
                    ax.plot_trisurf(plane_points[:, 0], plane_points[:, 1], plane_points[:, 2], color='cyan', alpha=0.5)
                    side_surface = Poly3DCollection(verts, alpha=0.3, facecolor='gray', edgecolor='none')
                    ax.add_collection3d(side_surface)
                    plt.gca().set_aspect('equal')
                    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))  # Make panes transparent
                    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
                    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
                    ax.set_axis_off()  # This removes everything including the frame
                    ax.grid(False)
                    plt.savefig(f"Segment {point[0]}_{point[1]} intersect at frame {f}")
                    # plt.show()
                    break
    def plot_IndividualLegLatency(self, group_info:Group):

        segs = [["L-fTT", "L-fLT"], ["L-mTT", "L-mLT"], ["L-hTT", "L-hLT"]]

        individual_leg_contact = dict()
        individual_leg_contact["Leg"] = []
        individual_leg_contact["ContactLatency"] = []
        individual_leg_contact["LegContactOrder"] = []
        num_of_leg_contact_pertrial = []
        for index in group_info.landing_trial_index:
            print(f"Fly: {index[0]} Trial: {index[1]}")
            pose_data = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            start = int(pose_data.moc)
            end = int(pose_data.mol)

            center_points = self.calculator.ReadAndTranspose("platform-tip", pose_data)
            platform_ctr_pts_traces = np.array(center_points[300:350])
            l = 0
            intersects_moment = dict()
            for f in range(start, end):
                line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
                    self.calculator.calculate_platform_surfaces(platform_traces=platform_ctr_pts_traces,
                                                                platform_center=center_points[f],
                                                                platform_offset=self.platform_offset,
                                                                radius=self.radius, height=self.platform_height))
                for point in segs:
                    if point[0][0:3] not in intersects_moment:
                        A = [pose_data.trial_data[f"{point[0]}"].x_coord[f],
                             pose_data.trial_data[f"{point[0]}"].y_coord[f],
                             pose_data.trial_data[f"{point[0]}"].z_coord[f]]
                        B = [pose_data.trial_data[f"{point[1]}"].x_coord[f],
                             pose_data.trial_data[f"{point[1]}"].y_coord[f],
                             pose_data.trial_data[f"{point[1]}"].z_coord[f]]

                        P0 = cylinder_bottom
                        d = direction
                        r = self.radius
                        h = self.platform_height
                        intersects, pt = self.calculator.check_cylinder_side_intersection(A, B, P0, d, r, h)
                        if intersects:
                            l += 1
                            # print(point)
                            print(f)
                            individual_leg_contact["Leg"].append(point[0][0:3])
                            individual_leg_contact["ContactLatency"].append((f - start) / self.fps)
                            intersects_moment[point[0][0:3]] = (f - start) / self.fps
                            break
            if l != 0:
                num_of_leg_contact_pertrial.append(l)
            for point in segs:
                if point[0][0:3] in intersects_moment:
                    larger = 0
                    for k in intersects_moment.keys():
                        if intersects_moment[k] < intersects_moment[point[0][0:3]] and k != point[0][0:3]:
                            larger += 1
                    individual_leg_contact["LegContactOrder"].append(larger + 1)
                    # print(f"Leg {point[0][0:3]}, Rank {larger + 1}, Latency {intersects_moment[point[0][0:3]]}")

        individual_leg_contact = pd.DataFrame(individual_leg_contact)
        print(individual_leg_contact)

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
        ax = sns.stripplot(data=individual_leg_contact, x='Leg', y='ContactLatency', jitter=0.3, alpha=0)

        for i, artist in enumerate(ax.collections):
            # Skip empty collections from alpha=0 trick
            if len(artist.get_offsets()) == 0:
                continue
            # Get the original group label
            group = individual_leg_contact['Leg'].unique()[i]
            # Get the subset
            sub = individual_leg_contact[individual_leg_contact['Leg'] == group]
            # Get jittered x positions from the original stripplot
            xy = artist.get_offsets()
            # Plot with actual sizes
            plt.scatter(xy[:, 0], xy[:, 1], s=(8 / sub['LegContactOrder']) * 30, alpha=0.4, edgecolors=None)

        ax.tick_params(axis="y", labelsize=25)
        ax.tick_params(axis="x", labelsize=25)
        ax.tick_params(width=3, length=20)
        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)
        ax.set_ylabel("Leg contact latency (s)", fontsize=25)
        ax.set_xlabel("", fontsize=25)
        ax.set_yticks([0, 0.5, 1])
        ax.set_ylim(-0.1, 1.1)
        sns.despine(trim=True)
        plt.title("Ranking individual leg's contact with the contact latency")
        plt.tight_layout()
        plt.show()
    def plot_IndiLeg3DTrajectory(self, kinematic_data:Trial):

        J = ["BC", "CT", "FT", "TT", "LT"]

        joint = "L-fCT"
        start = int(kinematic_data.moc)
        end = int(kinematic_data.mol)
        side = joint[0]
        Leg = joint[2]

        angs = self.calculator.Calculate_joint_angle(kinematic_data, self.angles)
        signal = np.asarray(angs[joint][start:end])
        peaks, troughs = self.detector.detect_peaks_troughs(signal=signal, leg=Leg)

        center_points = self.calculator.ReadAndTranspose("platform-tip", kinematic_data)
        platform_ctr_pts_traces = np.array(center_points[300:350])
        line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
            self.calculator.calculate_platform_surfaces(platform_traces=platform_ctr_pts_traces,
                                                        platform_center=center_points[start],
                                                        platform_offset=self.platform_offset,
                                                        radius=self.radius,
                                                        height=self.platform_height))

        s = 0
        for i in range(len(troughs) - 1):

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_trisurf(plane_points[:, 0], plane_points[:, 1], plane_points[:, 2], color='cyan', alpha=0.5)
            side_surface = Poly3DCollection(verts, alpha=0.3, facecolor='gray', edgecolor='none')
            ax.add_collection3d(side_surface)
            s += 1

            search_start = troughs[i]
            search_end = troughs[i + 1]
            # search_end = peaks[i]

            segment_starts = []
            segment_ends = []

            for j in range(len(J) - 1):
                segment_starts.append(np.array([kinematic_data.trial_data[f"{side}-{Leg}{J[j]}"].x_coord[search_start:search_end],
                                                kinematic_data.trial_data[f"{side}-{Leg}{J[j]}"].y_coord[search_start:search_end],
                                                kinematic_data.trial_data[f"{side}-{Leg}{J[j]}"].z_coord[search_start:search_end]]).T)
                segment_ends.append(np.array([kinematic_data.trial_data[f"{side}-{Leg}{J[j + 1]}"].x_coord[search_start:search_end],
                                              kinematic_data.trial_data[f"{side}-{Leg}{J[j + 1]}"].y_coord[search_start:search_end],
                                              kinematic_data.trial_data[f"{side}-{Leg}{J[j + 1]}"].z_coord[search_start:search_end]]).T)

            t = np.asarray(range(search_end - search_start))
            norm = Normalize(vmin=t.min(), vmax=int(t.max()))
            cmap = cm.plasma

            for s in range(len(segment_starts)):
                for f in range(len(t)):

                    xs1 = [segment_starts[s][f, 0], segment_ends[s][f, 0]]
                    ys1 = [segment_starts[s][f, 1], segment_ends[s][f, 1]]
                    zs1 = [segment_starts[s][f, 2], segment_ends[s][f, 2]]
                    ax.plot(xs1, ys1, zs1, color=cmap(norm(f)), linewidth=4, alpha=0.6)

            ax.set_xlim(-2, 2)
            ax.set_ylim(-2, 2)
            ax.set_zlim(-2, 2)

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.gca().set_aspect('equal')
            ax.grid(False)
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))  # Make panes transparent
            ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
            ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
            ax.set_axis_off()  # This removes everything including the frame
            fig.colorbar(sm, ax=ax, label='Time (Frame)')
            plt.show(block=True)
    def plot_leg_search_cycle(self, trial_info:Trial):
        start = int(trial_info.moc)
        end = int(trial_info.mol)
        angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)

        Joint1 = "L-fCT"
        Joint2 = "L-mCT"
        Joint3 = "L-hFT"
        Joint4 = "L-fFT"
        L_f_CT = np.asarray(angs[Joint1][start:end])
        L_f_FT = np.asarray(angs[Joint4][start:end])

        L_m_CT = np.asarray(angs[Joint2][start:end])
        L_h_CT = np.asarray(angs[Joint3][start:end])

        def psd_plot(data1, data2, data3):
            from scipy.signal import periodogram
            Hz = 51
            fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
            # Periodogram
            f_periodo, Pxx = periodogram(data1, trial_info.fps, nfft=trial_info.fps)
            f_periodo = f_periodo[:Hz]
            Pxx = Pxx[:Hz]
            ax[0].plot(f_periodo, Pxx, linewidth=5)
            f_periodo, Pxx = periodogram(data2, trial_info.fps, nfft=trial_info.fps)
            f_periodo = f_periodo[:Hz]
            Pxx = Pxx[:Hz]
            ax[1].plot(f_periodo, Pxx, linewidth=5)
            f_periodo, Pxx = periodogram(data3, trial_info.fps, nfft=trial_info.fps)
            f_periodo = f_periodo[:Hz]
            Pxx = Pxx[:Hz]
            ax[2].plot(f_periodo, Pxx, linewidth=5)

            def formatting(ax, yl, xl):
                ax.tick_params(axis="y", labelsize=15)
                ax.tick_params(axis="x", labelsize=15)
                ax.tick_params(width=3, length=10)
                ax.spines["left"].set_linewidth(2)  # Top border
                ax.spines["bottom"].set_linewidth(2)
                ax.set_yticks([0, yl / 2, yl])
                ax.set_ylim(-50, yl)
                ax.set_xticks([x for x in range(0, xl, 5)])

            formatting(ax[0], 500, Hz)
            formatting(ax[1], 100, Hz)
            formatting(ax[2], 100, Hz)
            fig.supylabel("Periodogram (PSD)", fontsize=25)
            fig.supxlabel("Frequency (Hz)", fontsize=25)
            sns.despine(trim=True)

            plt.tight_layout()
            plt.show()

        sig_to_plot = L_f_CT
        peaks, troughs = self.detector.detect_peaks_troughs(sig_to_plot, leg="L-f")
        psd_plot(L_f_CT, L_m_CT, L_h_CT)
        print(len(troughs))
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
        trough_val = sig_to_plot[troughs]
        peaks_val = sig_to_plot[peaks]
        seconds = [s/trial_info.fps for s in range(len(sig_to_plot))]
        sns.lineplot(x=seconds, y=sig_to_plot, linewidth=5, ax=ax, color="blue")
        sns.scatterplot(x=troughs / trial_info.fps, y=trough_val, s=150, color="green", zorder=10, ax=ax)
        # sns.scatterplot(x=peaks / trial_info.fps, y=peaks_val, s=150, color="green", zorder=10, ax=ax)

        """peaks, troughs = self.detector.detect_peaks_troughs(L_f_FT, leg=leg)
        trough_val = L_f_FT[troughs]
        peaks_val = L_f_FT[peaks]
        sns.lineplot(x=seconds, y=L_f_FT, linewidth=5, ax=ax, color="orange")
        sns.scatterplot(x=troughs / trial_info.fps, y=trough_val, s=150, color="red", zorder=10, ax=ax)
        sns.scatterplot(x=peaks / trial_info.fps, y=peaks_val, s=150, color="red", zorder=10, ax=ax)"""



        ax.tick_params(axis="y", labelsize=25)
        ax.tick_params(axis="x", labelsize=25)
        ax.tick_params(width=3, length=20)
        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)
        ax.set_ylabel("L-fCT angle", fontsize=25)
        ax.set_xlabel("Landing transition duration (s)", fontsize=25)
        ax.set_yticks([0, 30, 60, 90, 120, 150, 180])
        ax.set_ylim(-5, 185)
        ax.set_xticks([0, 0.5, 1])
        ax.set_xlim(-0.1, 1.1)
        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig("LegAngleTrace.pdf")
        plt.show()
    def plot_leg_search_trace(self, group_info:Group, standardized=False):

        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
        for index in group_info.get_targeted_trials(["Landing"]):
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            print(f"Reading F{index[0]} T{index[1]} data")
            start = int(trial_info.moc)
            end = int(trial_info.mol)

            ags = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            x = [i for i in range(trial_info.mol - trial_info.moc)]
            sns.lineplot(x=x, y=ags["L-fCT"][start:end], color="blue", alpha=0.5, linewidth=3, ax=ax[0])
            sns.lineplot(x=x, y=ags["L-mCT"][start:end], color="green", alpha=0.5, linewidth=3, ax=ax[1])
            sns.lineplot(x=x, y=ags["L-hCT"][start:end], color="red", alpha=0.5, linewidth=3, ax=ax[2])
            # sns.lineplot(x=x, y=ags["L-hCT"])
            # sns.lineplot(x=x, y=ags["R-fCT"])
            # sns.lineplot(x=x, y=ags["R-hCT"])
            ax[0].set_ylim(0, 180)
            ax[1].set_ylim(0, 180)
            ax[2].set_ylim(0, 180)
        plt.show()
    def plot_trajectory(self, trial_info:Trial, joints):

        start = int(trial_info.moc)
        end = int(trial_info.mol)
        # print(end - start)

        line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
            self.calculator.transform_coords_and_calculate_platform_data(trial_info=trial_info,
                                                                         platform_offset=self.platform_offset,
                                                                         platform_height=self.platform_height,
                                                                         radius=self.radius))
        center_points = self.calculator.ReadAndTranspose("platform-tip", trial_info)
        platform_ctr_pts_traces = np.array(center_points[start:end])

        num_points = len(platform_ctr_pts_traces)



        x = dict()
        y = dict()
        z = dict()

        t = np.linspace(0, 15, 15)
        # Step 2: Create color map based on time
        norm = Normalize(vmin=t.min(), vmax=t.max())
        Colors = cm.viridis(norm(t))
        p = 0
        for j in joints:

            joint = j[0:3] + "CT"

            x[j] = []
            y[j] = []
            z[j] = []
            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            for s in range(end - start):
                A = [trial_info.trial_data[f"{j[0:3]}TT"].x_coord[s + start],
                     trial_info.trial_data[f"{j[0:3]}TT"].y_coord[s + start],
                     trial_info.trial_data[f"{j[0:3]}TT"].z_coord[s + start]]
                B = [trial_info.trial_data[j].x_coord[s + start],
                     trial_info.trial_data[j].y_coord[s + start],
                     trial_info.trial_data[j].z_coord[s + start]]

                P1 = platform_ctr_pts_traces[s]
                d = direction
                r = self.radius
                h = self.platform_height
                intersects_side, pt_side = self.calculator.check_cylinder_side_intersection(A, B, P1, d, r, h)
                intersects_top, pt_top = self.detector.check_leg_platform_intersection(A, B, d, P1, self.platform_offset)
                if intersects_top or intersects_side:
                    end = s + start
                    print("Intersect")
                    print(end - start)
                    break

            CT_signal = angs[joint][start:end]

            from scipy.fft import fft, fftfreq
            from scipy.signal import periodogram

            f = fftfreq(len(CT_signal), 1 / self.fps)
            mask = f > 0

            # Periodogram
            f_periodo, Pxx = periodogram(CT_signal, self.fps)
            noisiness = 0
            if j[0:3] == "L-f" or j[0:3] == "R-f":
                noisiness = 20
            if j[0:3] == "L-m" or j[0:3] == "L-h" or j[0:3] == "R-h":
                noisiness = 10
            if len([f for f in f_periodo if f < 20]) <= noisiness:

                peaks, troughs = self.detector.detect_peaks_troughs(CT_signal, j[0:3])
                troughs = np.sort(troughs)
                if len(troughs) <= 1:
                    continue
                peaks = []
                for t in range(len(troughs) - 1):
                    peaks.append(list(CT_signal).index(max(CT_signal[troughs[t]:troughs[t + 1]])))
                peaks = np.array(peaks)

                """plt.show()
                sns.lineplot(CT_signal)
                plt.scatter(troughs, CT_signal[troughs])
                plt.scatter(peaks, CT_signal[peaks])
                plt.show()"""

                troughs = troughs + start
                peaks = peaks + start

                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')

                coords = self.detector.ReadCoordsAll(trial_info, start)
                for g, group in enumerate(self.key_point_pairs):
                    for i in range(len(group) - 1):  # Connect points in the group
                        p1 = coords[group[i]]
                        p2 = coords[group[i + 1]]

                        # Plot a line between p1 and p2
                        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], marker='o', color=self.colors[g])

                if p == 0:
                    side_surface = Poly3DCollection(verts, alpha=0.3, facecolor='gray', edgecolor='none')
                    ax.add_collection3d(side_surface)

                    ax.quiver(*platform_ctr_pts_traces[-1], *perp_vector1, color='r', arrow_length_ratio=0.1)
                    ax.quiver(*platform_ctr_pts_traces[-1], *perp_vector2, color='r', arrow_length_ratio=0.1)

                    for i in range(num_points):
                        ax.plot(platform_ctr_pts_traces[i:i + 2, 0], platform_ctr_pts_traces[i:i + 2, 1],
                                platform_ctr_pts_traces[i:i + 2, 2], color="grey", linewidth=6)

                    # Plot the best-fit line
                    # ax.plot(line_points[:, 0], line_points[:, 1], line_points[:, 2], 'r--', label="Best-Fit Line")
                    # Plot the normal plane
                    ax.plot_trisurf(plane_points[:, 0], plane_points[:, 1], plane_points[:, 2], color='cyan', alpha=0.5)

                from scipy.spatial import ConvexHull

                  # Choose any colormap you like
                t = np.linspace(0, len(troughs) - 1, len(troughs) - 1)
                t = np.linspace(0, troughs[-1] - start, troughs[-1] - start)
                # Step 2: Create color map based on time
                norm = Normalize(vmin=t.min(), vmax=t.max())
                Colors = cm.viridis(norm(t))
                n = 0
                for tr in range(len(troughs) - 1):
                    x[j].append(trial_info.trial_data[j].x_coord[troughs[tr]:troughs[tr + 1]])
                    y[j].append(trial_info.trial_data[j].y_coord[troughs[tr]:troughs[tr + 1]])
                    z[j].append(trial_info.trial_data[j].z_coord[troughs[tr]:troughs[tr + 1]])

                    # x[j].append(trial_info.trial_data[j].x_coord[troughs[tr]:troughs[tr + 1]])
                    # y[j].append(trial_info.trial_data[j].y_coord[troughs[tr]:troughs[tr + 1]])
                    # z[j].append(trial_info.trial_data[j].z_coord[troughs[tr]:troughs[tr + 1]])

                    # Step 1: Create line segments between consecutive points
                    points = np.array([x[j][-1], y[j][-1], z[j][-1]]).T.reshape(-1, 1, 3)
                    segments = np.concatenate([points[:-1], points[1:]], axis=1)


                    lc = Line3DCollection(segments, colors=Colors[tr], linewidth=2)
                    centroid_x = trial_info.trial_data[j].x_coord[troughs[tr]:troughs[tr + 1]]
                    centroid_y = trial_info.trial_data[j].y_coord[troughs[tr]:troughs[tr + 1]]
                    centroid_z = trial_info.trial_data[j].z_coord[troughs[tr]:troughs[tr + 1]]

                    points = np.array([centroid_x, centroid_y, centroid_z]).T
                    hull = ConvexHull(points)
                    ax.scatter(*points.T, alpha=0)

                    # Plot hull
                    for simplex in hull.simplices:
                        triangle = points[simplex]
                        # ax.add_collection3d(Poly3DCollection([triangle], color=Colors[tr], alpha=0.2, edgecolor='none'))

                    for k in range(troughs[tr + 1] - troughs[tr]):
                        # pass
                        ax.scatter(centroid_x[k], centroid_y[k], centroid_z[k], color=Colors[n], s=50, alpha=0.5)
                        n += 1
                    # ax.scatter(np.mean(centroid_x), np.mean(centroid_y), np.mean(centroid_z), color=Colors[tr], s=100, alpha=0.5)
                    # ax.add_collection3d(lc)
                    # Step 5: Add colorbar
            sm = plt.cm.ScalarMappable(cmap=cm.viridis, norm=norm)
            sm.set_array([])

            fig.colorbar(sm, ax=ax, label='Time (frame)')


            # Step 4: Set axes limits
            ax.set_xlim(-2, 2)
            ax.set_ylim(-2, 2)
            ax.set_zlim(-2, 2)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')



            plt.gca().set_aspect('equal')
            # ax.view_init(elev=90, azim=0)
            # ax.grid(False)
            # ax.set_xticks([])
            # ax.set_yticks([])
            # ax.set_zticks([])

            ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))  # Make panes transparent
            ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
            ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
            # ax.set_axis_off()  # This removes everything including the frame
            ax.view_init(elev=90, azim=270)
            plt.show(block=True)
            p += 1

        fig = plt.figure()
        ax = fig.add_subplot(111)
        for j in joints:
              # time values from 0 to 1
            for s, (points1, points2) in enumerate(zip(x[j], y[j])):
                # plt.scatter(points1, points2, color=Colors[s], s=5)

                for i in range(len(points1) - 1):
                    plt.plot(points1[i: i + 2], points2[i:i + 2], linewidth=4, alpha=0.5, color=Colors[s])  # light path underneath
        plt.xlabel("x")
        plt.ylabel("y")

        # plt.colorbar(label='Time (Frame)')
        plt.title("2D Trajectory (Color-coded by Time)")
        plt.axis('equal')
        plt.xlim(-2.5, 2.5)
        plt.ylim(-2.5, 2.5)
        plt.show()
    def plot_IndividualLegContactProbability(self, group_info:Group):
        segs = [["R-fTT", "R-fLT"], ["L-fTT", "L-fLT"], ["L-mTT", "L-mLT"], ["R-hTT", "R-hLT"], ["L-hTT", "L-hLT"]]

        individual_leg_contact = dict()
        individual_leg_contact["L-f"] = dict()
        individual_leg_contact["L-m"] = dict()
        individual_leg_contact["L-h"] = dict()
        individual_leg_contact["R-f"] = dict()
        individual_leg_contact["R-h"] = dict()
        num_of_leg_contact_pertrial = []

        for fly in range(group_info.total_fly_number):
            fly_index = [ind for ind in group_info.landing_trial_index if ind[0] == fly + 1]
            individual_leg_contact["L-f"][f"F{fly + 1}"] = []
            individual_leg_contact["L-m"][f"F{fly + 1}"] = []
            individual_leg_contact["L-h"][f"F{fly + 1}"] = []
            individual_leg_contact["R-f"][f"F{fly + 1}"] = []
            individual_leg_contact["R-h"][f"F{fly + 1}"] = []
            for trial_index in fly_index:

                pose_data = group_info.fly_kinematic_data[f"F{trial_index[0]}T{trial_index[1]}"]
                start = int(pose_data.moc)
                end = int(pose_data.mol)

                center_points = self.calculator.ReadAndTranspose("platform-tip", pose_data)
                platform_ctr_pts_traces = np.array(center_points[300:350])
                intersects_moment = dict()

                for f in range(start, end):
                    line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
                        self.calculator.calculate_platform_surfaces(platform_traces=platform_ctr_pts_traces,
                                                                    platform_center=center_points[f],
                                                                    platform_offset=self.platform_offset,
                                                                    radius=self.radius, height=self.platform_height))
                    for point in segs:
                        if point[0][0:3] not in intersects_moment:
                            A = [pose_data.trial_data[f"{point[0]}"].x_coord[f],
                                 pose_data.trial_data[f"{point[0]}"].y_coord[f],
                                 pose_data.trial_data[f"{point[0]}"].z_coord[f]]
                            B = [pose_data.trial_data[f"{point[1]}"].x_coord[f],
                                 pose_data.trial_data[f"{point[1]}"].y_coord[f],
                                 pose_data.trial_data[f"{point[1]}"].z_coord[f]]

                            P0 = cylinder_bottom
                            d = direction
                            r = self.radius
                            h = self.platform_height
                            intersects, pt = self.calculator.check_cylinder_side_intersection(A, B, P0, d, r, h)
                            if intersects:
                                individual_leg_contact[point[0][0:3]][f"F{fly + 1}"].append((f - start) / self.fps)
                                intersects_moment[point[0][0:3]] = (f - start) / self.fps
                                break
                for point in segs:
                    if point[0][0:3] not in intersects_moment:
                        individual_leg_contact[point[0][0:3]][f"F{fly + 1}"].append(np.nan)
        import pprint
        pprint.pprint(individual_leg_contact)

        # Compute probabilities relative to total array length (including NaNs)
        result = {}
        max_subgroups = 0

        for group, subgroups in individual_leg_contact.items():
            probs = []
            for subgroup, values in subgroups.items():
                values = np.array(values)
                total_len = len(values)
                num_positive = np.sum(values > 0)
                prob = num_positive / total_len if total_len > 0 else np.nan
                probs.append(prob)
            result[group] = probs
            max_subgroups = max(max_subgroups, len(probs))

        # Convert to DataFrame
        df = pd.DataFrame(result)


        ax = sns.stripplot(data=df, alpha=0.5, size=20, jitter=0.2)

        ax.tick_params(axis="y", labelsize=25)
        ax.tick_params(axis="x", labelsize=25)
        ax.tick_params(width=3, length=20)
        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)
        ax.set_ylabel("Contact probability", fontsize=25)
        ax.set_yticks([0, 0.5, 1])
        ax.set_ylim(-0.1, 1.1)
        sns.despine(trim=True)
        plt.tight_layout()
        print(f"Save {group_info.group_name} contact probability")
        plt.savefig(f"{group_info.group_name} contact probability")
        plt.close()
        # plt.show()

        # Initialize output structure with np.nan
        ranked_data = {
            group: {
                subgroup: [np.nan] * len(values)
                for subgroup, values in subgroups.items()
            }
            for group, subgroups in individual_leg_contact.items()
        }

        # Get list of groups and subgroups
        groups = list(individual_leg_contact.keys())
        subgroups = list(next(iter(individual_leg_contact.values())).keys())  # assume all groups share same subgroups

        # Iterate over subgroups
        for subgroup in subgroups:
            max_len = max(len(individual_leg_contact[group][subgroup]) for group in groups)

            # For each index i in subgroup arrays
            for i in range(max_len):
                indexed_values = []
                for group in groups:
                    arr = individual_leg_contact[group][subgroup]
                    value = arr[i] if i < len(arr) else np.nan
                    if not np.isnan(value):
                        indexed_values.append((value, group))

                # Sort valid (non-nan) values
                sorted_values = sorted(indexed_values, key=lambda x: x[0])

                # Assign rank only to non-nan entries
                for rank, (value, group_name) in enumerate(sorted_values):
                    ranked_data[group_name][subgroup][i] = rank

        # Example output
        pprint.pprint(ranked_data)
        from collections import Counter

        records = []

        for group, subgroups in ranked_data.items():
            for subgroup, rank_list in subgroups.items():
                rank_series = pd.Series(rank_list)
                total_len = len(rank_series)
                # Count valid rank values
                rank_counts = rank_series.value_counts(dropna=True).sort_index()
                for rank in range(5):  # ranks 0 to 4
                    count = rank_counts.get(rank, 0)
                    if total_len == 0:
                        break
                    prob = count / total_len  # ← includes NaNs in denominator
                    records.append({
                        "group": group,
                        "subgroup": subgroup,
                        "rank": rank + 1,
                        "probability": prob
                    })


        # Step 2: Create DataFrame
        df = pd.DataFrame(records)
        # pprint.pprint(df)

        # Step 3: Plot
        plt.figure(figsize=(10, 6))
        ax = sns.stripplot(data=df, x="group", y="probability", hue="rank", dodge=True, jitter=True, s=15, alpha=0.5)

        ax.tick_params(axis="y", labelsize=25)
        ax.tick_params(axis="x", labelsize=25)
        ax.tick_params(width=3, length=20)

        plt.xlabel("Group")
        plt.ylabel("Probability")
        plt.legend(title="Leg contact order")
        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)
        ax.set_ylabel("Probability", fontsize=25)
        ax.set_yticks([0, 0.5, 1])
        ax.set_ylim(-0.1, 1.1)
        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"{group_info.group_name} leg order probability")
        plt.close()
        # plt.show()

        # Map legs to assigned numbers
        leg_order = {'L-f': 1, 'L-m': 2, 'L-h': 3, 'R-f': 4, 'R-h': 5}

        # Store sequences
        sequence_list = []

        # Loop through each subgroup (F1, F2, etc.)
        subgroup_names = next(iter(ranked_data.values())).keys()

        for subgroup in subgroup_names:
            # Get max number of time points in this subgroup
            max_len = max(len(ranked_data[leg][subgroup]) for leg in leg_order)

            for i in range(max_len):
                # Gather all ranks at this time point
                ranks = []
                for leg, leg_id in leg_order.items():
                    leg_ranks = ranked_data[leg].get(subgroup, [])
                    if i < len(leg_ranks):
                        rank = leg_ranks[i]
                        if not pd.isna(rank):
                            ranks.append((rank, leg_id))  # (rank value, leg number)

                # Sort by rank and collect leg numbers
                sorted_legs = [str(leg_id) for rank_val, leg_id in sorted(ranks)]
                if sorted_legs:
                    sequence = ''.join(sorted_legs)
                    sequence_list.append(sequence)

        # Count occurrences
        sequence_counts = Counter(sequence_list)

        # Convert to DataFrame for plotting
        df_seq = pd.DataFrame(sequence_counts.items(), columns=["sequence", "count"]).sort_values("count",
                                                                                                  ascending=False)

        top_n = 10
        df_top_seq = df_seq.head(top_n)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df_top_seq["sequence"], df_top_seq["count"], color="skyblue", edgecolor="black")
        ax.set_xticklabels(df_top_seq["sequence"], rotation=45)
        ax.tick_params(axis="y", labelsize=25)
        ax.tick_params(axis="x", labelsize=25)
        ax.tick_params(width=3, length=20)
        ax.set_xlabel("Leg Sequence (ordered by rank)")
        ax.set_ylabel("Count")
        ax.set_title("Top 10 Most Frequent Leg Rank Sequences")
        plt.title(f"Top {top_n} Most Frequent Leg Rank Sequences")
        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)

        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"{group_info.group_name} leg sequence")
        plt.close()
        # plt.show()
    def plot_angle_change_psd(self, group_info:Group):
        # fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(5, 8), sharex=True)
        One_search_CT_psd = []
        Many_searches_CT_psd = []
        No_search_CT_psd = []

        One_search_FT_psd = []
        Many_searches_FT_psd = []
        No_search_FT_psd = []

        f_psd_data = []
        m_psd_data = []
        h_psd_data = []

        Joint1 = "R-fCT"
        Color = "mediumpurple"
        Hz = 21

        for index in group_info.landing_trial_index:
            print(f"F{index[0]}T{index[1]}")
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            start = int(trial_info.moc)
            end = int(trial_info.mol)

            line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
                self.calculator.transform_coords_and_calculate_platform_data(trial_info=trial_info,
                                                                             platform_offset=self.platform_offset,
                                                                             platform_height=self.platform_height,
                                                                             radius=self.radius))
            perp_vector1[1] = -1
            BC = self.calculator.ReadAndTranspose(Joint1, trial_info)
            TT = self.calculator.ReadAndTranspose(Joint1[0:3] + "TT", trial_info)
            L_h_BC = self.calculator.calculate_BC_platform_angle(BC, TT, perp_vector1)[start:end]

            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            L_f_CT = np.asarray(angs[Joint1][start:end])

            sig_to_use = L_f_CT
            searches = "0"
            CT_psd_collector = []
            peaks, troughs = self.detector.detect_peaks_troughs(sig_to_use, leg=Joint1[0:3])
            first_trough = 0
            last_trough = 0
            if len(troughs) - 1 <= 0:
                CT_psd_collector = No_search_CT_psd
                troughs = self.detector.find_first_trough_CT_ang(sig_to_use)
                first_trough = troughs
                last_trough = len(sig_to_use) - 1
                print("No search CT")
            elif len(troughs) - 1 == 1:
                CT_psd_collector = One_search_CT_psd
                first_trough = troughs[0]
                last_trough = troughs[-1]
                searches = "1"
                print("One search CT")
            else:
                CT_psd_collector = Many_searches_CT_psd
                first_trough = troughs[0]
                last_trough = troughs[-1]
                searches = "n"
                print("Many search CT")



            from scipy.signal import periodogram
            from scipy.interpolate import interp1d
            # Periodogram


            troughs = troughs - first_trough
            print(first_trough, last_trough + 1, len(sig_to_use))
            # sig_to_use = sig_to_use[first_trough:last_trough]
            sig_to_use = sig_to_use[first_trough:]

            x_old = np.linspace(0, 1, len(sig_to_use))
            x_new = np.linspace(0, 1, trial_info.fps)
            f = interp1d(x_old, sig_to_use, kind='linear')
            sig_to_use = f(x_new)

            f_periodo, Pxx = periodogram(sig_to_use, trial_info.fps, nfft=trial_info.fps)
            f_periodo = f_periodo[:Hz]
            Pxx = Pxx[:Hz]
            CT_psd_collector.append((f_periodo, Pxx))


            fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
            seconds = np.array([s / trial_info.fps for s in range(len(sig_to_use))])
            sns.lineplot(x=seconds, y=sig_to_use, linewidth=5, ax=ax[0], color="blue")

            ax[0].tick_params(axis="y", labelsize=25)
            ax[0].tick_params(axis="x", labelsize=25)
            ax[0].tick_params(width=3, length=20)
            ax[0].spines["left"].set_linewidth(2)  # Top border
            ax[0].spines["bottom"].set_linewidth(2)
            ax[0].set_ylabel(f"{Joint1} angle", fontsize=25)
            ax[0].set_xlabel("Landing transition duration (s)", fontsize=25)
            ax[0].set_yticks([0, 30, 60, 90, 120, 150, 180])
            ax[0].set_ylim(-5, 185)
            ax[0].set_xticks([0, 1])

            # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
            ax[1].plot(f_periodo, Pxx, linewidth=5)
            ax[1].tick_params(axis="y", labelsize=15)
            ax[1].tick_params(axis="x", labelsize=15)
            ax[1].tick_params(width=3, length=10)
            ax[1].spines["left"].set_linewidth(2)  # Top border
            ax[1].spines["bottom"].set_linewidth(2)
            ax[1].set_yticks([0, 250, 500])
            ax[1].set_ylim(-10, 510)
            ax[1].set_xticks([0, (Hz - 1)/ 2, Hz - 1])
            ax[1].set_xlabel("Hz", fontsize=25)
            plt.suptitle(f"Fly{index[0]}_Trial{index[1]}_search_{searches}_angle_psd")
            sns.despine(trim=True)
            plt.tight_layout()
            plt.savefig(f"Fly{index[0]}_Trial{index[1]}_angle_psd")
            # plt.show()
            plt.close()

        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(5, 8), sharex=True)

        def formating(ax, psd_data,  color, linestyle, hatch_style):
            if len(psd_data) > 0:
                psd_data = np.asarray(psd_data)
                frequencies = psd_data[:, 0, :]  # shape: (3, 21)
                powers = psd_data[:, 1, :]  # shape: (3, 21)
                # Ensure all frequency axes are identical (optional sanity check)
                if not np.allclose(frequencies[0], frequencies):
                    raise ValueError("Mismatch in frequency axes!")

                # Use the first frequency axis (they are assumed the same)
                f = frequencies[0]
                mean_pxx = powers.mean(axis=0)

                for data in psd_data:
                    # ax.plot(data[0], data[1], color="grey", linewidth=1, linestyle="solid")
                    pass
                print(np.shape(powers))
                std_pxx = powers.std(axis=0)   # SEM
                ax.plot(f, mean_pxx, color=color, linewidth=4, linestyle=linestyle)

                if len(hatch_style) != 0:
                    ax.fill_between(f, mean_pxx - std_pxx, mean_pxx + std_pxx, color="none", alpha=0.4, hatch=hatch_style, edgecolor=color)
                else:
                    ax.fill_between(f, mean_pxx - std_pxx, mean_pxx + std_pxx, color=color, alpha=0.4)

                yl = 500
                ax.set_ylim([-20, yl])
                ax.set_yticks([0, yl])
                ax.spines["left"].set_bounds(0, yl)

            ax.get_xaxis().set_visible(False)
            ax.tick_params(labelbottom=False)  # Hide x-axis labels
            ax.set_xlabel("")
            ax.tick_params(axis="y", labelsize=15)
            ax.tick_params(width=3, length=5)
            ax.spines["left"].set_linewidth(2)  # Top border
            ax.spines["bottom"].set_linewidth(0)

        fig.supylabel("Periodogram (PSD)", fontsize=15)
        fig.supxlabel("Frequency (Hz)", fontsize=15)
        ax[0].set_title(f"{Joint1} 1 search (n = {len(One_search_CT_psd)})", fontsize=15)
        ax[1].set_title(f"{Joint1} > 1 searches (n = {len(Many_searches_CT_psd)})", fontsize=15)
        ax[2].set_title(f"{Joint1} 0 search (n = {len(No_search_CT_psd)})", fontsize=15)


        formating(ax[0], One_search_CT_psd, Color, "solid", "")
        formating(ax[1], Many_searches_CT_psd, Color, "dashed", "//")
        formating(ax[2], No_search_CT_psd, Color, "dotted", "|")
        ax[-1].get_xaxis().set_visible(True)
        ax[-1].tick_params(labelbottom=True)
        ax[-1].set_xticks([0, (Hz - 1) / 2, Hz - 1])
        ax[-1].set_xlim(-2, Hz + 1)
        ax[-1].tick_params(axis="x", labelsize=15)
        ax[-1].tick_params(width=3, length=5)
        ax[-1].spines["bottom"].set_linewidth(2)

        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"{group_info.group_name} leg psd")
        plt.show()

        # plt.show()
    def plot_InidividualLegContactDistribution(self, group_info:Group):
        segs = [["R-fTT", "R-fLT"],
                ["R-hTT", "R-hLT"],
                ["L-fTT", "L-fLT"],
                ["L-mTT", "L-mLT"],
                ["L-hTT", "L-hLT"]]  # T3
        L_f = [np.nan, np.nan, 303]
        L_m = [551, np.nan, 302]
        L_h = [550, 295, 304]
        R_f = [547, 293, 312]
        R_h = [538, 294, 301]
        individual_leg_contact = dict()
        individual_leg_contact["Leg"] = []
        individual_leg_contact["ContactLatency"] = []
        individual_leg_contact["LegContactOrder"] = []
        individual_leg_contact["NormalizedLatency"] = []
        individual_leg_contact["ContactToMOL"] = []
        num_of_leg_contact_pertrial = []
        index_to_iterate = group_info.get_targeted_trials(["Landing"])
        index_to_iterate = [(1, 1), (1, 2), (1, 3)]
        for index in index_to_iterate:
            # print(f"Fly: {index[0]} Trial: {index[1]}")
            pose_data = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            start = int(pose_data.moc)
            end = int(pose_data.mol)


            line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
                self.calculator.transform_coords_and_calculate_platform_data(trial_info=pose_data,
                                                                             platform_offset=self.platform_offset,
                                                                             platform_height=self.platform_height,
                                                                             radius=self.radius))

            center_points = self.calculator.ReadAndTranspose("platform-tip", pose_data)
            l = 0
            intersects_moment = dict()
            dist_trace = []
            found = False
            contact = 0
            for current_frame in range(start, end):
                for point in segs:
                    if point[0][0:3] not in intersects_moment:
                        A = [pose_data.trial_data[f"{point[0]}"].x_coord[current_frame],
                             pose_data.trial_data[f"{point[0]}"].y_coord[current_frame],
                             pose_data.trial_data[f"{point[0]}"].z_coord[current_frame]]
                        B = [pose_data.trial_data[f"{point[1]}"].x_coord[current_frame],
                             pose_data.trial_data[f"{point[1]}"].y_coord[current_frame],
                             pose_data.trial_data[f"{point[1]}"].z_coord[current_frame]]

                        P1 = center_points[current_frame]
                        d = direction
                        r = self.radius
                        h = self.platform_height
                        intersects_side, pt_side, min_dist = self.calculator.check_cylinder_side_intersection(A, B, P1, d, r, h)
                        intersects_top, pt_top = self.detector.check_leg_platform_intersection(A, B, d, center_points[current_frame], self.platform_offset)
                        if intersects_side or intersects_top:
                            l += 1
                            if index[1] < 10:
                                print(f"Fly: {index[0]} Trial: {index[1]}   Leg: {point[0][0:3]} Contact latency: {(current_frame - start) / pose_data.fps:.5f}  Normalized latency: {(current_frame - start) / (end - start):.5f}  Frame ind: {current_frame}")
                            else:
                                print(f"Fly: {index[0]} Trial: {index[1]}  Leg: {point[0][0:3]} Contact latency: {(current_frame - start) / pose_data.fps:.5f}  Normalized latency: {(current_frame - start) / (end - start):.5f}  Frame ind: {current_frame}")

                            # self.plot_motion_vector_with_plane(pose_data, current_frame)
                            individual_leg_contact["Leg"].append(point[0][0:3])
                            individual_leg_contact["ContactLatency"].append((current_frame - start) / pose_data.fps)
                            individual_leg_contact["NormalizedLatency"].append((current_frame - start) / (end - start))
                            individual_leg_contact["ContactToMOL"].append((end - current_frame)/(end - start))
                            intersects_moment[point[0][0:3]] = (current_frame - start) / pose_data.fps

                            # print(point[0][0:3], (f - start) / self.fps, (f - start) / (end - start), f, start, end)
                            break
            plt.plot(dist_trace)
            plt.show()
            segments_length = self.calculator.Calculate_segment_length(trial_info=pose_data, skeletons=[["L-mTT", "platform-tip"], ["L-mTT", "R-platform-tip"], ["L-mTT", "L-platform-tip"]])


            if l != 0:
                num_of_leg_contact_pertrial.append(l)
            for point in segs:
                if point[0][0:3] in intersects_moment:
                    larger = 0
                    for k in intersects_moment.keys():
                        if intersects_moment[k] < intersects_moment[point[0][0:3]] and k != point[0][0:3]:
                            larger += 1
                    individual_leg_contact["LegContactOrder"].append(larger + 1)
                    # print(f"Leg {point[0][0:3]}, Rank {larger + 1}, Latency {intersects_moment[point[0][0:3]]}")

        Colors = ["blue", "orange", "green", "red", "cyan"]
        individual_leg_contact = pd.DataFrame(individual_leg_contact)
        print(individual_leg_contact)
        r"""fig, ax = plt.subplots(nrows=len(segs), ncols=1, figsize=(10, 8))
        for i in range(len(segs)):
            filtered_df = individual_leg_contact[individual_leg_contact['Leg'] == segs[i][0][0:3]]
            if len(filtered_df["NormalizedLatency"]) > 1:

                sns.kdeplot(filtered_df["NormalizedLatency"], bw_adjust=0.3, color=Colors[i], ax=ax[i])
                sns.histplot(filtered_df["NormalizedLatency"], alpha=0.5, binwidth=0.02, color=Colors[i], ax=ax[i])

            ax[i].tick_params(axis="y", labelsize=15)
            ax[i].tick_params(axis="x", labelsize=15)
            ax[i].tick_params(width=3, length=5)
            ax[i].spines["left"].set_linewidth(2)  # Top border
            ax[i].spines["bottom"].set_linewidth(2)
            ax[i].set_title(segs[i][0][0:3], fontsize=10)
            ax[i].set_xlabel("")
            # ax[i].set_xlabel("Normalized landing transition", fontsize=15)
            ax[i].set_xticks([0, 0.5, 1], labels=["0\nmoc", "0.5", "1\nmol"])
            ax[i].set_xlim(-0.1, 1.1)
            ax[i].set_yticks([0, 15])
            ax[i].set_ylim(-0.1, 15.1)
        sns.despine(trim=True)
        plt.suptitle(f"Leg contact latency {group_info.group_name}")
        plt.tight_layout()
        # plt.show()
        plt.savefig(f"{group_info.group_name} contact latency")
        plt.close()"""


        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
        sns.stripplot(x="Leg", y="ContactToMOL", hue="Leg", data=individual_leg_contact, size=10, alpha=0.4)

        sns.despine(trim=True)
        plt.suptitle(f"Leg contact latency {group_info.group_name}")
        plt.tight_layout()
        plt.savefig(f"{group_info.group_name} contact latency")
        # plt.close()
        plt.show()
    def plotting_exp(self, group_info:Group):
        angles_to_plane = []
        aziumths = []
        for index in group_info.get_targeted_trials(["Landing", "Flying"]):
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
                self.calculator.transform_coords_and_calculate_platform_data(trial_info=trial_info,
                                                                             platform_offset=self.platform_offset,
                                                                             platform_height=self.platform_height,
                                                                             radius=self.radius))

            start = trial_info.moc
            end = trial_info.mol
            tita_points = self.calculator.ReadAndTranspose("R-mTT", trial_info)
            lt_points = self.calculator.ReadAndTranspose("R-mLT", trial_info)
            tita_points = np.mean(tita_points[start - 20:start], axis=0)
            lt_points = np.mean(lt_points[start - 20:start], axis=0)
            angle_to_plane, azimuth, v, v_proj, n, ref = self.calculator.angle_with_plane_and_azimuth(tita_points,
                                                                                                      lt_points,
                                                                                                      direction,
                                                                                                      np.array([0, 1, 0]))
            aziumths.append(azimuth)
            angles_to_plane.append((90 - angle_to_plane) / 90)

            origin = np.array([0, 0, 0])
            normal_tip = n / np.linalg.norm(n)

            # Plot the normal vector from the origin
            ax.quiver(*origin, *n, color='g', length=1, normalize=True)

            # Plot the segment vector from the tip of the normal vector (repositioned for visualization)
            ax.quiver(*normal_tip, *v, color='r', length=1, normalize=True)

            # Plot the projected vector also from the normal tip
            ax.quiver(*origin, *v_proj, color='b', length=1, normalize=True)

            # Plot the reference direction from the origin
            ax.quiver(*origin, *ref, color='orange', linestyle='dashed', length=1,
                      normalize=True)
            print(self.calculator.angle_between_vectors_360(origin - np.array([0, 1, 0]), origin - v_proj, True))
            # Plane surface (XY plane)

            plane_size = 1.5
            xx, yy = np.meshgrid(np.linspace(-plane_size, plane_size, 10), np.linspace(-plane_size, plane_size, 10))
            zz = np.zeros_like(xx)
            ax.plot_surface(xx, yy, zz, alpha=0.2, color='gray')

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            # ax.set_title(f"Angle to Plane: {angle_to_plane:.2f}°, Azimuth: {azimuth:.2f}°")
            ax.legend()

            plt.gca().set_aspect('equal')
            plt.tight_layout()
            plt.show()
            self.plot_motion_vector_with_plane(trial_info, start)

        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)

        azimuths_rad = np.radians(aziumths)


        for theta, r in zip(azimuths_rad, angles_to_plane):
            ax.annotate('', xy=(theta, r), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color='crimson', lw=2))
        # ax.plot(angles_to_plane, aziumths, 'o-', label="Vectors")

        # Optional: Add labels and grid
        ax.set_theta_zero_location("N")  # 0° is at the top (north)
        ax.set_theta_direction(-1)  # Clockwise

        ax.set_title("Vector Azimuths", va='bottom')
        ax.legend()
        plt.show()
    def plot_FTCT_characteristic(self, group_info:Group):
        inward_data = pd.read_excel(r"C:\Users\agrawal-admin\Desktop\Landing\Graph\Others\WT-T2-TiTa_outward_filtered.xlsx")
        outward_data = pd.read_excel(r"C:\Users\agrawal-admin\Desktop\Landing\Graph\Others\WT-T2-TiTa_inward_filtered.xlsx")
        index_to_iterate = group_info.get_targeted_trials(["Landing", "Flying"])
        out_sig = []
        in_sig = []
        combined_sig = []

        FT = True
        CT = False

        outward_color = ""
        inward_color = ""
        if FT:
            outward_color = "orangered"
            inward_color = "deepskyblue"
        if CT:
            outward_color = "orange"
            inward_color = "blue"

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
        total = 0
        out = 0
        IT_index = []
        OT_index = []
        for index in index_to_iterate:
            # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
            total += 1
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]

            line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
                self.calculator.transform_coords_and_calculate_platform_data(trial_info=trial_info,
                                                                             platform_offset=self.platform_offset,
                                                                             platform_height=self.platform_height,
                                                                             radius=self.radius))

            start = trial_info.moc
            end = trial_info.mol
            tita_points = self.calculator.ReadAndTranspose("R-mTT", trial_info)
            lt_points = self.calculator.ReadAndTranspose("R-mLT", trial_info)
            tita_points = np.mean(tita_points[start - 20:start], axis=0)
            lt_points = np.mean(lt_points[start - 20:start], axis=0)
            angle_to_plane, azimuth, v, v_proj, n, ref = self.calculator.angle_with_plane_and_azimuth(tita_points, lt_points, direction, np.array([0, 1, 0]))
            tita_contact_angle = self.calculator.angle_between_vectors_360(np.array([0, 0, 0]) - np.array([0, 1, 0]), np.array([0, 0, 0]) - v_proj, True)


            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            output_ll = end - start
            if start < 0:
                start, leg, position = self.analyzer.DetermineTiTaMOC(trial_info)
                end = start + trial_info.fps
                output_ll = -1

            seconds = [s / (end - start) for s in range(end - start)]
            FT_posture = np.mean(angs["R-mFT"][start - 20:start])
            CT_signal = angs["R-mCT"][start:end]
            FT_signal = angs["R-mFT"][start:end]

            signal_to_use = FT_signal
            signal_to_display = None
            if FT:
                signal_to_display = FT_signal
            elif CT:
                signal_to_display = CT_signal

            analysis_duration = int((end - start) * 0.8)
            trend_duration = int((end - start) * 0.8)
            slope_outward, extreme_counts = self.detector.MOC_touch_type_classifier("TiTa", "slopes", signal_to_use,
                                                                                    analysis_duration=analysis_duration)
            trend_outward, general_trend = self.detector.MOC_touch_type_classifier("TiTa", "trend", signal_to_use,
                                                                                    trend_duration=trend_duration)
            inward_proj = (tita_contact_angle > 100 and tita_contact_angle < 170)

            # Manual data
            if isinstance(outward_data.iloc[index[0] - 1][index[1]], int) or isinstance(outward_data.iloc[index[0] - 1][index[1]], float):
                out_sig.append(signal_to_display)
            if isinstance(inward_data.iloc[index[0] - 1][index[1]], int) or isinstance(inward_data.iloc[index[0] - 1][index[1]], float):
                in_sig.append(signal_to_display)

            combined_sig.append(signal_to_display)

            if trend_outward or slope_outward or FT_posture < 30:
                # sns.lineplot(x=seconds, y=signal_to_display, color=outward_color, ax=ax[0], linewidth=1, alpha=0.5)
                # out_sig.append(signal_to_display)
                group_info.predicted_data[f"F{index[0]}T{index[1]}"] = output_ll
                # print(f"Fly {index[0]} Trial {index[1]}: Outward touch, start: {start}, trend:{general_trend}, extreme:{extreme_counts}, FT posture {FT_posture}")
                out += 1
                IT_index.append(index)
            else:
                # sns.lineplot(x=seconds, y=signal_to_display, color=inward_color, ax=ax[1], linewidth=1, alpha=0.5)
                group_info.predicted_data[f"F{index[0]}T{index[1]}"] = "OT"
                # print(f"Fly {index[0]} Trial {index[1]}, Inward touch,  start: {start}, trend:{general_trend}, extreme:{extreme_counts}, FT posture {FT_posture}")
                # in_sig.append(signal_to_display)
                OT_index.append(index)

        r"""top_graph_tick_value = [0, 180]
        ax.tick_params(axis="y", labelsize=15)
        ax.tick_params(axis="x", labelsize=15)
        ax.tick_params(width=3, length=5)
        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)
        ax.set_xticks([0, 0.5, 1], labels=["0\nmoc", "0.5", "1\nmol"])
        ax.set_xlim(-0.1, 1.1)
        ax.set_yticks([top_graph_tick_value[0], (top_graph_tick_value[0] + top_graph_tick_value[1]) / 2, top_graph_tick_value[1]])
        ax.set_ylim(top_graph_tick_value[0] - 5, top_graph_tick_value[1] + 5)
        ax.set_title("Outward bending contact", fontsize=15)"""
        r"""ax[1].set_title("Normal contact", fontsize=15)
        ax[1].tick_params(axis="y", labelsize=15)
        ax[1].tick_params(axis="x", labelsize=15)
        ax[1].tick_params(width=3, length=5)
        ax[1].spines["left"].set_linewidth(2)  # Top border
        ax[1].spines["bottom"].set_linewidth(2)
        ax[1].set_xticks([0, 0.5, 1], labels=["0\nmoc", "0.5", "1\nmol"])
        ax[1].set_xlim(-0.1, 1.1)
        ax[1].set_yticks([bottom_graph_tick_value[0], (bottom_graph_tick_value[0] + bottom_graph_tick_value[1]) / 2,bottom_graph_tick_value[1]])
        ax[1].set_ylim(bottom_graph_tick_value[0] - 5, bottom_graph_tick_value[1] + 5)"""

        print(out / total)

        # group_info.convert_to_output_data()

        # self.manipulator.OutptuPrediction(group_info.convert_to_output_data(), f"{group_info.group_name}")


        common_len = group_info.fps[0]  # any length you want
        resampled_in = []
        resampled_out = []
        resampled_combined = []

        # fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

        from scipy.interpolate import interp1d
        for s in in_sig:
            x_old = np.linspace(0, 1, len(s))
            x_new = np.linspace(0, 1, common_len)
            f = interp1d(x_old, s, kind='linear')
            resampled_in.append(f(x_new))

        for s in out_sig:
            x_old = np.linspace(0, 1, len(s))
            x_new = np.linspace(0, 1, common_len)
            f = interp1d(x_old, s, kind='linear')
            resampled_out.append(f(x_new))

        for s in combined_sig:
            x_old = np.linspace(0, 1, len(s))
            x_new = np.linspace(0, 1, common_len)
            f = interp1d(x_old, s, kind='linear')
            resampled_combined.append(f(x_new))

        resampled_out = np.array(resampled_out)
        mean = resampled_out.mean(axis=0)
        sem = resampled_out.std(axis=0) / np.sqrt(len(resampled_out))

        top_graph_tick_value = [30, 90]
        x = np.linspace(0, 1, common_len)
        ax.plot(x, mean, linewidth=5, color=outward_color)
        ax.fill_between(x, mean - sem, mean + sem, alpha=0.3, label='SEM', color=outward_color)
        ax.tick_params(axis="y", labelsize=15)
        ax.tick_params(axis="x", labelsize=15)
        ax.tick_params(width=3, length=5)
        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)
        ax.set_xticks([0, 0.5, 1], labels=["0\nmoc", "0.5", "1\nmol"])
        ax.set_xlim(-0.1, 1.1)
        ax.set_yticks([top_graph_tick_value[0], (top_graph_tick_value[0] + top_graph_tick_value[1]) / 2, top_graph_tick_value[1]])
        ax.set_ylim(top_graph_tick_value[0] - 5, top_graph_tick_value[1] + 5)

        resampled_in = np.array(resampled_in)
        mean = resampled_in.mean(axis=0)
        sem = resampled_in.std(axis=0) / np.sqrt(len(resampled_in))
        x = np.linspace(0, 1, common_len)
        ax.plot(x, mean,  linewidth=5, color=inward_color)
        ax.fill_between(x, mean - sem, mean + sem, alpha=0.3, label='SEM', color=inward_color)

        resampled_combined = np.array(resampled_combined)
        mean = resampled_combined.mean(axis=0)
        sem = resampled_combined.std(axis=0) / np.sqrt(len(resampled_combined))
        ax.plot(x, mean,  linewidth=5, color="indigo")
        ax.fill_between(x, mean - sem, mean + sem, alpha=0.3, label='SEM', color="indigo")


        fig.supylabel('T2 Right FT angle', fontsize=20)
        sns.despine(trim=True)
        plt.xlabel("Standardized landing transition", fontsize=20)

        plt.tight_layout()
        plt.savefig(f"IT-OT-FT angle change.pdf")
        plt.show()

        IT_LL = []
        IT_posture = []
        OT_LL = []
        OT_posture = []
        for index in IT_index:
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            if trial_info.moc > 0 and (trial_info.mol - trial_info.moc) <= trial_info.fps:
                IT_LL.append((trial_info.mol - trial_info.moc) / trial_info.fps)
                angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
                IT_posture.append(np.mean(angs["R-mFT"][:trial_info.fps]))
        for index in OT_index:
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            if trial_info.moc > 0 and (trial_info.mol - trial_info.moc) <= trial_info.fps:
                OT_LL.append((trial_info.mol - trial_info.moc) / trial_info.fps)
                angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
                OT_posture.append(np.mean(angs["R-mFT"][:trial_info.fps]))

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
        plt.scatter(x=IT_posture, y=IT_LL, color="blue", alpha=0.5, s=100)
        plt.scatter(x=OT_posture, y=OT_LL, color="red", alpha=0.5, s=100)

        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)
        ax.set_xticks([0, 45, 90])
        ax.set_xlim(-5, 95)
        ax.set_xlabel("R-mFT angle", fontsize=25)
        ax.set_yticks([0, 0.5, 1])
        ax.set_ylim(-0.1, 1.1)
        ax.set_ylabel("Landing latency", fontsize=25)
        ax.tick_params(axis="y", labelsize=25)
        ax.tick_params(axis="x", labelsize=25)
        ax.tick_params(width=3, length=5)
        sns.despine(trim=True)

        plt.show()
    def plot_FTCT_manual(self, group_info:Group):

        index_to_iterate = [(12, 13, 1), (1, 1, 1), (1, 2, 1), (1, 3, 1), (1, 4, 1), (1, 5, 1), (1, 6, 1), (1, 7, 1), (1, 8, 1), (1, 9, 1), (1, 10, 1),
                            (1, 12, 0), (1, 14, 1), (1, 15, 1), (1, 16, 1), (1, 17, 1), (1, 18, 1), (1, 20, 1), (2, 1, 0), (2, 3, 0), (2, 6, 0),
                            (2, 11, 0), (2, 16, 0), (4, 5, 1), (4, 6, 1), (5, 5, 0)]
        out_sig = []
        in_sig = []

        FT = False
        CT = True

        outward_color = ""
        inward_color = ""
        if FT:
            outward_color = "orangered"
            inward_color = "deepskyblue"
        if CT:
            outward_color = "orange"
            inward_color = "blue"

        # fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
        total = 0
        out = 0
        for index in index_to_iterate:
            fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
            total += 1
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]

            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            start = trial_info.moc
            end = trial_info.mol
            output_ll = end - start
            if start < 0:
                start, leg, position = self.analyzer.DetermineTiTaMOC(trial_info)
                end = start + trial_info.fps
                output_ll = -1


            seconds = [s / (end - start) for s in range(end - start)]
            CT_signal = angs["R-mCT"][start:end]
            FT_signal = angs["R-mFT"][start:end]

            signal_to_use = FT_signal
            signal_to_display = None
            if FT:
                signal_to_display = FT_signal
            elif CT:
                signal_to_display = CT_signal

            analysis_duration = int((end - start) * 0.5)
            x = np.arange(analysis_duration)
            general_trend, _, _, _, _ = linregress(x, signal_to_use[:analysis_duration])

            if index[2] == 1:
                sns.lineplot(x=seconds, y=signal_to_display, color=outward_color, ax=ax[0], linewidth=1, alpha=0.5)
                out_sig.append(signal_to_display)
                group_info.predicted_data[f"F{index[0]}T{index[1]}"] = -1
                print(f"Fly {index[0]} Trial {index[1]}: Outward touch, start: {start}, general trend:{general_trend}")
                out += 1
            else:
                sns.lineplot(x=seconds, y=signal_to_display, color=inward_color, ax=ax[1], linewidth=1, alpha=0.5)
                group_info.predicted_data[f"F{index[0]}T{index[1]}"] = output_ll
                print(f"Fly {index[0]} Trial {index[1]}, Inward touch,  start: {start}, general trend:{general_trend}")
                in_sig.append(signal_to_display)

            top_graph_tick_value = [0, 90]
            bottom_graph_tick_value = [0, 90]
            ax[0].tick_params(axis="y", labelsize=15)
            ax[0].tick_params(axis="x", labelsize=15)
            ax[0].tick_params(width=3, length=5)
            ax[0].spines["left"].set_linewidth(2)  # Top border
            ax[0].spines["bottom"].set_linewidth(2)
            ax[0].set_xticks([0, 0.5, 1], labels=["0\nmoc", "0.5", "1\nmol"])
            ax[0].set_xlim(-0.1, 1.1)
            ax[0].set_yticks([top_graph_tick_value[0], (top_graph_tick_value[0] + top_graph_tick_value[1]) / 2, top_graph_tick_value[1]])
            ax[0].set_ylim(top_graph_tick_value[0] - 5, top_graph_tick_value[1] + 5)
            ax[0].set_title("Outward bending contact", fontsize=15)
            ax[1].set_title("Normal contact", fontsize=15)
            ax[1].tick_params(axis="y", labelsize=15)
            ax[1].tick_params(axis="x", labelsize=15)
            ax[1].tick_params(width=3, length=5)
            ax[1].spines["left"].set_linewidth(2)  # Top border
            ax[1].spines["bottom"].set_linewidth(2)
            ax[1].set_xticks([0, 0.5, 1], labels=["0\nmoc", "0.5", "1\nmol"])
            ax[1].set_xlim(-0.1, 1.1)
            ax[1].set_yticks([bottom_graph_tick_value[0], (bottom_graph_tick_value[0] + bottom_graph_tick_value[1]) / 2,bottom_graph_tick_value[1]])
            ax[1].set_ylim(bottom_graph_tick_value[0] - 5, bottom_graph_tick_value[1] + 5)
            fig.supylabel('FT angle upon moc', fontsize=20)
            sns.despine(trim=True)
            plt.xlabel("Standardized landing transition duration", fontsize=20)
            plt.tight_layout()
            plt.show()

        # plt.show()
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
    def plot_angle_change_traces(self, group_info:Group):

        Joint1 = "R-mCT"
        Joint4 = "R-mFT"

        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

        collected_angle_1 = []
        collected_angle_2 = []
        seconds = np.asarray([s / group_info.fps[0] for s in range(group_info.fps[0])])
        for index in group_info.get_targeted_trials(["Landing"]):
            print(f"F{index[0]}T{index[1]}")
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            start = int(trial_info.moc)
            end = int(trial_info.mol)
            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)


            L_f_CT = np.asarray(angs[Joint1][start:end])
            x_old = np.linspace(0, 1, len(L_f_CT))
            x_new = np.linspace(0, 1, trial_info.fps)
            f = interp1d(x_old, L_f_CT, kind='linear')
            L_f_CT = f(x_new)
            # L_f_CT = self.calculator.normalize_list(L_f_CT)
            # sns.lineplot(x=seconds, y=L_f_CT, linewidth=1, ax=ax[0], color="grey")
            collected_angle_1.append(L_f_CT)


            L_f_FT = np.asarray(angs[Joint4][start:end])
            x_old = np.linspace(0, 1, len(L_f_FT))
            x_new = np.linspace(0, 1, trial_info.fps)
            f = interp1d(x_old, L_f_FT, kind='linear')
            L_f_FT = f(x_new)
            # L_f_FT = self.calculator.normalize_list(L_f_FT)
            # sns.lineplot(x=seconds, y=L_f_FT, linewidth=1, ax=ax[1], color="grey")
            collected_angle_2.append(L_f_FT)

        collected_angle_1 = np.asarray(collected_angle_1)
        mean_angle_1 = collected_angle_1.mean(axis=0)
        sem = collected_angle_1.std(axis=0) / np.sqrt(len(collected_angle_1))
        print(np.shape(sem))
        ax[0].fill_between(seconds, mean_angle_1 - sem, mean_angle_1 + sem, color="blue", alpha=0.4)
        sns.lineplot(x=seconds, y=mean_angle_1, linewidth=5, ax=ax[0], color="blue")


        collected_angle_2 = np.asarray(collected_angle_2)
        mean_angle_2 = collected_angle_2.mean(axis=0)
        sem = collected_angle_2.std(axis=0) / np.sqrt(len(collected_angle_2))
        ax[1].fill_between(seconds, mean_angle_2 - sem, mean_angle_2 + sem, color="orange", alpha=0.4)
        sns.lineplot(x=seconds, y=mean_angle_2, linewidth=5, ax=ax[1], color="orange")

        ax[0].tick_params(axis="y", labelsize=15)
        ax[0].tick_params(axis="x", labelsize=15)
        ax[0].tick_params(width=3, length=10)
        ax[0].spines["left"].set_linewidth(2)  # Top border
        ax[0].spines["bottom"].set_linewidth(2)
        ax[0].set_ylabel(f"{Joint1} angle", fontsize=25)
        ax[0].set_xlabel("Landing transition duration (s)", fontsize=25)
        # ax[0].set_yticks([0, 0.5, 1])
        # ax[0].set_ylim(-0.1, 1.1)
        ax[0].set_yticks([50, 70, 90])
        ax[0].set_ylim(45, 95)

        ax[1].tick_params(axis="y", labelsize=15)
        ax[1].tick_params(axis="x", labelsize=15)
        ax[1].tick_params(width=3, length=10)
        ax[1].spines["left"].set_linewidth(2)  # Top border
        ax[1].spines["bottom"].set_linewidth(2)
        ax[1].set_ylabel(f"{Joint4} angle", fontsize=25)
        ax[1].set_xlabel("Landing transition duration (s)", fontsize=25)
        ax[1].set_yticks([20, 40, 60])
        ax[1].set_ylim(15, 65)
        # ax[1].set_yticks([0, 0.5, 1])
        # ax[1].set_ylim(-0.1, 1.1)
        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"{group_info.group_name}_angle_traces")
        plt.show()
    def normalized_leg_angle_change_trace(self, group_info:Group):
        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(5, 8), sharex=True)
        One_search_CT = []
        Many_searches_CT = []
        No_search_CT = []

        Joint = "R-hBC"

        for index in group_info.landing_trial_index:
            print(f"F{index[0]}T{index[1]}")
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            start = int(trial_info.moc)
            end = int(trial_info.mol)

            line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
                self.calculator.transform_coords_and_calculate_platform_data(trial_info=trial_info,
                                                                             platform_offset=self.platform_offset,
                                                                             platform_height=self.platform_height,
                                                                             radius=self.radius))
            perp_vector1[1] = -1
            BC = self.calculator.ReadAndTranspose(Joint, trial_info)
            TT = self.calculator.ReadAndTranspose(Joint[0:3] + "TT", trial_info)
            L_h_BC = self.calculator.calculate_BC_platform_angle(BC, TT, perp_vector1)[start:end]

            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            f_m_CT = np.asarray(angs[Joint][start:end])
            sig_to_use = f_m_CT

            peaks, troughs = self.detector.detect_peaks_troughs(sig_to_use, leg=Joint[0:3])

            if len(troughs) - 1 <= 0:
                No_search_CT.append(sig_to_use[self.detector.find_first_trough_CT_ang(sig_to_use):])
            elif len(troughs) - 1 == 1:
                One_search_CT.append(sig_to_use[troughs[0]:])
            else:
                Many_searches_CT.append(sig_to_use[troughs[0]:])

        def plot_standardized_trace(ax, collected_data, color, linestyle):
            for data in collected_data:
                # seconds = [x / len(data) for x in range(len(data))]
                seconds = [x / trial_info.fps for x in range(len(data))]
                ax.plot(seconds, data, color="grey", linestyle=linestyle, linewidth=1)

            ax.set_ylim([-5, 185])
            ax.set_yticks([0, 90, 180])
            # ax.spines["left"].set_bounds(0, yl)

            common_len = group_info.fps[0]
            resampled = []

            from scipy.interpolate import interp1d
            for s in collected_data:
                x_old = np.linspace(0, 1, len(s))
                x_new = np.linspace(0, 1, common_len)
                f = interp1d(x_old, s, kind='linear')
                resampled.append(f(x_new))


            resampled = np.array(resampled)
            mean = resampled.mean(axis=0)
            sem = resampled.std(axis=0) / np.sqrt(len(resampled))

            x = np.linspace(0, 1, common_len)
            if not isinstance(mean, np.float64):
                # ax.plot(x, mean, label='Mean', color=color, linestyle=linestyle, linewidth=5)
                pass


            ax.get_xaxis().set_visible(False)
            ax.tick_params(labelbottom=False)  # Hide x-axis labels
            ax.set_xlabel("")
            ax.tick_params(axis="y", labelsize=15)
            ax.tick_params(width=3, length=5)
            ax.spines["left"].set_linewidth(2)  # Top border
            ax.spines["bottom"].set_linewidth(0)

        fig.supylabel("Joint angle", fontsize=15)
        fig.supxlabel("Landing transition duration (moc - mol)", fontsize=15)
        ax[0].set_title(f"{Joint} 1 search (n = {len(One_search_CT)})", fontsize=15)
        ax[1].set_title(f"{Joint} > 1 searches (n = {len(Many_searches_CT)})", fontsize=15)
        ax[2].set_title(f"{Joint} 0 search (n = {len(No_search_CT)})", fontsize=15)

        Color = "mediumpurple"
        plot_standardized_trace(ax[0], One_search_CT, Color, "solid")
        plot_standardized_trace(ax[1], Many_searches_CT, Color, "dashed")
        plot_standardized_trace(ax[2], No_search_CT, Color, "dotted")
        ax[-1].get_xaxis().set_visible(True)
        ax[-1].tick_params(labelbottom=True)
        ax[-1].set_xticks([0, 0.5, 1])
        ax[-1].set_xlim(-0.1, 1.1)
        ax[-1].tick_params(axis="x", labelsize=15)
        ax[-1].tick_params(width=3, length=5)
        ax[-1].spines["bottom"].set_linewidth(2)

        sns.despine(trim=True)
        plt.tight_layout()
        plt.show()
        # plt.savefig(f"{group_info.group_name} leg psd")
    def plot_angle_change_traces_groups(self, groups):

        Joint = "R-mCT"


        colors = ["blue", "red", "orange", "green", "deepskyblue", "cyan", "olive", "indigo"]
        fig, ax = plt.subplots(nrows=len(groups), ncols=1, figsize=(5, 8))

        for g, group_info in enumerate(groups):
            collected_angle_1 = []
            group_info.read_all_data()
            group_info.filter_nan_fly()
            seconds = np.asarray([s / group_info.fps[0] for s in range(group_info.fps[0])])
            for index in group_info.get_targeted_trials(["Landing"]):
                print(f"G{group_info.group_name} F{index[0]} T{index[1]}")
                trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
                start = int(trial_info.moc)
                end = int(trial_info.mol)
                angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)


                L_f_CT = np.asarray(angs[Joint][start:end])
                x_old = np.linspace(0, 1, len(L_f_CT))
                x_new = np.linspace(0, 1, group_info.fps[0])
                f = interp1d(x_old, L_f_CT, kind='linear')
                L_f_CT = f(x_new)
                L_f_CT = self.calculator.normalize_list(L_f_CT)
                sns.lineplot(x=seconds, y=L_f_CT, linewidth=1, ax=ax[g], color="grey")
                collected_angle_1.append(L_f_CT)


            collected_angle_1 = np.asarray(collected_angle_1)
            mean_angle_1 = collected_angle_1.mean(axis=0)
            sem = collected_angle_1.std(axis=0) / np.sqrt(len(collected_angle_1))
            print(np.shape(sem))
            # ax[g].fill_between(seconds, mean_angle_1 - sem, mean_angle_1 + sem, color=colors[g], alpha=0.4)
            sns.lineplot(x=seconds, y=mean_angle_1, linewidth=5, ax=ax[g], color=colors[g], linestyle="dashed")

            ax[g].set_title(f"{group_info.group_name}", fontsize=10)
            ax[g].tick_params(axis="y", labelsize=15)
            ax[g].tick_params(width=3, length=10)
            ax[g].spines["left"].set_linewidth(2)  # Top border
            ax[g].spines["bottom"].set_linewidth(0)
            # ax[g].set_yticks([0, 90, 180])
            # ax[g].set_ylim(-5, 185)
            # ax[g].set_yticks([20, 40, 60])
            # ax[g].set_ylim(18, 62)
            # ax[g].set_yticks([50, 70, 90])
            # ax[g].set_ylim(48, 92)
            ax[g].set_yticks([0, 0.5, 1])
            ax[g].set_ylim(-0.05, 1.05)
            ax[g].get_xaxis().set_visible(False)
            ax[g].tick_params(labelbottom=False)  # Hide x-axis labels
            ax[g].set_xlabel("")
            ax[g].set_xlim(-0.05, 1.05)
        fig.supylabel(f"{Joint} angle", fontsize=25)
        ax[-1].get_xaxis().set_visible(True)
        ax[-1].tick_params(labelbottom=True)  # Hide x-axis labels
        # ax[-1].set_xlabel("")
        ax[-1].set_xticks([0, 0.5, 1], labels=["0\nmoc", "0.5", "1\nmol"])
        ax[-1].spines["bottom"].set_linewidth(2)
        ax[-1].tick_params(axis="x", labelsize=15)
        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"Collected_mean_{Joint}_angle_traces")
        plt.show()
    def plot_Inidi_Leg_Contact(self, group_info:Group):
        segs = [["R-fTT", "R-fLT"],
                ["R-hTT", "R-hLT"],
                ["L-fTT", "L-fLT"],
                ["L-mTT", "L-mLT"],
                ["L-hTT", "L-hLT"]]  # T3

        L_f = [np.nan, np.nan, 303]
        L_m = [551, np.nan, 302]
        L_h = [550, 295, 304]
        R_f = [547, 293, 312]
        R_h = [538, 294, 301]

        indi_leg_min_dist = dict()


        index_to_iterate = group_info.get_targeted_trials(["Landing"])
        index_to_iterate = [(1, 1), (1, 2), (1, 3)]
        for i, index in enumerate(index_to_iterate):
            indi_leg_min_dist["L-f"] = []
            indi_leg_min_dist["L-m"] = []
            indi_leg_min_dist["L-h"] = []
            indi_leg_min_dist["R-f"] = []
            indi_leg_min_dist["R-h"] = []
            pose_data = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            start = int(pose_data.moc)
            end = int(pose_data.mol)


            line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
                self.calculator.transform_coords_and_calculate_platform_data(trial_info=pose_data,
                                                                             platform_offset=self.platform_offset,
                                                                             platform_height=self.platform_height,
                                                                             radius=self.radius))

            center_points = self.calculator.ReadAndTranspose("platform-tip", pose_data)
            for current_frame in range(start, end):
                for point in segs:
                    A = [pose_data.trial_data[f"{point[0]}"].x_coord[current_frame],
                         pose_data.trial_data[f"{point[0]}"].y_coord[current_frame],
                         pose_data.trial_data[f"{point[0]}"].z_coord[current_frame]]
                    B = [pose_data.trial_data[f"{point[1]}"].x_coord[current_frame],
                         pose_data.trial_data[f"{point[1]}"].y_coord[current_frame],
                         pose_data.trial_data[f"{point[1]}"].z_coord[current_frame]]

                    P1 = center_points[current_frame]
                    d = direction
                    r = self.radius
                    h = self.platform_height
                    intersects_side, pt_side, min_dist = self.calculator.check_cylinder_side_intersection(A, B, P1, d, r, h)
                    # intersects_top, pt_top = self.detector.check_leg_platform_intersection(A, B, d, center_points[current_frame], self.platform_offset)
                    indi_leg_min_dist[point[0][0:3]].append(min_dist)
            sns.lineplot(indi_leg_min_dist["L-f"], color="blue", linewidth=5)
            sns.lineplot(abs(np.gradient(indi_leg_min_dist["L-f"])), color="blue", linewidth=3)
            plt.axvline(self.detector.detect_leg_contact(indi_leg_min_dist["L-f"]), color="blue")

            sns.lineplot(indi_leg_min_dist["L-m"], color="orange", linewidth=5)
            sns.lineplot(abs(np.gradient(indi_leg_min_dist["L-m"])), color="orange", linewidth=3)
            plt.axvline(self.detector.detect_leg_contact(indi_leg_min_dist["L-m"]), color="orange")

            sns.lineplot(indi_leg_min_dist["L-h"], color="green", linewidth=5)
            sns.lineplot(abs(np.gradient(indi_leg_min_dist["L-h"])), color="green", linewidth=3)
            plt.axvline(self.detector.detect_leg_contact(indi_leg_min_dist["L-h"]), color="green")

            sns.lineplot(indi_leg_min_dist["R-f"], color="grey", linewidth=5)
            sns.lineplot(abs(np.gradient(indi_leg_min_dist["R-f"])), color="grey", linewidth=3)
            plt.axvline(self.detector.detect_leg_contact(indi_leg_min_dist["R-f"]), color="grey")

            sns.lineplot(indi_leg_min_dist["R-h"], color="cyan", linewidth=5)
            sns.lineplot(abs(np.gradient(indi_leg_min_dist["R-h"])), color="cyan", linewidth=3)
            plt.axvline(self.detector.detect_leg_contact(indi_leg_min_dist["R-h"]), color="cyan")
            plt.show()


        Colors = ["blue", "orange", "green", "red", "cyan"]



        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
    def plot_angle_relative_mol(self, group_info:Group):

        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
        for index in group_info.get_targeted_trials(["Landing"]):
            print(f"Fly {index[0]} Trial {index[1]}")
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            start = int(trial_info.moc)
            end = int(trial_info.mol)
            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            R_mCT = angs["R-mCT"][start:end]
            R_mFT = angs["R-mFT"][start:end]
            seconds = [(s - (end - start - 1)) / trial_info.fps for s in range(end - start)]
            # seconds = [s / trial_info.fps for s in range(end - start)]
            sns.lineplot(x=seconds, y=R_mCT, linewidth=1, ax=ax[0], color="blue")
            sns.lineplot(x=seconds, y=R_mFT, linewidth=1, ax=ax[1], color="orange")

        ax[0].tick_params(axis="y", labelsize=15)
        ax[0].tick_params(axis="x", labelsize=15)
        ax[0].tick_params(width=3, length=10)
        ax[0].spines["left"].set_linewidth(2)  # Top border
        ax[0].spines["bottom"].set_linewidth(2)
        ax[0].set_ylabel(f"R-mCT angle", fontsize=25)
        ax[0].set_xlabel("Landing transition duration (s)", fontsize=25)
        ax[0].set_xticks([-1, -0.5, 0], labels=["-1", "-0.5", "0\nmol"])
        ax[0].set_yticks([0, 70, 140])
        ax[0].set_ylim(-5, 145)

        ax[1].tick_params(axis="y", labelsize=15)
        ax[1].tick_params(axis="x", labelsize=15)
        ax[1].tick_params(width=3, length=10)
        ax[1].spines["left"].set_linewidth(2)  # Top border
        ax[1].spines["bottom"].set_linewidth(2)
        ax[1].set_ylabel(f"R-mFT angle", fontsize=25)
        ax[1].set_xlabel("Landing transition duration (s)", fontsize=25)
        ax[1].set_xticks([-1, -0.5, 0], labels=["-1", "-0.5", "0\nmol"])
        ax[1].set_yticks([0, 70, 140])
        ax[1].set_ylim(-5, 145)
        sns.despine(trim=True)
        plt.tight_layout()
        plt.show()
        return
    def plot_FT_change(self, group_info:Group):

        import matplotlib.cm as cm
        # Choose a colormap (e.g., viridis, plasma, coolwarm, etc.)
        cmap = cm.get_cmap('viridis', 10)

        # Generate list of colors
        colors = [cmap(i) for i in range(10)]

        color = ["", "red", "green"]
        C = colors[0]
        joint = "R-mFT"
        start = 2
        stop = 6
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 5))
        LO_traces = []
        NL_traces = []
        UseLight = False
        fly_start = 11
        fly_stop = 25
        for index in group_info.get_targeted_trials(["Landing"]):
            # if index[0] >= fly_start and index[0] <= fly_stop:
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            data = angs[joint][int(start * trial_info.fps):int(stop * trial_info.fps)]
            print(f"F{index[0]}T{index[1]}")
            # if np.mean(data[:100]) < 30:
            if not np.isnan(data).any():
                if UseLight:
                    if "LO" in group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"].data_path:
                        # seconds = [(s / trial_info.fps) + start for s in range(len(data))]
                        # sns.lineplot(x=seconds, y=data, linewidth=1, color="grey", ax=ax[0])
                        LO_traces.append(data)
                    if "NL" in group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"].data_path:
                        # seconds = [(s / trial_info.fps) + start for s in range(len(data))]
                        # sns.lineplot(x=seconds, y=data, linewidth=1, color="grey", ax=ax[1])
                        NL_traces.append(data)
                else:
                    LO_traces.append(data)



        LO_traces = np.asarray(LO_traces)
        avg = LO_traces.mean(axis=0)
        n = LO_traces.shape[0]
        sem = LO_traces.std(axis=0, ddof=1) / np.sqrt(n)

        seconds = [(s / group_info.fps[0]) + start for s in range(len(avg))]
        sns.lineplot(x=seconds, y=avg, linewidth=5, linestyle="dashed", color=C, alpha=0.7)
        ax.fill_between(seconds, avg - sem, avg + sem, alpha=0.25, color=C, linewidth=0)

        if UseLight:
            NL_traces = np.asarray(NL_traces)
            avg = NL_traces.mean(axis=0)
            n = NL_traces.shape[0]
            sem = NL_traces.std(axis=0, ddof=1) / np.sqrt(n)

            seconds = [(s / group_info.fps[0]) + start for s in range(len(avg))]
            sns.lineplot(x=seconds, y=avg, linewidth=5, linestyle="solid", color=C, alpha=0.7)
            ax.fill_between(seconds, avg - sem, avg + sem, alpha=0.25, color=C, linewidth=0)

        legend_handles = []  # List to store legend handles
        legend_labels = []
        legend_labels.append("ON")
        legend_labels.append("OFF")
        from matplotlib.lines import Line2D
        legend_handles.append(Line2D([0], [0], color="black", linestyle="dashed", lw=3))
        legend_handles.append(Line2D([0], [0], color="black", linestyle="solid", lw=3))
        ax.legend(legend_handles, legend_labels, fontsize=20, loc="upper right", frameon=True)


        ax.axvline(5, color="grey", linestyle="dashed", linewidth=3)
        ax.axvline(3, color="grey", linestyle="dashed", linewidth=3)


        ax.get_xaxis().set_visible(True)
        ax.tick_params(labelbottom=True)

        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)

        ax.set_xticks([2, 3, 4, 5, 6], labels=["2", "3\nlight start", "4", "5\nlight stop", "6"])
        ax.set_yticks([0, 90, 180])
        ax.set_ylim(-5, 185)

        ax.tick_params(axis="y", labelsize=15)
        ax.tick_params(axis="x", labelsize=15)
        ax.tick_params(width=3, length=5)

        ax.set_ylabel(f"{joint} angle", fontsize=25)
        ax.set_xlabel("Time (s)", fontsize=25)
        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"{group_info.group_name}WingAngleChange.pdf")
        plt.show()
    def plot_Flying_landing_FTCT(self, group_info:Group):

        FT = True
        CT = False

        Flying_color = ""
        Landing_color = ""
        if FT:
            Flying_color = "orange"
            Landing_color = "blue"
        if CT:
            Flying_color = "orange"
            Landing_color = "blue"

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
        total = 0
        out = 0
        F_signals = []
        L_signals = []

        index_to_iterate = group_info.get_targeted_trials(["Landing"])
        for index in index_to_iterate:
            print(f"Fly {index[0]} Trial {index[1]}")
            total += 1
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]

            start = trial_info.moc
            end = trial_info.mol


            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            seconds = [s / (end - start) for s in range(end - start)]
            CT_signal = angs["R-mCT"][start:end]
            FT_signal = angs["R-mFT"][start:end]

            signal_to_display = None
            if FT:
                signal_to_display = FT_signal

            elif CT:
                signal_to_display = CT_signal

            # sns.lineplot(x=seconds, y=signal_to_display, color="grey", ax=ax[0], linewidth=1)
            L_signals.append(signal_to_display)


        index_to_iterate = group_info.get_targeted_trials(["Flying"])
        print(index_to_iterate)
        for index in index_to_iterate:
            print(f"Fly {index[0]} Trial {index[1]}")
            total += 1
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]

            line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2 = (
                self.calculator.transform_coords_and_calculate_platform_data(trial_info=trial_info,
                                                                             platform_offset=self.platform_offset,
                                                                             platform_height=self.platform_height,
                                                                             radius=self.radius))

            start = trial_info.moc

            if start < 0:
                start, leg, position = self.analyzer.DetermineTiTaMOC(trial_info=trial_info)
                end = start + trial_info.fps
            else:
                end = start + trial_info.fps


            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            seconds = [s / (end - start) for s in range(end - start)]
            CT_signal = angs["R-mCT"][start:end]
            FT_signal = angs["R-mFT"][start:end]

            signal_to_display = None
            if FT:
                signal_to_display = FT_signal

            elif CT:
                signal_to_display = CT_signal

            # sns.lineplot(x=seconds, y=signal_to_display, color="grey", ax=ax[1], linewidth=1)
            F_signals.append(signal_to_display)




        common_len = group_info.fps[0]  # any length you want
        resampled_L = []
        resampled_F = []




        from scipy.interpolate import interp1d
        for s in L_signals:
            x_old = np.linspace(0, 1, len(s))
            x_new = np.linspace(0, 1, common_len)
            f = interp1d(x_old, s, kind='linear')
            resampled_L.append(f(x_new))

        for s in F_signals:
            x_old = np.linspace(0, 1, len(s))
            x_new = np.linspace(0, 1, common_len)
            f = interp1d(x_old, s, kind='linear')
            resampled_F.append(f(x_new))

        x = np.linspace(0, 1, common_len)

        resampled_L = np.array(resampled_L)
        mean = resampled_L.mean(axis=0)
        sem = resampled_L.std(axis=0) / np.sqrt(len(resampled_L))
        ax.plot(x, mean, linewidth=5, color=Landing_color)
        ax.fill_between(x, mean - sem, mean + sem, alpha=0.3, label='SEM', color=Landing_color)

        resampled_F = np.array(resampled_F)
        mean = resampled_F.mean(axis=0)
        ax.plot(x, mean, linewidth=5, color=Flying_color)
        sem = resampled_F.std(axis=0) / np.sqrt(len(resampled_F))
        ax.fill_between(x, mean - sem, mean + sem, alpha=0.3, label='SEM', color=Flying_color)


        bottom_graph_tick_value = [30, 90]
        ax.set_title("Flying", fontsize=15)
        ax.tick_params(axis="y", labelsize=15)
        ax.tick_params(axis="x", labelsize=15)
        ax.tick_params(width=3, length=5)
        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)
        ax.set_xticks([0, 0.5, 1], labels=["0\nmoc", "0.5", "1\nmol"])
        ax.set_xlim(-0.1, 1.1)
        ax.set_yticks([bottom_graph_tick_value[0], (bottom_graph_tick_value[0] + bottom_graph_tick_value[1]) / 2,bottom_graph_tick_value[1]])
        ax.set_ylim(bottom_graph_tick_value[0] - 5, bottom_graph_tick_value[1] + 5)
        fig.supylabel('T2 Right FT angle', fontsize=20)
        plt.xlabel("Standardized landing transition", fontsize=20)

        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig("L-F-FT angle.pdf")
        plt.show()
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


        # Find the maximum length among all lists
        # max_len = max(len(v) for v in collected_data.values())

        # Pad each list with NaN (or any other fill value) to the max length
        # padded = {k: v + [np.nan] * (max_len - len(v)) for k, v in collected_data.items()}
        collected_data = pd.DataFrame(collected_data)

        test_groups = collected_data.groupby("Group_Name")["RmFTAngle"].apply(list)
        self.calculator.Bootstrapping_test(list(test_groups["WT-T2-TiTa"]), list(test_groups["G106-HP1"]))
        self.calculator.Bootstrapping_test(list(test_groups["WT-T2-TiTa"]), list(test_groups["G107-HP2"]))
        self.calculator.Bootstrapping_test(list(test_groups["WT-T2-TiTa"]), list(test_groups["G108-HP3"]))
        self.calculator.Bootstrapping_test(list(test_groups["WT-T2-TiTa"]), list(test_groups["G114-ClFl"]))
        self.calculator.Bootstrapping_test(list(test_groups["WT-T2-TiTa"]), list(test_groups["G116-ClEx"]))
        self.calculator.Bootstrapping_test(list(test_groups["WT-T2-TiTa"]), list(test_groups["G117-HkFl"]))
        self.calculator.Bootstrapping_test(list(test_groups["WT-T2-TiTa"]), list(test_groups["G118-HkEx"]))
        self.calculator.Bootstrapping_test(list(test_groups["WT-T2-TiTa"]), list(test_groups["G119-Club"]))
        self.calculator.Bootstrapping_test(list(test_groups["WT-T2-TiTa"]), list(test_groups["G115-Iav"]))


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

                    """cutoff = 1  # remove frequencies below 1 Hz
                    data = highpass_filter(data, cutoff, trial_info.fps)
                    # data = data - np.mean(data)
                    X = np.fft.fft(data)  # Compute FFT
                    freqs = np.fft.fftfreq(len(data), 1 / trial_info.fps)  # Frequency axis
                    power = np.abs(X) ** 2  # Power spectrum
                    amplitude = np.abs(X)  # Amplitude spectrum

                    # Keep only positive frequencies
                    mask = freqs >= 0
                    freqs = freqs[mask]
                    power = power[mask]
                    amplitude = amplitude[mask]
                    """
                    # print(len(f))
                    # print(len(Pxx))

                    # sns.lineplot(sig)
                    # plt.show()
                    # sns.lineplot(x=f, y=Pxx)
                    # plt.xticks([0, 25, 50])
                    # plt.show()
                    # print(f)

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
        """# Create 3D figure
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        from scipy.stats import chi2
        def plot_ellipsoid(points, confidence=0.95, color="blue", alpha=0.25):
            # Mean + covariance
            center = np.mean(points, axis=0)
            cov = np.cov(points.T)

            # Eigenvalues/vectors
            eigvals, eigvecs = np.linalg.eigh(cov)

            # Scale eigenvalues for confidence region
            k = np.sqrt(chi2.ppf(confidence, df=3))
            radii = k * np.sqrt(eigvals)

            # Parametric ellipsoid grid
            u = np.linspace(0, 2 * np.pi, 40)
            v = np.linspace(0, np.pi, 20)

            x = radii[0] * np.outer(np.cos(u), np.sin(v))
            y = radii[1] * np.outer(np.sin(u), np.sin(v))
            z = radii[2] * np.outer(np.ones_like(u), np.cos(v))

            # Stack and rotate
            ellip = np.stack([x, y, z], axis=-1)
            ellip_rot = ellip @ eigvecs.T + center  # rotate + translate

            ax.plot_surface(
                ellip_rot[..., 0],
                ellip_rot[..., 1],
                ellip_rot[..., 2],
                color=color,
                alpha=alpha,
                linewidth=0,
            )

        for g, c in zip(unique_groups, colors):
            mask = groups_name == g
            ax.scatter(
                scores[mask, 0],  # PC1
                scores[mask, 1],  # PC2
                scores[mask, 2],  # PC3
                label=g,
                color=c,
                s=50,
                alpha=0.7
            )
            # plot_ellipsoid(scores[mask, :3], color=c, alpha=0.25)


        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_zlabel('PC3')
        plt.show()"""

        """ax.scatter(
                scores[mask, 0],  # PC1
                scores[mask, 1],  # PC2
                scores[mask, 2],  # PC3
                label=g,
                color=c,
                s=50,
                alpha=0.7
            )

        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_zlabel('PC3')
        ax.set_title('3D PCA of Trials')
        ax.legend()
        plt.tight_layout()
        plt.show()"""



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
        plt.show()
    def plot_ON_OFF_angle(self, group_info:Group):

        color = ["", "red", "green"]
        joint = "R-mTT"
        start = 2
        stop = 6
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 5))
        LO_angle = []
        NL_angle = []
        for index in group_info.get_targeted_trials(["Landing", "Flying"]):
            trial_info = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            MOC = trial_info.moc
            angs = self.calculator.Calculate_joint_angle(trial_info, self.angles)
            data = angs[joint][int(start * trial_info.fps):int(stop * trial_info.fps)]
            print(f"F{index[0]}T{index[1]}")
            if not np.isnan(data).any():
                if "LO" in group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"].data_path:
                    LO_angle.append(np.mean(data[MOC - 250:MOC]))
                if "NL" in group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"].data_path:
                    NL_angle.append(np.mean(data[MOC-250:MOC]))

        df = pd.DataFrame(
            {
                "Angles": LO_angle + NL_angle,
                "Group": [f"{group_info.group_name}-ON"] * len(LO_angle) + [f"{group_info.group_name}-OFF"] * len(NL_angle)
            }
        )
        sns.stripplot(data=df, x="Group", y="Angles", size=15, alpha=0.5, ax=ax)
        # sns.violinplot(data=df, x="Group", y="Angles", alpha=0.5, ax=ax)
        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)

        ax.set_yticks([0, 90, 180])
        ax.set_ylim(-5, 185)
        ax.set_xticks([0, 1])
        ax.set_xlim(-1, 2)

        ax.tick_params(axis="y", labelsize=15)
        ax.tick_params(axis="x", labelsize=15)
        ax.tick_params(width=3, length=5)

        ax.set_ylabel(f"{joint} angle", fontsize=25)
        sns.despine(trim=True)
        plt.tight_layout()
        plt.savefig(f"{group_info.group_name}WingAngleChange.pdf")
        plt.show()







    #  def plot_LT_distance_to_platform(self, trial_info:Trial):
