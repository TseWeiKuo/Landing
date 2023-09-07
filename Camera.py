# ===============================================================================
#    This sample illustrates how to grab and process images using the CInstantCamera class.
#    The images are grabbed and processed asynchronously, i.e.,
#    while the application is processing a buffer, the acquisition of the next buffer is done
#    in parallel.
#
#    The CInstantCamera class uses a pool of buffers to retrieve image data
#    from the camera device. Once a buffer is filled and ready,
#    the buffer can be retrieved from the camera object for processing. The buffer
#    and additional image data are collected in a grab result. The grab result is
#    held by a smart pointer after retrieval. The buffer is automatically reused
#    when explicitly released or when the smart pointer object is destroyed.
# ===============================================================================
import imageio
from pypylon import pylon
from pypylon import genicam
import concurrent.futures
import numpy
import sys
import math
import msvcrt
import time
import os
from imageio import get_writer
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *


# print('Create Directory for Data?..1. Yes  2. No')
mk_dir=1 # int(input('Create Directory?'))
if mk_dir==1:
    # dir_name=str(input('Directory_name:'))
    dir_path=r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\DataFolder"
    #adjust for Pierre's anipose format
    #dir_path_vid='D:/Sarah/Data/Videos/'+dir_name+'/videos-raw'
    dir_path_vid=r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\DataFolder\videos-raw"
    # Create target Directory if don't exist
    if not os.path.exists(dir_path_vid):
        os.mkdir(dir_path)
        os.mkdir(dir_path_vid)
        save_path=dir_path_vid+'/'
        print("Directory " , dir_path_vid,  " Created ")
    else:
        save_path=dir_path_vid+'/'
        print("Directory " , dir_path_vid ,  " already exists...save videos to this path")
else:
    print("Directory not created")
    #save_path='D:/Sarah/Data/Videos/'
    save_path=r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\DataFolder\videos-raw"


def save_video(cam_img):
    filename=r"Testing_images"
    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when IMAGES_TO_GRAB images have been retrieved.
        # Create writer
    #print('C:/Users/Brandon Pratt/Desktop/Brandon/Linear Treadmill/Data/Videos/' + filename +'.mp4')
    print(save_path + filename + cam_img[0] +'.avi')
    writer=get_writer(
       save_path + filename + cam_img[0] +'.avi',  # .mp4, mkv players often support H.264, Camera1
        # test harddrive speed
       #'E:/Brandon_Test/'+ filename +'.avi',
        # use .avi (not .mp4) format because can be opened in virtualdub
        fps=180,  # FPS is in units Hz; should be real-time...playback...set to actual
        codec='libx264',  # When used properly, this is basically
                          # "PNG for video" (i.e. lossless)
        quality=None,  # disables variable compression...0 to 10
        bitrate=None, #1000000, # set bit rate
        pixelformat='yuv420p',  # widely used
        macro_block_size=None,
        ffmpeg_params=['-preset','ultrafast','-crf','20', '-tune', 'zerolatency'], # crf:0-51 or tune: fastdecode
        input_params=None
    )

    # write video
    for img in cam_img[1]:
        writer.append_data(img)

    #close writer
    writer.close()
    return cam_img[0] + ' saved'


# specify trials and speed parameters
v_base = 5 # 5 mm/s...baseline driving speed
trial = 10 #10 number of trials per condition
# Number of images to be grabbed.
countOfImagesToGrab = 1000

# The exit code of the sample application.
exitCode = 0


try:
    # Create an instant camera object with the camera device found first.
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()

    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    # demonstrate some feature access
    new_width = camera.Width.GetValue() - camera.Width.GetInc()
    if new_width >= camera.Width.GetMin():
        camera.Width.SetValue(new_width)

    # The parameter MaxNumBuffer can be used to control the count of buffers
    # allocated for grabbing. The default value of this parameter is 10.
    camera.MaxNumBuffer = 5

    # Start the grabbing of c_countOfImagesToGrab images.
    # The camera device is parameterized with a default configuration which
    # sets up free-running continuous acquisition.
    camera.StartGrabbingMax(countOfImagesToGrab)
    video_frames = []
    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when c_countOfImagesToGrab images have been retrieved.
    while camera.IsGrabbing():
        # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        # Image grabbed successfully?
        if grabResult.GrabSucceeded():
            # Access the image data.)
            img = grabResult.Array
            video_frames.append(img)
        else:
            print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
        grabResult.Release()
    print(save_video(["Camera1", video_frames]))
    camera.Close()
except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e)
    exitCode = 1

sys.exit(exitCode)