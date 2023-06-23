import ROOT
from logger import *
import tqdm
import numpy as np

######################################################
######################################################
######################################################
class rdataStruct():
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
        self.FERS_dfers_trgtime = np.array([0], dtype=np.double)
        self.FERS_ifers_board = np.array([0], dtype=np.uint32)
        self.FERS_idet = np.array([0], dtype=np.uint32)
        self.FERS_vfers_ch0 = np.zeros(64, dtype=np.uint32)         # vector
        self.FERS_vfers_ch1 = np.zeros(64, dtype=np.uint32)         # vector
        self.FERS_vstrip0 = np.zeros(64, dtype=np.uint32)           # vector
        self.FERS_vstrip1 = np.zeros(64, dtype=np.uint32)           # vector
        self.FERS_vlg0 = np.zeros(64, dtype=np.int32)               # vector
        self.FERS_vhg0 = np.zeros(64, dtype=np.int32)               # vector
        self.FERS_vlg1 = np.zeros(64, dtype=np.int32)               # vector
        self.FERS_vhg1 = np.zeros(64, dtype=np.int32)               # vector
        self.FERS_dtime = np.array([0], dtype=np.double)
        #
        self.FERS_nametypes = [
            ["run",         self.FERS_irun,          "run/i",            "Run id number"],
            ["runTime",     self.FERS_drunTime,      "runTime/D",        "Posix time of the run start on the PC"],
            ["event",       self.FERS_ievent,        "event/i",          "Event id number"],
            ["timestamp",   self.FERS_dtimestamp,    "timestamp/D",      "Event posix timestamp (absolute)"],
            ["fers_evt",    self.FERS_ifers_evt,     "fers_evt/i",       "FERS event ID [0-1000]"],
            ["fers_trgtime",self.FERS_dfers_trgtime, "fers_trgtime/D",   "FERS trigger time from run start [us]"],
            ["fers_board",  self.FERS_ifers_board,   "fers_board/i",     "FERS board ID [0,1]"],
            ["det",         self.FERS_idet,          "det/i",            "Detector ID [0,1]"],
            ["fers_ch0",    self.FERS_vfers_ch0,     "fers_ch0[64]/i",   "FERS ch det0 [uint32]"],
            ["fers_ch1",    self.FERS_vfers_ch1,     "fers_ch1[64]/i",   "FERS ch det1 [uint32]"],
            ["strip0",      self.FERS_vstrip0,       "strip0[64]/i",     "Strip ID det0 [uint32]"],
            ["strip1",      self.FERS_vstrip1,       "strip1[64]/i",     "Strip ID det1 [uint32]"],
            ["lg0",         self.FERS_vlg0,          "lg0[64]/I",        "FERS low-gain (signed) ADC det0 [uint32]"],
            ["hg0",         self.FERS_vhg0,          "hg0[64]/I",        "FERS high-gain (signed) ADC det0 [uint32]"],
            ["lg1",         self.FERS_vlg1,          "lg1[64]/I",        "FERS low-gain (signed) ADC det1 [uint32]"],
            ["hg1",         self.FERS_vhg1,          "hg1[64]/I",        "FERS high-gain (signed) ADC det1 [uint32]"],
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
                logging.error("Provided runID is negative.")
                logging.warning("runID defaulting to 0")
                self.fileRunID = 0
        elif mode == "RECREATE" and setVars==None:
            logging.warning(f"ROOT file is in {mode} and setVars provided are {setVars}")
        

        # Open the given ROOT in read | write mode
        self.ROOTfile = ROOT.TFile.Open(fname, mode)
        logging.info(f"Opening {fname} in {mode} mode")
        
        if mode in ["NEW", "CREATE", "RECREATE", "UPDATE"]:
            logging.debug("Attaching branches to variables.")
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


    def __del__(self):
        #self.FERS_vlg.clear()
        #self.FERS_vhg.clear()
        if self.ROOTfile.IsOpen():
            self.ROOTfile.Close()
            del self.ROOTfile
        logging.info("[rootconverter] Memory cleared")
        
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
                # Filling is based on length. If the length of the array is 1 then fill the content of the arrya
                # otherwise fill the array itself
                if len(branch[1]) == 1:
                    branch[1][0] = kwargs[branch[0]]
                else:
                    np.copyto(branch[1], kwargs[branch[0]])
            except KeyError:
                if not self.FERS_fill_warnings[branch[0]]:
                    logging.warning(f"Leaf {branch[0]} not found in kwargs (further warnings suppressed)")
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
            fers_run : 0
            fers_runTime : 1
            fers_event : 2
            fers_timestamp : 3
            fers_fers_evt : 4
            fers_fers_trgtime : 5
            fers_fers_board : 6
            fers_det : 10
            fers_strip : 11
            fers_lg : 12
            fers_hg : 13
            fers_time : 14
            fers_vlg : 15
            fers_vhg : 16
            fers_vstrip : 17
            fers_vch : 18
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
                    logging.error(f"Branch {entry[0]} not found. This is nullptr")
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














if __name__ == "__main__":
    logging.info("Testing rdataStruct.py by generating a testMERGE.root in this dir...")
    roFile = rdataStruct("testMERGE.root")
    logging.info("Fill 1 without all kwargs")
    roFile.FERS_fill(fers_run = 0, lg0 = np.linspace(45,84,64, dtype=np.uint32))
    roFile.closeROOT()
    logging.info("File closed.")