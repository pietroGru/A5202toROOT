################################################################################################
# @info Classes for the ROOT input/output files from the various devices                       #
# @creation date 23/04/19                                                                      #
# @edit     date 23/08/06                                                                      #
#                                               more text here eventually                      #
################################################################################################
from logger import create_logger
import numpy as np
import ROOT
import tqdm

##############################################################
######## FERS A5202 to sensor ch. map ########################
##############################################################
# Dictionary with FERS channel to sensor associations
# FERS:[Sensor(upstream/downstream), stripNb]
# old map from Sergii (turned out to be wrong after all) # FERStoStrip = { 0  :  127, 1  :  125, 2  :  123, 3  :  121, 4  :  119, 5  :  117, 6  :  115, 7  :  113, 8  :  111, 9  :  109, 10 :  107, 11 :  105, 12 :  103, 13 :  101, 14 :  99, 15 :  97, 16 :  95, 17 :  93, 18 :  91, 19 :  89, 20 :  87, 21 :  85, 22 :  83, 23 :  81, 24 :  79, 25 :  77, 26 :  75, 27 :  73, 28 :  71, 29 :  69, 30 :  67, 31 :  65, 32 :  66, 33 :  68, 34 :  70, 35 :  72, 36 :  74, 37 :  76, 38 :  78, 39 :  80, 40 :  82, 41 :  84, 42 :  86, 43 :  88, 44 :  90, 45 :  92, 46 :  94, 47 :  96, 48 :  98, 49 :  100, 50 :  102, 51 :  104, 52 :  106, 53 :  108, 54 :  110, 55 :  112, 56 :  114, 57 :  116, 58 :  118, 59 :  120, 60 :  122, 61 :  124, 62 :  126, 63 :  128 }
FERStoStrip = {
    0   :   128,
    1   :   126,
    2   :   124,
    3   :   122,
    4   :   120,
    5   :   118,
    6   :   116,
    7   :   114,
    8   :   112,
    9   :   110,
    10  :   108,
    11  :   106,
    12  :   104,
    13  :   102,
    14  :   100,
    15  :   98,
    16  :   96,
    17  :   94,
    18  :   92,
    19  :   90,
    20  :   88,
    21  :   86,
    22  :   84,
    23  :   82,
    24  :   80,
    25  :   78,
    26  :   76,
    27  :   74,
    28  :   72,
    29  :   70,
    30  :   68,
    31  :   66,
    32  :   65,
    33  :   67,
    34  :   69,
    35  :   71,
    36  :   73,
    37  :   75,
    38  :   77,
    39  :   79,
    40  :   81,
    41  :   83,
    42  :   85,
    43  :   87,
    44  :   89,
    45  :   91,
    46  :   93,
    47  :   95,
    48  :   97,
    49  :   99,
    50  :   101,
    51  :   103,
    52  :   105,
    53  :   107,
    54  :   109,
    55  :   111,
    56  :   113,
    57  :   115,
    58  :   117,
    59  :   119,
    60  :   121,
    61  :   123,
    62  :   125,
    63  :   127
}

FERStoStrip = dict(sorted(FERStoStrip.items()))
FERStoStrip_singlenp = np.array(list(FERStoStrip.values()), dtype=np.uint16)
#FERStoStrip_GiulioCorretto_singlenp = np.array(list(FERStoStrip_GiulioCorretto.values()), dtype=np.uint16)
#FERStoStripMOD_GiulioOddEvenScambiati_singlenp = np.array(list(FERStoStripMOD_GiulioOddEvenScambiati.values()), dtype=np.uint16)
##############################################################
######## / FERS A5202 to sensor ch. map ######################
##############################################################




class rdataStruct_FERS():
    # rdataStruct_FERS logger
    logging = create_logger("rdataStruct_FERS")

    def __init__(self, fname, mode="RECREATE", setVars = None):
        ## Internal
        # mode state
        self.mode = mode
        # filename
        self.ROOTfilename = fname
    
        ######################################################
        ################
        ### TTree: FERSsetup
        ## Variable definitions
        #self.FERSsetup = None  
        self.FERSsetup_vrunIDs = ROOT.vector('unsigned int')()
        self.FERSsetup_vparName = ROOT.vector('string')()
        self.FERSsetup_vparValue = ROOT.vector('string')()
        self.FERSsetup_vparDescr = ROOT.vector('string')()
        self.FERSsetup_nametypes = [
            ("run"       , self.FERSsetup_vrunIDs,      "std::vector<unsigned int>",   "Run id number"),
            ("parName"   , self.FERSsetup_vparName,     "std::vector<string>",         "Parameter name"),
            ("parValue"  , self.FERSsetup_vparValue,    "std::vector<string>",         "Parameter value"),
            ("parDescr"  , self.FERSsetup_vparDescr,    "std::vector<string>",         "Parameter description")
        ]
        self.FERSsetup_fill_warnings = {item[0]:False for item in self.FERSsetup_nametypes}
        ################
        ### TTree: FERS   
        ## Variable definitions
        #self.FERS = None
        self.FERS_irun = np.array([0], dtype=np.uint32)
        self.FERS_drunTime = np.array([0], dtype=np.double)
        self.FERS_ievent = np.array([0], dtype=np.uint32)
        self.FERS_dtimestamp = np.array([0], dtype=np.double)
        self.FERS_ifers_evt = np.array([0], dtype=np.uint32)
        self.FERS_dfers_trgtime = np.array([0], dtype=np.double)
        self.FERS_ifers_board = np.array([0], dtype=np.uint16)
        self.FERS_ifers_ch = np.array([0], dtype=np.uint16)
        self.FERS_ifers_lg = np.array([0], dtype=np.int16)
        self.FERS_ifers_hg = np.array([0], dtype=np.int16)
        self.FERS_idet = np.array([0], dtype=np.uint16)
        self.FERS_istrip = np.array([0], dtype=np.uint16)
        self.FERS_dlg = np.array([0], dtype=np.double)
        self.FERS_dhg = np.array([0], dtype=np.double)
        self.FERS_nametypes = [
            ("run",             self.FERS_irun,          "run/i",            "Run id number"),
            ("runTime",         self.FERS_drunTime,      "runTime/D",        "Posix time of the run start on the PC"),
            ("event",           self.FERS_ievent,        "event/i",          "Event id number"),
            ("timestamp",       self.FERS_dtimestamp,    "timestamp/D",      "Event posix timestamp (absolute)"),
            ("fers_evt",        self.FERS_ifers_evt,     "fers_evt/i",       "FERS event ID [0-1000]"),
            ("fers_trgtime",    self.FERS_dfers_trgtime, "fers_trgtime/D",   "FERS trigger time from run start [us]"),
            ("fers_board",      self.FERS_ifers_board,   "fers_board/s",     "FERS board ID [0,1]"),
            ("fers_ch",         self.FERS_ifers_ch,      "fers_ch/s",        "FERS channel number [0-63]"),
            ("fers_lg",         self.FERS_ifers_lg,      "fers_lg/S",        "FERS low-gain ADC signed value [int16]"),
            ("fers_hg",         self.FERS_ifers_hg,      "fers_hg/S",        "FERS high-gain ADC signed value [int16]"),
            ("det",             self.FERS_idet,          "det/s",            "Detector ID [0,1]"),
            ("strip",           self.FERS_istrip,        "strip/s",          "Strip ID [1-192]"),
            ("lg",              self.FERS_dlg,           "lg/D",             "Calibrated LG charge [pC]"),
            ("hg",              self.FERS_dhg,           "hg/D",             "Calibrated HG charge [pC]")
        ]
        self.FERS_fill_warnings = {item[0]:False for item in self.FERS_nametypes}
        ######################################################
    
        # Get run id and filename
        if mode == "RECREATE" and type(setVars) is dict:
            self.fileFirstRunTime = setVars["fileRunTime"]
            self.fileRunID = setVars["fileRunID"]
            if self.fileRunID < 0:
                (self.logging).error("Provided runID is negative.")
                (self.logging).warning("runID defaulting to 0")
                self.fileRunID = 0
        elif mode == "RECREATE" and setVars==None:
            if ((self.logging).level==10): (self.logging).warning(f"ROOT file is in {mode} and setVars provided are {setVars}")
        
        # Open ROOT output file
        self.ROOTfile = ROOT.TFile.Open(fname, mode)
        (self.logging).debug(f"Opening {fname} in {mode} mode")
        if mode == "RECREATE":
            (self.logging).debug("Attaching branches to variables.")
            # Generate the FERSsetup TTree
            self.setupTTree_FERSsetup()
            # Generate the FERS TTree
            self.setupTTree_FERS()
        else:
            # FERSSetup
            self.FERSsetup = self.ROOTfile.FERSsetup
            ## todo Set branch addresses    
            # FERS
            self.FERS = self.ROOTfile.FERS
            # Set branch addresses
            self.FERS_bindBranches(self.FERS)


        
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
            (self.logging).critical("Tree 'data' is not initialized")
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
                (self.logging).critical("Problem here")
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
    # todo: set bind branch addresses
    
    
    ## Functions
    # Bind branches of the DT5730 to variables
    def FERS_bindBranches(self, tree):
        for item in self.FERS_nametypes:
            tree.SetBranchAddress(item[0], item[1])
    
    ## Fill tree with data
    #def FERS_fill(self, run, runTime, event, timestamp, fers_evt, fers_trgtime, fers_board, fers_ch, fers_lg, fers_hg, det, strip, lg, hg):
    #    if (self.FERS) is None:
    #        (self.logging).critical("Tree 'data' is not initialized")
    #        exit(0)
    #    self.FERS_irun[0] = run
    #    self.FERS_drunTime[0] = runTime
    #    self.FERS_ievent[0] = event
    #    self.FERS_dtimestamp[0] = timestamp
    #    self.FERS_ifers_evt[0] = fers_evt
    #    self.FERS_dfers_trgtime[0] = fers_trgtime
    #    self.FERS_ifers_board[0] = fers_board
    #    self.FERS_ifers_ch[0] = fers_ch
    #    self.FERS_ifers_lg[0] = np.int32(np.short(fers_lg))
    #    self.FERS_ifers_hg[0] = np.int32(np.short(fers_hg))
    #    self.FERS_idet[0] = det
    #    self.FERS_istrip[0] = strip
    #    self.FERS_dlg[0] = lg
    #    self.FERS_dhg[0] = hg
    #    # Fill the tree
    #    (self.FERS).Fill()

    # Fill tree with data
    def FERS_fill(self, **kwargs):
        if (self.FERS) is None:
            raise Exception("Tree 'data' is not initialized")
        for branch in self.FERS_nametypes:
            try:
                # Filling is based on length. If the length of the array is 1 then fill the content of the array
                # otherwise fill the array itself
                if len(branch[1]) == 1:
                    branch[1][0] = kwargs[branch[0]]
                else:
                    np.copyto(branch[1], kwargs[branch[0]])
            except KeyError:
                if not self.FERS_fill_warnings[branch[0]]:
                    (self.logging).warning(f"Leaf {branch[0]} not found in kwargs (further warnings suppressed)")
                    self.FERS_fill_warnings[branch[0]] = True
        # Fill the tree
        (self.FERS).Fill()
        
        
        
    # Get entry i-th of the FERS TTree (for read mode)
    def FERS_getEntry(self, i):
        """
        Description 
        
        Parameters
        ----------
            i (int): Entry number 

        Returns:
            FERS_irun : 0
            FERS_drunTime : 1
            FERS_ievent : 2
            FERS_dtimestamp : 3
            FERS_ifers_evt : 4
            FERS_dfers_trgtime : 5
            FERS_ifers_board : 6
            FERS_ifers_ch : 7 
            FERS_ifers_lg : 8
            FERS_ifers_hg : 9
            FERS_idet : 10
            FERS_istrip : 11 
            FERS_dlg : 12
            FERS_dhg : 13
        """
        (self.FERS).GetEntry(i)
        return [(self.FERS_irun)[0], (self.FERS_drunTime)[0], (self.FERS_ievent)[0], (self.FERS_dtimestamp)[0], (self.FERS_ifers_evt)[0], (self.FERS_dfers_trgtime)[0], (self.FERS_ifers_board)[0], (self.FERS_ifers_ch)[0], (self.FERS_ifers_lg)[0], (self.FERS_ifers_hg)[0], (self.FERS_idet)[0], (self.FERS_istrip)[0], (self.FERS_dlg)[0], (self.FERS_dhg)[0]]
    # Setup the FERS TTree
    def setupTTree_FERS(self):
        """
        Setup the TTree with the given name and title and the given nametypes.
        """
        
        self.FERS = ROOT.TTree("FERS", "FERS processed data")    # Define the TTree
        # Create branches
        for item in self.FERS_nametypes:
            if str(type(item[1])).find('std.vector') != -1:
                obj = (self.FERS).Branch(item[0], item[1])
            else:
                obj = (self.FERS).Branch(item[0], item[1], item[2])
        # Check if all the requested branch names have been used, or rather some
        # branch names were sanified due to incompatibility with ROOT nomenclature
        # e.g. like 'myvar.' which is not allowed
        # Get list of branch names
        branchNames = [branch.GetName() for branch in (self.FERS).GetListOfBranches()]
        if branchNames != [ item[0] for item in self.FERS_nametypes]:
            raise Exception("Some branch names were sanified due to incompatibility with ROOT nomenclature")
        # Set leaves description
        self.TREE_SetLeavesDescriptions(self.FERS, self.FERS_nametypes)

    
    
    ######################################################
    ######################################################
    ## Utilities
    # Set description (better readibility)
    def TREE_SetLeavesDescriptions(self, tree, tree_nametypes):
        for entry in tree_nametypes:
            tree.GetBranch(entry[0]).SetTitle(entry[3])

    # Write all the content of the output root file and clear datastructures for the next one
    def closeROOT(self):
        if self.mode != "READ":
            (self.FERSsetup).Write()
            (self.FERS).Write()
        # Single file
        if type(self.ROOTfilename) is not list:
            (self.ROOTfile).Close()
