import ROOT
import glob
import numpy as np
from datetime import datetime

outfnamePath = "/home/pietro/work/CLEAR_March/FERS/clear/processed/28mar23/"
routfiles = glob.glob(outfnamePath+"*.root")

FERS = ROOT.TChain("FERS", "TChain for the FERS data")

# Load all the files in the TChain
brokenFiles = []
for file in routfiles:
    ret = FERS.AddFile(file)
    if ret==0:
        brokenFiles.append(file)


#FERS.Draw("fers_hg:timestamp", "strip==96 && det==0")
#input()
#exit()

def printBrokenFiles(brokenList):
    for item in brokenList:
        print(f"mv {item} {item.replace('/data/', '/data/broken/')}")
#printBrokenFiles(brokenFiles)

startTime = FERS.GetMinimum("timestamp")
stopTime = FERS.GetMaximum("timestamp")

# Functions and object made available via the interpreter are accessible from the ROOT module
ROOT.gInterpreter.Declare(f'''
// Take timestamp in posix and return time in seconds
double getSeconds(double timestamp){{
    return (timestamp-{startTime});
}}

// Take timestamp in posix and return day
int getDay(double timestamp){{
    if (1680048000 <= timestamp && timestamp <= 1680134399){{
        return 29;
    }}else if(1680134400 <= timestamp && timestamp <= 1680220799){{
        return 30;
    }}else if(1680220800 <= timestamp && timestamp <= 1680307199){{
        return 31;
    }}else{{
        return -1;
    }}
}}

double avgQ(double avgV){{
    return (avgV/4.190)*2.0e3;
}}

bool timeSlice(double timestamp, int day, int hoursA, int minutesA, int secondsA, int hoursB, int minutesB, int secondsB){{
    if(getDay(timestamp) == day){{
        double tA = 0;
        switch(day){{
            case 29:
            tA = 1680048000.0;
            break;
            
            case 30:
            tA = 1680134400.0;
            break;
            
            case 31:
            tA = 1680220800.0;
            break;
        }}
        double tB = tA;
        
        tA = tA + hoursA*3600.0 + minutesA*60.0 + secondsA;
        tB = tB + hoursB*3600.0 + minutesB*60.0 + secondsB;
        
        return (timestamp >= tA && timestamp <= tB);  
    }}else{{
        return false;
    }}  
}}
''')


#29085041_A1561HDP_run0.root
def stripFilename(pathedFname:str):
    pos = pathedFname.rfind("/")
    if pos!=-1:
        return pathedFname[pos+1:]
    else:
        return pathedFname

# Get timetag from the filename
def getTimetag(fname: str) -> np.double:
    fname = stripFilename(fname)
    runTimeStr = fname[:8]
    runNb = int(fname[21:fname.rfind('.')])
    runTime = datetime.datetime(2023, 3, int(runTimeStr[0:2]), int(runTimeStr[2:4]), int(runTimeStr[4:6]), int(runTimeStr[6:8]))    
    return np.double(runTime.timestamp())


#print(ROOT.getDay(1680048001.0))
#print(ROOT.getDay(1680134401.0))
def eventsOver8192():
    print("HG")
    print(f'brd0 - {FERS.Draw("fers_hg:getSeconds(timestamp)", "fers_board==0 && fers_hg > 8192")}/{FERS.Draw("fers_hg:getSeconds(timestamp)", "fers_board==0")}')
    print(f'brd1 - {FERS.Draw("fers_hg:getSeconds(timestamp)", "fers_board==1 && fers_hg > 8192")}/{FERS.Draw("fers_hg:getSeconds(timestamp)", "fers_board==1")}')
    print() #empty line
    print("LG")
    print(f'brd0 - {FERS.Draw("fers_hg:getSeconds(timestamp)", "fers_board==0 && fers_lg > 8192")}/{FERS.Draw("fers_hg:getSeconds(timestamp)", "fers_board==0")}')
    print(f'brd1 - {FERS.Draw("fers_hg:getSeconds(timestamp)", "fers_board==1 && fers_lg > 8192")}/{FERS.Draw("fers_hg:getSeconds(timestamp)", "fers_board==1")}')
    input()


def eventsOver65000():
    canvas1 = ROOT.TCanvas("canvas1", "high gain")
    print(f'brd0 >65k -> {FERS.Draw("fers_hg", "fers_board==0 && fers_hg > 65000")}')
    canvas2 = ROOT.TCanvas("canvas2", "low gain")
    print(f'brd0 >65k -> {FERS.Draw("fers_lg", "fers_board==0 && fers_lg > 65000")}')
    input()

eventsOver8192()
print()
eventsOver65000()
exit()