import sys
from pathlib import Path

from pymongo import collection

import VisualizeData
import ManageDataBase

def main():
    print("Start")
    base = sys.argv[1]  # βαζετε απο τερματικο το path
    base = Path(base) #an to uelei path
    # 1. Παρε τα ονοματα απο τα αρχεια. Προσοχη είναι ομαδοποιημενα σε γυποσκοπιο+αξελερομετρο αναλογα με την κατηγορία δλδ
    # fileA =[ [filename-scrollup-gyr,filename-scrollup-acc] , ...] οπου Α ο χρηστης

    totalFiles = VisualizeData.getFilenames(base)
    filenamesA,filenamesB,filenamesS = VisualizeData.ClusteringResults(base)


    #2.Visualize 3axis & 6axis data
    VisualizeData.readcsv_plot(totalFiles)
    VisualizeData.PlotAllCluster(filenamesA,filenamesB,filenamesS)

#-----------END VISUALAZATION-------------------------------------------------------#

    #3.Connect 2 database
    print("Connect To Database")
    collection=ManageDataBase.Connect()

    #insert individualy acc and gyr
    print("insert individualy")
    dfACC, dfGyr, filacc, filgyr = ManageDataBase.AccOrGyr(totalFiles)
    ManageDataBase.Insert2Mongo(dfACC,filacc,dfGyr,filgyr,collection)

    #insert gyr and acc in pairs
    print("Insert clusters")
    ManageDataBase.Insert2MongoCluster(filenamesA,filenamesB,filenamesS,collection)

#------------------END OF PROCESSING-------------------------------------#

if __name__ == '__main__':
    main()