######################################################
######################################################
######################################################
######################################################
######################################################
class rdataStruct_FERS_newVector():
    # rdataStruct_FERS logger
    logging = create_logger("rdataStruct_FERS_newVector")
    
    def __init__(self, fname, mode="RECREATE", setVars = None):
        ## Internal
        # mode state
        self.mode = mode
        # filename
        self.ROOTfilename = fname

        ######################################################
        ### TTree: FERSsetup
        ## Variable definitions
        self.FERSsetup = None
        self.FERSsetup_vrunIDs = ROOT.vector('unsigned int')()
        self.FERSsetup_vparName = ROOT.vector('string')()
        self.FERSsetup_vparValue = ROOT.vector('string')()
        self.FERSsetup_vparDescr = ROOT.vector('string')()
        self.FERSsetup_nametypes = [
            ("run"       , self.FERSsetup_vrunIDs,      "std::vector<unsigned int>",   "Run id number"),
            ("parName"   , self.FERSsetup_vparName,     "std::vector<string>",         "Parameter name"),
            ("parValue"  , self.FERSsetup_vparValue,    "std::vector<string>",         "Parameter value"),
            ("parDescr"  , self.FERSsetup_vparDescr,    "std::vector<string>",         "Parameter description")
        ]
        self.FERSsetup_fill_warnings = {item[0]:False for item in self.FERSsetup_nametypes}
        ######################################################
        ################
        ### TTree: FERS   
        ## Variable definitions
        self.FERS = None
        self.FERS_irun = np.array([0], dtype=np.uint32)
        self.FERS_drunTime = np.array([0], dtype=np.double)
        self.FERS_ievent = np.array([0], dtype=np.uint32)
        self.FERS_dtimestamp = np.array([0], dtype=np.double)
        self.FERS_ifers_evt = np.array([0], dtype=np.uint32)
        self.FERS_vfers_trgtime = np.zeros(2, dtype=np.double)      # vector
        self.FERS_vfers_ch0 = np.zeros(64, dtype=np.uint16)         # vector
        self.FERS_vfers_ch1 = np.zeros(64, dtype=np.uint16)         # vector
        self.FERS_vstrip0 = np.zeros(64, dtype=np.uint16)           # vector
        self.FERS_vstrip1 = np.zeros(64, dtype=np.uint16)           # vector
        self.FERS_vlg0 = np.zeros(64, dtype=np.int16)               # vector
        self.FERS_vhg0 = np.zeros(64, dtype=np.int16)               # vector
        self.FERS_vlg1 = np.zeros(64, dtype=np.int16)               # vector
        self.FERS_vhg1 = np.zeros(64, dtype=np.int16)               # vector
        self.FERS_vclg0 = np.zeros(64, dtype=np.double)             # vector
        self.FERS_vchg0 = np.zeros(64, dtype=np.double)             # vector
        self.FERS_vclg1 = np.zeros(64, dtype=np.double)             # vector
        self.FERS_vchg1 = np.zeros(64, dtype=np.double)             # vector
        self.FERS_dtime = np.array([0], dtype=np.double)
        #
        self.FERS_nametypes = [
            ["run",         self.FERS_irun,          "run/i",            "Run id number"],
            ["runTime",     self.FERS_drunTime,      "runTime/D",        "Posix time of the run start on the PC"],
            ["event",       self.FERS_ievent,        "event/i",          "Event id number"],
            ["timestamp",   self.FERS_dtimestamp,    "timestamp/D",      "Event posix timestamp (absolute)"],
            ["fers_evt",    self.FERS_ifers_evt,     "fers_evt/i",       "FERS event ID [0-1000]"],
            ["fers_trgtime",self.FERS_vfers_trgtime, "fers_trgtime[2]/D","FERS trigger time from run start [us]"],
            ["fers_ch0",    self.FERS_vfers_ch0,     "fers_ch0[64]/s",   "FERS ch det0 [uint16]"],
            ["fers_ch1",    self.FERS_vfers_ch1,     "fers_ch1[64]/s",   "FERS ch det1 [uint16]"],
            ["strip0",      self.FERS_vstrip0,       "strip0[64]/s",     "Strip ID det0 [uint16]"],
            ["strip1",      self.FERS_vstrip1,       "strip1[64]/s",     "Strip ID det1 [uint16]"],
            ["lg0",         self.FERS_vlg0,          "lg0[64]/S",        "FERS low-gain (signed) ADC det0 [int16]"],
            ["hg0",         self.FERS_vhg0,          "hg0[64]/S",        "FERS high-gain (signed) ADC det0 [int16]"],
            ["lg1",         self.FERS_vlg1,          "lg1[64]/S",        "FERS low-gain (signed) ADC det1 [int16]"],
            ["hg1",         self.FERS_vhg1,          "hg1[64]/S",        "FERS high-gain (signed) ADC det1 [int16]"],
            ["clg0",        self.FERS_vclg0,         "clg0[64]/D",       "Calibrated LG charge det0 [pC]"],
            ["chg0",        self.FERS_vchg0,         "chg0[64]/D",       "Calibrated HG charge det0 [pC]"],
            ["clg1",        self.FERS_vclg1,         "clg1[64]/D",       "Calibrated LG charge det1 [pC]"],
            ["chg1",        self.FERS_vchg1,         "chg1[64]/D",       "Calibrated HG charge det1 [pC]"],
            ["time",        self.FERS_dtime,         "time/D",           "Event posix digitizer timestamp"]
        ]
        #
        self.FERS_fill_warnings = {item[0]:False for item in self.FERS_nametypes}      


        # Get run id and filename
        ## override fileRunID if parameter is given as external argument
        if mode == "RECREATE" and type(setVars) is dict:
            self.fileFirstRunTime = setVars["fileRunTime"]
            self.fileRunID = setVars["fileRunID"]
            if self.fileRunID < 0:
                (self.logging).error("Provided runID is negative.")
                (self.logging).warning("runID defaulting to 0")
                self.fileRunID = 0
        elif mode == "RECREATE" and setVars==None:
            (self.logging).warning(f"ROOT file is in {mode} and setVars provided are {setVars}")
        

        # Open the given ROOT in read | write mode
        self.ROOTfile = ROOT.TFile.Open(fname, mode)
        (self.logging).info(f"Opening {fname} in {mode} mode")
        
        if mode in ["NEW", "CREATE", "RECREATE", "UPDATE"]:
            (self.logging).debug("Attaching branches to variables.")
            self.setupTTree_FERSsetup() 
            self.setupTTree_FERS() 
        elif mode == "READ":
            self.FERSsetup = self.ROOTfile.FERSsetup
            self.FERS = self.ROOTfile.FERS
            # Set branch addresses
            self.bindBranches(self.FERSsetup)
            self.bindBranches(self.FERS)
        else:
            Exception(f"Mode {mode} not recognized.")


    #def __del__(self):
    #    #self.FERS_vlg.clear()
    #    #self.FERS_vhg.clear()
    #    (self.logging).info("[rootconverter] Memory cleared")
        
    ######################################################
    ######################################################

    
    ## FERSsetup methods
    # Setup fuction for TTree FERSsetup
    def setupTTree_FERSsetup(self):
        """
        Setup the TTree with the given name and title and the given nametypes.
        """
        
        self.FERSsetup = ROOT.TTree("FERSsetup", "TTree with run FERS setup settings")    # Define the TTree
        # Create branches
        for item in self.FERSsetup_nametypes:
            if str(type(item[1])).find('std.vector') != -1:
                obj = (self.FERSsetup).Branch(item[0], item[1])
            else:
                obj = (self.FERSsetup).Branch(item[0], item[1], item[2])
        # Check if all the requested branch names have been used, or rather some
        # branch names were sanified due to incompatibility with ROOT nomenclature
        # e.g. like 'myvar.' which is not allowed
        # Get list of branch names
        branchNames = [branch.GetName() for branch in (self.FERSsetup).GetListOfBranches()]
        if branchNames != [ item[0] for item in self.FERSsetup_nametypes]:
            raise Exception("Some branch names were sanified due to incompatibility with ROOT nomenclature")
        # Set leaves description
        self.TREE_SetLeavesDescriptions(self.FERSsetup, self.FERSsetup_nametypes)
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
            (self.logging).critical("Tree 'data' is not initialized")
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
                (self.logging).critical("Problem here")
                exit(-1)
            for j in range(len(entry.run)):
                self.FERSsetup_vrunIDs.push_back(i)
                self.FERSsetup_vparName.push_back(entry.parName[j])
                self.FERSsetup_vparValue.push_back(entry.parValue[j])
                self.FERSsetup_vparDescr.push_back(entry.parDescr[j])
        # Fill the TTree
        self.FERSsetup_fill()
    

    ## FERS methods
    # Setup fuction for TTree FERS
    def setupTTree_FERS(self):
        """
        Setup the TTree with the given name and title and the given nametypes.
        """
        
        self.FERS = ROOT.TTree("FERS", "FERS processed data")    # Define the TTree
        # Create branches
        for item in self.FERS_nametypes:
            if str(type(item[1])).find('std.vector') != -1:
                obj = (self.FERS).Branch(item[0], item[1])
            else:
                obj = (self.FERS).Branch(item[0], item[1], item[2])
        # Check if all the requested branch names have been used, or rather some
        # branch names were sanified due to incompatibility with ROOT nomenclature
        # e.g. like 'myvar.' which is not allowed
        # Get list of branch names
        branchNames = [branch.GetName() for branch in (self.FERS).GetListOfBranches()]
        if branchNames != [ item[0] for item in self.FERS_nametypes]:
            raise Exception("Some branch names were sanified due to incompatibility with ROOT nomenclature")
        # Set leaves description
        self.TREE_SetLeavesDescriptions(self.FERS, self.FERS_nametypes)
    # Fill tree with data
    def FERS_fill(self, **kwargs):
        if (self.FERS) is None:
            raise Exception("Tree 'data' is not initialized")
        for branch in self.FERS_nametypes:
            try:
                # Filling is based on length. If the length of the array is 1 then fill the content of the array
                # otherwise fill the array itself
                if len(branch[1]) == 1:
                    branch[1][0] = kwargs[branch[0]]
                else:
                    np.copyto(branch[1], kwargs[branch[0]])
            except KeyError:
                if not self.FERS_fill_warnings[branch[0]]:
                    (self.logging).warning(f"Leaf {branch[0]} not found in kwargs (further warnings suppressed)")
                    self.FERS_fill_warnings[branch[0]] = True
        # Fill the tree
        (self.FERS).Fill()
    # Get entry i-th of the FERS TTree (for read mode)
    def FERS_getEntry(self, i):
        """
        Description 
        
        Parameters
        ----------
            i (int): Entry number 

        Returns:
            run : 0
            runTime : 1
            event : 2
            timestamp : 3
            fers_evt : 4
            fers_trgtime : 5
            fers_ch0 : 6
            fers_ch1 : 7
            strip0 : 8
            strip1 : 9
            lg0 : 10
            hg0 : 11
            lg1 : 12
            hg1 : 13
            clg0 : 14
            chg0 : 15
            clg1 : 16
            chg1 : 17
            time : 18
        """

        (self.FERS).GetEntry(i)
        return [entry[1][0] for entry in self.FERS_nametypes]
    

    

    ## Utilities
    # Set description (better readibility)
    def TREE_SetLeavesDescriptions(self, tree, tree_nametypes):
        # If a branch name is not compatible with ROOT name conventions, the
        # name is first sanified and then a branch with that name is created.
        # For example 'myname2.' cannot exist
        # A naive comparison like 
        # for entry in tree_nametypes:
        #     tree.GetBranch(entry[0]).SetTitle(entry[3])
        # would fail since the GetBranch for 'myname2.' would return nullpointer

        # WARNING: using GetLeaf works but it produces a bug in the generated ROOT output
        # file such that the Data is not displayed when using sca. With the traditional TBrowser
        # it won't work either while with the web ROOT interface it works.

        for entry in tree_nametypes:
                try:
                    branch = tree.GetBranch(entry[0])
                    branch.SetTitle(entry[3])
                except ReferenceError:
                    (self.logging).error(f"Branch {entry[0]} not found. This is nullptr")
    # Bind branches of the DT5730 to variables
    def bindBranches(self, tree, nametypes):
        """
        Bind branches of the a TTree to internal variables of the class 
        """
        for item in nametypes:
            tree.SetBranchAddress(item[0], item[1])
    # Write all the content of the output root file and clear datastructures for the next one
    def closeROOT(self):
        if self.mode != "READ":
            (self.FERSsetup).Write()
            (self.FERS).Write()
        # Single file
        if type(self.ROOTfilename) is not list:
            (self.ROOTfile).Close()
            del self.ROOTfile

    ######################################################
    ######################################################
