from common.get_ini import Common_GetIni

from common.get_ini import common_get_keycount
# ファイルの存在チェック用モジュール
import os
import errno
import inspect

# from common.make_log import setup_logger

# logger = setup_logger(__name__)

# clsIni_kugiri = '/'
# clsIni_Inikakutyoushi = '.ini'
# vlsIni_DirPath = os.path.dirname(__file__)
# vlsIni_FileName = os.path.basename(__file__)
# vlsCmn_JobNumber = vlsIni_FileName[0:8]
# vlsIni_FilePath = vlsIni_DirPath + clsIni_kugiri + vlsCmn_JobNumber + clsIni_Inikakutyoushi
vlsIni_FilePath = 'D:/User_Application/STK00100/Bin/stk00100.ini'

def vgfGetIni():
    # iniファイルが存在するかチェック
    if os.path.exists(vlsIni_FilePath):
        # セクション・キーの定義
        clsIniSection_Default = 'Default'
        clsIniKey_LogFile = 'LogFile'
        clsIniSection_SpreadSheets = 'SpreadSheets'
        clsIniSection_Docs = 'Docs'
        clsIniSection_GAS = 'GAS'
        clsIniSection_Drive = 'Drive'
        clsIniKey_Google_APIType = 'APIType'
        clsIniKey_Google_Scope = 'Scope'
        clsIniKey_Google_TokenPikkleFile = 'TokenPikkleFile'
        clsIniKey_Google_CreadentialJsonFile = 'CreadentialJsonFile'
        clsIniKey_Google_SheetId = 'SheetId'
        clsIniKey_Google_SheetName = 'SheetName'

        clsIniKey_PNG_local_folder = 'PNG_local_folder'
        clsIniKey_GAS_ID = 'GAS_ID'
        clsIniKey_GAS_SS_SHEET_NAME = 'GAS_SS_SHEET_NAME'
        clsIniKey_GAS_SS_Name = 'GAS_SS_Name'

        clsIniSection_SyoukenMaster = 'SyoukenMaster'
        clsIniKey_Path = 'Path'
        clsIniKey_createPNGcount = 'createPNGCount'
        

        clsIniSection_Target_companies = 'Target_companies'
        clsIniSection_DataPeriods = 'DataPeriods'
        clsIniKey_PNG1 = 'PNG1'
        clsIniKey_PNG2 = 'PNG2'
        clsIniKey_PNG3 = 'PNG3'
        clsIniKey_PNG4 = 'PNG4'

        clsIniSection_DeleteFolders = 'DeleteFolders'
        clsIniKey_DeleteFoleder1 = 'DeleteFolder1'

        

        # global vgs_detelefolder_count 
        global vgs_LogFile
        # vgs_detelefolder_count = common_get_keycount(vlsIni_FilePath, clsIniSection_DeleteFolders)
        vgs_LogFile = Common_GetIni(vlsIni_FilePath, clsIniSection_Default, clsIniKey_LogFile)



        # global vgs_detelefolder_count 
        global vgs_detelefolder1
        # vgs_detelefolder_count = common_get_keycount(vlsIni_FilePath, clsIniSection_DeleteFolders)
        vgs_detelefolder1 = Common_GetIni(vlsIni_FilePath, clsIniSection_DeleteFolders, clsIniKey_DeleteFoleder1)


        global vgsSS_Scopes
        global vgsSS_APIType
        global vgsSS_SheetId
        global vgsSS_TokenPikkleFile
        global vgsSS_CreadentialJsonFile
        global vgsSS_SheetName
        vgsSS_Scopes = Common_GetIni(vlsIni_FilePath, clsIniSection_SpreadSheets, clsIniKey_Google_Scope)
        vgsSS_APIType = Common_GetIni(vlsIni_FilePath, clsIniSection_SpreadSheets, clsIniKey_Google_APIType)
        vgsSS_SheetId = Common_GetIni(vlsIni_FilePath, clsIniSection_SpreadSheets, clsIniKey_Google_SheetId)
        vgsSS_TokenPikkleFile = Common_GetIni(vlsIni_FilePath, clsIniSection_SpreadSheets, clsIniKey_Google_TokenPikkleFile)
        vgsSS_CreadentialJsonFile = Common_GetIni(vlsIni_FilePath, clsIniSection_SpreadSheets, clsIniKey_Google_CreadentialJsonFile)
        vgsSS_SheetName = Common_GetIni(vlsIni_FilePath, clsIniSection_SpreadSheets, clsIniKey_Google_SheetName)

        global vgsDocs_Scopes
        global vgsDocs_SheetId
        global vgsDocs_TokenPikkleFile
        global vgsDocs_CreadentialJsonFile
        vgsDocs_Scopes = Common_GetIni(vlsIni_FilePath, clsIniSection_Docs, clsIniKey_Google_Scope)
        vgsDocs_SheetId = Common_GetIni(vlsIni_FilePath, clsIniSection_Docs, clsIniKey_Google_SheetId)
        vgsDocs_TokenPikkleFile = Common_GetIni(vlsIni_FilePath, clsIniSection_Docs, clsIniKey_Google_TokenPikkleFile)
        vgsDocs_CreadentialJsonFile = Common_GetIni(vlsIni_FilePath, clsIniSection_Docs, clsIniKey_Google_CreadentialJsonFile)
        
        global vgsGAS_Scopes
        global vgsGAS_TokenPikkleFile
        global vgsGAS_CreadentialJsonFile
        global vgsPNG_local_folder
        global vgsGAS_ID
        global vgsGAS_GAS_SS_SHEET_NAME
        global vgsGAS_GAS_SS_Name 
        vgsGAS_Scopes = Common_GetIni(vlsIni_FilePath, clsIniSection_GAS, clsIniKey_Google_Scope)
        vgsGAS_TokenPikkleFile = Common_GetIni(vlsIni_FilePath, clsIniSection_GAS, clsIniKey_Google_TokenPikkleFile)
        vgsGAS_CreadentialJsonFile = Common_GetIni(vlsIni_FilePath, clsIniSection_GAS, clsIniKey_Google_CreadentialJsonFile)
        vgsPNG_local_folder = Common_GetIni(vlsIni_FilePath, clsIniSection_GAS, clsIniKey_PNG_local_folder)
        vgsGAS_ID = Common_GetIni(vlsIni_FilePath, clsIniSection_GAS, clsIniKey_GAS_ID)
        vgsGAS_GAS_SS_SHEET_NAME = Common_GetIni(vlsIni_FilePath, clsIniSection_GAS, clsIniKey_GAS_SS_SHEET_NAME)
        vgsGAS_GAS_SS_Name = Common_GetIni(vlsIni_FilePath, clsIniSection_GAS, clsIniKey_GAS_SS_Name)

        global vgsDrive_Scopes
        global vgsDrive_TokenPikkleFile
        global vgsDrive_CreadentialJsonFile
        vgsDrive_Scopes = Common_GetIni(vlsIni_FilePath, clsIniSection_Drive, clsIniKey_Google_Scope)
        vgsDrive_TokenPikkleFile = Common_GetIni(vlsIni_FilePath, clsIniSection_Drive, clsIniKey_Google_TokenPikkleFile)
        vgsDrive_CreadentialJsonFile = Common_GetIni(vlsIni_FilePath, clsIniSection_Drive, clsIniKey_Google_CreadentialJsonFile)

        global vgsSyoukenMaster_Path
        global vgsSyoukenMaster_createPNGcount
        vgsSyoukenMaster_Path = Common_GetIni(vlsIni_FilePath, clsIniSection_SyoukenMaster, clsIniKey_Path)
        vgsSyoukenMaster_createPNGcount = Common_GetIni(vlsIni_FilePath, clsIniSection_SyoukenMaster, clsIniKey_createPNGcount)

        global vgsPNG1_target_companies
        global vgsPNG1_target_data_period 
        global vgsPNG2_target_companies
        global vgsPNG2_target_data_period 
        global vgsPNG3_target_companies
        global vgsPNG3_target_data_period 
        global vgsPNG4_target_companies
        global vgsPNG4_target_data_period 
        vgsPNG1_target_companies = Common_GetIni(vlsIni_FilePath, clsIniSection_Target_companies, clsIniKey_PNG1)
        vgsPNG1_target_data_period = Common_GetIni(vlsIni_FilePath, clsIniSection_DataPeriods, clsIniKey_PNG1)
        vgsPNG2_target_companies = Common_GetIni(vlsIni_FilePath, clsIniSection_Target_companies, clsIniKey_PNG2)
        vgsPNG2_target_data_period = Common_GetIni(vlsIni_FilePath, clsIniSection_DataPeriods, clsIniKey_PNG2)
        vgsPNG3_target_companies = Common_GetIni(vlsIni_FilePath, clsIniSection_Target_companies, clsIniKey_PNG3)
        vgsPNG3_target_data_period = Common_GetIni(vlsIni_FilePath, clsIniSection_DataPeriods, clsIniKey_PNG3)
        vgsPNG4_target_companies = Common_GetIni(vlsIni_FilePath, clsIniSection_Target_companies, clsIniKey_PNG4)
        vgsPNG4_target_data_period = Common_GetIni(vlsIni_FilePath, clsIniSection_DataPeriods, clsIniKey_PNG4)

    else:
        # iniファイルが存在しない場合、エラー発生
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), vlsIni_FilePath)


if __name__ == '__main__':
    vgfGetIni()