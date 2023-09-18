from rdataStruct import rdataStruct_FERS_newVector as rdataStruct
from rdataStruct import FERStoStrip_singlenp
from tqdm import tqdm
import numpy as np
import datetime

from logger import create_logger
logging = create_logger("rootconverter")

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
        self.globalEventCounter = 0
        # Buffer contanining parsed data
        self.buffer = {
            "Tstamp_us": np.array([], dtype=np.double),
            "TrgID": np.array([], dtype=np.uint32),
            "Brd": np.array([], dtype=np.uint32),
            "Ch": np.array([], dtype=np.uint32),
            "LG": np.array([], dtype=np.int32),
            "HG": np.array([], dtype=np.int32),
            "timestamp": np.array([], dtype=np.double)
        }

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
    def parseLineData_toBuffer(self, line: str):
        Tstamp_us = line[:22]
        TrgID = line[23:33]
        Brd = line[33:35]
        Ch = line[37:39]
        LG = line[39:49]
        HG = line[49:-1]
        #
        #data_new = [0,0,0,0,0,0]
        # Data object
        strData_new = [Tstamp_us, TrgID, Brd, Ch, LG, HG]
        for i, item in enumerate(strData_new):
            if item.strip() == "":
                item = self.strData_prev[i]
            else:
                self.strData_prev[i] = item
        
        self.buffer['Tstamp_us'] = np.append(self.buffer['Tstamp_us'], np.double(self.strData_prev[0]))
        self.buffer['TrgID'] = np.append(self.buffer['TrgID'], np.uint32(self.strData_prev[1]))
        self.buffer['Brd'] = np.append(self.buffer['Brd'], np.uint32(self.strData_prev[2]))
        self.buffer['Ch'] = np.append(self.buffer['Ch'], np.uint16(self.strData_prev[3]))
        self.buffer['LG'] = np.append(self.buffer['LG'], np.int16(self.strData_prev[4]))
        self.buffer['HG'] = np.append(self.buffer['HG'], np.int16(self.strData_prev[5]))
        self.buffer['timestamp'] = np.append(self.buffer['timestamp'], np.double(self.strData_prev[0])+self.startTime)


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
                for i, line in tqdm(enumerate(infile)):
                    if i<9:
                        if i==4:
                            self.histoCh = self.parseEnergyHistoCh(line)
                    else:
                        self.parseLineData_toBuffer(line)
            
            # Data clustering by event and ROOT filling
            ## Make sure to have matched/complete data for all the events by trimming the data
            ## fields to match the dimension of the smallest one
            smallestDim = len(self.buffer['Tstamp_us'])
            for dataField in self.buffer:
                if len(self.buffer[dataField]) != smallestDim:
                    logging.warning("Data fields have different dimensions. Trimming to match the smallest one.")
                smallestDim = min(smallestDim, len(self.buffer[dataField]))
            for dataField in self.buffer:
                self.buffer[dataField] = self.buffer[dataField][:smallestDim] # This assumes that the missing data is at the end of the file
            ## Cluster the data by event
            ### Get the list of different events
            evtList = np.unique(self.buffer['TrgID'])
            mask_det0 = (self.buffer['Brd'] == 0)
            mask_det1 = (self.buffer['Brd'] == 1)

            brokenEvent = 0
            for event in evtList:
                # Build the mask
                mask = self.buffer['TrgID'] == event
                maskd0 = mask & mask_det0
                maskd1 = mask & mask_det1

                if np.max(maskd0) == False or np.max(maskd1) == False:
                    brokenEvent += 1
                    continue # handle cases where no overlap is present
                
                fers_evt = event
                fers_trgtime = np.array([self.buffer['Tstamp_us'][maskd0][0], self.buffer['Tstamp_us'][maskd1][0]])
                fers_ch0 = self.buffer['Ch'][maskd0]
                fers_ch1 = self.buffer['Ch'][maskd1]
                strip0 = FERStoStrip_singlenp[fers_ch0][:,1]
                strip1 = FERStoStrip_singlenp[fers_ch1][:,1]
                lg0 = self.buffer['LG'][maskd0]
                hg0 = self.buffer['HG'][maskd0]
                lg1 = self.buffer['LG'][maskd1]
                hg1 = self.buffer['HG'][maskd1]
                timestamp = self.startTime+self.buffer['Tstamp_us'][maskd0][0]
                
                self.rfile.FERS_fill(
                    run = self.runID,
                    runTime = self.startTime,
                    event = self.globalEventCounter,
                    fers_evt = fers_evt,
                    fers_trgtime = fers_trgtime,
                    fers_ch0 = fers_ch0,
                    fers_ch1 = fers_ch1,
                    strip0 = strip0,
                    strip1 = strip1,
                    lg0 = lg0,
                    hg0 = hg0,
                    lg1 = lg1,
                    hg1 = hg1,
                    timestamp = timestamp
                )
                self.globalEventCounter += 1
                #print("fers_evt         ", fers_evt)
                #print("fers_trgtime     ", fers_trgtime)
                #print("fers_ch0         ", fers_ch0)
                #print("fers_ch1         ", fers_ch1)
                #print("strip0           ", strip0)
                #print("strip1           ", strip1)
                #print("lg0              ", lg0)
                #print("hg0              ", hg0)
                #print("lg1              ", lg1)
                #print("hg1              ", hg1)
                #print("timestamp        ", timestamp)

            if brokenEvent: logging.error(f"Lost event {brokenEvent} (out of {len(evtList)}), that is {brokenEvent/len(evtList)*100.:.2f} %")
            # Close the ROOT file
            self.closeROOT()
            logging.info(f"Run {self.runID} converted to ROOT file")
            return True
        else:
            return False
##############################################################
######## / rootconverter class ###############################
##############################################################



if __name__=="__main__":
    logging.info("Test function for the class rootconverter")
    test = rootconverter("/home/pietro/cleardaq/CLEAR_Vesper/FERS/data/230621/Run163_list.txt", "/home/pietro/work/CLEAR_March/FERS/TB4-192_FERS/")
    test.convert()
    logging.info("Goodbye")