######################################################
######################################################
######################################################
class rdataStruct_SYNCH():
    # rdataStruct_SYNCH logger
    logging = create_logger("rdataStruct_SYNCH")
    
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
            (self.logging).critical("Tree 'data' is not initialized")
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
                (self.logging).critical("Problem here")
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
    # todo: set bind branch addresses
    
    
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
    FERS_dtime = np.array([0], dtype=np.double)
    FERS_ilag = np.array([0], dtype=np.int32) # 30/7/23 00:13 lag value
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
        ("hg",          FERS_dhg,           "hg/D",             "Calibrated HG charge [pC]"),
        ("time",        FERS_dtime,         "time/D",           "Event posix digitizer timestamp"),
        ("lag",         FERS_ilag,          "lag/I",            "Offset in trigger units between DT5730 and FERS datapoint")
    ]
    ## Functions
    # Bind branches of the DT5730 to variables
    def FERS_bindBranches(self, tree):
        for item in self.FERS_nametypes:
            tree.SetBranchAddress(item[0], item[1])
    # Fill tree with data
    def FERS_fill(self, run, runTime, event, timestamp, fers_evt, fers_trgtime, fers_board, fers_ch, fers_lg, fers_hg, det, strip, lg, hg, time, lag):
        if (self.FERS) is None:
            (self.logging).critical("Tree 'data' is not initialized")
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
        self.FERS_dtime[0] = time
        self.FERS_ilag[0] = lag
        # Fill the tree
        (self.FERS).Fill()
    # Get entry i-th of the FERS TTree (for read mode)
    def FERS_getEntry(self, i) -> tuple:
        """
        Description 
        
        Parameters
        ----------
            i (int): Entry number 

        Returns: (tuple)
            FERS_irun : 0
            FERS_drunTime : 1
            FERS_ievent : 2
            FERS_dtimestamp : 3
            FERS_ifers_evt : 4
            FERS_dfers_trgtime : 5
            FERS_ifers_board : 6
            FERS_ifers_ch : 7 
            FERS_ifers_lg : 8
            FERS_ifers_hg : 9
            FERS_idet : 10
            FERS_istrip : 11 
            FERS_dlg : 12
            FERS_dhg : 13
            FERS_dtime : 14
            FERS_ilag : 15
        """
        (self.FERS).GetEntry(i)
        return ((self.FERS_irun)[0], (self.FERS_drunTime)[0], (self.FERS_ievent)[0], (self.FERS_dtimestamp)[0], (self.FERS_ifers_evt)[0], (self.FERS_dfers_trgtime)[0], (self.FERS_ifers_board)[0], (self.FERS_ifers_ch)[0], (self.FERS_ifers_lg)[0], (self.FERS_ifers_hg)[0], (self.FERS_idet)[0], (self.FERS_istrip)[0], (self.FERS_dlg)[0], (self.FERS_dhg)[0], (self.FERS_dtime)[0], (self.FERS_ilag)[0])
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
            tree.GetBranch(entry[0]).SetTitle(entry[3])

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
        if mode == "RECREATE" and type(setVars) is dict:
            self.fileFirstRunTime = setVars["fileRunTime"]
            self.fileRunID = setVars["fileRunID"]
            if self.fileRunID < 0:
                (self.logging).error("Provided runID is negative.")
                (self.logging).warning("runID defaulting to 0")
                self.fileRunID = 0
        elif mode == "RECREATE" and setVars==None:
            if ((self.logging).level==10): (self.logging).warning(f"ROOT file is in {mode} and setVars provided are {setVars}")
        
        # Open ROOT output file
        self.ROOTfile = ROOT.TFile.Open(fname, mode)
        (self.logging).debug(f"Opening {fname} in {mode} mode")
        if mode == "RECREATE":
            (self.logging).debug("Attaching branches to variables.")
            # Generate the FERSsetup TTree
            self.setupTTree_FERSsetup()
            # Generate the FERS TTree
            self.setupTTree_FERS()
        else:
            # FERSSetup
            self.FERSsetup = self.ROOTfile.FERSsetup
            ## todo Set branch addresses    
            # FERS
            self.FERS = self.ROOTfile.FERS
            # Set branch addresses
            self.FERS_bindBranches(self.FERS)
