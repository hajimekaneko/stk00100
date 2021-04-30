import os
import glob

def common_remove_allfiles(pathname, recursive=True):
    if os.path.isdir(pathname):
        pathname = pathname + '/*'
        for p in glob.glob(pathname, recursive=recursive):
            if os.path.isfile(p):
                os.remove(p)
    else:
        logger.error("PATHにディレクトリが存在しません。")