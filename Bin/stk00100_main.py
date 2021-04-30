# 参照記事：https://qiita.com/connvoi_tyou/items/7cd7ffd5a98f61855f5c
# GoogleDOcsAPI: https://rimever.hatenablog.com/entry/2019/10/16/060000

from __future__ import print_function
import os.path
import copy
import glob

# test
#dou?


import stk00100_iniget as Ini
from stk00100_iniget import vgfGetIni
from common.make_log import setup_logger
vgfGetIni()
logger = setup_logger(__name__)


from stk00100_filedelete import remove_allfiles_before_exe

from common.operate_googleapi import SpreadSheet
from common.operate_googleapi import Drive
from common.operate_googleapi import GAS

import get_stock_yahoo
import get_stock_pandas



def create_PNG():
    # iniから値を取得
    logger.info("INI取得")

    # 業務前削除
    logger.info("業務前削除")
    remove_allfiles_before_exe()

    # GoogleSpreadSheet認証
    # SS = SpreadSheet()
    # SS.Authentication(Ini.vgsSS_TokenPikkleFile, Ini.vgsSS_CreadentialJsonFile, Ini.vgsSS_Scopes, Ini.vgsSS_APIType)
    # ExistFile = SS.CheckExists(Ini.vgsSS_SheetId, Ini.vgsSS_SheetName)
    # すでにファイルが存在すれば削除
    # if ExistFile:
    #     SS.DeleteSheets(Ini.vgsSS_SheetId, ExistFile)
    # vgsSheetId = SS.AddSheets(Ini.vgsSS_SheetId, Ini.vgsSS_SheetName)

    # 株価データを格納
    logger.info("PNG作成")
    list_create_PNG_data_period = []
    list_create_PNG_data_companies = []

    list_create_PNG_data_period.append(Ini.vgsPNG1_target_data_period)
    list_create_PNG_data_period.append(Ini.vgsPNG2_target_data_period)
    list_create_PNG_data_period.append(Ini.vgsPNG3_target_data_period)
    list_create_PNG_data_period.append(Ini.vgsPNG4_target_data_period)
    list_create_PNG_data_companies.append(Ini.vgsPNG1_target_companies)
    list_create_PNG_data_companies.append(Ini.vgsPNG2_target_companies)
    list_create_PNG_data_companies.append(Ini.vgsPNG3_target_companies)
    list_create_PNG_data_companies.append(Ini.vgsPNG4_target_companies)

    json_create_PNG_info = []
    dict_create_PNG_info = {}
    for i in range(int(Ini.vgsSyoukenMaster_createPNGcount)):
        dict_create_PNG_info['target_period']  = list_create_PNG_data_period[i]
        dict_create_PNG_info['target_companies']= list_create_PNG_data_companies[i]
        json_create_PNG_info.append(copy.deepcopy(dict_create_PNG_info))

    # 株価PNGを取得
    for i in range(int(Ini.vgsSyoukenMaster_createPNGcount)):
        STKData, STKTimeRange, STKCompanyLength, df_Sorce = get_stock_pandas.company_stock(Ini.vgsSyoukenMaster_Path, json_create_PNG_info[i])
        # StartColumn = 1 
        # StartRow = 1
        # SS.Write(Ini.vgsSS_SheetId, StartColumn, STKCompanyLength, StartRow, STKTimeRange, STKData)
        get_stock_pandas.get_figure(df_Sorce, json_create_PNG_info[i]['target_period'])
        # SS.ChangeFormat(Ini.vgsSS_SheetId, vgsSheetId)


def upload_PNG(drive):
    # Drive内ファイル削除
    logger.info("Drive内ファイル削除")
    targetDrive = drive.get_drive_folder_id(['programing', 'User_Data', 'STK00100', 'images'])
    image_ids = drive.list_drive_fileids(targetDrive)
    for image_id in image_ids:
        drive.delete_file(image_id)

    # ファイルアップロード
    logger.info("ファイルアップロード")
    files = glob.glob(Ini.vgsPNG_local_folder)
    path_Images = []
    for file in files:
        path_Images.append(file)
    for image in path_Images:
        drive.upload_file(image, targetDrive)

    image_ids = drive.list_drive_fileids(targetDrive)
    return image_ids

def update_spreadsheet(gas, image_ids):
    # SpreadSheet作成

    targetDrive = drive.get_drive_folder_id(['programing', 'User_Data', 'STK00100'])
    # 指定のフォルダにあるファイル一覧を取得
    image_id = drive.get_drive_fileid(targetDrive, Ini.vgsGAS_GAS_SS_Name)

    logger.info("SpreadSheet作成")
    SS_info_dict = gas.display_image_tmp(image_id, Ini.vgsGAS_GAS_SS_SHEET_NAME, image_ids)
    gas.display_image(Ini.vgsGAS_ID, SS_info_dict, image_ids)

if __name__ == '__main__':

    FLG="EST"
    if FLG=="TEST":
        import pandas as pd 
        import pandas_datareader.data as web
        import datetime
        
        stockdata=web.DataReader("9984.JP", "stooq").dropna()

        from bokeh.plotting import figure  ,output_notebook , show
        from bokeh.layouts import column
        from math import pi
        
        stockdatarange=stockdata[:'2015-1-1']
        
        inc = stockdatarange.Close > stockdatarange.Open
        dec = stockdatarange.Open > stockdatarange.Close
        w = 12*60*60*1000 # half day in ms
        
        p = figure(x_axis_type="datetime", plot_width=800, title = "9984 Candlestick")
        p.xaxis.major_label_orientation = pi/4
        p.grid.grid_line_alpha=0.1
        
        p.segment(stockdatarange.index, stockdatarange.High, stockdatarange.index, stockdatarange.Low, color="black")
        p.vbar(stockdatarange.index[inc], w, stockdatarange.Open[inc], stockdatarange.Close[inc], fill_color="#D5E1DD", line_color="black")
        p.vbar(stockdatarange.index[dec], w, stockdatarange.Open[dec], stockdatarange.Close[dec], fill_color="#F2583E", line_color="black")
    else:
        logger.info("■■処理開始■■")
        create_PNG()
        # GoogleDrive認証
        logger.info("Drive認証")
        drive = Drive()
        drive.Authentication(Ini.vgsDrive_TokenPikkleFile, Ini.vgsDrive_CreadentialJsonFile, Ini.vgsDrive_Scopes, 'Drive')
        image_ids = upload_PNG(drive)

        # GAS認証
        logger.info("GAS認証")
        gas = GAS()
        drive
        gas.Authentication(Ini.vgsGAS_TokenPikkleFile, Ini.vgsGAS_CreadentialJsonFile, Ini.vgsGAS_Scopes, 'Script')
        update_spreadsheet(gas, image_ids)
        logger.info("■■処理終了■■")