######################################################
######################################################
######################################################
class rdataStruct_MERGE():
    # rdataStruct_MERGE logger
    logging = create_logger("rdataStruct_MERGE")


    def __init__(self, fname, mode="RECREATE", setVars = None):
        ## Internal
        # mode state
        self.mode = mode
        # filename
        self.ROOTfilename = fname

        ######################################################
        ################
        ### TTree: FERS   
        ## Variable definitions
        self.FERS_irun = np.array([0], dtype=np.uint32)
        self.FERS_drunTime = np.array([0], dtype=np.double)
        self.FERS_ievent = np.array([0], dtype=np.uint32)
        self.FERS_vtimestamp = np.array([0,0], dtype=np.double)
        self.FERS_vfers_evt = np.array([0,0], dtype=np.uint32)
        self.FERS_vfers_trgtime = np.array([0,0], dtype=np.double)
        self.FERS_vfers_ch0 = np.zeros(64, dtype=np.uint32)         # vector
        self.FERS_vfers_ch1 = np.zeros(64, dtype=np.uint32)         # vector
        self.FERS_vstrip0 = np.zeros(64, dtype=np.uint32)           # vector
        self.FERS_vstrip1 = np.zeros(64, dtype=np.uint32)           # vector
        self.FERS_vlg0 = np.zeros(64, dtype=np.int32)               # vector
        self.FERS_vhg0 = np.zeros(64, dtype=np.int32)               # vector
        self.FERS_vlg1 = np.zeros(64, dtype=np.int32)               # vector
        self.FERS_vhg1 = np.zeros(64, dtype=np.int32)               # vector
        self.FERS_vclg0 = np.zeros(64, dtype=np.double)             # vector
        self.FERS_vchg0 = np.zeros(64, dtype=np.double)             # vector
        self.FERS_vclg1 = np.zeros(64, dtype=np.double)             # vector
        self.FERS_vchg1 = np.zeros(64, dtype=np.double)             # vector
        self.FERS_dtime = np.array([0], dtype=np.double)
        self.FERS_ilag = np.array([0], dtype=np.int32)              # 30/7/23 00:13 lag value
        #
        self.FERS_nametypes = [
            ("run",         self.FERS_irun,          "run/i",            "Run id number"),
            ("runTime",     self.FERS_drunTime,      "runTime/D",        "Posix time of the run start on the PC"),
            ("event",       self.FERS_ievent,        "event/i",          "Event id number"),
            ("timestamp",   self.FERS_vtimestamp,    "timestamp[2]/D",   "Event posix timestamp (absolute)"),
            ("fers_evt",    self.FERS_vfers_evt,     "fers_evt[2]/i",    "FERS event ID [0-1000]"),
            ("fers_trgtime",self.FERS_vfers_trgtime, "fers_trgtime[2]/D","FERS trigger time from run start [us]"),
            ("fers_ch0",    self.FERS_vfers_ch0,     "fers_ch0[64]/i",   "FERS ch det0 [uint32]"),
            ("fers_ch1",    self.FERS_vfers_ch1,     "fers_ch1[64]/i",   "FERS ch det1 [uint32]"),
            ("strip0",      self.FERS_vstrip0,       "strip0[64]/i",     "Strip ID det0 [uint32]"),
            ("strip1",      self.FERS_vstrip1,       "strip1[64]/i",     "Strip ID det1 [uint32]"),
            ("lg0",         self.FERS_vlg0,          "lg0[64]/I",        "FERS low-gain (signed) ADC det0 [int32]"),
            ("hg0",         self.FERS_vhg0,          "hg0[64]/I",        "FERS high-gain (signed) ADC det0 [int32]"),
            ("lg1",         self.FERS_vlg1,          "lg1[64]/I",        "FERS low-gain (signed) ADC det1 [int32]"),
            ("hg1",         self.FERS_vhg1,          "hg1[64]/I",        "FERS high-gain (signed) ADC det1 [int32]"),
            ("clg0",        self.FERS_vclg0,         "clg0[64]/D",       "Calibrated FERS LG charge det0 [pC]"),
            ("chg0",        self.FERS_vchg0,         "chg0[64]/D",       "Calibrated FERS HG charge det0 [pC]"),
            ("clg1",        self.FERS_vclg1,         "clg1[64]/D",       "Calibrated FERS LG charge det1 [pC]"),
            ("chg1",        self.FERS_vchg1,         "chg1[64]/D",       "Calibrated FERS HG charge det1 [pC]"),
            ("time",        self.FERS_dtime,         "time/D",           "Event posix digitizer timestamp"),
            ("lag",         self.FERS_ilag,          "lag/I",            "Offset in trigger units between DT5730 and FERS datapoint")
        ]
        ################
        ### TTree: DT5730   
        ## Variable definitions
        self.DT5730_irun = np.array([0], dtype=np.uint32)
        self.DT5730_drunTime = np.array([0], dtype=np.double)
        self.DT5730_ievent = np.array([0], dtype=np.uint32)
        self.DT5730_dtimestamp = np.array([0], dtype=np.double)
        self.DT5730_idgt_evt = np.array([0], dtype=np.uint32)
        self.DT5730_idgt_trgtime = np.array([0], dtype=np.uint64)
        self.DT5730_idgt_evtsize = np.array([0], dtype=np.uint32)
        self.DT5730_favg = np.array([0], dtype=np.double)
        self.DT5730_fstd = np.array([0], dtype=np.double)
        self.DT5730_iptNb = np.array([0], dtype=np.uint32)
        self.DT5730_favgV = np.array([0], dtype=np.double)
        self.DT5730_fstdV = np.array([0], dtype=np.double)
        self.DT5730_favgQ = np.array([0], dtype=np.double)
        self.DT5730_ftrgtime = np.array([0], dtype=np.double)
        self.DT5730_nametypes = [
            ("run",         self.DT5730_irun,          "run/i",           "Run id number"),
            ("runTime",     self.DT5730_drunTime,      "runTime/D",       "Posix time of the run start on the PC"),
            ("event",       self.DT5730_ievent,        "event/i",         "Event id number"),
            ("timestamp",   self.DT5730_dtimestamp,    "timestamp/D",     "Event posix timestamp (absolute)"),
            ("dgt_evt",     self.DT5730_idgt_evt,      "dgt_evt/i",       "Dgt event counter"),
            ("dgt_trgtime", self.DT5730_idgt_trgtime,  "dgt_trgtime/l",   "Dgt trg counter [32-bit counter, 8ns res., 17.179s range]"),
            ("dgt_evtsize", self.DT5730_idgt_evtsize,  "dgt_evtsize/i",   "Number of samples in the waveform [1sample=2ns]"),
            ("avg",         self.DT5730_favg,          "avg/D",           "Average ADC value in window (-5000:-1) [0-16383]"),
            ("std",         self.DT5730_fstd,          "std/D",           "Standard deviation ADC values [0-16383]"),
            ("ptNb",        self.DT5730_iptNb,         "ptNb/i",          "Number of points in the avgGatingwindow [#]"),
            ("avgV",        self.DT5730_favgV,         "avgV/D",          "Average voltage in the window [V]"),
            ("stdV",        self.DT5730_fstdV,         "stdV/D",          "Standard deviation in the window [V]"),
            ("avgQ",        self.DT5730_favgQ,         "avgQ/D",          "Average cal. charge in the window [nC]"),
            ("trgtime",     self.DT5730_ftrgtime,      "trgtime/D",       "Dgt trg counter converted in time using runTime as T0 start")
        ]
        ################
        ### TTree: A1561HDP  
        ## Variable definitions   
        self.A1561HDP_irun = np.array([0], dtype=np.uint32)
        self.A1561HDP_ievent = np.array([0], dtype=np.uint32)
        self.A1561HDP_dtimestamp = np.array([0], dtype=np.double)
        self.A1561HDP_bs0 = np.array([False], dtype=np.bool_)
        self.A1561HDP_dc0V = np.array([0], dtype=np.double)
        self.A1561HDP_dc0I = np.array([0], dtype=np.double)
        self.A1561HDP_bs1 = np.array([False], dtype=np.bool_)
        self.A1561HDP_dc1V = np.array([0], dtype=np.double)
        self.A1561HDP_dc1I = np.array([0], dtype=np.double)
        self.A1561HDP_bkill = np.array([False], dtype=np.bool_)
        self.A1561HDP_nametypes = [
            ("run",         self.A1561HDP_irun,          "run/i",            "Run id number"),
            ("event",       self.A1561HDP_ievent,        "event/i",          "Event id number"),
            ("timestamp",   self.A1561HDP_dtimestamp,    "timestamp/D",      "Event posix timestamp (absolute)"),
            ("s0",          self.A1561HDP_bs0,           "s0/O",             "Channel 0 status [on/off]"),
            ("c0V",         self.A1561HDP_dc0V,          "c0V/D",            "Channel 0 voltage [V]"),
            ("c0I",         self.A1561HDP_dc0I,          "c0I/D",            "Channel 0 current [uA]"),
            ("s1",          self.A1561HDP_bs1,           "s1/O",             "Channel 1 status [on/off]"),
            ("c1V",         self.A1561HDP_dc1V,          "c1V/D",            "Channel 1 voltage [V]"),
            ("c1I",         self.A1561HDP_dc1I,          "c1I/D",            "Channel 1 current [uA]"),
            ("kill",        self.A1561HDP_bkill,         "kill/O",           "Interrupt CTRL+C pressed in this run")
        ]
        ################
        ### TTree: BASLER   
        ## Variable definitions
        self.BASLER_dtimestamp = np.array([0], dtype=np.double)
        self.BASLER_dgain = np.array([0], dtype=np.double)
        self.BASLER_dexposure = np.array([0], dtype=np.double)
        self.BASLER_dpx_num_hor = np.array([0], dtype=np.double)
        self.BASLER_dprofile_mean_hor = np.array([0], dtype=np.double)
        self.BASLER_dmean_se_hor = np.array([0], dtype=np.double)
        self.BASLER_dprofile_sigma_hor = np.array([0], dtype=np.double)
        self.BASLER_dsigma_se_hor = np.array([0], dtype=np.double)
        self.BASLER_dprofile_amp_hor = np.array([0], dtype=np.double)
        self.BASLER_damp_se_hor = np.array([0], dtype=np.double)
        self.BASLER_dchi_sqr_hor = np.array([0], dtype=np.double)
        self.BASLER_dr_sqr_hor = np.array([0], dtype=np.double)
        self.BASLER_bgood_hor_fit_flag = np.array([False], dtype=np.bool_)
        self.BASLER_dpx_num_ver = np.array([0], dtype=np.double)
        self.BASLER_dprofile_mean_ver = np.array([0], dtype=np.double)
        self.BASLER_dmean_se_ver = np.array([0], dtype=np.double)
        self.BASLER_dprofile_sigma_ver = np.array([0], dtype=np.double)
        self.BASLER_dsigma_se_ver = np.array([0], dtype=np.double)
        self.BASLER_dprofile_amp_ver = np.array([0], dtype=np.double)
        self.BASLER_damp_se_ver = np.array([0], dtype=np.double)
        self.BASLER_dchi_sqr_ver = np.array([0], dtype=np.double)
        self.BASLER_dr_sqr_ver = np.array([0], dtype=np.double)
        self.BASLER_bgood_ver_fit_flag = np.array([False], dtype=np.bool_)
        self.BASLER_time = np.array([0], dtype=np.double)
        #
        self.BASLER_nametypes = [
            ("timestamp",            self.BASLER_dtimestamp,             "timestamp/D",              "desc"),
            ("gain",                 self.BASLER_dgain,                  "gain/D",                   "desc"),
            ("exposure",             self.BASLER_dexposure,              "exposure/D",               "desc"),
            ("px_num_hor",           self.BASLER_dpx_num_hor,            "px_num_hor/D",             "desc"),
            ("profile_mean_hor",     self.BASLER_dprofile_mean_hor,      "profile_mean_hor/D",       "desc"),
            ("mean_se_hor",          self.BASLER_dmean_se_hor,           "mean_se_hor/D",            "desc"),
            ("profile_sigma_hor",    self.BASLER_dprofile_sigma_hor,     "profile_sigma_hor/D",      "desc"),
            ("sigma_se_hor",         self.BASLER_dsigma_se_hor,          "sigma_se_hor/D",           "desc"),
            ("profile_amp_hor",      self.BASLER_dprofile_amp_hor,       "profile_amp_hor/D",        "desc"),
            ("amp_se_hor",           self.BASLER_damp_se_hor,            "amp_se_hor/D",             "desc"),
            ("chi_sqr_hor",          self.BASLER_dchi_sqr_hor,           "chi_sqr_hor/D",            "desc"),
            ("r_sqr_hor",            self.BASLER_dr_sqr_hor,             "r_sqr_hor/D",              "desc"),
            ("good_hor_fit_flag",    self.BASLER_bgood_hor_fit_flag,     "good_hor_fit_flag/O",      "desc"),
            ("px_num_ver",           self.BASLER_dpx_num_ver,            "px_num_ver/D",             "desc"),
            ("profile_mean_ver",     self.BASLER_dprofile_mean_ver,      "profile_mean_ver/D",       "desc"),
            ("mean_se_ver",          self.BASLER_dmean_se_ver,           "mean_se_ver/D",            "desc"),
            ("profile_sigma_ver",    self.BASLER_dprofile_sigma_ver,     "profile_sigma_ver/D",      "desc"),
            ("sigma_se_ver",         self.BASLER_dsigma_se_ver,          "sigma_se_ver/D",           "desc"),
            ("profile_amp_ver",      self.BASLER_dprofile_amp_ver,       "profile_amp_ver/D",        "desc"),
            ("amp_se_ver",           self.BASLER_damp_se_ver,            "amp_se_ver/D",             "desc"),
            ("chi_sqr_ver",          self.BASLER_dchi_sqr_ver,           "chi_sqr_ver/D",            "desc"),
            ("r_sqr_ver",            self.BASLER_dr_sqr_ver,             "r_sqr_ver/D",              "desc"),
            ("good_ver_fit_flag",    self.BASLER_bgood_ver_fit_flag,     "good_ver_fit_flag/O",      "desc"),
            ("time",                 self.BASLER_time,                   "time/D",                   "Event posix digitizer timestamp")
        ]
        ################
        ### TTree: MERGE
        self.MERGE = None
        self.MERGE_nametypes = []           # dynamically filled by _createMERGE_nametypes
        self.MERGE_fill_warnings = {}       # dynamically filled by _createMERGE_nametypes
        self._createMERGE_nametypes()
        #
        # This entry in the MERGE TTree signal the amount of data overlap between the datasources 
        self.evtSync = np.array([0], dtype=np.uint32)
        evtSync = ("evtSync",   self.evtSync,   "evtSync/i",   "4-bit mask with status of the overlap (basler,a1561hdp,fers,dt5730)")
        self.MERGE_nametypes.append(evtSync)
        self.MERGE_fill_warnings[evtSync[0]] = False
        ######################################################
        
        # Get run id and filename
        if mode == "RECREATE" and type(setVars) is dict:
            self.fileFirstRunTime = setVars["fileRunTime"]
            self.fileRunID = setVars["fileRunID"]
            if self.fileRunID < 0:
                (self.logging).error("Provided runID is negative.")
                (self.logging).warning("runID defaulting to 0")
                self.fileRunID = 0
        elif mode == "RECREATE" and setVars==None:
            if ((self.logging).level==10): (self.logging).warning(f"ROOT file is in {mode} and setVars provided are {setVars}")
        
        # Open ROOT output file
        self.ROOTfile = ROOT.TFile.Open(fname, mode)
        (self.logging).debug(f"Opening {fname} in {mode} mode")
        if mode == "RECREATE":
            (self.logging).debug("Attaching branches to variables.")
            # Generate the MERGE TTree
            self.setupTTree_MERGE()
        else:
            # MERGE
            self.MERGE = self.ROOTfile.MERGE
            # Set branch addresses
            self.MERGE_bindBranches(self.MERGE)


    #def __del__(self):
    #    """"""
    #    #self.FERS_vlg.clear()
    #    #self.FERS_vhg.clear()
    #    #(self.logging).info("[rootconverter] Memory cleared")
    

    
    def _createArrayList(self):
        """
        Get from the MERGE_nametypes the list of arrays and put into the 
        self._arrayList list.
        """
        pass

    def _clearArrays(self):
        pass
  
    # Dynamically create the nametypes for the MERGE TTree.
    def _createMERGE_nametypes(self):
        """
        Dynamically create the nametypes for the MERGE TTree.
        The nametypes are created by merging the nametypes of the three TTree
        (FERS, DT5730, A1561HDP, BASLER) and prepending the name of the source TTree
        to the name of the variable.
        """
        mergeItems = { 'dt5730': self.DT5730_nametypes, 'fers': self.FERS_nametypes, 'a1561hdp': self.A1561HDP_nametypes, 'basler': self.BASLER_nametypes }
        for source in mergeItems:
            for item in mergeItems[source]:
                nitem = list(item)
                nitem[0] = f"{source}_" + nitem[0]
                nitem[2] = f"{source}_" + nitem[2]
                nitem[3] = f"({source}) " + nitem[3]
                (self.MERGE_nametypes).append(nitem)
                self.MERGE_fill_warnings[nitem[0]] = False

    # Bind branches of the DT5730 to variables
    def MERGE_bindBranches(self, tree):
        """
        Bind branches of the MERGE TTree to internal variables of the class 
        """
        for item in self.FERS_nametypes:
            tree.SetBranchAddress(item[0], item[1])


    # Fill tree with data
    def MERGE_fill(self, **kwargs):
        if (self.MERGE) is None:
            raise Exception("Tree 'data' is not initialized")
        for branch in self.MERGE_nametypes:
            try:
                # Filling is based on length. If the length of the array is 1 then fill the content of the arrya
                # otherwise fill the array itself
                if len(branch[1]) == 1:
                    branch[1][0] = kwargs[branch[0]]
                else:
                    np.copyto(branch[1], kwargs[branch[0]])
            except KeyError:
                if not self.MERGE_fill_warnings[branch[0]]:
                    (self.logging).warning(f"Leaf {branch[0]} not found in kwargs (further warnings suppressed)")
                    self.MERGE_fill_warnings[branch[0]] = True
        # Fill the tree
        (self.MERGE).Fill()


    
    # Get entry i-th of the FERS TTree (for read mode)
    def MERGE_getEntry(self, i):
        """
        Description 
        
        Parameters
        ----------
            i (int): Entry number 

        Returns:
        
fers_run
fers_runTime
fers_event
fers_timestamp
fers_fers_evt
fers_fers_trgtime
fers_fers_ch0
fers_fers_ch1
fers_strip0
fers_strip1
fers_lg0
fers_hg0
fers_lg1
fers_hg1
fers_clg0
fers_chg0
fers_clg1
fers_chg1
fers_time
fers_lag

dt5730_run
dt5730_runTime
dt5730_event
dt5730_timestamp
dt5730_dgt_evt
dt5730_dgt_trgtime
dt5730_dgt_evtsize
dt5730_avg
dt5730_std
dt5730_ptNb
dt5730_avgV
dt5730_stdV
dt5730_avgQ
dt5730_trgtime

a1561hdp_run
a1561hdp_event
a1561hdp_timestamp
a1561hdp_s0
a1561hdp_c0V
a1561hdp_c0I
a1561hdp_s1
a1561hdp_c1V
a1561hdp_c1I
a1561hdp_kill

            fers_run : 0
            fers_runTime : 1
            fers_event : 2
            fers_timestamp : 3
            fers_fers_evt : 4
            fers_fers_trgtime : 5
            fers_strip : 11
            fers_lg : 12
            fers_hg : 13
            fers_time : 14
            fers_vlg : 15
            fers_vhg : 16
            
            fers_vclg : 15
            fers_vchg : 16
            
            fers_vstrip : 17
            fers_vch : 18
            dt5730_run : 18
            dt5730_runTime : 19
            dt5730_event : 20
            dt5730_timestamp : 21
            dt5730_dgt_evt : 22
            dt5730_dgt_trgtime : 23
            dt5730_dgt_evtsize : 24
            dt5730_avg : 25
            dt5730_std : 26
            dt5730_ptNb : 27
            dt5730_avgV : 28
            dt5730_stdV : 29
            dt5730_avgQ : 30
            dt5730_trgtime : 31
            a1561hdp_run : 32
            a1561hdp_event : 33
            a1561hdp_timestamp : 34
            a1561hdp_s0 : 35
            a1561hdp_c0V : 36
            a1561hdp_c0I : 37
            a1561hdp_s1 : 38
            a1561hdp_c1V : 39
            a1561hdp_c1I : 40
            a1561hdp_kill : 41
        """

        (self.MERGE).GetEntry(i)
        return [entry[1][0] for entry in self.MERGE_nametypes]
    
    # Setup the MERGE TTree
    def setupTTree_MERGE(self):
        # Define the TTree
        self.MERGE = ROOT.TTree("MERGE", "Merged synchronized data")
        # Create branches
        for item in (self.MERGE_nametypes):
            if str(type(item[1])).find('std.vector') != -1:
                obj = (self.MERGE).Branch(item[0], item[1])
            else:
                obj = (self.MERGE).Branch(item[0], item[1], item[2])
        # Check if all the requested branch names have been used, or rather some
        # branch names were sanified due to incompatibility with ROOT nomenclature
        # e.g. like 'myvar.' which is not allowed
        # Get list of branch names
        branchNames = [branch.GetName() for branch in self.MERGE.GetListOfBranches()]
        if branchNames != [ item[0] for item in self.MERGE_nametypes]:
            raise Exception("Some branch names were sanified due to incompatibility with ROOT nomenclature")
        # Set leaves description
        self.TREE_SetLeavesDescriptions(self.MERGE, self.MERGE_nametypes)


    ## Utilities
    # Set description (better readibility)
    def TREE_SetLeavesDescriptions(self, tree, tree_nametypes):
        # If a branch name is not compatible with ROOT name conventions, the
        # name is first sanified and then a branch with that name is created.
        # For example 'myname2.' cannot exist
        # A naive comparison like 
        # for entry in tree_nametypes:
        #     tree.GetBranch(entry[0]).SetTitle(entry[3])
        # would fail since the GetBranch for 'myname2.' would return nullpointer

        # WARNING: using GetLeaf works but it produces a bug in the generated ROOT output
        # file such that the Data is not displayed when using sca. With the traditional TBrowser
        # it won't work either while with the web ROOT interface it works.

        for entry in tree_nametypes:
                try:
                    branch = tree.GetBranch(entry[0])
                    branch.SetTitle(entry[3])
                except ReferenceError:
                    (self.logging).error(f"Branch {entry[0]} not found. This is nullptr")


    # Write all the content of the output root file and clear datastructures for the next one
    def closeROOT(self):
        if self.mode != "READ":
            (self.MERGE).Write()
            #(self.MERGE).ResetBranchAddresses()
        # Single file
        if type(self.ROOTfilename) is not list:
            (self.ROOTfile).Close()
            del self.ROOTfile

    ######################################################
    ######################################################

