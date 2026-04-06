import os
from kinematic_object import Group, Trial, Point
import KinematicPlot as kp
import warnings

from kinematic_utilities import SimpleCalculation, DetectCharacteristics

warnings.filterwarnings(action="ignore", category=RuntimeWarning)
warnings.filterwarnings(action="ignore", category=FutureWarning)

def Group_meta_data(Video_duration=7, Trials_num=20):
    global Key_points

    global WT_T1_CTF_Fly_Num
    global WT_T2_CTF_Fly_Num
    global WT_T3_CTF_Fly_Num
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

    global WT_Green_Fly_Num
    global ANxGTACR_Fly_Num
    global LexA_Br_Fly_Num
    global MTGal4_Fly_Num
    global IavxGTACR_Fly_Num
    global CSS048xGTACR_Fly_Num
    global CSS021xGTACR_Fly_Num

    global WT_T2_CTF_Fly_Num
    global G108_CTF_Fly_Num
    global Trial_offset

    DataFolder = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19"
    LandingDataFolder = r"C:\Users\agrawal-admin\Desktop\LandingData"

    """
    WT T1 CxTr
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "WT-T1-CxTr"
    Kine_path = os.path.join(DataFolder, r"Network-05-30\LPAcrossLegsJoints\T1-CxTr")
    LaLPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T1-CxTr\T1-CxTr-LL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T1-CxTr\T1-CxTr-MOC_old.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T1-CxTr\T1-CxTr-MOL.xlsx")
    WT_T1_CTF = Group(moc_data_path=MOCPath,
               mol_data_path=MOLPath,
               ll_data_path=LaLPath,
               fly_kinematic_data_path=Kine_path,
               group_name=GroupName,
               angles=Angles,
               joints=Key_points,
               total_fly_number=WT_T1_CTF_Fly_Num,
               fps=FPS,
               trial_num=Trials_num,
               trials_offset=Trial_offset,
               video_duration=Video_duration)

    """
    WT T1 TiTa
    """
    FPS = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 250, 250, 250]
    GroupName = "WT-T1-TiTa"
    Kine_path = os.path.join(DataFolder, "Network-01-18-2026\LPAcrossLegsJoints\T1-TiTa")
    LaLPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T1-TiTa\T1-TiTaLP.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T1-TiTa\MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T1-TiTa\MOL.xlsx")
    WT_T1_TTa = Group(moc_data_path=MOCPath,
                  mol_data_path=MOLPath,
                  ll_data_path=LaLPath,
                  fly_kinematic_data_path=Kine_path,
                  group_name=GroupName,
                  angles=Angles,
                  joints=Key_points,
                  total_fly_number=WT_T1_TTa_Fly_Num,
                  fps=FPS,
                  trials_offset=Trial_offset,
                  trial_num=Trials_num,
                  video_duration=Video_duration)
    """
    WT T2 CxTr
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "WT-T2-CxTr"
    Kine_path = os.path.join(DataFolder, "Network-05-30\LPAcrossLegsJoints\T2-CxTr")
    LaLPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T2-CxTr\T2-CxTr-LL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T2-CxTr\T2-CxTr-MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T2-CxTr\T2-CxTr-MOL.xlsx")
    WT_T2_CTF = Group(moc_data_path=MOCPath,
                      mol_data_path=MOLPath,
                      ll_data_path=LaLPath,
                      fly_kinematic_data_path=Kine_path,
                      group_name=GroupName,
                      angles=Angles,
                      joints=Key_points,
                      total_fly_number=WT_T2_CTF_Fly_Num,
                      fps=FPS,
                      trial_num=Trials_num,
                      trials_offset=Trial_offset,
                      video_duration=Video_duration)
    """
    WT T2 TiTa
    """
    FPS = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
    GroupName = "WT-T2-TiTa"
    Kine_path = os.path.join(DataFolder, "Network-01-18-2026\LPAcrossLegsJoints\T2-TiTa")
    LaLPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T2-TiTa\T2-TiTaLP.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T2-TiTa\T2-TiTaMOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T2-TiTa\T2-TiTaMOL.xlsx")
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
    WT T3 CxTr
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "WT-T3-CxTr"
    Kine_path = os.path.join(DataFolder, "Network-01-18-2026\LPAcrossLegsJoints\T3-CxTr")
    LaLPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T3-CxTr\T3-CxTr-LL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T3-CxTr\T3-CxTr-MOC-old.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T3-CxTr\T3-CxTr-MOL.xlsx")
    WT_T3_CTF = Group(moc_data_path=MOCPath,
                      mol_data_path=MOLPath,
                      ll_data_path=LaLPath,
                      fly_kinematic_data_path=Kine_path,
                      group_name=GroupName,
                      angles=Angles,
                      joints=Key_points,
                      total_fly_number=WT_T3_CTF_Fly_Num,
                      fps=FPS,
                      trials_offset=Trial_offset,
                      trial_num=Trials_num,
                      video_duration=Video_duration)

    """
    WT T3 TiTa
    """
    FPS = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 250, 250, 250, 250, 250]
    GroupName = "WT-T3-TiTa"
    Kine_path = os.path.join(DataFolder, "Network-01-18-2026\LPAcrossLegsJoints\T3-TiTa")
    LaLPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T3-TiTa\T3-TiTaLP.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T3-TiTa\MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "LPAcrossLegsJoints\T3-TiTa\MOL.xlsx")
    WT_T3_TTa = Group(moc_data_path=MOCPath,
                  mol_data_path=MOLPath,
                  ll_data_path=LaLPath,
                  fly_kinematic_data_path=Kine_path,
                  group_name=GroupName,
                  angles=Angles,
                  joints=Key_points,
                  total_fly_number=WT_T3_TTa_Fly_Num,
                  fps=FPS,
                  trials_offset=Trial_offset,
                  trial_num=Trials_num,
                  video_duration=Video_duration)


    """
    G106 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G106-HP1"
    Kine_path = os.path.join(DataFolder, "Network-03-14\HCS+_UASKir2.1eGFP\G106-HP1_T2-TiTa")
    LaLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G106-HP1_T2-TiTa\G106-HP1_T2-TiTa-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G106-HP1_T2-TiTa\G106-HP1_T2-TiTa-MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G106-HP1_T2-TiTa\G106-HP1_T2-TiTa-MOL.xlsx")
    G106_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=G106_TTa_Fly_Num,
                 trials_offset=Trial_offset,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)


    """
    G107 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G107-HP2"
    Kine_path = os.path.join(DataFolder, "Network-05-30\HCS+_UASKir2.1eGFP\G107-HP2_T2-TiTa")
    LaLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G107-HP2_T2-TiTa\G107-HP2_T2-TiTa-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G107-HP2_T2-TiTa\MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G107-HP2_T2-TiTa\MOL.xlsx")
    G107_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 trials_offset=Trial_offset,
                 total_fly_number=G107_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G108 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G108-HP3"
    Kine_path = os.path.join(DataFolder, "Network-05-30\HCS+_UASKir2.1eGFP\G108-HP3_T2-TiTa")
    LaLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G108-HP3_T2-TiTa\G108-HP3_T2-TiTa-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G108-HP3_T2-TiTa\G108MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G108-HP3_T2-TiTa\MOL.xlsx")
    G108_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 trials_offset=Trial_offset,
                 total_fly_number=G108_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G114 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G114-ClFl"
    Kine_path = os.path.join(DataFolder, "Network-05-30\HCS+_UASKir2.1eGFP\G114-ClFl_T2-TiTa")
    LaLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G114-ClFl_T2-TiTa\G114-ClFl_T2-TiTa-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G114-ClFl_T2-TiTa\MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G114-ClFl_T2-TiTa\MOL.xlsx")
    G114_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 trials_offset=Trial_offset,
                 total_fly_number=G114_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G115 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G115-Iav"
    Kine_path = os.path.join(DataFolder, "Network-05-30\HCS+_UASKir2.1eGFP\G115-Iav_T2-TiTa")
    LaLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G115-Iav_T2-TiTa\G115-Iav_T2-TiTa-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G115-Iav_T2-TiTa\MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G115-Iav_T2-TiTa\MOL.xlsx")
    G115_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 trials_offset=Trial_offset,
                 total_fly_number=G115_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G116 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G116-ClEx"
    Kine_path = os.path.join(DataFolder, "Network-05-30\HCS+_UASKir2.1eGFP\G116-ClEx_T2-TiTa")
    LaLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G116-ClEx_T2-TiTa\G116-ClEx_T2-TiTa-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G116-ClEx_T2-TiTa\MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G116-ClEx_T2-TiTa\MOL.xlsx")
    G116_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 trials_offset=Trial_offset,
                 total_fly_number=G116_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G117 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G117-HkFl"
    Kine_path = os.path.join(DataFolder, "Network-05-30\HCS+_UASKir2.1eGFP\G117-HkFl_T2-TiTa")
    LaLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G117-HkFl_T2-TiTa\G117-HkFl_T2-TiTa-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G117-HkFl_T2-TiTa\MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G117-HkFl_T2-TiTa\MOL.xlsx")
    G117_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 trials_offset=Trial_offset,
                 total_fly_number=G117_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G118 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G118-HkEx"
    Kine_path = os.path.join(DataFolder, "Network-05-30\HCS+_UASKir2.1eGFP\G118-HkEx_T2-TiTa")
    LaLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G118-HkEx_T2-TiTa\G118-HkEx_T2-TiTa-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G118-HkEx_T2-TiTa\MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G118-HkEx_T2-TiTa\MOL.xlsx")
    G118_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 trials_offset=Trial_offset,
                 total_fly_number=G118_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    G119 T2 TiTa
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "G119-Club"
    Kine_path = os.path.join(DataFolder, "Network-05-30\HCS+_UASKir2.1eGFP\G119-Club_T2-TiTa")
    LaLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G119-Club_T2-TiTa\G119-Club_T2-TiTa-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G119-Club_T2-TiTa\G119MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "HCS+_UASKir2.1eGFP\G119-Club_T2-TiTa\MOL.xlsx")
    G119_T2_TTa = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 trials_offset=Trial_offset,
                 total_fly_number=G119_TTa_Fly_Num,
                 fps=FPS,
                 trial_num=Trials_num,
                 video_duration=Video_duration)

    """
    WT-Green
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "WT-Green"
    Kine_path = os.path.join(DataFolder, r"Network-01-18-2026\Optogenetics\WT-Green-Max")
    LaLPath = os.path.join(LandingDataFolder, "OPTO\WT-Green\WT-Green-Max-LL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "OPTO\WT-Green\WT-Green-Max-MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "OPTO\WT-Green\WT-Green-Max-MOL.xlsx")
    WT_Green = Group(moc_data_path=MOCPath,
                     mol_data_path=MOLPath,
                     ll_data_path=LaLPath,
                     fly_kinematic_data_path=Kine_path,
                     group_name=GroupName,
                     angles=Angles,
                     joints=Key_points,
                     total_fly_number=WT_Green_Fly_Num,
                     fps=FPS,
                     trial_num=30,
                     video_duration=Video_duration)


    """
    ANxGTACR
    """
    FPS = [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
    GroupName = "ANxGTACR"
    Kine_path = os.path.join(DataFolder, r"Network-01-18-2026\Optogenetics\ANxGTACR-Max")
    LaLPath = os.path.join(LandingDataFolder, "OPTO\ANxGTACR-12mW\ANxGTACR-12mW-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "OPTO\ANxGTACR-12mW\ANxGTACR-12mW-MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "OPTO\ANxGTACR-12mW\ANxGTACR-12mW-MOL.xlsx")
    ANxGTACR = Group(moc_data_path=MOCPath,
                 mol_data_path=MOLPath,
                 ll_data_path=LaLPath,
                 fly_kinematic_data_path=Kine_path,
                 group_name=GroupName,
                 angles=Angles,
                 joints=Key_points,
                 total_fly_number=ANxGTACR_Fly_Num,
                 fps=FPS,
                 trial_num=30,
                 video_duration=Video_duration)

    """
    Tarsal Bristle x GTACR
    """
    Kine_path = os.path.join(DataFolder, "Network-07-04\Optogenetics\L006xL011-Max")
    LaLPath = os.path.join(LandingDataFolder, "OPTO\TaBRIxLexAG-12mW\TaBRIxLexAG-12mW-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "OPTO\TaBRIxLexAG-12mW\TaBRIxLexAG-12mW-MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "OPTO\TaBRIxLexAG-12mW\TaBRIxLexAG-12mW-MOL.xlsx")
    LexA_Br = Group(moc_data_path=MOCPath,
                    mol_data_path=MOLPath,
                    ll_data_path=LaLPath,
                    fly_kinematic_data_path=Kine_path,
                    group_name="LexA-Br-Green",
                    angles=Angles,
                    joints=Key_points,
                    total_fly_number=LexA_Br_Fly_Num,
                    fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
                    trial_num=30,
                    video_duration=Video_duration)

    """
    Empty Gal4 x GTACR
    """
    Kine_path = os.path.join(DataFolder, r"Network-01-18-2026\Optogenetics\GTACRxEmpty-Max")
    LaLPath = os.path.join(LandingDataFolder, "OPTO\MTGal4xGTACR-12mW\MTGal4xGTACR-12mW-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "OPTO\MTGal4xGTACR-12mW\MTGal4xGTACR-12mW-MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "OPTO\MTGal4xGTACR-12mW\MTGal4xGTACR-12mW-MOL.xlsx")
    MTGal4 = Group(moc_data_path=MOCPath,
                   mol_data_path=MOLPath,
                   ll_data_path=LaLPath,
                   fly_kinematic_data_path=Kine_path,
                   group_name="MTGal4",
                   angles=Angles,
                   joints=Key_points,
                   total_fly_number=MTGal4_Fly_Num,
                   fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
                   trial_num=30,
                   video_duration=Video_duration)

    """
    IAV x GTACR
    """
    Kine_path = os.path.join(DataFolder, r"Network-01-18-2026\Optogenetics\IavxGTACR-Max")
    LaLPath = os.path.join(LandingDataFolder, "OPTO\IAVxGTACR-12mW\IAVxGTACR-12mW-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "OPTO\IAVxGTACR-12mW\IAVxGTACR-12mW-MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "OPTO\IAVxGTACR-12mW\IAVxGTACR-12mW-MOL.xlsx")
    IavxGTACR = Group(moc_data_path=MOCPath,
                      mol_data_path=MOLPath,
                      ll_data_path=LaLPath,
                      fly_kinematic_data_path=Kine_path,
                      group_name="IavxGTACR",
                      angles=Angles,
                      joints=Key_points,
                      total_fly_number=IavxGTACR_Fly_Num,
                      fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
                      trial_num=30,
                      video_duration=Video_duration)

    """
    CSS048 x GTACR
    """
    Kine_path = os.path.join(DataFolder, r"Network-01-18-2026\Optogenetics\CSS048xGTACR-Max")
    LaLPath = os.path.join(LandingDataFolder, "OPTO\CS048xGTACR-12mW\CS048xGTACR-12mW-ALL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "OPTO\CS048xGTACR-12mW\CS048xGTACR-12mW-MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "OPTO\CS048xGTACR-12mW\CS048xGTACR-12mW-MOL.xlsx")
    CSS048xGTACR = Group(moc_data_path=MOCPath,
                      mol_data_path=MOLPath,
                      ll_data_path=LaLPath,
                      fly_kinematic_data_path=Kine_path,
                      group_name="CSS048xGTACR",
                      angles=Angles,
                      joints=Key_points,
                      total_fly_number=CSS048xGTACR_Fly_Num,
                      fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
                      trial_num=30,
                      video_duration=Video_duration)

    """
    CSS021 x GTACR
    """
    Kine_path = os.path.join(DataFolder, r"Network-01-18-2026\Optogenetics\CSS021xGTACR")
    LaLPath = os.path.join(LandingDataFolder, "OPTO\CSS021xGTACR-12mW\CSS021xGTACR-12mW-LL.xlsx")
    MOCPath = os.path.join(LandingDataFolder, "OPTO\CSS021xGTACR-12mW\CSS021xGTACR-12mW-MOC.xlsx")
    MOLPath = os.path.join(LandingDataFolder, "OPTO\CSS021xGTACR-12mW\CSS021xGTACR-12mW-MOL.xlsx")
    CSS021xGTACR = Group(moc_data_path=MOCPath,
                         mol_data_path=MOLPath,
                         ll_data_path=LaLPath,
                         fly_kinematic_data_path=Kine_path,
                         group_name="CSS021xGTACR",
                         angles=Angles,
                         joints=Key_points,
                         total_fly_number=CSS021xGTACR_Fly_Num,
                         fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250,
                              250],
                         trial_num=30,
                         video_duration=Video_duration)



    AllCSxChr = Group(
        fly_kinematic_data_path=os.path.join(DataFolder, "Network-07-04\Optogenetics\AllCSxChr"),
        group_name="AllCSxChr",
        angles=Angles,
        joints=Key_points,
        total_fly_number=15,
        ll_data_path=r"C:\Users\agrawal-admin\Desktop\LandingData\OPTO\ALLCSxCHR-400uW-ALL.xlsx",
        fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    ANxChr = Group(
        fly_kinematic_data_path=os.path.join(DataFolder, "Network-01-18-2026\OPTO\ANxCHR-4mW"),
        group_name="ANxChr",
        angles=Angles,
        joints=Key_points,
        total_fly_number=10,
        ll_data_path=r"C:\Users\agrawal-admin\Desktop\LandingData\OPTO\ANxCHR-4mW-ALL.xlsx",
        fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    BrixL006 = Group(
        fly_kinematic_data_path=os.path.join(DataFolder, "Network-01-18-2026\OPTO\TaBRIxLexAR-4mW"),
        group_name="LexA-Bri-Red",
        angles=Angles,
        joints=Key_points,
        total_fly_number=9,
        ll_data_path=r"C:\Users\agrawal-admin\Desktop\LandingData\OPTO\TaBRIxLexAR-4mW-ALL.xlsx",
        fps=[250, 250, 250, 250, 250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    CSS48xChr = Group(
        fly_kinematic_data_path=os.path.join(DataFolder, r"Network-01-18-2026\Optogenetics\CSS48xChr-Max"),
        group_name="CSS48xChr",
        angles=Angles,
        ll_data_path=r"C:\Users\agrawal-admin\Desktop\LandingData\OPTO\CS048xCHR-12mW-ALL.xlsx",
        joints=Key_points,
        total_fly_number=18,
        fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    CSS21xChr = Group(
        fly_kinematic_data_path=os.path.join(DataFolder, r"Network-01-18-2026\Optogenetics\CSS021xChr-Max"),
        group_name="CSS21xChr",
        angles=Angles,
        ll_data_path=r"C:\Users\agrawal-admin\Desktop\LandingData\OPTO\CSS021xCHR-12mW-ALL.xlsx",
        joints=Key_points,
        total_fly_number=10,
        fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    IavxChr = Group(
        fly_kinematic_data_path=os.path.join(DataFolder, r"Network-01-18-2026\Optogenetics\IavxChr-Max"),
        group_name="IAVxChr",
        angles=Angles,
        ll_data_path=r"C:\Users\agrawal-admin\Desktop\LandingData\OPTO\IAVxCHR-12mW-ALL.xlsx",
        joints=Key_points,
        total_fly_number=12,
        fps=[250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250],
        trial_num=30,
        video_duration=7)

    return (WT_T1_CTF, WT_T1_TTa, WT_T2_CTF, WT_T2_TTa, WT_T3_CTF, WT_T3_TTa, G106_T2_TTa, G107_T2_TTa, G108_T2_TTa, G114_T2_TTa,
            G115_T2_TTa, G116_T2_TTa, G117_T2_TTa, G118_T2_TTa, G119_T2_TTa, ANxChr, BrixL006, ANxGTACR, LexA_Br, AllCSxChr, CSS48xChr, CSS21xChr, IavxChr,
            MTGal4, IavxGTACR, WT_Green, CSS048xGTACR, CSS021xGTACR)

if __name__ == "__main__":

    os.chdir(r"C:\Users\agrawal-admin\Desktop\Landing")
    Key_points = ["L-wing", "L-wing-hinge", "R-wing", "R-wing-hinge", "abdomen-tip",
                  "platform-tip", "L-platform-tip", "R-platform-tip", "platform-axis",
                  "R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT", "R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT",
                  "R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT", "L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT",
                  "L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT", "L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT"]

    Angles = [["R-mCT", "R-mFT", "R-mTT"], ["L-mCT", "L-mFT", "L-mTT"], ["L-wing", "L-wing-hinge", "R-wing"]]

    WT_T1_CTF_Fly_Num = 15
    WT_T2_CTF_Fly_Num = 18
    WT_T3_CTF_Fly_Num = 17
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
    WT_Green_Fly_Num = 9
    ANxGTACR_Fly_Num = 12
    LexA_Br_Fly_Num = 15
    MTGal4_Fly_Num = 15
    IavxGTACR_Fly_Num = 17
    CSS048xGTACR_Fly_Num = 23
    CSS021xGTACR_Fly_Num = 19

    G108_CTF_Fly_Num = 13
    WT_T2_CTF_Fly_Num = 18


    WT_T1_CTF_Fly_Num = 15
    WT_T2_CTF_Fly_Num = 18
    WT_T3_CTF_Fly_Num = 17
    WT_T1_TTa_Fly_Num = 15
    WT_T2_TTa_Fly_Num = 15
    WT_T3_TTa_Fly_Num = 20

    G106_TTa_Fly_Num = 1
    G107_TTa_Fly_Num = 1
    G108_TTa_Fly_Num = 1
    G114_TTa_Fly_Num = 1
    G115_TTa_Fly_Num = 1
    G116_TTa_Fly_Num = 2
    G117_TTa_Fly_Num = 1
    G118_TTa_Fly_Num = 1
    G119_TTa_Fly_Num = 1

    WT_Green_Fly_Num = 9
    ANxGTACR_Fly_Num = 12
    LexA_Br_Fly_Num = 15
    MTGal4_Fly_Num = 15
    IavxGTACR_Fly_Num = 17
    CSS048xGTACR_Fly_Num = 23
    CSS021xGTACR_Fly_Num = 19

    Trial_offset = 3
    # WT_T2_CTF_Fly_Num = 1
    # G108_CTF_Fly_Num = 5

    (WT_T1_CTF, WT_T1_TTa, WT_T2_CTF, WT_T2_TTa, WT_T3_CTF, WT_T3_TTa, G106_T2_TTa, G107_T2_TTa, G108_T2_TTa, G114_T2_TTa,
     G115_T2_TTa, G116_T2_TTa, G117_T2_TTa, G118_T2_TTa, G119_T2_TTa, ANxChr, BrixL006, ANxGTACR, LexA_Br, AllCSxChr, CSS48xChr, CSS21xChr, IavxChr,
     MTGal4, IavxGTACR, WT_Green, CSS048xGTACR, CSS021xGTACR) = Group_meta_data()

    # MTGal4.read_all_data()
    WT_T1_TTa.read_all_data()
    WT_T1_TTa.filter_nan_fly()
    WT_T2_TTa.read_all_data()
    WT_T2_TTa.filter_nan_fly()
    WT_T3_TTa.read_all_data()
    WT_T3_TTa.filter_nan_fly()

    # WT_T1_CTF.read_all_data()
    # WT_T1_CTF.filter_nan_fly()
    # WT_T2_CTF.read_all_data()
    # WT_T2_CTF.filter_nan_fly()
    # WT_T3_CTF.read_all_data()
    # WT_T3_CTF.filter_nan_fly()
    # G106_T2_TTa.read_all_data()
    # G106_T2_TTa.filter_nan_fly()
    # G107_T2_TTa.read_all_data()
    # G107_T2_TTa.filter_nan_fly()
    # G108_T2_TTa.read_all_data()
    # G108_T2_TTa.filter_nan_fly()
    # G114_T2_TTa.read_all_data()
    # G114_T2_TTa.filter_nan_fly()
    # G115_T2_TTa.read_all_data()
    # G115_T2_TTa.filter_nan_fly()
    # G116_T2_TTa.read_all_data()
    # G116_T2_TTa.filter_nan_fly()
    # G117_T2_TTa.read_all_data()
    # G117_T2_TTa.filter_nan_fly()
    # G118_T2_TTa.read_all_data()
    # G118_T2_TTa.filter_nan_fly()
    # G119_T2_TTa.read_all_data()
    # G119_T2_TTa.filter_nan_fly()
    # ANxGTACR.read_all_data()
    # ANxGTACR.filter_opto_data()
    # CSS048xGTACR.read_all_data()
    # CSS048xGTACR.filter_opto_data()
    # WT_Green.read_all_data()
    # LexA_Br.read_all_data()
    # MTGal4.read_all_data()
    # IavxGTACR.read_all_data()
    """ANxGTACR.read_all_data()
    ANxGTACR.filter_opto_data()
    LexA_Br.read_all_data()
    LexA_Br.filter_opto_data()
    MTGal4.read_all_data()
    MTGal4.filter_opto_data()
    IavxGTACR.read_all_data()
    IavxGTACR.filter_opto_data()
    WT_Green.read_all_data()
    WT_Green.filter_opto_data()
    CSS048xGTACR.read_all_data()
    CSS048xGTACR.filter_opto_data()
    CSS021xGTACR.read_all_data()
    CSS021xGTACR.filter_opto_data()"""

    """ANxChr.read_all_trials()
    BrixL006.read_all_trials()
    CSS48xChr.read_all_trials()
    CSS21xChr.read_all_trials()
    IavxChr.read_all_trials()
    AllCSxChr.read_all_trials()"""
    # ANxGTACR.read_all_trials()


    plotter = kp.PlotCreator(0.03, 3, 0.35, 250)
    os.chdir(r"C:\Users\agrawal-admin\Desktop\Landing\stat and figures")
    # plotter.plot_LS_vs_LL(WT_T2_TTa, False, r"C:\Users\agrawal-admin\Desktop\Landing\WT-T2-TiTa--0.71.csv", r"C:\Users\agrawal-admin\Desktop\Landing\WT-T2-TiTa-WT-T2-TiTa-LS_data_.csv")
    # plotter.plot_LS_vs_LL(ANxGTACR, True)
    # plotter.plot_IT_vs_OT(WT_T2_TTa)

    # plotter.plot_LP([WT_T1_TTa, WT_T2_TTa, WT_T3_TTa])
    # plotter.plot_secondary_contact_probability([WT_T1_TTa, WT_T2_TTa, WT_T3_TTa])
    # plotter.plot_secondary_contact_probability_OPTO(ANxGTACR)
    # plotter.plot_secondary_contact_probability_OPTO(LexA_Br)
    # plotter.plot_secondary_contact_probability_OPTO(MTGal4)
    # plotter.plot_secondary_contact_probability_OPTO(IavxGTACR)
    # plotter.plot_secondary_contact_probability_OPTO(WT_Green)
    # plotter.plot_secondary_contact_probability_OPTO(CSS048xGTACR)
    # plotter.plot_secondary_contact_probability_OPTO(CSS021xGTACR)
    # plotter.plot_LL([WT_T1_TTa, WT_T2_TTa, WT_T3_TTa])
    # plotter.analyzer.combine_data(WT_T1_TTa, "LS", False)
    # plotter.analyzer.combine_data(WT_T1_TTa, "SC", False)
    # plotter.analyzer.combine_data(WT_T3_TTa, "LS", False)
    # plotter.analyzer.combine_data(WT_T3_TTa, "SC", False)

    # plotter.analyzer.combine_data(CSS021xGTACR, "LS", True)
    # plotter.analyzer.combine_data(CSS021xGTACR, "SC", True)
    """plotter.analyzer.combine_data(WT_T2_TTa, "LS", False)
    plotter.analyzer.combine_data(WT_T2_TTa, "SC", False)

    plotter.analyzer.combine_data(ANxGTACR, "LS", True)
    plotter.analyzer.combine_data(ANxGTACR, "SC", True)

    plotter.analyzer.combine_data(LexA_Br, "LS", True)
    plotter.analyzer.combine_data(LexA_Br, "SC", True)

    plotter.analyzer.combine_data(MTGal4, "LS", True)
    plotter.analyzer.combine_data(MTGal4, "SC", True)

    plotter.analyzer.combine_data(IavxGTACR, "LS", True)
    plotter.analyzer.combine_data(IavxGTACR, "SC", True)

    plotter.analyzer.combine_data(WT_Green, "LS", True)
    plotter.analyzer.combine_data(WT_Green, "SC", True)

    plotter.analyzer.combine_data(CSS048xGTACR, "LS", True)
    plotter.analyzer.combine_data(CSS048xGTACR, "SC", True)

    plotter.analyzer.combine_data(CSS021xGTACR, "LS", True)
    plotter.analyzer.combine_data(CSS021xGTACR, "SC", True)"""
    # plotter.plot_Chrimson_ang_change([ANxChr, BrixL006, CSS48xChr, CSS21xChr, IavxChr, AllCSxChr])
    # plotter.plot_chrimson_LP([ANxChr, BrixL006, CSS48xChr, CSS21xChr, IavxChr, AllCSxChr])
    # plotter.plot_combined_LS_and_SC([CSS021xGTACR], True, "orange")
    # plotter.plot_Opto_data(CSS021xGTACR)
    # plotter.plot_combined_LS_and_SC([ANxGTACR], True, "magenta")
    # plotter.plot_IT_vs_OT(WT_T2_TTa)
    # plotter.plot_combined_LS_and_SC([WT_T1_TTa, WT_T2_TTa, WT_T3_TTa], False, "green")
    # plotter.plot_combined_LS_and_SC([ANxGTACR], True, "magenta")
    # plotter.plot_combined_LS_and_SC([LexA_Br], True, "green")
    # plotter.plot_combined_LS_and_SC([MTGal4], True, "blue")
    # plotter.plot_combined_LS_and_SC([IavxGTACR], True, "brown")
    # plotter.plot_combined_LS_and_SC([WT_Green], True, "grey")
    # plotter.plot_combined_LS_and_SC([CSS048xGTACR], True, "red")
    plotter.plot_combined_LS_and_SC([CSS021xGTACR], True, "orange")













