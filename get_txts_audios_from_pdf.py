import pdfplumber
import os
from global_used_paths import pdf_out_path_collect_list

#提取全部文字，并保存
def extract_text_allpage (pdf_path,pdf_txt_out_dir):
    pdf = pdfplumber.open(pdf_path)
    for page_no,page in enumerate(pdf.pages,1):
        page_content = page.extract_text()
        # 页码也会读进来，11-12行处理掉文末的页码
        remove_idx=page_content.rfind('\n')
        page_content = page_content[0:remove_idx]
        # 读音而已，没必要有空行
        page_content = page_content.replace("\n",'')
        pdf_txt_out_path=pdf_txt_out_dir+os.sep+str(page_no).zfill(3)+".txt"
        pdf_mp3_out_path=pdf_txt_out_dir+os.sep+str(page_no).zfill(3)+".mp3"
        with open(pdf_txt_out_path,'w',encoding="utf-8") as f:
            f.write(page_content)
        audio_comm=f"edge-tts --voice zh-CN-YunyangNeural --rate=-20% -f \"{pdf_txt_out_path}\" --write-media \"{pdf_mp3_out_path}\""
        os.system(audio_comm)

def main():
    for pdf_out_path_idx,pdf_out_path in enumerate(pdf_out_path_collect_list):
        # extract_text_onepage(path,1)
        pdf_txt_out_dir = os.path.dirname(pdf_out_path)+os.sep+"pic_mp3"
        if not os.path.exists(pdf_txt_out_dir):
            os.makedirs(pdf_txt_out_dir)
        extract_text_allpage(pdf_out_path,pdf_txt_out_dir)

if __name__ == '__main__':
    main()