######################################################
######################################################
######################################################
class rdataStruct_BASLER():
    # rdataStructBASLER logger
    logging = create_logger("rdataStructBASLER")
    
    
    def __init__(self, fname, mode="RECREATE", setVars = None):
        ## Internal
        # mode state
        self.mode = mode
        # filename
        self.ROOTfilename = fname

        ######################################################
        ################
        ### TTree: BASLER   
        ## Variable definitions
        self.BASLER = None
        self.BASLER_dtimestamp = np.array([0], dtype=np.double)
        self.BASLER_dgain = np.array([0], dtype=np.double)
        self.BASLER_dexposure = np.array([0], dtype=np.double)
        self.BASLER_dpx_num_hor = np.array([0], dtype=np.double)
        self.BASLER_dprofile_mean_hor = np.array([0], dtype=np.double)
        self.BASLER_dmean_se_hor = np.array([0], dtype=np.double)
        self.BASLER_dprofile_sigma_hor = np.array([0], dtype=np.double)
        self.BASLER_dsigma_se_hor = np.array([0], dtype=np.double)
        self.BASLER_dprofile_amp_hor = np.array([0], dtype=np.double)
        self.BASLER_damp_se_hor = np.array([0], dtype=np.double)
        self.BASLER_dchi_sqr_hor = np.array([0], dtype=np.double)
        self.BASLER_dr_sqr_hor = np.array([0], dtype=np.double)
        self.BASLER_bgood_hor_fit_flag = np.array([False], dtype=np.bool_)
        self.BASLER_dpx_num_ver = np.array([0], dtype=np.double)
        self.BASLER_dprofile_mean_ver = np.array([0], dtype=np.double)
        self.BASLER_dmean_se_ver = np.array([0], dtype=np.double)
        self.BASLER_dprofile_sigma_ver = np.array([0], dtype=np.double)
        self.BASLER_dsigma_se_ver = np.array([0], dtype=np.double)
        self.BASLER_dprofile_amp_ver = np.array([0], dtype=np.double)
        self.BASLER_damp_se_ver = np.array([0], dtype=np.double)
        self.BASLER_dchi_sqr_ver = np.array([0], dtype=np.double)
        self.BASLER_dr_sqr_ver = np.array([0], dtype=np.double)
        self.BASLER_bgood_ver_fit_flag = np.array([False], dtype=np.bool_)
        self.BASLER_time = np.array([0], dtype=np.double)
        #
        self.BASLER_nametypes = [
            ["timestamp",            self.BASLER_dtimestamp,             "timestamp/D",              "desc"],
            ["gain",                 self.BASLER_dgain,                  "gain/D",                   "desc"],
            ["exposure",             self.BASLER_dexposure,              "exposure/D",               "desc"],
            ["px_num_hor",           self.BASLER_dpx_num_hor,            "px_num_hor/D",             "desc"],
            ["profile_mean_hor",     self.BASLER_dprofile_mean_hor,      "profile_mean_hor/D",       "desc"],
            ["mean_se_hor",          self.BASLER_dmean_se_hor,           "mean_se_hor/D",            "desc"],
            ["profile_sigma_hor",    self.BASLER_dprofile_sigma_hor,     "profile_sigma_hor/D",      "desc"],
            ["sigma_se_hor",         self.BASLER_dsigma_se_hor,          "sigma_se_hor/D",           "desc"],
            ["profile_amp_hor",      self.BASLER_dprofile_amp_hor,       "profile_amp_hor/D",        "desc"],
            ["amp_se_hor",           self.BASLER_damp_se_hor,            "amp_se_hor/D",             "desc"],
            ["chi_sqr_hor",          self.BASLER_dchi_sqr_hor,           "chi_sqr_hor/D",            "desc"],
            ["r_sqr_hor",            self.BASLER_dr_sqr_hor,             "r_sqr_hor/D",              "desc"],
            ["good_hor_fit_flag",    self.BASLER_bgood_hor_fit_flag,     "good_hor_fit_flag/O",      "desc"],
            ["px_num_ver",           self.BASLER_dpx_num_ver,            "px_num_ver/D",             "desc"],
            ["profile_mean_ver",     self.BASLER_dprofile_mean_ver,      "profile_mean_ver/D",       "desc"],
            ["mean_se_ver",          self.BASLER_dmean_se_ver,           "mean_se_ver/D",            "desc"],
            ["profile_sigma_ver",    self.BASLER_dprofile_sigma_ver,     "profile_sigma_ver/D",      "desc"],
            ["sigma_se_ver",         self.BASLER_dsigma_se_ver,          "sigma_se_ver/D",           "desc"],
            ["profile_amp_ver",      self.BASLER_dprofile_amp_ver,       "profile_amp_ver/D",        "desc"],
            ["amp_se_ver",           self.BASLER_damp_se_ver,            "amp_se_ver/D",             "desc"],
            ["chi_sqr_ver",          self.BASLER_dchi_sqr_ver,           "chi_sqr_ver/D",            "desc"],
            ["r_sqr_ver",            self.BASLER_dr_sqr_ver,             "r_sqr_ver/D",              "desc"],
            ["good_ver_fit_flag",    self.BASLER_bgood_ver_fit_flag,     "good_ver_fit_flag/O",      "desc"],
            ["time",                 self.BASLER_time,                   "time/D",                   "Synchronized timestamp"]
        ]
        self.BASLER_fill_warnings = { item[0]:False for item in self.BASLER_nametypes}       # filled by the nametypes
        ######################################################
        
        # Get run id and filename
        if mode == "RECREATE" and type(setVars) is dict:
            self.fileFirstRunTime = setVars["fileRunTime"]
            self.fileRunID = setVars["fileRunID"]
            if self.fileRunID < 0:
                (self.logging).error("Provided runID is negative.")
                (self.logging).warning("runID defaulting to 0")
                self.fileRunID = 0
        elif mode == "RECREATE" and setVars==None:
            if ((self.logging).level==10): (self.logging).warning(f"ROOT file is in {mode} and setVars provided are {setVars}")
        
        # Open ROOT output file
        self.ROOTfile = ROOT.TFile.Open(fname, mode)
        (self.logging).debug(f"Opening {fname} in {mode} mode")
        if mode == "RECREATE":
            (self.logging).debug("Attaching branches to variables.")
            # Generate the MERGE TTree
            self.setupTTree_BASLER()
        else:
            # MERGE
            self.BASLER = self.ROOTfile.BASLER
            # Set branch addresses
            self.BASLER_bindBranches(self.BASLER)


    # Bind branches of the BASLER to variables
    def BASLER_bindBranches(self, tree):
        """
        Bind branches of the BASLER TTree to internal variables of the class 
        """
        for item in self.BASLER_nametypes:
            tree.SetBranchAddress(item[0], item[1])


    # Fill tree with data
    def BASLER_fill(self, **kwargs):
        if (self.BASLER) is None:
            raise Exception("Tree 'data' is not initialized")
        for branch in self.BASLER_nametypes:
            try:
                # Filling is based on length. If the length of the array is 1 then fill the content of the arrya
                # otherwise fill the array itself
                if len(branch[1]) == 1:
                    branch[1][0] = kwargs[branch[0]]
                else:
                    np.copyto(branch[1], kwargs[branch[0]])
            except KeyError:
                if not self.BASLER_fill_warnings[branch[0]]:
                    (self.logging).warning(f"Leaf {branch[0]} not found in kwargs (further warnings suppressed)")
                    self.BASLER_fill_warnings[branch[0]] = True
        # Fill the tree
        (self.BASLER).Fill()
    
    
    
    # Get entry i-th of the BASLER TTree (for read mode)
    def BASLER_getEntry(self, i):
        """
        Description 
        
        Parameters
        ----------
            i (int): Entry number 

        Returns:
        ----------
            timestamp : 0
            gain : 1
            exposure : 2
            px_num_hor : 3
            profile_mean_hor : 4
            mean_se_hor : 5
            profile_sigma_hor : 6
            sigma_se_hor : 7
            profile_amp_hor : 8
            amp_se_hor : 9
            chi_sqr_hor : 10
            r_sqr_hor : 11
            good_hor_fit_flag : 12
            px_num_ver : 13
            profile_mean_ver : 14
            mean_se_ver : 15
            profile_sigma_ver : 16
            sigma_se_ver : 17
            profile_amp_ver : 18
            amp_se_ver : 19
            chi_sqr_ver : 20
            r_sqr_ver : 21
            good_ver_fit_flag : 22
            time : 23
        """

        (self.MERGE).GetEntry(i)
        return [entry[1][0] for entry in self.MERGE_nametypes]
    
    # Setup the MERGE TTree
    def setupTTree_BASLER(self):
        # Define the TTree
        self.BASLER = ROOT.TTree("BASLER", "BASLER synchronized data with FERS timestamps")
        # Create branches
        for item in (self.BASLER_nametypes):
            if str(type(item[1])).find('std.vector') != -1:
                obj = (self.BASLER).Branch(item[0], item[1])
            else:
                obj = (self.BASLER).Branch(item[0], item[1], item[2])
        # Check if all the requested branch names have been used, or rather some
        # branch names were sanified due to incompatibility with ROOT nomenclature
        # e.g. like 'myvar.' which is not allowed
        # Get list of branch names
        branchNames = [branch.GetName() for branch in self.BASLER.GetListOfBranches()]
        if branchNames != [ item[0] for item in self.BASLER_nametypes]:
            raise Exception("Some branch names were sanified due to incompatibility with ROOT nomenclature")
        # Set leaves description
        self.TREE_SetLeavesDescriptions(self.BASLER, self.BASLER_nametypes)


    ## Utilities
    # Set description (better readibility)
    def TREE_SetLeavesDescriptions(self, tree, tree_nametypes):
        # If a branch name is not compatible with ROOT name conventions, the
        # name is first sanified and then a branch with that name is created.
        # For example 'myname2.' cannot exist
        # A naive comparison like 
        # for entry in tree_nametypes:
        #     tree.GetBranch(entry[0]).SetTitle(entry[3])
        # would fail since the GetBranch for 'myname2.' would return nullpointer

        # WARNING: using GetLeaf works but it produces a bug in the generated ROOT output
        # file such that the Data is not displayed when using sca. With the traditional TBrowser
        # it won't work either while with the web ROOT interface it works.

        for entry in tree_nametypes:
                try:
                    branch = tree.GetBranch(entry[0])
                    branch.SetTitle(entry[3])
                except ReferenceError:
                    (self.logging).error(f"Branch {entry[0]} not found. This is nullptr")


    # Write all the content of the output root file and clear datastructures for the next one
    def closeROOT(self):
        if self.mode != "READ":
            (self.BASLER).Write()
        # Single file
        if type(self.ROOTfilename) is not list:
            (self.ROOTfile).Close()
            del self.ROOTfile

    ######################################################
    ######################################################

