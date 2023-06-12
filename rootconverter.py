from logger import *
from rdataStruct import *
import datetime

##############################################################
######## rootconverter class #################################
##############################################################
### Class
# FERS ASCII (list + info) to ROOT class
class rootconverter():
    def __init__(self, path, outputROOTdirectory) -> None:
        logging.debug(f"rootconverter - Filename: {path}")
        self.fname, self.inputTXTdirectory = self.utils_extractFilename(path)
        self.outputROOTdirectory = outputROOTdirectory
        # Run ID (from file), path of the filename of the data file and info file
        self.runID = self.utils_parseRunID(self.fname)
        self.fname_list = self.inputTXTdirectory+f"Run{self.runID}_list.txt"
        self.fname_info = self.inputTXTdirectory+f"Run{self.runID}_Info.txt"
        # Number of channels in the energy histogram
        self.histoCh = -1
        # Run info from RunN_info.txt
        self.runSetup = []
        self.startTime = -1
        self.stopTime = -1
        self.elapsedTime = -1
        #
        self.parseLineData_prev = []
        self.strData_prev = ["-1" for i in range(6)]
        # Global variables for ROOT filesaving
        rfilename = self.outputROOTdirectory+f"Run{self.runID}_list.root"
        self.rfile = rdataStruct(rfilename, "RECREATE")

    # Get run filename without extentions from the string
    def utils_extractFilename(self, path: str) -> tuple:
        slash = path.rfind('/')
        dottxt = path.rfind(".txt")
        if slash==-1:
            pathtxt = ""
            filename = path[:dottxt]
        else:
            pathtxt = path[:slash+1]
            filename = path[slash+1:dottxt]
        return (filename, pathtxt)

    # Set the output directory of the ROOT files
    def setOutputROOTDir(self, path: str):
        if path[-1] != '/':
            path = path + '/' 
        self.outputROOTdirectory = path
    
    # Get the runID from the filename
    def utils_parseRunID(self, filename: str):
        # Strip off absolute path and file extension
        posA = filename.rfind('Run')
        posB = filename.find('_', posA)
        return int(filename[posA+3:posB])
    
    # Parse the data line
    def parseLineData_toROOT(self, line: str):
        Tstamp_us = line[:22]
        TrgID = line[23:33]
        Brd = line[33:35]
        Ch = line[37:39]
        LG = line[39:49]
        HG = line[49:-1]
        #
        data_new = [0,0,0,0,0,0]
        # Data object
        strData_new = [Tstamp_us, TrgID, Brd, Ch, LG, HG]
        for i, item in enumerate(strData_new):
            if item.strip() == "":
                item = self.strData_prev[i]
            else:
                self.strData_prev[i] = item
            data_new[i] = float(item)
        event = 0
        runTime = self.startTime
        trgTime = runTime + np.double(data_new[0]*1e-6)
        if self.rFileOpen:
            (self.rfile).FERS_fill(self.runID, runTime, event, trgTime, data_new[1], data_new[0], data_new[2], data_new[3], data_new[4], data_new[5], data_new[2], FERStoStrip_single[data_new[3]], 0, 0)
            #self.runDataTree.Fill(self.runID, runTime, event, data_new[0], data_new[1], data_new[2], data_new[3], data_new[4], data_new[5], trgTime)
        return data_new

    # Parse the energy histo channel line
    def parseEnergyHistoCh(self, line: str):
        return int(line[29:-1])

    # Prepare the ROOT file
    def prepareROOT(self, fname: str):
        self.rFileOpen = True

    # Close the instance of the ROOT file currently open
    def closeROOT(self):
        if self.rFileOpen:
            #self.runSetupTree.Write()
            #self.runDataTree.Write()
            #self.rfile.Close()
            self.rfile.closeROOT()
            self.rFileOpen = False

    # Take as input the filename.txt or path/filename.txt and return filename
    def fnameToROOT(self, fname: str):
        result = fname
        posB = fname.rfind('.')
        # Convert the path/filename.txt to filename.txt 
        if fname.rfind('/') != -1:
            #logging.debug(f"fname: {fname}")
            posA = fname.rfind('/')
            result = fname[posA+1:posB]
            #logging.debug("Case A: ", result)
        else:
            result = fname[:posB]
            #logging.debug("Case B: ", result)
        #logging.debug(fname, result+".root")
        return result+".root"

    # Get run info parsing
    def processRunInfo(self, stream):
        logging.info("Let's see...")
        # Process the line
        def parseLine(line: str):
            if line[0] != '#' and '#' in line:
                parName  = line[:35]
                parValue = line[35:56]
                parDescr = line[58:-1]
                return [parName.strip(), parValue.strip(), parDescr.strip()]
            else:
                return None
        # Fill with the acquisition start time/end time
        (self.runSetup).append(("runStartTime", f"{self.startTime}", "Acquisition start time [posix int ms]"))
        (self.runSetup).append(("runStopTime", f"{self.stopTime}", "Acquisition end time [posix int ms]"))
        # Fill the self.runInfo var
        for line in stream:
            ldat = parseLine(line)
            if type(ldat) is list:
                (self.runSetup).append(ldat)
                # For ROOT
                self.rfile.FERSsetup_pushback(self.runID, ldat[0], ldat[1], ldat[2])
                #self.vrunIDs.push_back(self.runID)
                #self.vparName.push_back(ldat[0])
                #self.vparValue.push_back(ldat[1])
                #self.vparDescr.push_back(ldat[2])
        # Debug
        #for i, entry in enumerate(self.runSetup):
        #    print(i, entry)

    # Check if the run has been completed (condition verified when the info file is written)
    def isRunClosed(self):
        try:
            infoFile = open(self.fname_info, 'r')
            for i, line in enumerate(infoFile):
                if i>=3 and i<=5:
                    starPos = line.find("Start Time: ")
                    stopPos = line.find("Stop Time:  ")
                    elapPos = line.find("Elapsed time = ")
                    
                    if starPos != -1:
                        if line.find(":", 11) != -1:
                            # Old date format
                            logging.warning("Start/stop time in old format")
                            startTime = datetime.datetime(
                                day=int(line[12:14]),
                                month=int(line[15:17]),
                                year=int(line[18:22]),
                                hour=int(line[23:25]),
                                minute=int(line[26:28])
                            )
                            if len(line) >29: startTime.second = int(line[29:31])
                            self.startTime = startTime.timestamp()
                        else:
                            # New date format
                            self.startTime   = np.double(int(line[starPos+12:-1])) / np.uint(1000)

                    if stopPos != -1:
                        if line.find(":", 10) != -1:
                            # Old date format
                            stopTime = datetime.datetime(
                                day=int(line[12:14]),
                                month=int(line[15:17]),
                                year=int(line[18:22]),
                                hour=int(line[23:25]),
                                minute=int(line[26:28])
                            )
                            if len(line) >29: stopTime.second = int(line[29:31])
                            self.stopTime = stopTime.timestamp()
                        else:
                            # New date format
                            self.stopTime    = np.double(int(line[stopPos+12:-1])) / np.uint(1000)
                    
                    if elapPos != -1:
                        elapsedTime_us = line[elapPos+15:line.find(' us', elapPos)]
                        #logging.debug(f"|{elapsedTime_us}|")
                        try:
                            self.elapsedTime = float(elapsedTime_us)
                        except ValueError:
                            self.elapsedTime = 0
                            logging.error(f"Unable to determine elapsed time for line: {line}")
                        #logging.debug(self.startTime, self.stopTime, self.elapsedTime)
                if i>6:
                    break
            self.processRunInfo(infoFile)
            if self.startTime != -1 and self.stopTime != -1 and self.elapsedTime != -1: return True
        except FileNotFoundError:
            # Run not closed yet
            logging.info(f"Path: {self.fname_info}\nFileNotFoundError. Run not closed yet.")
            return False         

    # Convert txt to root file
    def convert(self):
        # Get filename of the ROOT file
        rfilename = self.outputROOTdirectory+f"Run{self.runID}_list.root"
        #logging.debug(f"rfilename: {rfilename}")
        if self.isRunClosed():
            # Open and prepare the ROOT file with setup data
            self.prepareROOT(rfilename)
            # Store run setup in ROOT
            #logging.debug(self.runSetupTree)
            #self.runSetupTree.Fill()
            self.rfile.FERSsetup_fill()
            # Store run datapoints in ROOT
            with open(self.fname_list, 'r') as infile:
                for i, line in enumerate(infile):
                    if i<9:
                        if i==4:
                            self.histoCh = self.parseEnergyHistoCh(line)
                    else:
                        self.parseLineData_toROOT(line)
            # Close the ROOT file
            self.closeROOT()
            logging.info(f"Run {self.runID} converted to ROOT file")
            return True
        else:
            return False
