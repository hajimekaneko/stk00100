# ==================================================
# iniファイルの読み込み
# ==================================================
# coding: utf-8
import configparser


# --------------------------------------------------
# read_file()関数によるiniファイルの読み込み
# --------------------------------------------------

def Common_GetIni(vlsIni_Path, vlsIni_Section, vlsIni_Key):
    config_ini = configparser.ConfigParser()

    with open(vlsIni_Path, encoding='utf-8') as fp:
        config_ini.read_file(fp)
        # iniの値取得
        read_default = config_ini[vlsIni_Section]
        var = read_default.get(vlsIni_Key)

        # 結果表示
        return var

def common_get_keycount(vlsIni_Path, vlsIni_Section):
    with open(vlsIni_Path, encoding='utf-8') as fp:
        config_ini.read_file(fp)
        # iniの値取得
        read_default = config_ini[vlsIni_Section]
        var = len(read_default)

        # 結果表示
        return var