######################################################
######################################################
######################################################
class rdataStruct_A1561HDP():
    # rdataStruct_A1561HDP logger
    logging = create_logger("rdataStruct_A1561HDP")
    
    def __init__(self, fname, mode="RECREATE"):
        ## Internal
        # mode state
        self.mode = mode
        # filename
        self.ROOTfilename = fname

        ######################################################
        ################
        ### TTree: A1561HDP  
        ## Variable definitions   
        self.A1561HDP = None
        self.A1561HDP_irun = np.array([0], dtype=np.uint32)
        self.A1561HDP_ievent = np.array([0], dtype=np.uint32)
        self.A1561HDP_dtimestamp = np.array([0], dtype=np.double)
        self.A1561HDP_bs0 = np.array([False], dtype=np.bool_)
        self.A1561HDP_dc0V = np.array([0], dtype=np.double)
        self.A1561HDP_dc0I = np.array([0], dtype=np.double)
        self.A1561HDP_bs1 = np.array([False], dtype=np.bool_)
        self.A1561HDP_dc1V = np.array([0], dtype=np.double)
        self.A1561HDP_dc1I = np.array([0], dtype=np.double)
        self.A1561HDP_bkill = np.array([False], dtype=np.bool_)
        self.A1561HDP_dfiletime = np.array([0], dtype=np.double)
        self.A1561HDP_dtime = np.array([-1], dtype=np.double)
        #
        self.A1561HDP_nametypes = [
            ("run",         self.A1561HDP_irun,          "run/i",            "Run id number"),
            ("event",       self.A1561HDP_ievent,        "event/i",          "Event id number"),
            ("timestamp",   self.A1561HDP_dtimestamp,    "timestamp/D",      "Event posix timestamp (absolute)"),
            ("filetime",    self.A1561HDP_dfiletime,     "filetime/D",       "Event timestamp generated from run start and file write time (absolute)"),
            ("s0",          self.A1561HDP_bs0,           "s0/O",             "Channel 0 status [on/off]"),
            ("c0V",         self.A1561HDP_dc0V,          "c0V/D",            "Channel 0 voltage [V]"),
            ("c0I",         self.A1561HDP_dc0I,          "c0I/D",            "Channel 0 current [uA]"),
            ("s1",          self.A1561HDP_bs1,           "s1/O",             "Channel 1 status [on/off]"),
            ("c1V",         self.A1561HDP_dc1V,          "c1V/D",            "Channel 1 voltage [V]"),
            ("c1I",         self.A1561HDP_dc1I,          "c1I/D",            "Channel 1 current [uA]"),
            ("kill",        self.A1561HDP_bkill,         "kill/O",           "Interrupt CTRL+C pressed in this run"),
            ("time",        self.A1561HDP_dtime,         "time/D",           "Event posix digitizer timestamp")
        ]
        self.A1561HDP_fill_warnings = { item[0]:False for item in self.A1561HDP_nametypes}       # filled by the nametypes
        ######################################################
        
        # Open ROOT output file
        self.ROOTfile = ROOT.TFile.Open(fname, mode)
        (self.logging).debug(f"Opening {fname} in {mode} mode")
        if mode == "RECREATE":
            (self.logging).debug("Attaching branches to variables.")
            # Generate the FERS TTree
            self.setupTTree_A1561HDP()
        else:
            # A1561HDP
            self.A1561HDP = self.ROOTfile.A1561HDP
            # Set branch addresses
            self.A1561HDP_bindBranches(self.A1561HDP)
    
    
    # Bind branches of the A1561HDP to variables
    def A1561HDP_bindBranches(self, tree):
        """
        Bind branches of the A1561HDP TTree to internal variables of the class 
        """
        for item in self.A1561HDP_nametypes:
            tree.SetBranchAddress(item[0], item[1])
    
    
    # Fill tree with data
    def A1561HDP_fill(self, **kwargs):
        if (self.A1561HDP) is None:
            raise Exception("Tree 'data' is not initialized")
        for branch in self.A1561HDP_nametypes:
            try:
                # Filling is based on length. If the length of the array is 1 then fill the content of the arrya
                # otherwise fill the array itself
                if len(branch[1]) == 1:
                    branch[1][0] = kwargs[branch[0]]
                else:
                    np.copyto(branch[1], kwargs[branch[0]])
            except KeyError:
                if not self.A1561HDP_fill_warnings[branch[0]]:
                    (self.logging).warning(f"Leaf {branch[0]} not found in kwargs (further warnings suppressed)")
                    self.A1561HDP_fill_warnings[branch[0]] = True
        # Fill the tree
        (self.A1561HDP).Fill()
    
    
    
    # Get entry i-th of the A1561HDP TTree (for read mode)
    def A1561HDP_getEntry(self, i):
        """
        Description 
        
        Parameters
        ----------
            i (int): Entry number 

        Returns:
        ----------
            run : 0
            event : 1
            timestamp : 2
            filetime : 3
            s0 : 4
            c0V : 5
            c0I : 6
            s1 : 7
            c1V : 8
            c1I : 9
            kill : 10
            time : 11
        """

        (self.A1561HDP).GetEntry(i)
        return [entry[1][0] for entry in self.A1561HDP_nametypes]
    

    # Setup the A1561HDP TTree
    def setupTTree_A1561HDP(self):
        # Define the TTree
        self.A1561HDP = ROOT.TTree("A1561HDP", "A1561HDP processed data")
        # Create branches
        for item in (self.A1561HDP_nametypes):
            if str(type(item[1])).find('std.vector') != -1:
                obj = (self.A1561HDP).Branch(item[0], item[1])
            else:
                obj = (self.A1561HDP).Branch(item[0], item[1], item[2])
        # Check if all the requested branch names have been used, or rather some
        # branch names were sanified due to incompatibility with ROOT nomenclature
        # e.g. like 'myvar.' which is not allowed
        # Get list of branch names
        branchNames = [branch.GetName() for branch in self.A1561HDP.GetListOfBranches()]
        if branchNames != [ item[0] for item in self.A1561HDP_nametypes]:
            raise Exception("Some branch names were sanified due to incompatibility with ROOT nomenclature")
        # Set leaves description
        self.TREE_SetLeavesDescriptions(self.A1561HDP, self.A1561HDP_nametypes)


    ## Utilities
    # Set description (better readibility)
    def TREE_SetLeavesDescriptions(self, tree, tree_nametypes):
        # If a branch name is not compatible with ROOT name conventions, the
        # name is first sanified and then a branch with that name is created.
        # For example 'myname2.' cannot exist
        # A naive comparison like 
        # for entry in tree_nametypes:
        #     tree.GetBranch(entry[0]).SetTitle(entry[3])
        # would fail since the GetBranch for 'myname2.' would return nullpointer

        # WARNING: using GetLeaf works but it produces a bug in the generated ROOT output
        # file such that the Data is not displayed when using sca. With the traditional TBrowser
        # it won't work either while with the web ROOT interface it works.

        for entry in tree_nametypes:
                try:
                    branch = tree.GetBranch(entry[0])
                    branch.SetTitle(entry[3])
                except ReferenceError:
                    (self.logging).error(f"Branch {entry[0]} not found. This is nullptr")


    # Write all the content of the output root file and clear datastructures for the next one
    def closeROOT(self):
        if self.mode != "READ":
            (self.A1561HDP).Write()
        # Single file
        if type(self.ROOTfilename) is not list:
            (self.ROOTfile).Close()
            del self.ROOTfile

    ######################################################
    ######################################################


