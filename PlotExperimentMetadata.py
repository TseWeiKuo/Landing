import cv2
import os

def Get3D_path(source_folder):
    AllFiles = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".mp4"):
                input_file_path = os.path.join(root, file)
                AllFiles.append(input_file_path)

    return AllFiles
for file in Get3D_path(r"C:\Users\agrawal-admin\Desktop\Supplement videos\GTACR"):
    # Input and output video paths
    input_path = file
    output_path = input_path[:-4] + "dotted.mp4"

    # Open input video
    cap = cv2.VideoCapture(input_path)

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec

    # Create VideoWriter
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Frame range
    start_frame, end_frame = 0, 1750
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Add red dot between frame 751 and 1251
        if start_frame <= frame_idx <= end_frame:
            # Coordinates: (x, y) – top right corner
            center = (40, height - 100)   # 20 px from right and top
            radius = 20
            color = (0, 255, 0)  # BGR: Red
            thickness = -1       # filled circle
            cv2.circle(frame, center, radius, color, thickness)

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
    print("Done! Saved as", output_path)