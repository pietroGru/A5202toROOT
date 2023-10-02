from os.path import exists
import time
import glob
import pickle
import signal
from logger import *
from rootconverter import *
from datetime import datetime
import threading


##############################################################
######## globals #############################################
##############################################################
# Counter of the ROOT file number
runID = 0
# Counter for the cumulative number of events in this session
eventID = 0
# List of FERS data file processed to ROOT
procTXT = []
# Path of the list of FERS datafiles processed to ROOT so far (from disk)
daqStartTime = datetime.now()
rFilename = daqStartTime.strftime("%d%H%M%S_") + f"FERS_run{runID}.root"
#
procROOTList = "/home/pietro/work/CLEAR_March/FERS/TB4-192_FERS/runList.dat"
# List of ROOT files processed in this session
txtProcessedSession = []
# Path where FERS data files are located 
a5202dataDir = "/home/pietro/clearDaq/CLEAR_Vesper/FERS/data/nightly/"
a5202dataDir = "/home/pietro/work/CLEAR_March/FERS/TB4-192_FERS_analysis/processed_uncal/31mar23/outputfolder/"
# Path where output ROOT files are located
outputROOTdirectory = "/home/pietro/work/CLEAR_March/FERS/processed/nightly/"
outputROOTdirectory = "/home/pietro/work/CLEAR_March/FERS/TB4-192_FERS_analysis/processed_uncal/31mar23/outputfolder/"


exitCall = False                # Boolean signalling exit interrupt call
writingROOT = False             # ROOT writing status
dumpCacheRunStatus = False      # Cache dump status


##############################################################
######## Cache utilites ######################################
##############################################################
def checkCache(cache_fname: str):
    """
    Check the cache-file containing information about the list of already processed (converted to ROOT) FERS datafiles
    
    Parameters
    ----------
        cache_fname (str): Path of the cache file
        
    Returns:
    --------    
        runID (int): Run number of the last processed FERS datafile
        eventID (int): Event number of the last processed FERS datafile
        procROOT (list): List of the processed FERS datafiles
    """
    
    runID = 0
    eventID = 0
    procROOT = []
    if exists(cache_fname):
        # Gather data from the file
        with open(cache_fname, 'rb') as infile:
            # Read back payload from file
            payload = pickle.load(infile)
            runID = payload[0] + 1
            eventID = payload[1] + 1
            procROOT = payload[2]
            logging.info(f"[checkCache] Read from file cache_fers.dat : OK")
    else:
        logging.warning(f"No cache present.")
    return (runID, eventID, procROOT)


def dumpCache(cache_fname: str, dumpCacheRunStatus: bool):
    """
    Dump the cache-file containing information about the list of already processed (converted to ROOT) FERS datafiles
    
    Parameters
    ----------
        cache_fname (str): Path of the cache file
        
    Returns:
    --------
        None
    """    
    
    if dumpCacheRunStatus:
        return
    else:
        # Get run filename without extentions from the path like.
        # For example: _extractFilename(/home/pietro/work/CLEAR_March/FERS/Janus_3.0.3/bin/MsgLog.txt) -> MsgLog.txt
        def _extractFilename(path: str):
            idx = path.rfind('/')
            if idx > 0 :
                return path[idx+1:] 
            else:
                return path
        #   
        # Save runList of the processed ROOT files on file
        with open(cache_fname, 'wb') as outfile:
            # Read back payload from file
            payload = [runID, eventID, procTXT]
            pickle.dump(payload, outfile)
            logging.info(f"[dumpCache] File {cache_fname} saved : OK")
        # Print stats of the converted ROOT files
        logging.info("--------------------------------------")
        logging.info("Summary of the files converted to ROOT in this session")
        for i, item in enumerate(txtProcessedSession):
            logging.info(f"{i} : {_extractFilename(item)}")
        logging.info("--------------------------------------")
        # Greetings
        logging.status("Goodbye :)\n")

        dumpCacheRunStatus = True





##############################################################
######## Aux functions #######################################
##############################################################
# Convert a FERS file to ROOT
def makeROOT(fname):
    logging.debug(f"makeROOT - Filename: {fname}")
    exampleClass = rootconverter(fname, outputROOTdirectory)
    exampleClass.convert()


# Get run filename without extentions from the path like.
# For example: _extractFilename(/home/pietro/work/CLEAR_March/FERS/Janus_3.0.3/bin/MsgLog.txt) -> MsgLog.txt
def _extractFilename(path: str):
    idx = path.rfind('/')
    if idx > 0 :
        return path[idx+1:] 
    else:
        return path


# Get the data filename and return the info filename
# Run1_list.txt -> Run1_Info.txt)
def _infoFilename(fname: str):
    return fname.replace("_list.txt", "_Info.txt")





def exitRoutine() -> None: 
    """
    Exit routine function:
    1. Save list of processed FERS runs for future execution of this program.
    2. Print the summary of the processed FERS run since the beginning.
    3. Gracefully exit.
    """
    dumpCache(procROOTList, dumpCacheRunStatus)
    # Wait for the produced to finish
    exit(0)
    
 
# Interrupt signal handler function
def handler_SIGINT(signum: signal.Signals, frame) -> None:
    """
    Exit signal interrupt handler function
    """ 
    global exitCall
    exitCall = True
    print(); logging.critical("Interrupt signal from main thread")
    if writingROOT:
        logging.warning("ROOT write pending. Waiting for completion...")
    else:
        exitRoutine()



# Main conversion loop of txt files to ROOT
def convertLoop():
    """
    Main conversion loop of txt files from Janus to ROOT
    """
    
    global writingROOT
    aux_firstPrint = True
    # Main loop
    logging.info("Starting main loop")
    while True:
        # Handle SIGTERM interrupt in case the signal is called during ROOT file writing
        if exitCall:
            return
        
        # Get the list of files in the directory
        runList_new = glob.glob(a5202dataDir+"Run*_list.txt")
        infoList = glob.glob(a5202dataDir+"Run*_Info.txt")
        # Loop over the list of Run*_list file in the dir,
        # compare with the previously processed ROOT and eventually
        # process any new file        
        for item in runList_new:
            # If the run is not among those already processed
            if (item not in procTXT):
                if aux_firstPrint:
                    logging.warning(f"New item {_extractFilename(item)} found. Waiting for closure")
                    aux_firstPrint = False
                #
                if (_infoFilename(item) in infoList):
                    writingROOT = True
                    aux_firstPrint = True

                    logging.info(f"Run {_extractFilename(item)} closed. Converting to ROOT...")
                    # This is a new file, let's convert to ROOT format
                    makeROOT(item)
                    # Add the file to the list
                    procTXT.append(item)
                    txtProcessedSession.append(item)
                    writingROOT = False
                    #
                    logging.info(f"Run {_extractFilename(item)[:-4]}.root OK")
            
        # To reduce CPU load
        time.sleep(2)




if __name__ == "__main__":
    # Check cache for the FERS run converted in previous executions
    runID, eventID, procTXT = checkCache(procROOTList)
    # Register the interrupt handler
    signal.signal(signal.SIGINT, handler_SIGINT)
    # Create the DT5730 readout thread
    producer_thread = threading.Thread(target=convertLoop)
    #producer_thread.daemon = True
    # start the producer thread
    producer_thread.start()
    # Wait for the produced to finish
    producer_thread.join()