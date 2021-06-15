from ngdlsdk.constants import CONVERTER_TYPE
from ngdlsdk.zip import NGDLTRACE
from ngdlsdk.api import NGDLAPI
from datetime import datetime
from datetime import timezone 
import os
import logging
import unittest
import filecmp
import sys
import colorama
colorama.init()
class Testing_API_tracetool(unittest.TestCase):
############################################################################################# Functions #################################################################################################################
    logging.basicConfig(level = logging.INFO,format = '[%(asctime)s] [\033[32m%(levelname)s\033[0m] %(message)s')
    logger = logging.getLogger()#__name__)
    ############################################################################################# Var Setting #################################################################################################################
    # Home path
    homePath = 'C:/Users/zhengkun.li/Desktop/SDKAutomaticTest'

    # Start datetime  Download
    startDateTime = datetime(2021,4 , 14, 9, 0, 0)#01.03.2021 08:00:00

    # End datetime  Download
    endDateTime = datetime(2021, 4, 16, 11, 0, 0)#01.03.2021 08:05:00

    # Define the target device ip
    ipStr = "192.168.1.122"

    # Define delete option
    delete_option = False

    # Define Datalogger model
    # dl_model = 'DATALOGGER_2'
    dl_model = 'DATALOGGER2F'
    # dl_model = 'DL2F_withFR'
    #################################### 129   ####################################
    # Output converted folder
    destFolder = homePath+"/sdkConverted"

    numStart = startDateTime.year * 10000 + startDateTime.month * 100 + startDateTime.day
    numStratSpecif = startDateTime.hour*10000 + startDateTime.minute *100 + startDateTime.second
    numEnd = endDateTime.year * 10000 + endDateTime.month * 100 + endDateTime.day
    numEndSpecif =  endDateTime.hour*10000 + endDateTime.minute *100 + endDateTime.second
    
    # Define all the tested channel
    allCh = ['CAN1','CAN2','CAN3','CAN4','CAN5','CAN6','CAN7','CAN8','CAN9','CAN10','CAN11','CAN12','UART1','UART2','UART3','UART4','UART5','UART6','UART7','UART8','LIN1','LIN2','LIN3','LIN4','LIN5','LIN6','LIN7','LIN8','LIN9','LIN10',
    'ETH1','ETH2','ETH3','ETH4','ETH5','ETH6','ETH7','ETH8','ETH9','ETH10','ETH-LOG1','ETH-LOG2','ETH-LOG3','ETH-LOG4','ETH-LOG5','ETH-LOG6']

    #define the channel and the converted file NAME relation
    all_channel_relation = {'CAN1': 'can1', 'CAN2': 'can2', 'CAN3': 'can3', 'CAN4': 'can4', 'CAN5': 'can5', 'CAN6': 'can6', 'CAN7': 'can7', 'CAN8': 'can8', 'CAN9': 'can9', 'CAN10': 'can10',  'CAN11': 'can11',  'CAN12': 'can12', 
    'UART1': 'uart1', 'UART2': 'uart2', 'UART3': 'uart3', 'UART4': 'uart4', 'UART5': 'uart5', 'UART6': 'uart6', 'UART7':'UART7','UART8':'UART8', 
    'LIN1': 'lin1', 'LIN2': 'lin2', 'LIN3': 'lin3', 'LIN4': 'lin4', 'LIN5': 'lin5', 'LIN6': 'lin6', 'LIN7': 'lin7', 'LIN8': 'lin8', 'LIN9': 'lin9', 'LIN10': 'lin10', 
    'ETH1': 'GE1', 'ETH2': 'GE2', 
    'ETH3': 'BR1', 'ETH4': 'BR2', 'ETH5': 'BR3', 'ETH6': 'BR4', 'ETH7': 'BR5', 'ETH8': 'BR6', 'ETH9': 'BR7', 'ETH10': 'BR8', 
    'ETH-LOG1': 'eso21002', 'ETH-LOG2': 'eso21003', 'ETH-LOG3': 'eso21005', 'ETH-LOG4': 'conbox21002', 
    'ETH-LOG5': 'ocu', 
    'ETH-LOG6': 'dlt'}
    
    # define channel dict
    channel_dict = {
    CONVERTER_TYPE.CAN_ASC:['CAN1','CAN2','CAN3','CAN4','CAN5','CAN6','CAN7','CAN8','CAN9','CAN10','CAN11','CAN12'],
    CONVERTER_TYPE.CAN_BLF:['CAN1','CAN2','CAN3','CAN4','CAN5','CAN6','CAN7','CAN8','CAN9','CAN10','CAN11','CAN12'],
    CONVERTER_TYPE.UART_TXT:['UART1','UART2','UART3','UART4','UART5','UART6','UART7','UART8'],
    CONVERTER_TYPE.UART_ASCII_HEX:['UART1','UART2','UART3','UART4','UART5','UART6','UART7','UART8'],
    CONVERTER_TYPE.LIN_ASC:['LIN1','LIN2','LIN3','LIN4','LIN5','LIN6','LIN7','LIN8','LIN9','LIN10'],
    CONVERTER_TYPE.ETH_PCAP:['ETH1','ETH2','ETH3','ETH4','ETH5','ETH6','ETH7','ETH8','ETH9','ETH10'],
    CONVERTER_TYPE.ETHLOG_ESOTRACE:['ETH-LOG3','ETH-LOG4','ETH-LOG5','ETH-LOG6'],#'ETH-LOG1','ETH-LOG2',
    CONVERTER_TYPE.ETHLOG_DLT:['ETH-LOG6'],
    CONVERTER_TYPE.ETHLOG_BIN:['ETH-LOG5','ETH-LOG2']
    ,CONVERTER_TYPE.RAW:['ETH-LOG2']
    }




    # define the base line 
    base_line = {"20210329_090000_20210329_150000_48":{CONVERTER_TYPE.ETHLOG_BIN:['ETH-LOG2'],CONVERTER_TYPE.ETH_PCAP:['ETH7'], CONVERTER_TYPE.LIN_ASC:['LIN3'],CONVERTER_TYPE.ETHLOG_ESOTRACE:['ETH-LOG1','ETH-LOG3']},#'BR5', 'LIN3' ,'ESO21002', 'ESO21003' ,'ESO21005'
            "20210416_090000_20210416_120000_48":{ CONVERTER_TYPE.ETHLOG_DLT:['ETH-LOG6'],CONVERTER_TYPE.ETHLOG_ESOTRACE:['ETH-LOG4'],CONVERTER_TYPE.UART_TXT:['UART1','UART2','UART3','UART4','UART5'],CONVERTER_TYPE.UART_ASCII_HEX:['UART1','UART2','UART3','UART4','UART5']},#'conbox21002', 'dlt', 'uart1','uart1','uart1','uart1','uart5'
            "20210330_090000_20210330_120000_48":{ CONVERTER_TYPE.CAN_ASC:['CAN1'], CONVERTER_TYPE.CAN_BLF:['CAN1']},
            "20210325_090000_20210325_160000_122":{ CONVERTER_TYPE.CAN_ASC:['CAN1'], CONVERTER_TYPE.CAN_BLF:['CAN1'],CONVERTER_TYPE.ETHLOG_BIN:['ETH-LOG5']},
             "20210615_090000_20210615_132200_50":{CONVERTER_TYPE.LIN_ASC:["LIN1","LIN4","LIN7"]}}
    time_base_line = {"20210329_090000_20210329_150000_48":{'start_time':datetime(2021,3 , 29, 9, 0, 0),'end_time':datetime(2021,3 , 29, 15, 0, 0)},
                "20210416_090000_20210416_120000_48":{'start_time':datetime(2021,4 , 16, 9, 0, 0),'end_time':datetime(2021,4 , 16, 12, 0, 0)},
                "20210330_090000_20210330_120000_48":{'start_time':datetime(2021,3 , 30, 9, 0, 0),'end_time':datetime(2021,3 , 30, 12, 0, 0)},
                "20210325_090000_20210325_160000_122":{'start_time':datetime(2021,3 , 25, 9, 0, 0),'end_time':datetime(2021,3 , 25, 16, 0, 0)},
                "20210615_090000_20210615_132200_50":{'start_time':datetime(2021,6 , 15, 9, 0,0),'end_time':datetime(2021,6 , 15, 13, 22,0)}}
    # RES DICT
    res_dict = {
    CONVERTER_TYPE.CAN_ASC:0,
    CONVERTER_TYPE.CAN_BLF:0,
    CONVERTER_TYPE.UART_TXT:0,
    CONVERTER_TYPE.UART_ASCII_HEX:0,
    CONVERTER_TYPE.LIN_ASC:0,
    CONVERTER_TYPE.ETH_PCAP:0,
    CONVERTER_TYPE.ETHLOG_ESOTRACE:0,#'ETH-LOG1','ETH-LOG2',
    CONVERTER_TYPE.ETHLOG_DLT:0,
    CONVERTER_TYPE.ETHLOG_BIN:0
    }
    #sum dict
    sum_dict = {
    CONVERTER_TYPE.CAN_ASC:0,
    CONVERTER_TYPE.CAN_BLF:0,
    CONVERTER_TYPE.UART_TXT:0,
    CONVERTER_TYPE.UART_ASCII_HEX:0,
    CONVERTER_TYPE.LIN_ASC:0,
    CONVERTER_TYPE.ETH_PCAP:0,
    CONVERTER_TYPE.ETHLOG_ESOTRACE:0,#'ETH-LOG1','ETH-LOG2',
    CONVERTER_TYPE.ETHLOG_DLT:0,
    CONVERTER_TYPE.ETHLOG_BIN:0
    }
    ###########################################################################################################################################################################################################################
    # def test_1_download_and_getconfig_getmetadata(self):
    #     # print(cmp_file(zipPath, SDKzipPath))
    #     converter = NGDLTRACE()
    #     api = NGDLAPI(self.ipStr,True)
    #     configApi = api.get_config()
    #     for i in configApi:
    #         print(i)
    #         for j in configApi[i]:
    #             print(f"  {j}\n") 
        
    #     ####  Download all  ####
    #     for zip_pkg in self.time_base_line:
    #         time1 = datetime.now()
    #         print(f"start time = {time1}\n")
    #         api.download("./download_test/sdkDownloads", [{'start': self.time_base_line[zip_pkg]['start_time'],'end': self.time_base_line[zip_pkg]['end_time']}], self.allCh ,True)
    #         time2 = datetime.now()
    #         print(f"end time = {time2}\n")

    #     print(converter.get_convert_metadata(self.SDKzipPath))

    ##########################################################################################  Convertion test  ################################################################################################
    # start convertion
    def test_2_zip_convert(self):
        class bcolors:
            HEADER = '\033[95m'
            OKBLUE = '\033[94m'
            OKCYAN = '\033[96m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'
        logging.basicConfig(level = logging.INFO,format = '[%(asctime)s] [\033[32m%(levelname)s\033[0m] %(message)s')
        logger = logging.getLogger()
        converter = NGDLTRACE()
        # check all types of convertion
        for zip_pkg in self.base_line:

            # select different zip
            for type_ in self.base_line[zip_pkg]:

                # select different type
                for channel in self.base_line[zip_pkg][type_]:

                    #select different channel
                    config_dict =[]
                    print(bcolors.OKCYAN+'Start convertion '+str(channel).ljust(10," ")+bcolors.ENDC)
                    if type_ == CONVERTER_TYPE.UART_ASCII_HEX:
                        path_pre = f"{zip_pkg}_{str(self.all_channel_relation[channel]).lower()}_hex"
                        suffix = ".txt"
                    elif type_ == CONVERTER_TYPE.ETHLOG_BIN:
                        if channel == 'ETH-LOG2':
                            path_pre = f"{zip_pkg}_{str(self.all_channel_relation[channel]).lower()}"
                            suffix = ".raw"
                        elif channel == "ETH-LOG5":   
                            path_pre = f"{zip_pkg}_{str(self.all_channel_relation[channel]).lower()}"
                            suffix = ".ocu" 
                    else:
                        suffix = "."+str(type_).split('_')[-1].lower()
                        path_pre = f"{zip_pkg}_{str(self.all_channel_relation[channel]).lower()}"
                    config_dict = [{"type":type_,
                                    "time_start":self.time_base_line[zip_pkg]['start_time'],
                                    "time_end":self.time_base_line[zip_pkg]['end_time'],
                                    "output_path":"./convert_test/"+path_pre+suffix ,
                                    "port":channel,
                                    "split_size":100000000}]
                    logger.info(f"{channel} -> {suffix}")
                    converter.convert_zip(f"./baseline_trace/{zip_pkg}.zip",config_dict)
                    for k in range(0,10):
                        splitnumber = f"00{k}"
                        try:
                            if filecmp.cmp(f"./convert_test/{path_pre}_{splitnumber}{suffix}",f"./baseline_trace/sdkConvert0427_3932/{path_pre}_{splitnumber}{suffix}"):
                                self.res_dict[type_] += 1
                                self.sum_dict[type_] += 1
                            else:
                                self.sum_dict[type_] += 1
                        except:
                            pass
        print("**************** Conversion result *****************")
        print("  Convert type  |  Total  |   Passed    |  Result  ")
        print(f"CAN    -> ASC   |    {self.sum_dict[CONVERTER_TYPE.CAN_ASC]}    |     {self.res_dict[CONVERTER_TYPE.CAN_ASC]}      |    {(bcolors.OKGREEN + 'Passed') if self.sum_dict[CONVERTER_TYPE.CAN_ASC]== self.res_dict[CONVERTER_TYPE.CAN_ASC] else (bcolors.FAIL + 'Failed')}{bcolors.ENDC}")
        print(f"CAN    -> BLF   |    {self.sum_dict[CONVERTER_TYPE.CAN_BLF]}    |     {self.res_dict[CONVERTER_TYPE.CAN_BLF]}      |    {(bcolors.OKGREEN + 'Passed') if self.sum_dict[CONVERTER_TYPE.CAN_BLF]== self.res_dict[CONVERTER_TYPE.CAN_BLF] else (bcolors.FAIL + 'Failed')}{bcolors.ENDC}")
        print(f"UART   -> TXT   |    {self.sum_dict[CONVERTER_TYPE.UART_TXT]}    |     {self.res_dict[CONVERTER_TYPE.UART_TXT]}      |    {(bcolors.OKGREEN + 'Passed') if self.sum_dict[CONVERTER_TYPE.UART_TXT]== self.res_dict[CONVERTER_TYPE.UART_TXT] else (bcolors.FAIL + 'Failed')}{bcolors.ENDC}")
        print(f"UART   -> ASCII |    {self.sum_dict[CONVERTER_TYPE.UART_ASCII_HEX]}    |     {self.res_dict[CONVERTER_TYPE.UART_ASCII_HEX]}      |    {(bcolors.OKGREEN + 'Passed') if self.sum_dict[CONVERTER_TYPE.UART_ASCII_HEX]== self.res_dict[CONVERTER_TYPE.UART_ASCII_HEX] else (bcolors.FAIL + 'Failed')}{bcolors.ENDC}")
        print(f"LIN    -> ASC   |    {self.sum_dict[CONVERTER_TYPE.LIN_ASC]}    |     {self.res_dict[CONVERTER_TYPE.LIN_ASC]}      |    {(bcolors.OKGREEN + 'Passed') if self.sum_dict[CONVERTER_TYPE.LIN_ASC]== self.res_dict[CONVERTER_TYPE.LIN_ASC] else (bcolors.FAIL + 'Failed')}{bcolors.ENDC}")
        print(f"ETH    -> PCAP  |    {self.sum_dict[CONVERTER_TYPE.ETH_PCAP]}    |     {self.res_dict[CONVERTER_TYPE.ETH_PCAP]}      |    {(bcolors.OKGREEN + 'Passed') if self.sum_dict[CONVERTER_TYPE.ETH_PCAP]== self.res_dict[CONVERTER_TYPE.ETH_PCAP] else (bcolors.FAIL + 'Failed')}{bcolors.ENDC}")
        print(f"ETHLOG -> ESO   |    {self.sum_dict[CONVERTER_TYPE.ETHLOG_ESOTRACE]}    |     {self.res_dict[CONVERTER_TYPE.ETHLOG_ESOTRACE]}      |    {(bcolors.OKGREEN + 'Passed') if self.sum_dict[CONVERTER_TYPE.ETHLOG_ESOTRACE]== self.res_dict[CONVERTER_TYPE.ETHLOG_ESOTRACE] else (bcolors.FAIL + 'Failed')}{bcolors.ENDC}")
        print(f"ETHLOG -> DLT   |    {self.sum_dict[CONVERTER_TYPE.ETHLOG_DLT]}    |     {self.res_dict[CONVERTER_TYPE.ETHLOG_DLT]}      |    {(bcolors.OKGREEN + 'Passed') if self.sum_dict[CONVERTER_TYPE.ETHLOG_DLT]== self.res_dict[CONVERTER_TYPE.ETHLOG_DLT] else (bcolors.FAIL + 'Failed')}{bcolors.ENDC}")
        print(f"ETHLOG -> BIN   |    {self.sum_dict[CONVERTER_TYPE.ETHLOG_BIN]}    |     {self.res_dict[CONVERTER_TYPE.ETHLOG_BIN]}      |    {(bcolors.OKGREEN + 'Passed') if self.sum_dict[CONVERTER_TYPE.ETHLOG_BIN]== self.res_dict[CONVERTER_TYPE.ETHLOG_BIN] else (bcolors.FAIL + 'Failed')}{bcolors.ENDC}")
        # print(f"ETHLOG -> RAW   |    {self.sum_dict[CONVERTER_TYPE.RAW]}    |     {self.res_dict[CONVERTER_TYPE.RAW]}      |    {(bcolors.OKGREEN + 'Passed') if self.sum_dict[CONVERTER_TYPE.RAW]== self.res_dict[CONVERTER_TYPE.RAW] else (bcolors.FAIL + 'Failed')}{bcolors.ENDC}")

    ################################################################################# test delete func #######################################################################################################
    def test_3_delete(self):
        api = NGDLAPI(self.ipStr,True)
        if(self.delete_option):
            print('**************************************************************   Start convertion file deletion   **************************************************************')
            print(api.delete_trace(self.startDateTime,self.endDateTime))
            try:
                api.download(self.homePath+"/sdkDownloads", [{'start': self.startDateTime,'end': self.endDateTime}], self.allCh , True)
            except AttributeError:
                logging.Logger.info("Delete function normal")
            else:
                logging.Logger.error("Data delete failed, delete function error")

    ################################################################################# test syn func #######################################################################################################
    # def test_4_ntp(self):
    #     api = NGDLAPI(self.ipStr,True)
    #     print('**************************************************************       Start NTP configuration        **************************************************************')
    #     #api.sync_npt("off")
    #     try:
    #         api.sync_ntp("off")#"off"/'on'
    #     except:
    #         print('Set NPT syncronization failed!')
    #     else:
    #         print('Set NPT syncronization success!')
    #     api.sync_ntp("on")#"off"/'on
    # ################################################################################# test set time func #######################################################################################################
    # def test_ntp(self):   
    #     api = NGDLAPI(self.ipStr,True)
    #     api.sync_ntp("off")#"off"/'on
    #     print('**************************************************************      Start time configuration        **************************************************************')
    #     try:
    #         api.sync_time("2021-02-24 12:00:00")#"2015-11-20 16:10:40"
    #     except:
    #         print('Set time failed!')
    #     else: 
    #         print('Set time success!')
    #     api.sync_ntp("on")#"off"/'on'


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
   