# https://hk29.hatenablog.jp/entry/2020/04/25/170130

import sys
from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import japanize_matplotlib 
from datetime import date 

from common.make_log import setup_logger

logger = setup_logger(__name__)

def get_SyoukenCodeMaster(SyoukenMasterPath, KabukaCodeMaster):
    df = pd.read_csv(SyoukenMasterPath, header=0)
    Company_Name = df[df['Code'] == int(KabukaCodeMaster)].iloc[0, 1]
    return Company_Name


def company_stock(SyoukenMasterPath, dict_create_PNG_info):
    end = date.today()  # 今日の日付
    start = (pd.Period(end, 'D')-int(dict_create_PNG_info['target_period'] )).start_time 

    CompanyCodes = dict_create_PNG_info['target_companies'].split(', ')

    df = pd.DataFrame()
    for CompanyCode in CompanyCodes:
        company_code_Tokyo = CompanyCode + '.T'
        CompanyName = get_SyoukenCodeMaster(SyoukenMasterPath, CompanyCode)
        new_df = data.get_data_yahoo(company_code_Tokyo, end=end, start=start)
        new_df = new_df.rename(columns={'Close': CompanyName})
        df = pd.concat([df, new_df], axis=1)
    df = df.drop(["High","Low", "Open","Volume", "Adj Close"], axis=1)
    img_df = df.copy()
    df = df.rename_axis(index='日時')
    
    df = df.reset_index()
    df['日時'] = df['日時'].dt.strftime('%Y-%m-%d')
    STKData = df.values
    STKData = np.insert(STKData, 0, df.columns.values, axis=0).tolist()

    return STKData, len(STKData), len(df.columns), img_df

def get_figure(img_df, Period):

    fig, ax = plt.subplots(figsize=(10 ,5))

    labels = img_df.columns    
    ax.set_xlabel('time')  # x軸ラベル
    ax.set_ylabel('price')  # y軸ラベル 
    for i in range(len(img_df.columns)):
        ax.plot(img_df.index, img_df.iloc[:,int(i)], label=labels[i])
    ax.legend(loc=0)    # 凡例
    # fig.tight_layout()  # レイアウトの設定
    fig.suptitle("直近" + Period + "日の株価推移")
    file_name=Period + '日.png'
    logger.info("PNG作成：" + file_name)
    plt.savefig('D:/User_Application/STK00100/PNG/' + file_name) # 画像の保存
    # plt.show()

if __name__ == '__main__':
    import stk00100_iniget as Ini
    from stk00100_iniget import vgfGetIni
    vgfGetIni()
    a,b,c,d = company_stock(Ini.vgsSyoukenMaster_Path, Ini.vgsPNG1_target_data_period, Ini.vgsPNG1_target_companies)
    get_figure(d, Ini.vgsPNG1_target_data_period )