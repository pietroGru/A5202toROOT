import glob

#dataPath = "/home/pietro/dataNfs/29mar23/"
dataPath = "/home/pietro/dataNfs/CLEAR_March/FERS/data/31mar23/"

listFiles = glob.glob(dataPath+"Run*_list.txt")
infoFiles = glob.glob(dataPath+"Run*_Info.txt")

def checkUnpaired():
    print(f"There are {len(listFiles)} 'list' files and {len(infoFiles)} 'info' files")
    unpaired = []
    for item in listFiles:
        if item.replace("_list", "_Info") not in infoFiles:
            print(f"File {item[item.rfind('/')+1:]} has no info partner")
            unpaired.append(item)
    
    if unpaired != []:
        print() # empty line
        for item in unpaired:
            print(f"mv {item} {item[:item.rfind('/')]}/unpaired/{item[item.rfind('/')+1:]}")

def checkMoreInfoThanList():
    if len(listFiles) < len(infoFiles):
        print("Too many info for the list")
        infoFilesFromList = [item.replace("_list", "_Info") for item in listFiles]
        print(set(infoFiles) - set(infoFilesFromList))



checkUnpaired()
print() # empty line
checkMoreInfoThanList()
print() # empty line

def checkWrongHistoBinning():
    wrongBinningList = []
    for fname in listFiles:
        with open(fname) as infile:
            [infile.readline() for i in range(4)]
            line = infile.readline()[:-1]
            histoChStrIdx = line.rfind(": ")
            #
            try:
                histoCh = int(line[histoChStrIdx+1:])
            except ValueError:
                print(f"ValueError for {fname[fname.rfind('/')+1:]} with line ->{line}")
            #
            if histoCh != 8192:
                print(f"File {fname[fname.rfind('/')+1:]} has {histoCh} bins in the histogram")
                wrongBinningList.append(fname)
    
    if wrongBinningList != []:
        print() # empty line
        for item in wrongBinningList:
            print(f"mv {item} {item[:item.rfind('/')]}/wrongbinning/")
            print(f"mv {item.replace('_list', '_Info')} {item[:item.rfind('/')]}/wrongbinning/")
        
checkWrongHistoBinning()

