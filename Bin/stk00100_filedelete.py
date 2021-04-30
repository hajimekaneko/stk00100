from common.delete_file import common_remove_allfiles

import stk00100_iniget as Ini
from stk00100_iniget import vgfGetIni

# from common.make_log import setup_logger

# logger = setup_logger(__name__)

def remove_allfiles_before_exe():
    common_remove_allfiles(Ini.vgs_detelefolder1)

if __name__ == '__main__':
    vgfGetIni()
    remove_allfiles_before_exe()