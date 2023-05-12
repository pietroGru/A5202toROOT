#include "TChain.h"

// Take timestamp in posix and return day
int getDay(double timestamp){
    if(1679961600 <= timestamp && timestamp <= 1680047999){
        return 28;
    }else if (1680048000 <= timestamp && timestamp <= 1680134399){
        return 29;
    }else if(1680134400 <= timestamp && timestamp <= 1680220799){
        return 30;
    }else if(1680220800 <= timestamp && timestamp <= 1680307199){
        return 31;
    }else{
        return -1;
    }
}

int getHour(double timestamp){
    if(1679961600 <= timestamp && timestamp <= 1680047999){
        return (int)((timestamp-1679961600)/3600.0);
    }else if (1680048000 <= timestamp && timestamp <= 1680134399){
        return (int)((timestamp-1680048000)/3600.0);
    }else if(1680134400 <= timestamp && timestamp <= 1680220799){
        return (int)((timestamp-1680134400)/3600.0);
    }else if(1680220800 <= timestamp && timestamp <= 1680307199){
        return (int)((timestamp-1680220800)/3600.0);
    }else{
        return -1;
    }
}

int getMinute(double timestamp){
    return (int)((timestamp - getHour(timestamp)*3600.0) / 60.0);
}

int getSecond(double timestamp){
    return (int)((timestamp - getHour(timestamp)*3600.0 - getMinute(timestamp)*60.0));
}


double avgQ(double avgV){
    return (avgV/4.190)*2.0e3;
}

bool timeSlice(double timestamp, int day, int hoursA, int minutesA, int secondsA, int hoursB, int minutesB, int secondsB){
    if(getDay(timestamp) == day){
        double tA = 0;
        switch(day){
            case 28:
            tA = 1679961600.0;
            break;

            case 29:
            tA = 1680048000.0;
            break;
            
            case 30:
            tA = 1680134400.0;
            break;
            
            case 31:
            tA = 1680220800.0;
            break;
        }
        double tB = tA;
        
        tA = tA + hoursA*3600.0 + minutesA*60.0 + secondsA;
        tB = tB + hoursB*3600.0 + minutesB*60.0 + secondsB;
        
        return (timestamp >= tA && timestamp <= tB);  
    }else{
        return false;
    }  
}

double timeRound(double timestamp){
    return round(timestamp*10.)/10.;
}

auto outfnamePath28 = "/home/pietro/work/CLEAR_March/FERS/clear/processed/28mar23/*.root";
auto outfnamePath29 = "/home/pietro/work/CLEAR_March/FERS/clear/processed/29mar23/*.root";
auto outfnamePath30 = "/home/pietro/work/CLEAR_March/FERS/clear/processed/30mar23/*.root";
auto outfnamePath31 = "/home/pietro/work/CLEAR_March/FERS/clear/processed/31mar23/*.root";
auto FERS = new TChain("FERS", "TChain for the FERS data");
TH1D* lags;

void timeLags(){
    TTreeReader reader(FERS);
    TTreeReaderValue<unsigned int> event(reader, "event");
    TTreeReaderValue<double> timestamp(reader, "timestamp");
    lags = new TH1D("lags", "Time difference FERS;diff [s];counts", 240, 0, 2.4);
    size_t evtCounter=0;
    double last_timestamp=0;
    while(reader.Next()){
        double diff = round((*timestamp - last_timestamp)*10.)/10.;
        //std::cout << evtCounter << "\t" << *event << "\t" << std::setprecision(18) << *timestamp << "\t" << diff << (diff == 0.100 ? " true" : " false") << std::endl;;
        last_timestamp = *timestamp;
        evtCounter++;
        if(diff!=0) lags->Fill(abs(diff));

        //if(evtCounter>100) break;
    }
    lags->Draw();
}





void utils(){
    FERS->Add(outfnamePath28);
    FERS->Add(outfnamePath29);
    FERS->Add(outfnamePath30);
    FERS->Add(outfnamePath31);
    //FERS->Draw("fers_hg:timestamp", "(fers_board==0)", "*");
    timeLags();
}