##############################################################
######## / rootconverter class ###############################
##############################################################










##############################################################
######## FERS A5202 to sensor ch. map ########################
##############################################################
# Dictionary with FERS channel to sensor associations
# FERS:[Sensor(upstream/downstream), stripNb]
FERStoStrip_single = {
    0  :  127,
    1  :  125,
    2  :  123,
    3  :  121,
    4  :  119,
    5  :  117,
    6  :  115,
    7  :  113,
    8  :  111,
    9  :  109,
    10 :  107,
    11 :  105,
    12 :  103,
    13 :  101,
    14 :  99,
    15 :  97,
    16 :  95,
    17 :  93,
    18 :  91,
    19 :  89,
    20 :  87,
    21 :  85,
    22 :  83,
    23 :  81,
    24 :  79,
    25 :  77,
    26 :  75,
    27 :  73,
    28 :  71,
    29 :  69,
    30 :  67,
    31 :  65,
    32 :  66,
    33 :  68,
    34 :  70,
    35 :  72,
    36 :  74,
    37 :  76,
    38 :  78,
    39 :  80,
    40 :  82,
    41 :  84,
    42 :  86,
    43 :  88,
    44 :  90,
    45 :  92,
    46 :  94,
    47 :  96,
    48 :  98,
    49 :  100,
    50 :  102,
    51 :  104,
    52 :  106,
    53 :  108,
    54 :  110,
    55 :  112,
    56 :  114,
    57 :  116,
    58 :  118,
    59 :  120,
    60 :  122,
    61 :  124,
    62 :  126,
    63 :  128
}
##############################################################
######## / FERS A5202 to sensor ch. map ######################
##############################################################