######################################################
######################################################
######################################################
class rdataStruct_FERS_buddy():
    # rdataStruct_FERS logger
    logging = create_logger("rdataStructFERSbuddy")

    def __init__(self, fname, mode="RECREATE", setVars = None):
        ## Internal
        # mode state
        self.mode = mode
        # filename
        self.ROOTfilename = fname
    
        ######################################################
        ################
        ### TTree: FERS
        ## Variable definitions
        #self.FERS = None
        self.FERS_irun = np.array([0], dtype=np.uint32)
        self.FERS_dtimestamp = np.array([0], dtype=np.double)
        self.FERS_ifers_evt = np.array([0], dtype=np.uint32)
        self.FERS_idet = np.array([0], dtype=np.uint32)
        
        
        self.FERS_istripMask = np.array([-1], dtype=np.uint32)
        self.FERS_berrMask = np.array([0], dtype=np.bool_)
        
        self.FERS_if1_status = np.array([-1], dtype=np.uint32)
        self.FERS_df1_chisqr = np.array([-1], dtype=np.double)
        self.FERS_df1_sigAmp = np.array([-1], dtype=np.double)
        self.FERS_df1_sigMea = np.array([-1], dtype=np.double)
        self.FERS_df1_sigSig = np.array([-1], dtype=np.double)
        self.FERS_df1_bacCon = np.array([-1], dtype=np.double)

        self.FERS_nametypes = [
            ("run",             self.FERS_irun,         "run/i",            "Run id number"),
            ("timestamp",       self.FERS_dtimestamp,   "timestamp/D",      "Event posix timestamp (absolute)"),
            ("fers_evt",        self.FERS_ifers_evt,    "fers_evt/i",       "FERS event ID [0-1000]"),
            ("det",             self.FERS_idet,         "det/i",            "Detector ID [0,1]"),
            #
            ("stripMask",       self.FERS_istripMask,   "stripMask/i",      "Strip mask for the fit parameters EFO (even:0, full:1, odd:2)"),
            ("errMask",         self.FERS_berrMask,     "errMask/O",        "Error mask (0 for fit pars, 1 for uncertainties)"),
            #
            ("f1_status",       self.FERS_if1_status,   "f1_status/i",      "Fit m.1 (gaus+const). Status"),
            ("f1_chisqr",       self.FERS_df1_chisqr,   "f1_chisqr/D",      "Fit m.1 (gaus+const). Chi square"),
            ("f1_sigAmp",       self.FERS_df1_sigAmp,   "f1_sigAmp/D",      "Fit m.1 (gaus+const). Amplitude [pC]"),
            ("f1_sigMea",       self.FERS_df1_sigMea,   "f1_sigMea/D",      "Fit m.1 (gaus+const). Mean [strip]"),
            ("f1_sigSig",       self.FERS_df1_sigSig,   "f1_sigSig/D",      "Fit m.1 (gaus+const). Sigma [mm]"),
            ("f1_bacCon",       self.FERS_df1_bacCon,   "f1_bacCon/D",      "Fit m.1 (gaus+const). Bckg constant [pC]")

            #("fit2_SigAmpl",      FITResults_dfitSchemeB_SigAmpl,     "fB_SigAmpl/D",     "Fit par.s (gausSig+gaussBckg) - Signal Amplitude [pC]"),
            #("fit2_SigMean",      FITResults_dfitSchemeB_SigMean,     "fB_SigMean/D",     "Fit par.s (gausSig+gaussBckg) - Signal Mean [strip]"),
            #("fit2_SigSigma",     FITResults_dfitSchemeB_SigSigma,    "fB_SigSigma/D",    "Fit par.s (gausSig+gaussBckg) - Signal Sigma [mm]"),
            #("fit2_BacAmpl",      FITResults_dfitSchemeB_BacAmpl,     "fB_BacAmpl/D",     "Fit par.s (gausSig+gaussBckg) - Background Amplitude [pC]"),
            #("fit2_BacMean",      FITResults_dfitSchemeB_BacMean,     "fB_BacMean/D",     "Fit par.s (gausSig+gaussBckg) - Background Mean [strip]"),
            #("fit2_BacSigma",     FITResults_dfitSchemeB_BacSigma,    "fB_BacSigma/D",    "Fit par.s (gausSig+gaussBckg) - Background Sigma [mm]")
        ]
        ######################################################
    
        # Get run id and filename
        if mode == "RECREATE" and type(setVars) is dict:
            self.fileFirstRunTime = setVars["fileRunTime"]
            self.fileRunID = setVars["fileRunID"]
            if self.fileRunID < 0:
                (self.logging).error("Provided runID is negative.")
                (self.logging).warning("runID defaulting to 0")
                self.fileRunID = 0
        elif mode == "RECREATE" and setVars==None:
            if ((self.logging).level==10): (self.logging).warning(f"ROOT file is in {mode} and setVars provided are {setVars}")
        
        # Open ROOT output file
        self.ROOTfile = ROOT.TFile.Open(fname, mode)
        (self.logging).debug(f"Opening {fname} in {mode} mode")
        if mode == "RECREATE":
            (self.logging).debug("Attaching branches to variables.")
            ## Generate the FERSsetup TTree
            #self.setupTTree_FERSsetup()
            # Generate the FERS TTree
            self.setupTTree_FERS()
        else:
            ## FERSSetup
            #self.FERSsetup = self.ROOTfile.FERSsetup
            ## todo Set branch addresses    
            # FERS
            self.FERS = self.ROOTfile.FERS
            # Set branch addresses
            self.FERS_bindBranches(self.FERS)
    
    ## Functions
    # Bind branches of the DT5730 to variables
    def FERS_bindBranches(self, tree):
        for item in self.FERS_nametypes:
            tree.SetBranchAddress(item[0], item[1])
    # Fill tree with data
    def FERS_fill(self, run, timestamp, fers_evt, det, stripMask, errMask, f1_status, f1_chisqr, f1_sigAmp, f1_sigMea, f1_sigSig, f1_bacCon):
        if (self.FERS) is None:
            (self.logging).critical("Tree 'data' is not initialized")
            exit(0)
        self.FERS_irun[0] = run
        self.FERS_dtimestamp[0] = timestamp
        self.FERS_ifers_evt[0] = fers_evt
        self.FERS_idet[0] = det
        self.FERS_istripMask[0] = stripMask
        self.FERS_berrMask[0] = errMask
        self.FERS_if1_status[0] = f1_status
        self.FERS_df1_chisqr[0] = f1_chisqr
        self.FERS_df1_sigAmp[0] = f1_sigAmp
        self.FERS_df1_sigMea[0] = f1_sigMea
        self.FERS_df1_sigSig[0] = f1_sigSig
        self.FERS_df1_bacCon[0] = f1_bacCon
        # Fill the tree
        (self.FERS).Fill()
    # Get entry i-th of the FERS TTree (for read mode)
    def FERS_getEntry(self, i):
        """
        Description 
        
        Parameters
        ----------
            i (int): Entry number 

        Returns:            
            FERS_irun : 0
            FERS_dtimestamp : 1
            FERS_ifers_evt : 2
            FERS_idet : 3
            FERS_istripMask : 4
            FERS_berrMask : 5
            FERS_if1_status : 6
            FERS_df1_chisqr : 7
            FERS_df1_sigAmp : 8
            FERS_df1_sigMea : 9
            FERS_df1_sigSig : 10
            FERS_df1_bacCon : 11            
        """
        (self.FERS).GetEntry(i)
        return [(self.FERS_irun)[0], (self.FERS_dtimestamp)[0], (self.FERS_ifers_evt)[0], (self.FERS_idet)[0], (self.FERS_istripMask)[0], (self.FERS_berrMask)[0], (self.FERS_if1_status)[0], (self.FERS_df1_chisqr)[0], (self.FERS_df1_sigAmp)[0], (self.FERS_df1_sigMea)[0], (self.FERS_df1_sigSig)[0], (self.FERS_df1_bacCon)[0]]
    # Setup the FERS TTree
    def setupTTree_FERS(self):
        # Define the TTree
        self.FERS = ROOT.TTree("FERS_ana", "FERS analysis data")
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
            tree.GetBranch(entry[0]).SetTitle(entry[3])

    # Write all the content of the output root file and clear datastructures for the next one
    def closeROOT(self):
        if self.mode != "READ":
            (self.FERS).Write()
        # Single file
        if type(self.ROOTfilename) is not list:
            (self.ROOTfile).Close()



