import ROOT
from logger import *
import tqdm
import numpy as np

class rdataStruct():
    # ROOT file    
    ROOTfile = None
    ROOTfilename = ""
    mode = None 
    
    ######################################################
    ### TTree: FERSsetup
    ## Variable definitions
    FERSsetup = None  
    FERSsetup_vrunIDs = ROOT.vector('unsigned int')()
    FERSsetup_vparName = ROOT.vector('string')()
    FERSsetup_vparValue = ROOT.vector('string')()
    FERSsetup_vparDescr = ROOT.vector('string')()
    FERSsetup_nametypes = [
        ("run"       , FERSsetup_vrunIDs,      "std::vector<unsigned int>",   "Run id number"),
        ("parName"   , FERSsetup_vparName,     "std::vector<string>",         "Parameter name"),
        ("parValue"  , FERSsetup_vparValue,    "std::vector<string>",         "Parameter value"),
        ("parDescr"  , FERSsetup_vparDescr,    "std::vector<string>",         "Parameter description")
    ]
    ## Functions
    # Store in local variables
    def FERSsetup_pushback(self, runIDs, parName, parValue, parDescr):
        self.FERSsetup_vrunIDs.push_back(runIDs)
        self.FERSsetup_vparName.push_back(parName)
        self.FERSsetup_vparValue.push_back(parValue)
        self.FERSsetup_vparDescr.push_back(parDescr)
    # Clear vectors
    def FERSsetup_clear(self):
        self.FERSsetup_vrunIDs.clear()
        self.FERSsetup_vparName.clear()
        self.FERSsetup_vparValue.clear()
        self.FERSsetup_vparDescr.clear()
    # Fill locals into ttree
    def FERSsetup_fill(self):
        if (self.FERSsetup) is None:
            logging.critical("Tree 'data' is not initialized")
            exit(0)
        (self.FERSsetup).Fill()
        self.FERSsetup_clear()
    # Clone an input FERSsetup TTree to this FERSsetup
    def FERSsetup_import(self, inFERSsetup):
        # Clear any previous content of the vectors
        self.FERSsetup_clear()
        # Loop over the input inFERSsetup and fill the vectors
        for i, entry in tqdm.tqdm(enumerate(inFERSsetup), total=inFERSsetup.GetEntries()):
            a = len(entry.run)
            b = len(entry.parName)
            c = len(entry.parValue) 
            d = len(entry.parDescr) 
            if (a != b) and (a!=c) and (a!=d):
                logging.critical("Problem here")
                exit(-1)
            for j in range(len(entry.run)):
                self.FERSsetup_vrunIDs.push_back(i)
                self.FERSsetup_vparName.push_back(entry.parName[j])
                self.FERSsetup_vparValue.push_back(entry.parValue[j])
                self.FERSsetup_vparDescr.push_back(entry.parDescr[j])
        # Fill the TTree
        self.FERSsetup_fill()
    #
    # Setup the FERSsetup TTree
    def setupTTree_FERSsetup(self):
        # Define the TTree
        self.FERSsetup = ROOT.TTree("FERSsetup", "TTree with run FERS setup settings")
        # Set branch addresses
        for item in (self.FERSsetup_nametypes):
            (self.FERSsetup).Branch(item[0], item[1])
        # Set leaves description
        self.TREE_SetLeavesDescriptions(self.FERSsetup, self.FERSsetup_nametypes)
    
    
    
    ######################################################
    ### TTree: FERS   
    ## Variable definitions
    FERS = None
    FERS_irun = np.array([0], dtype=np.uint32)
    FERS_drunTime = np.array([0], dtype=np.double)
    FERS_ievent = np.array([0], dtype=np.uint32)
    FERS_dtimestamp = np.array([0], dtype=np.double)
    FERS_ifers_evt = np.array([0], dtype=np.uint32)
    FERS_dfers_trgtime = np.array([0], dtype=np.double)
    FERS_ifers_board = np.array([0], dtype=np.uint32)
    FERS_ifers_ch = np.array([0], dtype=np.uint32)
    FERS_ifers_lg = np.array([0], dtype=np.int32)
    FERS_ifers_hg = np.array([0], dtype=np.int32)
    FERS_idet = np.array([0], dtype=np.uint32)
    FERS_istrip = np.array([0], dtype=np.uint32)
    FERS_dlg = np.array([0], dtype=np.double)
    FERS_dhg = np.array([0], dtype=np.double)
    FERS_nametypes = [
        ("run",         FERS_irun,          "run/i",            "Run id number"),
        ("runTime",     FERS_drunTime,      "runTime/D",        "Posix time of the run start on the PC"),
        ("event",       FERS_ievent,        "event/i",          "Event id number"),
        ("timestamp",   FERS_dtimestamp,    "timestamp/D",      "Event posix timestamp (absolute)"),
        ("fers_evt",    FERS_ifers_evt,     "fers_evt/i",       "FERS event ID [0-1000]"),
        ("fers_trgtime",FERS_dfers_trgtime, "fers_trgtime/D",   "FERS trigger time from run start [us]"),
        ("fers_board",  FERS_ifers_board,   "fers_board/i",     "FERS board ID [0,1]"),
        ("fers_ch",     FERS_ifers_ch,      "fers_ch/i",        "FERS channel number [0-63]"),
        ("fers_lg",     FERS_ifers_lg,      "fers_lg/I",        "FERS low-gain ADC signed value [int32]"),
        ("fers_hg",     FERS_ifers_hg,      "fers_hg/I",        "FERS high-gain ADC signed value [int32]"),
        ("det",         FERS_idet,          "det/i",            "Detector ID [0,1]"),
        ("strip",       FERS_istrip,        "strip/i",          "Strip ID [1-192]"),
        ("lg",          FERS_dlg,           "lg/D",             "Calibrated LG charge [pC]"),
        ("hg",          FERS_dhg,           "hg/D",             "Calibrated HG charge [pC]")
    ]
    ## Functions
    # Bind branches of the DT5730 to variables
    def FERS_bindBranches(self, tree):
        for item in self.FERS_nametypes:
            tree.SetBranchAddress(item[0], item[1])
    # Fill tree with data
    def FERS_fill(self, run, runTime, event, timestamp, fers_evt, fers_trgtime, fers_board, fers_ch, fers_lg, fers_hg, det, strip, lg, hg):
        if (self.FERS) is None:
            logging.critical("Tree 'data' is not initialized")
            exit(0)
        self.FERS_irun[0] = run
        self.FERS_drunTime[0] = runTime
        self.FERS_ievent[0] = event
        self.FERS_dtimestamp[0] = timestamp
        self.FERS_ifers_evt[0] = fers_evt
        self.FERS_dfers_trgtime[0] = fers_trgtime
        self.FERS_ifers_board[0] = fers_board
        self.FERS_ifers_ch[0] = fers_ch
        self.FERS_ifers_lg[0] = np.int32(np.short(fers_lg))
        self.FERS_ifers_hg[0] = np.int32(np.short(fers_hg))
        self.FERS_idet[0] = det
        self.FERS_istrip[0] = strip
        self.FERS_dlg[0] = lg
        self.FERS_dhg[0] = hg
        # Fill the tree
        (self.FERS).Fill()
    #   
    # Setup the FERS TTree
    def setupTTree_FERS(self):
        # Define the TTree
        self.FERS = ROOT.TTree("FERS", "FERS processed data")
        # Create branches
        for item in (self.FERS_nametypes):
            (self.FERS).Branch(item[0], item[1], item[2])
        # Set leaves description
        self.TREE_SetLeavesDescriptions(self.FERS, self.FERS_nametypes)

    
    
    ######################################################
    ######################################################
    ## Utilities
    # Set description (better readibility)
    def TREE_SetLeavesDescriptions(self, tree, tree_nametypes):
        for entry in tree_nametypes:
            tree.GetLeaf(entry[0]).SetTitle(entry[3])

    # Write all the content of the output root file and clear datastructures for the next one
    def closeROOT(self):
        if self.mode != "READ":
            (self.FERSsetup).Write()
            (self.FERS).Write()
            #(self.DT5730raw).Write()
        # Single file
        if type(self.ROOTfilename) is not list:
            (self.ROOTfile).Close()

    def __init__(self, fname, mode="RECREATE", setVars = None):
        ## Internal
        # mode state
        self.mode = mode
        # filename
        self.ROOTfilename = fname
        # Get run id and filename
        if mode == "READ":
            self.getRunID_fromFilename(fname)
        elif mode == "RECREATE" and type(setVars) is dict:
            self.fileFirstRunTime = setVars["fileRunTime"]
            self.fileRunID = setVars["fileRunID"]
            if self.fileRunID < 0:
                logging.error("Provided runID is negative.")
                logging.warning("runID defaulting to 0")
                self.fileRunID = 0
        elif mode == "RECREATE" and setVars==None:
            logging.warning(f"ROOT file is in {mode} and setVars provided are {setVars}")
        
        # Open ROOT output file
        self.ROOTfile = ROOT.TFile.Open(fname, mode)
        logging.info(f"Opening {fname} in {mode} mode")
        if mode == "RECREATE":
            logging.debug("Attaching branches to variables.")
            # Generate the FERSsetup TTree
            self.setupTTree_FERSsetup()
            # Generate the FERS TTree
            self.setupTTree_FERS()
        else:
            logging.warning(f"TTree {fname} in read mode")
            self.DT5730setup = self.ROOTfile.FERSsetup
            self.FERS = self.ROOTfile.FERS
######################################################
######################################################
######################################################
