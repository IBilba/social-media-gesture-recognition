import datetime
import sys
import pandas as pd
from fontTools.ufoLib import filenames
from pymongo import MongoClient

#Αν δεν ειμαι σε cloud περιβαλλον
def Connect():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['IoTSocial'] # or any other name
    collection = db['sensor_data']
    return collection

#for all the filenames i did not do the clusters
#Χωρισμος σε γυροσκοπιο ή accelerometer
def AccOrGyr(totalFile):
    dfACC = []
    dfGyr = []
    filacc = []
    filgyr = []
    for file in totalFile:
        if "acc" or "ac" in file.lower():
            dfACC.append(pd.read_csv(file))
            filacc.append(file)
        elif "gyr" in file.lower():
            dfGyr.append(pd.read_csv(file))
            filgyr.append(file)
        else:
            print("Unknown")
    return dfACC, dfGyr, filacc, filgyr
#insert 2 mongo
def Insert2Mongo(dfACC,filacc,dfGyr,filgyr,collection):
    #accelerometer first
    for i in range(len(dfACC)):
        current_filename = filacc[i]
        name_parts = current_filename.stem.split('_')
        current_user = name_parts[-1]
        document = {
           "data": {
                "acc_x": dfACC[i].iloc[:, 0].tolist(),
                "acc_y": dfACC[i].iloc[:, 1].tolist(),
                "acc_z": dfACC[i].iloc[:, 2].tolist()
           },
                "gesture_id": name_parts[0],
                "sensor": "Accelerometer",
                "user": current_user,
                "datetime": datetime.datetime.now(datetime.timezone.utc)
        }
        collection.insert_one(document)
    #gyroscpe next
    for i in range(len(dfGyr)):
        current_filename = filgyr[i]
        name_parts = current_filename.stem.split('_')
        current_user = name_parts[-1]
        document = {
            "data": {
                "gyr_x": dfGyr[i].iloc[:, 0].tolist(),
                "gyr_y": dfGyr[i].iloc[:, 1].tolist(),
                "gyr_z": dfGyr[i].iloc[:, 2].tolist()
            },
            "gesture_id": name_parts[0],
            "sensor": "Accelerometer",
            "user": current_user,
            "datetime": datetime.datetime.now(datetime.timezone.utc)
        }
        collection.insert_one(document)
    print("Insert finished")

#--------------------end process for all filenames----------------------------------#

#now for clustering
def helperProcess(filenames):
    df = []
    for f1, f2 in zip(filenames[0::2], filenames[1::2]):
        tmp = []
        tmp.append(pd.read_csv(f1))
        tmp.append(pd.read_csv(f2))
        df.append(tmp)
    return df
def Insert2MongoCluster(fileuser1,fileuser2,fileuser3,collection):
    dftotal = helperProcess(fileuser1) + helperProcess(fileuser2) +helperProcess(fileuser3)
    names = fileuser1 + fileuser2 + fileuser3
    metadata_files = names[0::2]
    for i in range(len(dftotal)):
        clean_name = metadata_files[i].stem
        name_parts = clean_name.split('_')
        current_user = name_parts[-1]
        document = {
           "data": {
                "acc_x": dftotal[i][0].iloc[:, 0].tolist(),
                "acc_y": dftotal[i][0].iloc[:, 1].tolist(),
                "acc_z": dftotal[i][0].iloc[:, 2].tolist(),
                "gyr_x": dftotal[i][1].iloc[:, 0].tolist(),
                "gyr_y": dftotal[i][1].iloc[:, 1].tolist(),
                "gyr_z": dftotal[i][1].iloc[:, 2].tolist()
           },
                "gesture_id": name_parts[0],
                "sensor": "Accelerometer + Gyroscope",
                "user": current_user,
                "datetime": datetime.datetime.now(datetime.timezone.utc)
        }
        collection.insert_one(document)
    print(f"Insert finished: {len(dftotal)} documents added.")

#----------end process for acc + gyr-----------------------------------#

