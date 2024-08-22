from get_latex_compile_new import main as main1
from get_txts_audios_from_pdf import main as main2
from get_pics_from_pdf import main as main3
from get_mp4_and_merge import main as main4

from global_used_paths import txt_file_dir

import os
import concurrent.futures
import psycopg2
from datetime import datetime,timedelta
import uuid

def get_file_jitianqian(file_path):
    time_delta:timedelta = datetime.now()-datetime.fromtimestamp(os.path.getctime(file_path))
    return time_delta.days

def scan_txt_files(directory,xinxiandu=1000):
    # 扫描指定目录下的所有txt文件
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt') and get_file_jitianqian(directory+os.sep+f)<=xinxiandu]

def main(txt_path):
    main1(txt_path)
    main2()
    main3()
    main4()

if __name__ == '__main__':
    txt_files = scan_txt_files(txt_file_dir)
    for txt_file in txt_files:
        main(txt_file)
    # 超线程测试没问题！
    # with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
    #     executor.map(main, txt_files)
