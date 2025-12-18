import os

from kinematic_object import Group, Trial, Point
import KinematicPlot as kp
import warnings

from kinematic_utilities import SimpleCalculation, DetectCharacteristics

warnings.filterwarnings(action="ignore", category=RuntimeWarning)
warnings.filterwarnings(action="ignore", category=FutureWarning)

def Group_meta_data(Video_duration=7, Trials_num=20):
    global Key_points

    global WT_T1_TTa_Fly_Num
    global WT_T2_TTa_Fly_Num
    global WT_T3_TTa_Fly_Num
    global G106_TTa_Fly_Num
    global G107_TTa_Fly_Num
    global G108_TTa_Fly_Num
    global G114_TTa_Fly_Num
    global G115_TTa_Fly_Num
    global G116_TTa_Fly_Num
    global G117_TTa_Fly_Num
    global G118_TTa_Fly_Num
    global G119_TTa_Fly_Num

    global WT_T2_CTF_Fly_Num
    global G108_CTF_Fly_Num



    """
    WT T1 TiTa
    """
    r"""FPS = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 250, 250, 250]
    GroupName = "WT-T1-TiTa"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\LPAcrossLegsJoints\T1-TiTa"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\LPAcrossLegsJoints\T1-TiTa\T1-TiTaLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\LPAcrossLegsJoints\T1-TiTa\MOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\LPAcrossLegsJoints\T1-TiTa\MOL.xlsx"
    WT_T1_TTa = Group(moc_data_path=MOCPath,
                  mol_data_path=MOLPath,
                  ll_data_path=LaLPath,
                  fly_kinematic_data_path=Kine_path,
                  group_name=GroupName,
                  angles=Angles,
                  joints=Key_points,
                  total_fly_number=WT_T1_TTa_Fly_Num,
                  fps=FPS,
                  trial_num=Trials_num,
                  video_duration=Video_duration)"""

    """
    WT T2 TiTa
    """
    FPS = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
    Trial_offset = 0
    GroupName = "WT-T2-TiTa"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-05-30\LPAcrossLegsJoints\T2-TiTa"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-T2-TiTaLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-T2-TiTaMOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-T2-TiTaMOL.xlsx"
    WT_T2_TTa = Group(moc_data_path=MOCPath,
               mol_data_path=MOLPath,
               ll_data_path=LaLPath,
               fly_kinematic_data_path=Kine_path,
               group_name=GroupName,
               angles=Angles,
               joints=Key_points,
               total_fly_number=WT_T2_TTa_Fly_Num,
               fps=FPS,
               trial_num=Trials_num,
               trials_offset=Trial_offset,
               video_duration=Video_duration)
    """
    WT T2 CxTr
    """
    r"""FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    Trial_offset = 0
    GroupName = "WT-T2-CxTr"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-05-30\LPAcrossLegsJoints\T2-CxTr"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\LPAcrossLegsJoints\T2-CxTr\T2-CxTrLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\LPAcrossLegsJoints\T2-CxTr\MOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\LPAcrossLegsJoints\T2-CxTr\MOL.xlsx"
    WT_T2_CTF = Group(moc_data_path=MOCPath,
               mol_data_path=MOLPath,
               ll_data_path=LaLPath,
               fly_kinematic_data_path=Kine_path,
               group_name=GroupName,
               angles=Angles,
               joints=Key_points,
               total_fly_number=WT_T2_TTa_Fly_Num,
               fps=FPS,
               trial_num=Trials_num,
               trials_offset=Trial_offset,
               video_duration=Video_duration)"""
    """
    WT T3 TiTa
    """
    r"""FPS = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 250, 250, 250, 250, 250]
    GroupName = "WT-T3-TiTa"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-05-30\LPAcrossLegsJoints\T3-TiTa"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\LPAcrossLegsJoints\T3-TiTa\T3-TiTaLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\LPAcrossLegsJoints\T3-TiTa\MOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\LPAcrossLegsJoints\T3-TiTa\MOL.xlsx"
    WT_T3_TTa = Group(moc_data_path=MOCPath,
                  mol_data_path=MOLPath,
                  ll_data_path=LaLPath,
                  fly_kinematic_data_path=Kine_path,
                  group_name=GroupName,
                  angles=Angles,
                  joints=Key_points,
                  total_fly_number=WT_T3_TTa_Fly_Num,
                  fps=FPS,
                  trial_num=Trials_num,
                  video_duration=Video_duration)"""


    """
    G106 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G106-HP1"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-03-14\HCS+_UASKir2.1eGFP\G106-HP1_T2-TiTa"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HP1-T2-TiTaLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HP1-T2-TiTaMOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HP1-T2-TiTaMOL.xlsx"
    G106_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=G106_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)


    """
    G107 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G107-HP2"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-05-30\HCS+_UASKir2.1eGFP\G107-HP2_T2-TiTa"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HP2-T2-TiTaLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HP2-T2-TiTaMOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HP2-T2-TiTaMOL.xlsx"
    G107_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=G107_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G108 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G108-HP3"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-05-30\HCS+_UASKir2.1eGFP\G108-HP3_T2-TiTa"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HP3-T2-TiTaLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HP3-T2-TiTaMOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HP3-T2-TiTaMOL.xlsx"
    G108_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=G108_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G114 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G114-ClFl"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-05-30\HCS+_UASKir2.1eGFP\G114-ClFl_T2-TiTa"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\ClFl-T2-TiTaLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\ClFl-T2-TiTaMOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\ClFl-T2-TiTaMOL.xlsx"
    G114_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=G114_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G115 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G115-Iav"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-05-30\HCS+_UASKir2.1eGFP\G115-Iav_T2-TiTa"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\Iav-T2-TiTaLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\Iav-T2-TiTaMOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\Iav-T2-TiTaMOL.xlsx"
    G115_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=G115_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G116 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G116-ClEx"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-04-26\HCS+_UASKir2.1eGFP\G116-ClEx_T2-TiTa"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\ClEx-T2-TiTaLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\ClEx-T2-TiTaMOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\ClEx-T2-TiTaMOL.xlsx"
    G116_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=G116_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G117 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G117-HkFl"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-05-30\HCS+_UASKir2.1eGFP\G117-HkFl_T2-TiTa"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HKFL-T2-TiTaLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HKFL-T2-TiTaMOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HKFL-T2-TiTaMOL.xlsx"
    G117_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=G117_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G118 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G118-HkEx"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-05-30\HCS+_UASKir2.1eGFP\G118-HkEx_T2-TiTa"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HKEX-T2-TiTaLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HKEX-T2-TiTaMOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HKEX-T2-TiTaMOL.xlsx"
    G118_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=G118_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G119 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G119-Club"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-05-30\HCS+_UASKir2.1eGFP\G119-Club_T2-TiTa"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\CLUB-T2-TiTaLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\CLUB-T2-TiTaMOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\CLUB-T2-TiTaMOL.xlsx"
    G119_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=G119_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    ANxGTACR
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "ANxGTACR"
    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\Optogenetics\ANxGTACR-Max"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\ANxGTACRLP.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\ANxGTACRMOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\ANxGTACRMOL.xlsx"
    ANxGTACR = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=9,
                 fps=FPS,
                 trial_num=30,
                 video_duration=Video_duration)




    ADxChr = Group(
        fly_kinematic_data_path=r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\Optogenetics\ANxChr-3mW",
        group_name="ADxChr",
        angles=Angles,
        joints=Key_points,
        total_fly_number=10,
        fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    ADxChr_NATR = Group(
        fly_kinematic_data_path=r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\Optogenetics\ANxChr-NATR-3mW",
        group_name="ADxChr-NoATR",
        angles=Angles,
        joints=Key_points,
        total_fly_number=10,
        fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    IavxChr = Group(
        fly_kinematic_data_path=r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\Optogenetics\G115xChr-30Hz-22ms-2s",
        group_name="IavxChr",
        angles=Angles,
        joints=Key_points,
        total_fly_number=15,
        fps=[250, 250, 250, 250, 250,
             250, 250, 250, 250, 250,
             250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    IavxChr_NATR = Group(
        fly_kinematic_data_path=r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\Optogenetics\G115xChr-NATR",
        group_name="IavxChr-NoATR",
        angles=Angles,
        joints=Key_points,
        total_fly_number=15,
        fps=[250, 250, 250, 250, 250,
             250, 250, 250, 250, 250,
             250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    AllCSxChr = Group(
        fly_kinematic_data_path=r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\Optogenetics\AllCSxChr",
        group_name="AllCSxChr",
        angles=Angles,
        joints=Key_points,
        total_fly_number=15,
        fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    AllCSxChr_NATR = Group(
        fly_kinematic_data_path=r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\Optogenetics\AllCSxChr-NATR",
        group_name="AllCSxChr-NoATR",
        angles=Angles,
        joints=Key_points,
        total_fly_number=11,
        fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)


    ANxChr = Group(
        fly_kinematic_data_path=r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\Optogenetics\ANxChr-3mW",
        group_name="ANxChr",
        angles=Angles,
        joints=Key_points,
        total_fly_number=10,
        fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    BrixL006 = Group(
        fly_kinematic_data_path=r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\Optogenetics\BrixL006-3mW",
        group_name="BrixL006",
        angles=Angles,
        joints=Key_points,
        total_fly_number=9,
        fps=[250, 250, 250, 250, 250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    Kine_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\Optogenetics\L006xL011-Max"
    LaLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\L006xL011-Max\All.xlsx"
    MOCPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\L006xL011-Max\MOC.xlsx"
    MOLPath = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\L006xL011-Max\MOL.xlsx"
    LexA_Br = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name="LexA-Br-Green",
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=15,
                 fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
                 trial_num=30,
                 video_duration=Video_duration)

    WT_Opto = Group(
        fly_kinematic_data_path=r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\Optogenetics\CT-WT-NC-22ms-2s",
        group_name="WT",
        angles=Angles,
        joints=Key_points,
        total_fly_number=4,
        fps=[250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    WT_T1_TTa = None
    # WT_T2_TTa = None
    WT_T3_TTa = None
    WT_T2_CTF = None
    return (WT_T1_TTa, WT_T2_TTa, WT_T3_TTa, G106_T2_TTa, G107_T2_TTa, G108_T2_TTa, G114_T2_TTa,
            G115_T2_TTa, G116_T2_TTa, G117_T2_TTa, G118_T2_TTa, G119_T2_TTa, ANxChr, BrixL006, WT_Opto, ANxGTACR, LexA_Br)

if __name__ == "__main__":

    os.chdir(r"C:\Users\agrawal-admin\Desktop\Landing\Graph")
    Key_points = ["L-wing", "L-wing-hinge", "R-wing", "R-wing-hinge", "abdomen-tip",
                  "platform-tip", "L-platform-tip", "R-platform-tip", "platform-axis",
                  "R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT", "R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT",
                  "R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT", "L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT",
                  "L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT", "L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT"]

    Angles = [["R-mCT", "R-mFT", "R-mTT"], ["L-mCT", "L-mFT", "L-mTT"], ["L-wing", "L-wing-hinge", "R-wing"]]

    WT_T1_TTa_Fly_Num = 15
    WT_T2_TTa_Fly_Num = 15
    WT_T3_TTa_Fly_Num = 20
    G106_TTa_Fly_Num = 16
    G107_TTa_Fly_Num = 14
    G108_TTa_Fly_Num = 17
    G114_TTa_Fly_Num = 16
    G115_TTa_Fly_Num = 16
    G116_TTa_Fly_Num = 18
    G117_TTa_Fly_Num = 18
    G118_TTa_Fly_Num = 15
    G119_TTa_Fly_Num = 18

    G108_CTF_Fly_Num = 13
    WT_T2_CTF_Fly_Num = 18

    WT_T2_TTa_Fly_Num = 15
    G106_TTa_Fly_Num = 16
    G107_TTa_Fly_Num = 14
    G108_TTa_Fly_Num = 17
    G114_TTa_Fly_Num = 1
    G115_TTa_Fly_Num = 16
    G116_TTa_Fly_Num = 15
    G117_TTa_Fly_Num = 18
    G118_TTa_Fly_Num = 15
    G119_TTa_Fly_Num = 18


    # WT_T2_CTF_Fly_Num = 1
    # G108_CTF_Fly_Num = 5

    (WT_T1_TTa, WT_T2_TTa, WT_T3_TTa, G106_T2_TTa, G107_T2_TTa, G108_T2_TTa, G114_T2_TTa,
     G115_T2_TTa, G116_T2_TTa, G117_T2_TTa, G118_T2_TTa, G119_T2_TTa, ANxChr, BrixL006, WT_Opto, ANxGTACR, LexA_Br) = Group_meta_data()

    exp = [WT_T2_TTa, G107_T2_TTa, G108_T2_TTa, G114_T2_TTa, G115_T2_TTa, G117_T2_TTa, G118_T2_TTa, G119_T2_TTa]

    # G114_NC_22ms.read_all_trials()
    # G114_NC_NATR_22ms.read_all_trials()
    # G114_NC_Cons.read_all_trials()

    # WT_T1_TTa.read_all_data() # size bad
    # WT_T1_TTa.filter_nan_fly()
    # WT_T2_TTa.read_all_data() # good
    # WT_T2_TTa.filter_nan_fly()
    # ANxChr.read_all_trials()
    # BrixL006.read_all_trials()
    # WT_Opto.read_all_trials()
    # WT_T3_TTa.read_all_data() # size bad
    # WT_T3_TTa.filter_nan_fly()
    # G106_T2_TTa.read_all_data() # size bad
    # G106_T2_TTa.filter_nan_fly()

    # G107_T2_TTa.read_all_data() # size bad
    # G107_T2_TTa.filter_nan_fly()
    LexA_Br.read_all_data()
    # G108_T2_TTa.read_all_data() # good
    # G108_T2_TTa.filter_nan_fly()

    # G114_T2_TTa.read_all_data() # good
    # G114_T2_TTa.filter_nan_fly()  # good

    # G115_T2_TTa.read_all_data() # good
    # G115_T2_TTa.filter_nan_fly()

    # G116_T2_TTa.read_all_data()
    # G116_T2_TTa.filter_nan_fly()

    # G117_T2_TTa.read_all_data() # good
    # G117_T2_TTa.filter_nan_fly()

    # G118_T2_TTa.read_all_data() # good
    # G118_T2_TTa.filter_nan_fly()

    # G119_T2_TTa.read_all_data() # good
    # G119_T2_TTa.filter_nan_fly()
    # WT_T2_CTF.read_all_data() # bad
    # G108_T2_CTF.read_all_data() # good
    KirGroups = [WT_T2_TTa, G106_T2_TTa, G107_T2_TTa, G108_T2_TTa, G114_T2_TTa, G116_T2_TTa, G117_T2_TTa, G118_T2_TTa, G119_T2_TTa, G115_T2_TTa]
    # KirGroups = [WT_T2_TTa, G106_T2_TTa]
    plotter = kp.PlotCreator(0.03, 3, 0.5, 250)
    plotter.plot_ON_OFF_angle(LexA_Br)
    # plotter.plot_motion_vector_with_plane(WT_T2_TTa.fly_kinematic_data["F2T7"], 50)
    # IavxChr_NATR.read_all_trials()
    # AllCSxChr.read_all_trials()
    # AllCSxChr_NATR.read_all_trials()
    # AllCSxChr.read_all_trials()
    # ANxGTACR.read_all_data()
    # ANxGTACR.filter_nan_fly()
    # plotter.plot_FT_change(WT_Opto)
    # plotter.plot_FT_change(AllCSxChr_NATR)
    # plotter.plot_flying_posture_over_trial(G117)
    # plotter.plot_tarsus_contact_vs_latency(G117)
    # plotter.MakePlot(G117)
    # plotter.plot_motion_vector_with_plane(G117.fly_kinematic_data["F1T1"], int(G117.fly_kinematic_data["F1T1"].moc))
    # plotter.plot_posture_angle_change(G117.fly_kinematic_data["F1T1"])
    # plotter.plot_FT_ang_ll(G117)
    # plotter.plot_IndiLegContactPointWithPlatform(G117.fly_kinematic_data["F1T1"], int(G117.fly_kinematic_data["F1T1"].moc))
    # plotter.plot_IndividualLegLatency(G117)
    # index_to_iterate = [(5, 5), (2, 11), (4, 5), (4, 13), (4, 15), (4, 16), (4, 18)]
    # index_to_iterate = WT_T2_TTa.get_targeted_trials(["Landing"])
    # for t in index_to_iterate:
        # print(f"Fly: {t[0]} Trial: {t[1]}")
        # if t[1] == 13:
        # plotter.plot_leg_search_cycle(WT_T2_TTa.fly_kinematic_data[f"F{t[0]}T{t[1]}"], "R-f")
    # plotter.plot_FTCT_characteristic(WT_T2_TTa)
    # plotter.plot_FTCT_characteristic(WT_T2_TTa)
    # plotter.plot_InidividualLegContactDistribution(WT_T3_TTa)
    # plotter.plot_CTF_MOC(G108_CTF)
    # plotter.plot_FTCT_characteristic(WT_T2_TTa)
    # plotter.plot_CTF_MOC(G108_CTF.fly_kinematic_data[f"F{2}T{2}"])
    # plotter.plot_trajectory(WT.fly_kinematic_data["F1T1"], ["L-mLT"])
    # plotter.plot_angle_change_psd(WT_T2_TTa)
    # plotter.plot_Inidi_Leg_Contact(WT_T2_TTa)
    # plotter.normalized_leg_angle_change_trace(WT_T2_TTa)
    # plotter.plotting_exp(WT_T2_TTa)
    # plotter.plot_angle_change_traces_groups(exp)

    # print(WT_T2_TTa.landing_trial_index)
    # plotter.plot_angle_relative_mol(WT_T2_TTa)
    # print([(s - (10 - 1)) / 100 for s in range(10)])
    # plotter.plot_FT_change([G114_NC_22ms, G114_NC_NATR_22ms, G114_NC_Cons])













