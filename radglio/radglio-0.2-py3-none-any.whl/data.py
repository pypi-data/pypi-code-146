

import os
import shutil
import pydicom
import pandas as pd


def RTstruct_UID(path):
    rtstruct_dicom = []
    instand_uid = []
    structure_setlabel = []

    for file in os.listdir(path=path):
        if file.endswith('.dcm'):
            dicom = pydicom.dcmread(os.path.join(path, file))
            if dicom.Modality == "RTSTRUCT":
                rtstruct_dicom.append(file)
                uid = dicom.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].SeriesInstanceUID
                instand_uid.append(uid)
                structure_setlabel.append(dicom.StructureSetLabel)

    info = {
        "Structure Set Label" : structure_setlabel,
        "Series Instance UID" : instand_uid,
        "SOP Instance UID"    : rtstruct_dicom

    }
    return info


def MR_UID(path):

    RTSTRUCTSeriesInstanceUID = []
    MRSeriesInstanceUID = []
    SeriesDescription = []
    DicomFile = []
    FileName = []

    uid_rtstruct = RTstruct_UID(path=path).get("Series Instance UID")
    label = RTstruct_UID(path=path).get("Structure Set Label")
    
    index = 0
    for i in uid_rtstruct:
        for file in os.listdir(path=path):
            if file.endswith('.dcm'):
                dicom = pydicom.dcmread(os.path.join(path, file))
                if dicom.Modality == "MR":
                    uid = dicom.SeriesInstanceUID
                    series_description = dicom.SeriesDescription
                    if i == uid:
                        RTSTRUCTSeriesInstanceUID.append(i)
                        MRSeriesInstanceUID.append(uid)
                        SeriesDescription.append(series_description)
                        DicomFile.append(file)
                        FileName.append(label[index])
        index = index + 1

    res = {
        "RTSTRUCT SeriesInstanceUID" : RTSTRUCTSeriesInstanceUID,
        "MR SeriesInstanceUID" : MRSeriesInstanceUID,
        "Series Description": SeriesDescription,
        "Dicom File" : DicomFile,
        "File Name" : FileName
    }
                   
    return res


def create_folder(file_path):
    try:
        raw_data = MR_UID(path=file_path)
        data = pd.DataFrame(raw_data)
        label = RTstruct_UID(path=file_path).get("Structure Set Label")
        rtstruct = RTstruct_UID(path=file_path).get("SOP Instance UID")

        # cheack folder name
        index = 0
        for name in label:
            if name in os.listdir(file_path):
                print("Folder Already Created")
                # cheack file name
                for i in range(data.shape[0]):
                    file = data["Dicom File"][i]
                    original_path = os.path.join(file_path, file)
                    moving_path = os.path.join(file_path, data["File Name"][i])
                    shutil.copy(original_path, moving_path)

            else:
                # create folder
                folder_name = os.path.join(file_path, name)
                os.mkdir(folder_name)
                original_path = os.path.join(file_path, rtstruct[index])
                moving_path = os.path.join(folder_name)
                shutil.copy(original_path, moving_path)

            index = index + 1

        # cheack file name
        for i in range(data.shape[0]):
            file = data["Dicom File"][i]
            original_path = os.path.join(file_path, file)
            moving_path = os.path.join(file_path, data["File Name"][i])
            shutil.copy(original_path, moving_path)

    except Exception as e:
        print(e)

    return

def radglio_data_preparation(path):
    try:
        folders = os.listdir(path=path)
        for folder in folders:
            subfolders = os.listdir(os.path.join(path,folder))
            for subfolder in subfolders:
                if subfolder.endswith('.csv'):
                    pass
                else:
                    file_paths = os.path.join(path, folder, subfolder)
                    create_folder(file_path=file_paths)

        res = {
            "success" : True,
            "message" : "Data Preparation Done !"
        }

    except Exception as e:
        res = {
            "success" : False,
            "message" : str(e)
        }

    return res

