import cv2
import os

def ExtractFramesValue(Vidfile):
    cap = cv2.VideoCapture(Vidfile)
    Frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Break the loop if there are no more frames
        else:
            Frames.append(frame)
    return Frames
def FilterFrames(ExtractedF_Dir):
    os.chdir(ExtractedF_Dir)
    print(ExtractedF_Dir)
    global remaining_files
    for dir in os.listdir(ExtractedF_Dir):
        if len(remaining_files) == 0:
            for Img in os.listdir(os.path.join(ExtractedF_Dir, "1")):
                if Img.endswith(".png"):
                    remaining_files.append(Img)
        else:
            for Img in os.listdir(dir):
                if Img.endswith(".png") and Img not in remaining_files:
                    os.remove(os.path.join(dir, Img))

def ExtractFrames(Video_files_path, ExtractedF_Dir, extract_frame_range, step):
    global Total_frames_num
    global FolderName

    cam = 1
    for key in Video_files_path.keys():
        Videos = []

        print(f"Processing {key}'s data")
        FlyNum = 0


        for Vid_file in Video_files_path[key]:
            print(Vid_file)
            FlyNum += 1
            Videos.extend(ExtractFramesValue(Vid_file))

        extracted_frame_ind = range(extract_frame_range[0], extract_frame_range[1], step)

        Frames_output_directory = os.path.join(ExtractedF_Dir, FolderName + key)

        if not os.path.exists(Frames_output_directory):
            os.mkdir(Frames_output_directory)

        for f in range(FlyNum):
            for i in range(len(extracted_frame_ind)):
                output_file_path = os.path.join(Frames_output_directory, f"img{extracted_frame_ind[i]:04d}.png")
                cv2.imwrite(output_file_path, Videos[extracted_frame_ind[i] + f * Total_frames_num])
        cam += 1
Vid_Dir = os.path.join(r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\Agrawal_Lab\vids")
ExtractedFPath = os.path.join(r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\Agrawal_Lab\frames")
Total_frames_num = 1400
extract_frame_range = [300, 800]
step = 4
remaining_files = []
FolderName = ""
Vid_By_Cam = dict()


for file in os.listdir(Vid_Dir):
    cam_number = int(file.split("_Cam")[1].split(".")[0])
    # Add the file to the corresponding camera number key in the dictionary
    if str(cam_number) in Vid_By_Cam.keys():
        Vid_By_Cam[str(cam_number)].append(os.path.join(Vid_Dir, file))
    else:
        Vid_By_Cam[str(cam_number)] = [os.path.join(Vid_Dir, file)]



# ExtractFrames(Vid_By_Cam, ExtractedFPath, extract_frame_range, step)
FilterFrames(ExtractedFPath)

