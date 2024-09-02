import subprocess
import time
import os
from time import sleep
import shutil
from global_used_paths import pdf_out_path_collect_list
import glob

def a2v(audio_file:str,img_file:str,video_file:str):
    not_divisible_by_two="-vf \"scale=2*trunc(iw/2):2*trunc(ih/2),setsar=1\""      
    # command_str=f"ffmpeg -loop 1 -i \"{img_file}\" -i \"{audio_file}\" {not_divisible_by_two} -c:v h264_qsv -tune stillimage -c:a aac -b:a 192k -shortest \"{video_file}\" -y"
    # 使用 Nvidia 显卡进行加速会更快一点（平均每page大约21s左右）
    command_str=f"ffmpeg -loop 1 -i \"{img_file}\" -i \"{audio_file}\" {not_divisible_by_two} -c:v h264_nvenc -b:v 10000k -c:a aac -b:a 192k -shortest \"{video_file}\" -y"
    print(command_str)
    os.system(command_str)

def main():
    for pdf_out_path_idx,pdf_out_path in enumerate(pdf_out_path_collect_list):
        pdf_pic_out_dir = os.path.dirname(pdf_out_path)+os.sep+"pic_mp3"
        mylist_path = os.path.abspath(pdf_pic_out_dir+os.sep+"mylist.txt")
        open(mylist_path,"w").close()
        mp3_list=glob.glob(os.path.join(pdf_pic_out_dir, "*.mp3"))
        pic_list=glob.glob(os.path.join(pdf_pic_out_dir, "*.jpg"))
        for mp3_path,pic_path in zip(mp3_list,pic_list):
            mp4_path=os.path.abspath(mp3_path.replace(".mp3",".mp4"))
            with open(mylist_path,'a',encoding='gbk', errors='ignore') as f:
                f.write(f"file \'{mp4_path}\'\n")
            a2v(mp3_path,pic_path,mp4_path)
        final_out_path = pdf_out_path.replace(".pdf",".mp4")
        concat_comm=f"ffmpeg -f concat -safe 0 -i {mylist_path} -c copy \"{final_out_path}\" -y"
        os.system(concat_comm) 
        # move mp4 文件
        shutil.move(f"{final_out_path}","D:/tempUseDir/Alldowns"+os.sep+os.path.basename(final_out_path))


if __name__ == '__main__':
    main()

