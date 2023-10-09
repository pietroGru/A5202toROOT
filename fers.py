from datetime import datetime as dttm
from sys import argv as CLIargs
from rootconverter import *
from os.path import exists
import threading
import pickle
import signal
import time
import glob

# fers.py logger
from logger import create_logger
logging = create_logger("fers")

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
daqStartTime = dttm.now()

rFilename = daqStartTime.strftime("%d%H%M%S_") + f"FERS_run{runID}.root"
#
procROOTList = "runList.dat"
# List of ROOT files processed in this session
txtProcessedSession = []
# Path where FERS data files are located 
a5202dataDir = "./"
# Path where output ROOT files are located
outputROOTdirectory = "./"

exitCall = False                # Boolean signalling exit interrupt call
writingROOT = False             # ROOT writing status
dumpCacheRun = False            # Cache dump mode (True = dump cache, False = do not dump cache)
rfoutFormat = True              # ROOT file mode (True = vector, False = tree)


##############################################################
######## Cache utilites ######################################
##############################################################
# Check the cache-file containing information about the list of already processed (converted to ROOT) FERS datafiles
def checkCache(cache_fname: str) -> tuple:
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


# Dump the cache-file containing information about the list of already processed (converted to ROOT) FERS datafiles
def dumpCache(cache_fname: str) -> None:
    """
    Dump the cache-file containing information about the list of already processed (converted to ROOT) FERS datafiles
    
    Parameters
    ----------
        cache_fname (str): Path of the cache file
        
    Returns:
    --------
        None
    """
    
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





##############################################################
######## Aux functions #######################################
##############################################################
# Convert a FERS file to ROOT
def makeROOT(fname, mode) -> None:
    logging.debug(f"makeROOT - Filename: {fname}")
    exampleClass = rootconverter(fname, outputROOTdirectory, rfileModeVector=mode)
    exampleClass.convert()


# Get run filename without extentions from the path like.
# For example: _extractFilename(/home/pietro/work/CLEAR_March/FERS/Janus_3.0.3/bin/MsgLog.txt) -> MsgLog.txt
def _extractFilename(path: str) -> str:
    idx = path.rfind('/')
    if idx > 0 :
        return path[idx+1:] 
    else:
        return path


# Get the data filename and return the info filename
# Run1_list.txt -> Run1_Info.txt)
def _infoFilename(fname: str) -> str:
    return fname.replace("_list.txt", "_Info.txt")



# Exit routine function
def exitRoutine() -> None: 
    """
    Exit routine function:
    1. Save list of processed FERS runs for future execution of this program.
    2. Print the summary of the processed FERS run since the beginning.
    3. Gracefully exit.
    """
    if dumpCacheRun:
        dumpCache(procROOTList)
    else:
        logging.warning("Cache dump off.")
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
        if exitCall: break
        
        # Get the list of files in the directory
        runList_new = glob.glob(a5202dataDir+"Run*_list.txt")
        runList_new = sorted(runList_new, key=lambda x: int(x[x.rfind('Run')+3:x.rfind('_')]))  # Sort not striclty needed here
        infoList = glob.glob(a5202dataDir+"Run*_Info.txt")
        infoList = sorted(infoList, key=lambda x: int(x[x.rfind('Run')+3:x.rfind('_')]))     # Sort not striclty needed here
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
                    
                    if exists(item.replace('.txt', '.root').replace(a5202dataDir, outputROOTdirectory)):
                        logging.warning(f"Run {_extractFilename(item)} already converted. Skipping...")
                    else:
                        logging.info(f"Run {_extractFilename(item)} closed. Converting to ROOT...")
                        # This is a new file, let's convert to ROOT format
                        makeROOT(item, rfoutFormat)
                        
                    # Add the file to the list
                    procTXT.append(item)
                    txtProcessedSession.append(item)
                    writingROOT = False
                    #
                    logging.info(f"Run {_extractFilename(item)[:-4]}.root OK")
            
        # To reduce CPU load
        time.sleep(2)


# Handle CLI arguments
if len(CLIargs) > 1:
    internalArgs = [a5202dataDir, outputROOTdirectory, dumpCacheRun, rfoutFormat]
    for i, arg in enumerate(CLIargs[1:]):
        if i == 2 or i == 3: arg = bool(int(arg))
        internalArgs[i] = arg
    a5202dataDir, outputROOTdirectory, dumpCacheRun, rfoutFormat = internalArgs[0], internalArgs[1], internalArgs[2], internalArgs[2]
    logging.info(f"Janus input file directory: {a5202dataDir}")
    logging.info(f"ROOT output file directory: {outputROOTdirectory}")
    logging.info(f"Saving cache file is      : {'on' if dumpCacheRun==True else 'off'}")
    logging.info(f"ROOT output file format   : {'vector' if rfoutFormat==True else 'tree'}")
    


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