######################################################
######################################################
######################################################

# Test methods
if __name__ == "__main__":
    # rdataStruct_FERS logger
    logging = create_logger("test_rdataStruct", 10)
    
    
    ## Test the MERGE class
    #logging.info("Testing rdataStructMERGE class by generating a testMERGE.root in this dir...")
    #roFile = rdataStruct_MERGE("testMERGE.root")
    #logging.info("Fill 1 without all kwargs")
    #roFile.MERGE_fill(fers_run = 0, fers_vlg = np.linspace(45,84,64, dtype=np.uint32))
    #logging.info("Fill 2 without all kwargs")
    #roFile.MERGE_fill(fers_run = 1, fers_vlg = np.linspace(99,163,64, dtype=np.uint32))
    #roFile.closeROOT()
    #logging.info("File closed.")
        
    ## Test the BASLER class
    #logging.info("Testing rdataStructBASLER class by generating a testBASLER.root in this dir...")
    #roFile = rdataStruct_BASLER("testBASLER.root")
    #logging.info("Fill 1 without all kwargs")
    #roFile.BASLER_fill(timestamp = 0)
    #logging.info("Fill 2 without all kwargs")
    #roFile.BASLER_fill(timestamp = 1)
    #roFile.closeROOT()
    #logging.info("File closed.")