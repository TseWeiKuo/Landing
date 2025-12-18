import os
import numpy as np
import pandas as pd
from openpyxl.styles import PatternFill
from openpyxl import load_workbook
from scipy.signal import find_peaks, hilbert
import matplotlib.pyplot as plt
from kinematic_object import Group, Trial
import warnings
import seaborn as sns
import pywt
warnings.filterwarnings(action="ignore", category=FutureWarning)

"""
These functions are responsible for preprocessing of angle data and 3D pose data
"""
class SimpleCalculation:
    # Smooth the input data using ema
    def exponential_moving_average(self, data, alpha):
        if isinstance(data, pd.Series):
            data = data.tolist()
        smoothed_data = [data[0]]
        for i in range(1, len(data)):
            smoothed_data.append(alpha * data[i] + (1 - alpha) * smoothed_data[-1])
        return smoothed_data
    # Normalized the input list based on min-max method
    def normalize_list(self, data, method="min-max"):
        if method == "min-max":
            min_val = min(data)
            max_val = max(data)
            if max_val == min_val:
                raise ValueError("Cannot perform Min-Max normalization when all values are the same.")
            return [(x - min_val) / (max_val - min_val) for x in data]
        if method == "z-score":
            """
            Perform Z-score normalization on a 1D signal.

            Parameters:
            -----------
            signal : array-like
                Input signal (list or 1D numpy array).

            Returns:
            --------
            normalized_signal : numpy.ndarray
                Z-score normalized signal with mean = 0 and std = 1.
            """
            signal = np.asarray(data)
            mean = np.mean(signal)
            std = np.std(signal)
            if std == 0:
                return np.zeros_like(signal)  # Avoid division by zero
            return (signal - mean) / std
    # Calculate the distance between two point in 3D space
    def Calculate_distance_between_points(self, x, y, z, x1, y1, z1):
        return np.sqrt((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2)
    # Calculate the angle between pt1, pt2, and pt3 in 3D space
    def calculate_angle(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        # Define points as numpy arrays
        pt1 = np.array([x1, y1, z1])
        pt2 = np.array([x2, y2, z2])
        pt3 = np.array([x3, y3, z3])

        # Define vectors
        vecA = pt1 - pt2
        vecB = pt3 - pt2

        # Calculate dot product and magnitudes
        dot_product = np.dot(vecA, vecB)
        magnitude_A = np.linalg.norm(vecA)
        magnitude_B = np.linalg.norm(vecB)

        # Calculate angle in radians
        angle_rad = np.arccos(dot_product / (magnitude_A * magnitude_B))

        # Convert to degrees if needed
        angle_deg = np.degrees(angle_rad)

        return angle_deg
    # Transpose a dataframe
    def TransposeData(self, df):
        df = pd.DataFrame(df)
        df = df.T
        return df
    # Calculate the specified segments' length and return a dictionary
    def Calculate_segment_length(self, trial_info:Trial, skeletons):
        # Initialize the dictionary data to stor segments' length
        collected_seg_length_data = dict()

        # Iterate through the specified segments
        for seg in skeletons:

            # If segment not in dictionary, create one
            if f"{seg[0]}_{seg[1]}" not in collected_seg_length_data.keys():
                collected_seg_length_data[f"{seg[0]}_{seg[1]}"] = []

            for f in range(trial_info.total_frames_number):
                collected_seg_length_data[f"{seg[0]}_{seg[1]}"].append(
                    self.Calculate_distance_between_points(
                        x=trial_info.trial_data[f"{seg[0]}"].x_coord[f],
                        y=trial_info.trial_data[f"{seg[0]}"].y_coord[f],
                        z=trial_info.trial_data[f"{seg[0]}"].z_coord[f],
                        x1=trial_info.trial_data[f"{seg[1]}"].x_coord[f],
                        y1=trial_info.trial_data[f"{seg[1]}"].y_coord[f],
                        z1=trial_info.trial_data[f"{seg[1]}"].z_coord[f]))

        # Convert the dictionary to dataframe
        collected_seg_length_data = pd.DataFrame(collected_seg_length_data)

        # return the data
        return collected_seg_length_data
    # Calculate the angles between specified key points.
    def Calculate_joint_angle(self, data:Trial, angles):

        collected_angle_data = dict()

        for ag in angles:
            if f"{ag[1]}" not in collected_angle_data.keys():
                collected_angle_data[f"{ag[1]}"] = []

            for f in range(data.total_frames_number):
                angle = self.calculate_angle(x1=data.trial_data[f"{ag[0]}"].x_coord[f],
                                             y1=data.trial_data[f"{ag[0]}"].y_coord[f],
                                             z1=data.trial_data[f"{ag[0]}"].z_coord[f],
                                             x2=data.trial_data[f"{ag[1]}"].x_coord[f],
                                             y2=data.trial_data[f"{ag[1]}"].y_coord[f],
                                             z2=data.trial_data[f"{ag[1]}"].z_coord[f],
                                             x3=data.trial_data[f"{ag[2]}"].x_coord[f],
                                             y3=data.trial_data[f"{ag[2]}"].y_coord[f],
                                             z3=data.trial_data[f"{ag[2]}"].z_coord[f])
                collected_angle_data[f"{ag[1]}"].append(angle)
            collected_angle_data[f"{ag[1]}"] = np.array(collected_angle_data[f"{ag[1]}"])
        return collected_angle_data
    # Calculate the absolute value of derivative of the input data
    def Calculate_derivative(self, data):
        if len(data) < 2:
            raise ValueError("The input list must contain at least two elements to calculate a derivative.")

        # Compute the differences between consecutive elements
        data = [data[i + 1] - data[i] for i in range(len(data) - 1)]
        data = [abs(x) for x in data]
        return data
    # Calculate the angle between a vector and a normal plane given the plane's normal vector
    def angle_between_vectors(self, v, n):
        """
        Calculate the angle (in degrees) between a vector and a plane
        given the vector and the normal vector of the plane.

        Parameters:
        v : array-like
            The input vector.
        n : array-like
            The normal vector of the plane.

        Returns:
        angle_deg : float
            The angle between the vector and the plane in degrees.
        """
        v = np.array(v)
        n = np.array(n)

        # Normalize the vectors
        v_norm = np.linalg.norm(v)
        n_norm = np.linalg.norm(n)

        # Dot product
        dot_product = np.dot(v, n)

        # Angle between v and n
        phi_rad = np.arccos(np.clip(dot_product / (v_norm * n_norm), -1.0, 1.0))
        # Angle between vector and plane is 90 - phi
        theta_rad = np.pi / 2 - phi_rad
        # Convert to degrees
        angle_deg = np.degrees(theta_rad)

        return angle_deg
    # Calculate the intersection between a segment and a plane.
    def line_plane_intersection(self, p1, p2, normal, d):
        # Line represented as p(t) = p1 + t * (p2 - p1)
        direction = np.array(p2) - np.array(p1)
        denom = np.dot(normal, direction)

        if abs(denom) < 1e-6:  # Parallel case
            return None, None

        t = -(np.dot(normal, p1) + d) / denom

        if 0 <= t <= 1:  # Ensure intersection is within the segment
            return p1 + t * direction, t
        return None, None
    # Determine if the intersection is inside a circle determined by the radius and certain point
    def is_inside_circle(self, intersection, center, radius):
        distance_to_tip = np.linalg.norm(intersection - center)
        return np.linalg.norm(intersection - center) <= radius
    # Finding the direction of the best fit line in 3D space
    def best_fit_line_3d(self, points):
        points = np.array(points)
        centroid = np.mean(points, axis=0)
        centered_points = points - centroid
        _, _, Vt = np.linalg.svd(centered_points)
        direction = Vt[0]  # First principal component
        return centroid, direction
    # Detect the contact between leg segment and side of cylindrical platform
    def check_cylinder_side_intersection(self, A, B, P1, d, r, h, n_steps=100):
        """
        Check if the segment AB intersects the side surface of a finite cylinder,
        using the cylinder's top point instead of the base.

        Parameters:
            A, B : ndarray
                Endpoints of the leg segment (3D).
            P1 : ndarray
                A point at the top of the cylinder axis.
            d : ndarray
                Unit vector of the cylinder axis (pointing from base to top).
            r : float
                Radius of the cylinder.
            h : float
                Height of the cylinder.
            n_steps : int
                Number of steps to interpolate along the segment.

        Returns:
            (bool, point, min_dist): True and intersection point if intersects, otherwise False, None
        """

        A, B, P1, d = map(np.asarray, (A, B, P1, d))
        d = d / np.linalg.norm(d)  # ensure it's a unit vector

        # Calculate the base of the cylinder from the top point
        P0 = P1 - h * d
        min_dist = np.inf
        for t in np.linspace(0, 1, n_steps):
            Pt = A + t * (B - A)
            v = Pt - P0
            proj_len = np.dot(v, d)
            dist_to_axis = np.linalg.norm(v - proj_len * d)
            if dist_to_axis < min_dist:
                min_dist = dist_to_axis
            if 0 <= proj_len <= h:
                if np.isclose(dist_to_axis, r) or dist_to_axis < r:
                    return True, Pt, min_dist
        return False, None, min_dist
    def ReadAndTranspose(self, point, kinematic_data: Trial):
        return np.transpose(np.asarray([kinematic_data.trial_data[point].x_coord,
                                        kinematic_data.trial_data[point].y_coord,
                                        kinematic_data.trial_data[point].z_coord]))
    def calculate_platform_surfaces(self, platform_traces, platform_center, platform_offset, radius, height):

        centroid, direction = self.best_fit_line_3d(platform_traces)

        # Generate points along the best-fit line
        t_vals = np.linspace(-10, 10, 100)
        line_points = centroid + np.outer(t_vals, direction)

        # Generate a normal plane to the direction vector at the centroid
        normal_vector = direction
        # Create two perpendicular vectors using cross products
        if np.allclose(normal_vector, [1, 0, 0]):  # Handle edge case if aligned with x-axis
            perp_vector1 = np.cross(normal_vector, [0, 1, 0])
        else:
            perp_vector1 = np.cross(normal_vector, [1, 0, 0])

        perp_vector1 /= np.linalg.norm(perp_vector1)  # Normalize
        perp_vector2 = np.cross(normal_vector, perp_vector1)
        perp_vector2 /= np.linalg.norm(perp_vector2)  # Normalize

        # Generate a circular grid
        u_vals = np.linspace(-radius, radius, 50)
        v_vals = np.linspace(-radius, radius, 50)
        U, V = np.meshgrid(u_vals, v_vals)

        # Convert to polar coordinates to filter for a circular region
        mask = U ** 2 + V ** 2 <= radius ** 2  # Boolean mask for circle

        # Apply mask to keep only circular region
        U = U[mask]
        V = V[mask]

        platform_plane_origin = platform_center + platform_offset * direction  # Shift the plane up
        plane_points = platform_plane_origin + U[..., None] * perp_vector1 + V[..., None] * perp_vector2

        # Define top and bottom centers of the cylinder
        cylinder_top = platform_plane_origin
        cylinder_bottom = cylinder_top - direction * height
        # Generate points around the circumference

        theta = np.linspace(0, 2 * np.pi, 60)
        circle_top = np.array([
            cylinder_top + radius * (np.cos(t) * perp_vector1 + np.sin(t) * perp_vector2)
            for t in theta
        ])
        circle_bottom = np.array([
            cylinder_bottom + radius * (np.cos(t) * perp_vector1 + np.sin(t) * perp_vector2)
            for t in theta
        ])
        # Create side surface polygons (vertical quads)
        verts = []
        for i in range(len(theta) - 1):
            quad = [circle_bottom[i], circle_bottom[i + 1], circle_top[i + 1], circle_top[i]]
            verts.append(quad)

        return line_points, plane_points, verts, cylinder_top, cylinder_bottom, direction, perp_vector1, perp_vector2

    def angle_between_vectors_360(self, a, b, degrees=True):
        """
        Calculate the angle between two vectors a and b.

        Parameters:
        -----------
        a, b : array-like
            Input vectors (1D arrays).
        degrees : bool
            If True, return angle in degrees. Otherwise, radians.

        Returns:
        --------
        angle : float
            Angle between vectors in radians or degrees.
        """
        a = np.array(a)
        b = np.array(b)

        # Normalize both vectors
        a_norm = a / np.linalg.norm(a)
        b_norm = b / np.linalg.norm(b)

        # Calculate angle using atan2 of the determinant and dot product
        dot = np.dot(a_norm, b_norm)
        det = a_norm[0] * b_norm[1] - a_norm[1] * b_norm[0]  # 2D cross product (scalar)

        angle_rad = np.arctan2(det, dot)
        angle_deg = np.degrees(angle_rad)

        # Convert from [-180, 180] to [0, 360]
        return angle_deg % 360

    def angle_between_vectors_unsigned(self, a, b, degrees=True):
        a = np.array(a)
        b = np.array(b)

        # Normalize both vectors
        a_norm = a / np.linalg.norm(a)
        b_norm = b / np.linalg.norm(b)

        # Clamp the dot product to avoid floating-point errors
        dot = np.clip(np.dot(a_norm, b_norm), -1.0, 1.0)

        angle_rad = np.arccos(dot)

        return np.degrees(angle_rad) if degrees else angle_rad

    def Coordinates_transformation(self, trial_info:Trial, new_axis):
        for p in trial_info.trial_data.keys():
            points = np.array([trial_info.trial_data[p].x_coord, trial_info.trial_data[p].y_coord, trial_info.trial_data[p].z_coord]).T
            transformed_points = points @ new_axis
            transformed_points = transformed_points.T
            trial_info.trial_data[p].x_coord = transformed_points[0]
            trial_info.trial_data[p].y_coord = transformed_points[1]
            trial_info.trial_data[p].z_coord = transformed_points[2]

    def normalize_psd_data_global_minmax(self, psd_data):
        """
        Normalize power values using global min and max across all trials.

        Parameters:
        - psd_data: list of (freqs, power) tuples

        Returns:
        - normalized_psd_data: list of (freqs, normalized_power) tuples
        """
        # Flatten all power arrays to compute global min and max
        all_power_values = np.concatenate([np.asarray(power) for _, power in psd_data])
        global_min = np.nanmin(all_power_values)
        global_max = np.nanmax(all_power_values)
        global_range = global_max - global_min

        # Apply normalization
        normalized_psd_data = []
        for freqs, power in psd_data:
            power = np.asarray(power)
            if global_range != 0:
                norm_power = (power - global_min) / global_range
            else:
                norm_power = power - global_min  # All values were identical
            normalized_psd_data.append((freqs, norm_power))

        return normalized_psd_data

    def transform_coords_and_calculate_platform_data(self, trial_info:Trial, platform_offset, radius, platform_height, frame=0):

        if frame == 0:
            start = int(trial_info.moc)
        else:
            start = frame

        center_points = self.ReadAndTranspose("platform-tip", trial_info)
        platform_ctr_pts_traces = np.array(center_points[300:350])

        line_points_before, plane_points_before, verts_before, cylinder_top, cylinder_bottom, direction_before, perp_vector1_before, perp_vector2_before = (
            self.calculate_platform_surfaces(platform_traces=platform_ctr_pts_traces,
                                             platform_center=center_points[start],
                                             platform_offset=platform_offset,
                                             radius=radius,
                                             height=platform_height))

        # coordinates transformation
        v1 = perp_vector1_before  # new Y-axis
        v2_proj = direction_before - np.dot(direction_before, v1) * v1  # remove v1 component from v2
        v2 = v2_proj / np.linalg.norm(v2_proj)  # new Z-axis (orthogonalized)
        v0 = np.cross(v1, v2)  # new X-axis, orthogonal to both
        v0 = v0 / np.linalg.norm(v0)
        # Double-check orthogonality (optional)
        assert np.isclose(np.dot(v0, v1), 0)
        assert np.isclose(np.dot(v0, v2), 0)
        assert np.isclose(np.dot(v1, v2), 0)

        # Each column is a basis vector
        R = np.column_stack([v0, v1, v2])  # shape (3, 3)

        # Transform coordinates based on platform motion and L-R-mBC vector
        self.Coordinates_transformation(trial_info, R)

        center_points = self.ReadAndTranspose("platform-tip", trial_info)
        platform_ctr_pts_traces = np.array(center_points[300:350])

        line_points_after, plane_points_after, verts_after, cylinder_top, cylinder_bottom, direction_after, perp_vector1_after, perp_vector2_after = (
            self.calculate_platform_surfaces(platform_traces=platform_ctr_pts_traces,
                                             platform_center=center_points[start],
                                             platform_offset=platform_offset,
                                             radius=radius,
                                             height=platform_height))

        # return line_points_before, plane_points_before, verts_before, cylinder_top, cylinder_bottom, direction_before, perp_vector1_before, perp_vector2_before
        return line_points_after, plane_points_after, verts_after, cylinder_top, cylinder_bottom, direction_after, perp_vector1_after, perp_vector2_after
    def angle_with_plane_and_azimuth(self, pt1, pt2, normal, reference_dir=np.array([0, 1, 0])):
        pt1 = np.asarray(pt1)
        pt2 = np.asarray(pt2)
        n = np.asarray(normal)
        ref = np.asarray(reference_dir)

        v = pt2 - pt1
        v_norm = np.linalg.norm(v)
        n_norm = np.linalg.norm(n)

        dot = np.dot(v, n)
        angle_to_normal = np.arccos(np.clip(dot / (v_norm * n_norm), -1.0, 1.0))
        sin_angle = np.clip(np.abs(np.dot(v, n)) / (v_norm * n_norm), 0.0, 1.0)
        angle_to_plane = np.degrees(np.arcsin(sin_angle))

        v_proj = v - np.dot(v, n) / n_norm ** 2 * n

        v_proj_norm = np.linalg.norm(v_proj)
        if v_proj_norm == 0:
            azimuth = None
        else:
            ref = ref - np.dot(ref, n) / n_norm ** 2 * n
            ref = ref / np.linalg.norm(ref)

            v_proj_unit = v_proj / v_proj_norm
            dot_proj = np.dot(ref, v_proj_unit)
            cross = np.cross(ref, v_proj_unit)
            sign = np.sign(np.dot(cross, n))
            azimuth = np.degrees(np.arccos(np.clip(dot_proj, -1.0, 1.0)))
            if sign < 0:
                azimuth = 360 - azimuth

        return angle_to_plane, azimuth, v, v_proj, n, ref
    def calculate_BC_platform_angle(self, BC, FT, platform_direction):
        BC_angles = []
        for i in range(len(BC)):
            ag = self.angle_between_vectors_unsigned(FT[i] - BC[i], platform_direction - BC[i])
            BC_angles.append(ag)
        return np.asarray(BC_angles)
    def calculate_rhythmicity(self, signal, fps):


        analytic_signal = hilbert(signal)
        phase = np.angle(analytic_signal)

        # 3. Compute pACF (Phase autocorrelation)
        max_lag_cycles = int(len(signal) / (fps / 10)) # up to 10 cycles
        lags = np.arange(0, max_lag_cycles, 0.1)  # lags in cycles
        pACF = []
        samples_per_cycle = int(fps / 10)
        # print(max_lag_cycles)
        for lag in lags:
            shift = int(lag * samples_per_cycle)  # convert lag in cycles → samples
            if shift == 0:
                pACF.append(1.0)  # autocorrelation at lag 0 = 1
                continue
            if shift != len(signal):
                phase_shifted = np.roll(phase, -shift)

                phase_diff = phase[:-shift] - phase[shift:]
                # phase_diff = phase - phase_shifted
                # plt.plot(phase)
                # plt.plot(phase_shifted)
                # plt.show()
                # compute PLV = |average of complex exponentials|
                plv = np.abs(np.mean(np.exp(1j * phase_diff)))
                # print(plv)
                pACF.append(plv)

        pACF = np.array(pACF)
        # pACF = self.normalize_list(pACF)
        # 4. Normalize pACF to explained variance function
        pACF_norm = pACF / np.sum(pACF)

        # 5. Cumulative function
        CF = np.cumsum(pACF_norm)
        # 6. Lifetime score = first lag where CF > 0.9
        threshold = 0.8
        lifetime_idx = np.where(CF >= threshold)[0][0]
        lifetime_cycles = lags[lifetime_idx]

        MakePlot = True
        print(lifetime_cycles / max_lag_cycles)
        if MakePlot:
            # 7. Plot
            plt.figure(figsize=(12, 4))
            plt.subplot(1, 3, 1)
            plt.plot(lags, pACF, 'o-')
            plt.xlabel("Lag (cycles)")
            plt.ylabel("pACF")
            plt.title("Phase Autocorrelation")
            plt.ylim(-0.1, 1.1)
            plt.yticks([0, 1])

            plt.subplot(1, 3, 2)
            plt.plot(lags, pACF_norm, 'o-')
            plt.xlabel("Lag (cycles)")
            plt.title("Normalized pACF")

            plt.subplot(1, 3, 3)
            plt.plot(lags, CF, 'o-')
            plt.axhline(threshold, color='r', linestyle='--')
            plt.axvline(lifetime_cycles, color='g', linestyle='--')
            plt.xlabel("Lag (cycles)")
            plt.ylabel("Cumulative pACF")
            # plt.title(f"Lifetime = {lifetime_cycles / max_lag_cycles:.2f} cycles")
            plt.show()

        # return lifetime_cycles / max_lag_cycles

    def calculate_velocity(self, trial_info:Trial, points):
        velocity_data = dict()
        for p in points:
            dt = 1 / trial_info.fps  # fps = frames per second
            # Stack coordinates
            coords = np.stack([trial_info.trial_data[p].x_coord, trial_info.trial_data[p].y_coord, trial_info.trial_data[p].z_coord], axis=1)
            # Compute velocity using finite differences
            velocities = np.diff(coords, axis=0) / dt  # shape (n_timepoints-1, 3)
            # Compute speed (magnitude)
            speed = np.linalg.norm(velocities, axis=1)  # shape (n_timepoints-1,)
            velocity_data[p] = speed
        return velocity_data
"""
These functions are responsible for detecting various characteristic of the angle and 3D data
"""
class DetectCharacteristics:
    def __init__(self, radius=0, FPS=0):
        self.radius = radius
        self.calculator = SimpleCalculation()
        self.fps = FPS
    def detect_brief_landing(self, angle_data, bl_range, wing_ang_fold_th, wing_ang_drop_percent, window_size, st_base_th, consecutive_fold_th):

        # Calculate the start and end baseline of wing angle
        start_baseline = np.mean(angle_data[:bl_range])
        end_baseline = np.mean(angle_data[-bl_range:])

        chunk_size = 10
        consecutive_chunk = 0

        if start_baseline > st_base_th:

            for i in range(0, len(angle_data), window_size):
                curr_v = np.mean(angle_data[i:i + window_size])
                if curr_v / start_baseline < (1 - wing_ang_drop_percent) and curr_v < wing_ang_fold_th:
                    consecutive_chunk += 1
                else:
                    consecutive_chunk = 0
                if consecutive_chunk >= consecutive_fold_th:
                    stop_idx = i - (consecutive_fold_th - 1) * window_size
                    return True, stop_idx
        return False, 0
    def detect_Not_Flying(self, angle_data, bl_range):
        start_base_line = np.mean(angle_data[:bl_range])
        end_base_line = np.mean(angle_data[-bl_range:])
        if start_base_line < 2:
            return True
        else:
            return False
    def detect_moment_of_landing(self, trace_data, wing_distance_threshold, wind_size, duration_threshold):
        wing_fold_duration = 0
        cons_th = 4

        for i in range(0, len(trace_data), wind_size):
            if np.average(trace_data[i:i+wind_size]) < wing_distance_threshold:
                wing_fold_duration += 1
            else:
                wing_fold_duration = 0
            if wing_fold_duration > duration_threshold:
                return i - ((cons_th - 1) * wind_size), True
        return 0, False
    def detectFlying(self, angle_data, bl_range, wing_ang_fold_th, window_size):
        chunk_size = 20
        start_base_line = np.mean(angle_data[:bl_range])
        end_base_line = np.mean(angle_data[-bl_range:])
        if start_base_line > wing_ang_fold_th and end_base_line > wing_ang_fold_th:
            for i in range(0, len(angle_data), window_size):
                current_v = np.mean(angle_data[i:i + window_size])
                if current_v < wing_ang_fold_th:
                    return False
        return True
    def detect_moment_of_landing_WingAngle(self, angle_data, wing_angle_threshold, wind_size, duration_threshold):
        wing_fold_duration = 0
        cons_th = 3

        for i in range(0, len(angle_data), wind_size):
            if np.average(angle_data[i:i+wind_size]) < wing_angle_threshold:
                wing_fold_duration += 1
            else:
                wing_fold_duration = 0
            if wing_fold_duration > duration_threshold:
                return i - ((cons_th - 1) * wind_size), True
        return 0, False
    def check_leg_platform_intersection(self, leg_p1, leg_p2, direction, center_point, platform_offset):
        # Compute platform radius
        # Compute the plane equation

        platform_plane_origin = center_point + platform_offset * direction  # Shift the plane up
        d = -np.dot(direction, platform_plane_origin)

        # Find intersection point
        intersection, intersect_proportion = self.calculator.line_plane_intersection(np.array(leg_p1), np.array(leg_p2), direction, d)
        # print(f"Top intersection: {intersection} proportion:{intersect_proportion}")
        if intersection is not None and self.calculator.is_inside_circle(intersection, np.array(platform_plane_origin), self.radius):
            return True, intersect_proportion
        return False, None
    def detect_leg_stuck(self, CT_FT_ag, CT_TT_ag, CT_LT_ag, moc,  mol, alpha):
        wind_size = 3

        smoothed_CT_FT = self.calculator.exponential_moving_average(CT_FT_ag[moc:mol], alpha)
        smoothed_CT_TT = self.calculator.exponential_moving_average(CT_TT_ag[moc:mol], alpha)
        smoothed_CT_LT = self.calculator.exponential_moving_average(CT_LT_ag[moc:mol], alpha)

        from scipy.stats import linregress

        for i in range(wind_size, len(smoothed_CT_FT), wind_size):
            w1 = smoothed_CT_FT[i:i + wind_size]
            w2 = smoothed_CT_TT[i:i + wind_size]
            w3 = smoothed_CT_LT[i:i + wind_size]

            TT_angle_threshold = 0
            LT_angle_threshold = 0

            # Condition 1: mean of list1 window is 0
            cond1 = np.mean(w1) > 0.0

            df = None

            if i < 50:
                x = np.arange(i)  # x values for regression
                slope2, _, _, _, _ = linregress(x, smoothed_CT_TT[:i])
                slope3, _, _, _, _ = linregress(x, smoothed_CT_LT[:i])
                df = pd.DataFrame({
                    'm2': smoothed_CT_TT[:i],
                    'm3': smoothed_CT_LT[:i]
                })

                # Compute correlation matrix
                corr = df.corr(method="pearson")

            else:
                x = np.arange(50)  # x values for regression
                slope2, _, _, _, _ = linregress(x, smoothed_CT_TT[i - 50:i])
                slope3, _, _, _, _ = linregress(x, smoothed_CT_LT[i - 50:i])

                df = pd.DataFrame({
                    'm2': smoothed_CT_TT[i - 50:i],
                    'm3': smoothed_CT_LT[i - 50:i]
                })

                # Compute correlation matrix
                corr = df.corr(method="pearson")


            cond2 = slope2 > 0
            cond3 = slope3 > 0

            cond4 = np.mean(w2) > TT_angle_threshold and np.mean(w3) > LT_angle_threshold
            # cond5 = corr["m2"]["m3"] > 0.8
            if cond1 and cond2 and cond4 and cond3:
                return i - 1  # return end index of the matching window
        return 0
    def detect_movement_start(self, data):
        for i in range(len(data)):
            if data[i] > 0.03:
                return i
        return np.inf
    def detect_stable_posture(self, Angle_data):
        sum_move = 0
        for k in Angle_data.keys():
            postureData = self.calculator.Calculate_derivative(self.calculator.exponential_moving_average(Angle_data[k][:self.fps], 0.1))
            peaks, _ = find_peaks(postureData, height=3)
            sum_move += len(peaks)
        print(sum_move)
        if sum_move > 10:
            return False
        else:
            return True
    def find_first_trough_CT_ang(self, Angle_data):
        from scipy.stats import linregress
        wind = 5
        for f in range(len(Angle_data) - wind):
            x = np.arange(wind)
            slope, _, _, _, _ = linregress(x, Angle_data[f:f + wind])
            if slope >= 5:
                return f
        return 0
    def find_last_trough_CT_ang(self, Angle_data):
        counts = 0
        derivative = np.gradient(Angle_data)
        for d in range(len(derivative)):
            if derivative[d] < -4:
                counts += 1
            if counts >= 5 and d == len(derivative) - 1:
                return d
            if abs(derivative[d]) < 2 and counts >= 5:
                return d
        return 0
    def detect_cycle_present(self, Angle_data):
        derivative = np.gradient(Angle_data)
        rise = False
        drops = 0
        sequence = []
        for d in range(len(derivative)):
            if derivative[d] > 6 and not rise:
                rise = True
                sequence.append(d)
            if derivative[d] < -4:
                drops += 1
            if drops > 5 and d == len(derivative) - 1:
                sequence.append(d)
                break
            if abs(derivative[d]) < 2 and drops > 0:
                sequence.append(d)
                break

        return sequence
    def ReadCoordsAll(self, kinematic_data:Trial, fnum):
        points = ["L-wing", "L-wing-hinge", "R-wing", "R-wing-hinge", "abdomen-tip", "platform-tip", "L-platform-tip",
                  "R-platform-tip", "platform-axis",
                  "R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT",
                  "R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT",
                  "R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT",
                  "L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT",
                  "L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT",
                  "L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT"]
        coords = dict()
        for p in points:
            coords[p] = np.asarray([kinematic_data.trial_data[p].x_coord[fnum],
                                    kinematic_data.trial_data[p].y_coord[fnum],
                                    kinematic_data.trial_data[p].z_coord[fnum]])
        return coords
    def leg_search_cycle_start_classifier(self, peaks, troughs, angle_data):
        peaks_num = len(peaks)
        troughs_num = len(troughs)
        if troughs_num == 0 and peaks_num == 1:
            # print("need one more troughs")
            last_troughs = self.find_last_trough_CT_ang(angle_data)
            if last_troughs > 0:
                troughs = np.insert(troughs, 0, self.find_first_trough_CT_ang(angle_data))
                troughs = np.insert(troughs, 1, last_troughs)
        if troughs_num > 0 and abs(troughs_num - peaks_num) < 2:
            # print("Troughs detected")
            # print(troughs)
            if troughs[0] > 10:
                initial_troughs = self.find_first_trough_CT_ang(angle_data[:troughs[0]])
                if initial_troughs > 0:
                    troughs = np.insert(troughs, 0, initial_troughs)

            if self.all_elements_in_between(troughs, peaks):
                # print("need one more troughs")
                last_troughs = self.find_last_trough_CT_ang(angle_data)
                if last_troughs > 0:
                    troughs = np.insert(troughs, 1, last_troughs)
                    # if not self.all_elements_in_between(peaks[-1], troughs):
                    #     troughs = []
            """if troughs[-1] < len(angle_data) - 20:
                troughs = np.insert(troughs, len(troughs), len(angle_data) - 1)"""

            return peaks, troughs
        """if troughs_num == 0:
            print("No troughs detected")
            initial_troughs = self.find_first_trough_CT_ang(angle_data)
            # troughs = np.insert(troughs, 0, initial_troughs)
            ind = self.detect_cycle_present(angle_data)
            if len(ind) == 2:
                troughs = np.insert(troughs, 0, ind[0])
                troughs = np.insert(troughs, 1, ind[1])"""
            # last_troughs = self.find_last_trough_CT_ang()
        """if peaks_num > 0 and troughs_num > 0 and peaks_num - troughs_num < 2:
            if peaks_num > troughs_num and peaks[0] < troughs[0]:
                troughs = np.insert(troughs, 0, self.find_first_trough_CT_ang(self.calculator.Calculate_derivative(angle_data)))
            if peaks_num == troughs_num and peaks[0] < troughs[0]:
                troughs = np.insert(troughs, 0, self.find_first_trough_CT_ang(self.calculator.Calculate_derivative(angle_data)))
                peaks = np.insert(peaks, len(peaks), len(angle_data) - 1)
            if peaks_num < troughs_num and peaks[0] > troughs[0]:
                peaks = np.insert(peaks, len(peaks), len(angle_data) - 1)
        elif peaks_num == 1 and troughs_num ==0:
            troughs = np.insert(troughs, 0, self.find_first_trough_CT_ang(self.calculator.Calculate_derivative(angle_data)))
            troughs = np.insert(troughs, len(troughs), len(angle_data) - 1)
        else:
            return np.array([0]), np.array([0])"""
        return peaks, troughs
    def detect_peaks_troughs(self, signal, leg):

        peak_prom = 25
        if leg[2] != "h":
            troughs, props = find_peaks(-signal, prominence=10, height=(-150, -10))
            # troughs = np.array([int(t) for t in troughs if -signal[t] >= 5])

            peaks, properties = find_peaks(signal, prominence=peak_prom)
            # peaks = np.array([int(p) for p in peaks if signal[p] >= 5])
            peaks, troughs = self.leg_search_cycle_start_classifier(peaks, troughs, signal)

            # Get the surrounding minima (left and right base of the peak)
            left_bases = properties['left_bases']
            right_bases = properties['right_bases']

            # Set threshold for minimav
            minima_threshold = 10

            # Keep only peaks whose surrounding minima are BOTH below the threshold
            selected_peaks = []
            for peak, left, right in zip(peaks, left_bases, right_bases):
                if signal[left] < minima_threshold and signal[right] < minima_threshold:
                    selected_peaks.append(peak)

            selected_peaks = np.array(selected_peaks)

        else:
            troughs, props = find_peaks(-signal, prominence=10, height=(-150, -10))

            peaks, _ = find_peaks(signal, prominence=peak_prom)

            peaks, troughs = self.leg_search_cycle_start_classifier(peaks, troughs, signal)

        return peaks, troughs
    def Detect_hard_touch(self, trial_info:Trial):
        pose_data = trial_info
        moc = trial_info.moc
        mol = trial_info.mol


        if moc < 0:
            moc = 440
            mol = moc + trial_info.fps

        center_points = self.calculator.ReadAndTranspose("platform-tip", pose_data)
        centroid, platform_direction = self.calculator.best_fit_line_3d(center_points[300:350])

        j1 = "R-mBC"
        j2 = "R-mFT"
        j3 = "R-mTT"
        j4 = "R-mLT"

        def utilities(joints, pose: Trial, platform_direction):
            angle_between_p = []
            for f in range(pose.total_frames_number):
                temp = np.asarray([pose_data.trial_data[f"{joints[1]}"].x_coord[f] -
                                   pose_data.trial_data[f"{joints[0]}"].x_coord[f],
                                   pose_data.trial_data[f"{joints[1]}"].y_coord[f] -
                                   pose_data.trial_data[f"{joints[0]}"].y_coord[f],
                                   pose_data.trial_data[f"{joints[1]}"].z_coord[f] -
                                   pose_data.trial_data[f"{joints[0]}"].z_coord[f]])
                angle_between_p.append(self.calculator.angle_between_vectors(temp, platform_direction))
            return angle_between_p
        CT_FT_angle_between_p = utilities([j1, j2], pose_data, platform_direction)
        CT_TT_angle_between_p = utilities([j1, j3], pose_data, platform_direction)
        CT_LT_angle_between_p = utilities([j1, j4], pose_data, platform_direction)


        smoothed_CT_FT = self.calculator.exponential_moving_average(CT_FT_angle_between_p, 0.01)
        smoothed_CT_TT = self.calculator.exponential_moving_average(CT_TT_angle_between_p, 0.01)
        smoothed_CT_LT = self.calculator.exponential_moving_average(CT_LT_angle_between_p, 0.01)

        normalized_CT_FT = self.calculator.normalize_list(smoothed_CT_FT)
        normalized_CT_TT = self.calculator.normalize_list(smoothed_CT_TT)
        normalized_CT_LT = self.calculator.normalize_list(smoothed_CT_LT)

        FT_baseline = np.mean(normalized_CT_FT[moc:moc + 10])
        TT_baseline = np.mean(normalized_CT_TT[moc:moc + 10])
        """top_graph_tick_value = [-0, 1]
        off_set = 0.1
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
        plt.plot(normalized_CT_FT, color="blue", linewidth=3)
        plt.plot(normalized_CT_TT, color="orange", linewidth=3)
        ax.tick_params(axis="y", labelsize=15)
        ax.tick_params(axis="x", labelsize=15)
        ax.tick_params(width=3, length=5)
        ax.spines["left"].set_linewidth(2)  # Top border
        ax.spines["bottom"].set_linewidth(2)
        ax.set_xticks([0, 875, 1750], labels=["0", "3.5", "7"])
        ax.set_xlim(-100, 1850)
        ax.set_yticks([top_graph_tick_value[0], (top_graph_tick_value[0] + top_graph_tick_value[1]) / 2, top_graph_tick_value[1]])
        ax.set_ylim(top_graph_tick_value[0] - off_set, top_graph_tick_value[1] + off_set)
        sns.despine(trim=True)
        plt.ylabel("Normalized angle relative to horizontal plane",fontsize=15)
        plt.xlabel("Video duration",fontsize=15)
        plt.show()"""

        FT_drop = False
        TT_drop = False
        TT_rise = False
        for i in range(moc, len(normalized_CT_FT)):
            if ((normalized_CT_FT[i] - FT_baseline) / FT_baseline) < -0.3:
                FT_drop = True
                break
        for i in range(moc, len(normalized_CT_TT)):
            if ((normalized_CT_TT[i] - TT_baseline) / TT_baseline) < -0.3 and normalized_CT_TT[i] > 0.2:
                TT_drop = True
                TT_rise = False
                break
            if ((normalized_CT_TT[i] - TT_baseline) / TT_baseline) > 0.3 and normalized_CT_TT[i] > 0.2:
                TT_rise = True
                TT_drop = False
                break

        if FT_drop and TT_rise:
            print("Hard touch")
            return True
        elif FT_drop and TT_drop:
            print("Normal touch")
            return False
        else:
            print("Unable to tell")



        alpha = 0.5
        # return CT_FT_angle_between_p, CT_TT_angle_between_p, CT_LT_angle_between_p
        leg_stuck = self.detect_leg_stuck(CT_FT_angle_between_p, CT_TT_angle_between_p, CT_LT_angle_between_p, moc, mol, alpha)
        return leg_stuck
    def MOC_touch_type_classifier(self, joint, type, signal_to_use, trend_duration=0, analysis_duration=0):
        from scipy.stats import linregress

        if joint == "TiTa":

            if type == "slopes":
                wind = 10
                slopes = []
                for f in range(analysis_duration - wind):
                    x = np.arange(wind)
                    slope, _, _, _, _ = linregress(x, signal_to_use[f:f + wind])

                    slopes.append(slope)
                extreme_counts = len([e for e in slopes if e > 2])
                return extreme_counts > 3, extreme_counts
            if type == "trend":
                x = np.arange(trend_duration)
                general_trend, _, _, _, _ = linregress(x, signal_to_use[:trend_duration])
                return general_trend >= 0.03, general_trend
            if type == "posture":

                pass


        if joint == "CxTr":
            pass
        return None
    def all_elements_in_between(self, list1, list2):
        """
        Check if each element in list1 is between two consecutive elements in sorted list2.

        Parameters:
        ----------
        list1 : list of floats or ints
        list2 : list of floats or ints (must have len >= 2)

        Returns:
        -------
        True if all elements in list1 fall strictly between consecutive elements of list2.
        """
        list2 = sorted(list2)
        for x in list1:
            found = False
            for a, b in zip(list2, list2[1:]):
                if a < x < b:
                    found = True
                    break
            if not found:
                return False
        return True
    def detect_leg_contact(self, data):
        deri = np.gradient(data)
        for i in range(len(data)):
            if data[i] < 0.55 and deri[i] < 0.05:
                return i
        return np.nan
"""
These functions are responsible for manipulating files
"""
class FileManipulation:
    # Extract the data path of the csv files and organize them in the order by fly number
    def Write_to_csv(self, LandingProbData, LandingLatencyData, output_path, compare_path):
        Manual_data = pd.read_excel(compare_path)
        T = ["Trial_" + str(i) for i in range(1, 21)]
        Manual_data = Manual_data[T]
        # Create an Excel writer using openpyxl
        excel_writer = pd.ExcelWriter(output_path, engine='openpyxl')
        LandingProbData.to_excel(excel_writer, index=False, sheet_name='Sheet1')
        # Access the workbook and sheet
        workbook = excel_writer.book
        sheet = workbook['Sheet1']

        # Define cell colors
        yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
        orange_fill = PatternFill(start_color='FFC000', end_color='FFC000', fill_type='solid')
        red_fill = PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')
        blue_fill = PatternFill(start_color='9BC2E6', end_color='9BC2E6', fill_type='solid')
        gray_fill = PatternFill(start_color='696969', end_color='696969', fill_type='solid')

        # Apply cell colors based on conditions
        for row_idx in range(2, sheet.max_row + 1):  # Start from row 2 (excluding header)
            for col_idx in range(2, sheet.max_column + 1):  # Start from column 2 (excluding Fly# column)
                cell_value = sheet.cell(row=row_idx, column=col_idx).value
                cell = sheet.cell(row=row_idx, column=col_idx)
                if cell_value == 1:
                    if isinstance(Manual_data[T].iloc[row_idx - 2][col_idx - 2], str):
                        cell.fill = gray_fill
                    else:
                        if Manual_data[T].iloc[row_idx - 2][col_idx - 2] > 1:
                            cell.fill = yellow_fill
                        else:
                            cell.fill = gray_fill
                    cell.value = LandingLatencyData[row_idx - 2][col_idx - 2]
                elif cell_value == -1:
                    if Manual_data[T].iloc[row_idx - 2][col_idx - 2] == -1:
                        cell.fill = orange_fill
                    else:
                        cell.fill = gray_fill
                elif cell_value == 0:
                    if isinstance(Manual_data[T].iloc[row_idx - 2][col_idx - 2], str):
                        if Manual_data[T].iloc[row_idx - 2][col_idx - 2] == "NotFlying":
                            cell.fill = blue_fill
                        else:
                            cell.fill = gray_fill
                    else:
                        cell.fill = gray_fill
                    cell.value = "NotFlying"
                elif isinstance(type(cell_value), type(str)):
                    # print("N/A")
                    # print(cell_value)
                    if pd.isna(Manual_data[T].iloc[row_idx - 2][col_idx - 2]):
                        cell.fill = red_fill
                    else:
                        cell.fill = gray_fill
                    cell.value = 'N/A'
        # Save the Excel file
        excel_writer.save()
        print("Excel file has been created with modifications.")
    def OutptuHardtouchPrediction(self, Predicted_Data, outputpath):
        df_transformed = pd.DataFrame(Predicted_Data, columns=[f"Trial_{i + 1}" for i in range(20)])
        df_transformed.insert(0, "Fly#", range(1, len(df_transformed) + 1))

        # Save to an Excel file
        output_file = f"{outputpath}.xlsx"
        df_transformed.to_excel(output_file, index=False)

        # Load the workbook for formatting
        wb = load_workbook(output_file)
        ws = wb.active

        # Define color fills
        color_fills = {
            "-1": PatternFill(start_color="FF9933", end_color="FF9933", fill_type="solid"),
            "number": PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
            # Yellow for other numbers
        }

        # Apply color coding (skip header row)
        for row in ws.iter_rows(min_row=2, min_col=2):  # Start from column 2 to skip "Fly#"
            for cell in row:
                if isinstance(cell.value, (int, float)) and cell.value == -1:
                    cell.fill = color_fills["-1"]
                elif isinstance(cell.value, (int, float)):  # Any other number
                    cell.fill = color_fills["number"]

        # Save the formatted workbook
        wb.save(output_file)

        print(f"File saved as {output_file}")
    def OutptuPrediction(self, Predicted_Data, outputpath):
        df_transformed = pd.DataFrame(Predicted_Data, columns=[f"Trial_{i + 1}" for i in range(20)])
        df_transformed.insert(0, "Fly#", range(1, len(df_transformed) + 1))

        # Replace NaN values with "N/A" for display
        df_transformed.fillna("N/A", inplace=True)

        # Save to an Excel file
        output_file = f"{outputpath}.xlsx"
        df_transformed.to_excel(output_file, index=False)

        # Load the workbook for formatting
        wb = load_workbook(output_file)
        ws = wb.active

        # Define color fills
        color_fills = {
            "N/A": PatternFill(start_color="FF6666", end_color="FF6666", fill_type="solid"),  # Red for N/A
            "NF": PatternFill(start_color="9BC2E6", end_color="9BC2E6", fill_type="solid"),  # Blue for NF
            "-1": PatternFill(start_color="FFC000", end_color="FFC000", fill_type="solid"),  # Orange for -1
            "OT": PatternFill(start_color="92D050", end_color="92D050", fill_type="solid"),
            "number": PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
            # Yellow for other numbers
        }

        # Apply color coding (skip header row)
        for row in ws.iter_rows(min_row=2, min_col=2):  # Start from column 2 to skip "Fly#"
            for cell in row:
                if isinstance(cell.value, str) and cell.value == "N/A":
                    cell.fill = color_fills["N/A"]
                elif isinstance(cell.value, str) and cell.value == "NF":
                    cell.fill = color_fills["NF"]
                elif isinstance(cell.value, (int, float)) and cell.value == -1:
                    cell.fill = color_fills["-1"]
                elif isinstance(cell.value, str) and cell.value == "OT":
                    cell.fill = color_fills["OT"]
                elif isinstance(cell.value, (int, float)):  # Any other number
                    cell.fill = color_fills["number"]

        # Save the formatted workbook
        wb.save(output_file)

        print(f"File saved as {output_file}")
    def addColumns_to_file(self, data, filename, group):
        if os.path.exists(f"{filename}.csv"):
            df = pd.read_csv(f"{filename}.csv")

            if len(data) < len(df):
                data += [np.nan] * (len(df) - len(data))
            elif len(data) > len(df):
                extra_rows = len(data) - len(df)
                df = df.reindex(range(len(df) + extra_rows))

            df[group] = data
        else:
            df = pd.DataFrame({group: data})
        df.to_csv(f"{filename}.csv", index=False)
"""
These functions are responsible for analyzing the fly group data
"""
class GroupDataAnalyzer:
    def __init__(self, platform_offset, radius, FPS):
        self.fps = FPS
        self.detector = DetectCharacteristics(radius, FPS)
        self.calculator = SimpleCalculation()
        self.manipulator = FileManipulation()
        self.offset = platform_offset
    def DetermineTiTaMOC(self, trial_info:Trial):
        start = int(trial_info.fps)
        end = int(trial_info.fps * 4)

        center_points = self.calculator.ReadAndTranspose("platform-tip", trial_info)
        R_mTT_points = self.calculator.ReadAndTranspose("R-mTT", trial_info)
        R_mLT_points = self.calculator.ReadAndTranspose("R-mLT", trial_info)
        L_mTT_points = self.calculator.ReadAndTranspose("L-mTT", trial_info)
        L_mLT_points = self.calculator.ReadAndTranspose("L-mLT", trial_info)
        contact_count_L = 0
        contact_count_R = 0
        Contact_threshold = 1

        centroid, direction = self.calculator.best_fit_line_3d(center_points[300:350])
        for frame in range(start, end):
            # print(frame)
            Intersect_R, position_R = self.detector.check_leg_platform_intersection(R_mTT_points[frame],
                                                                                    R_mLT_points[frame],
                                                                                    direction,
                                                                                    center_points[frame],
                                                                                    self.offset)

            Intersect_L, position_L = self.detector.check_leg_platform_intersection(L_mTT_points[frame],
                                                                                    L_mLT_points[frame],
                                                                                    direction,
                                                                                    center_points[frame],
                                                                                    self.offset)

            if Intersect_L:
                contact_count_L += 1
            else:
                contact_count_L = 0
            if contact_count_L >= Contact_threshold:
                return frame, "L", position_L

            if Intersect_R:
                contact_count_R += 1
            else:
                contact_count_R = 0
            if contact_count_R >= Contact_threshold:
                return frame, "R", position_R
        return 0, "NoContact", None
    def CategorizeTrial(self, trial_info:Trial):
        angles = [["R-wing", "R-wing-hinge", "abdomen-tip"], ["L-wing", "L-wing-hinge", "abdomen-tip"]]
        WingTipDistance = self.calculator.Calculate_segment_length(trial_info, [["L-wing", "R-wing"]])
        NF = self.detector.detect_Not_Flying(WingTipDistance["L-wing_R-wing"], trial_info.fps)
        if NF:
            # Categorized as Not Flying
            return 0, None
        else:
            # Determine if the wing folds
            WingAbTipAngle = self.calculator.Calculate_joint_angle(trial_info, angles)
            R_mol, RL = self.detector.detect_moment_of_landing_WingAngle(WingAbTipAngle["R-wing-hinge"], 50, 4, 2)
            L_mol, LL = self.detector.detect_moment_of_landing_WingAngle(WingAbTipAngle["L-wing-hinge"], 50, 4, 2)
            # mol, L = detect_moment_of_landing(WingTipDistance["L-wing_R-wing"], 2, 4, 3)
            if RL or LL:
                # Categorized as successful landing, may still require further examination for N/A data
                return 1, min([R_mol, L_mol])
            else:
                # Categorized as continuous flying, required further examination for N/A data
                return -1, None
    def movement_start_latency(self, group_info:Group):
        Angles = [["L-fBC", "L-fCT", "L-fFT"], ["L-fCT", "L-fFT", "L-fTT"]]
        movement_start_list = []
        ms_to_landing_list = []
        for index in group_info.landing_trial_index:
            print(f"Fly {index[0]}", f"Trial {index[1]}")
            moc = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"].moc
            mol = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"].mol
            ags = self.calculator.Calculate_joint_angle(group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"], Angles)
            if self.detector.detect_stable_posture(ags):
                ms = []
                for k in ags.keys():
                    ms.append(self.detector.detect_movement_start(self.calculator.Calculate_derivative(list(ags[k][moc:mol]))))
                if min(ms) < group_info.fps and min(ms) > 0:
                    movement_start_list.append(min(ms) / group_info.fps)
                    ms_to_landing_list.append((group_info.mol_data.iloc[index[0]][index[1]] - min(ms)) / group_info.fps)

        self.manipulator.addColumns_to_file(movement_start_list, "MovementStart", group_info.group_name)
        self.manipulator.addColumns_to_file(ms_to_landing_list, "MStoLanding", group_info.group_name)
    def Analyze_3D_pose_data(self, group_info:Group):
        LandingLatency_Data = []
        for i in range(group_info.total_fly_number):
            Fly_LandingLatency_Data = []
            for t in range(20):
                if f"F{i + 1}T{t + 1}" not in group_info.fly_kinematic_data_path:
                    break
                pose_data = Trial(fly_number=i + 1,
                                  trial_number=t + 1,
                                  fps=group_info.fps,
                                  total_frames_number=group_info.fps * group_info.video_duration,
                                  group_name=group_info.group_name,
                                  trial_data_path=group_info.fly_kinematic_data_path[f"F{i + 1}T{t + 1}"],
                                  joints=group_info.joints)

                trial_type, MOL = self.CategorizeTrial(pose_data)
                if trial_type == 0:
                    Fly_LandingLatency_Data.append("NF")
                elif trial_type == 1:
                    MOC, contact_point, tarsus_position = self.DetermineTiTaMOC(pose_data)
                    if contact_point == "NoContact" or contact_point == "L":
                        Fly_LandingLatency_Data.append(np.nan)
                    else:
                        Fly_LandingLatency_Data.append(MOL)
                        # Fly_LandingLatency_Data.append(MOL)
                elif trial_type == -1:
                    MOC, contact_point, tarsus_position = self.DetermineTiTaMOC(pose_data)
                    if contact_point == "NoContact" or contact_point == "L":
                        Fly_LandingLatency_Data.append(np.nan)
                    else:
                        Fly_LandingLatency_Data.append(-1)
            LandingLatency_Data.append(Fly_LandingLatency_Data)
        return LandingLatency_Data
    def Determine_all_flying_posture(self, group_info:Group, filter_high_latency=False):
        angles = [["R-mCT", "R-mFT", "R-mTT"], ["L-mCT", "L-mFT", "L-mTT"]]
        for index in group_info.get_targeted_trials(["Landing", "Flying"]):
            joints_angle = self.calculator.Calculate_joint_angle(group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"], angles)
            if filter_high_latency:
                if self.detector.detect_stable_posture(joints_angle):
                    group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"].L_stable_FT_angle = np.mean(joints_angle["R-mFT"][:group_info.fps])
                    group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"].R_stable_FT_angle = np.mean(joints_angle["L-mFT"][:group_info.fps])
                else:
                    group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"].L_stable_FT_angle = None
                    group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"].R_stable_FT_angle = None
            else:
                group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"].L_stable_FT_angle = np.mean(joints_angle["R-mFT"][:group_info.fps])
                group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"].R_stable_FT_angle = np.mean(joints_angle["L-mFT"][:group_info.fps])

        # self.manipulator.OutptuPrediction(collected_stable_posture, f"{groupname}_StablePosture_CT")
    def TiTa_relative_contact(self, group_info:Group):
        Contact_relative_position = []
        Latency = []
        for index in group_info.get_targeted_trials("Landing"):
            print(f"Determine TiTa contact point for fly {index[0]}", f"Trial {index[1]}")
            pose_data = group_info.fly_kinematic_data[f"F{index[0]}T{index[1]}"]
            moc, leg, tarsus_contact_position =  self.DetermineTiTaMOC(pose_data)
            if leg == "R":
                if (group_info.ll_data.iloc[index[0] - 1][index[1] - 1] / group_info.fps) < 1:
                    Contact_relative_position.append(tarsus_contact_position)
                    Latency.append(group_info.ll_data.iloc[index[0] - 1][index[1] - 1] / group_info.fps)
        return Contact_relative_position, Latency
