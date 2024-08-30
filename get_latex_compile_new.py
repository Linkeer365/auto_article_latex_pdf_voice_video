import re
import os
import shutil
import sys
from get_title_infos import get_title_infos
from global_used_paths import latex_template_path,txt_file_dir,pdf_out_path_collect_list

# 需要保证段落刚好是 \n\n，这个很好保证吧！

def save_files(title_info_dict,txt_file_path,tex_filename):
    filename=title_info_dict['filename']
    title=title_info_dict['<Your-Title>']
    author=title_info_dict['<Your-Author>']
    date=title_info_dict['<Your-Date>'].replace("-","")
    if not os.path.exists(f'./records/{title}-{author}-{date}'):
        os.makedirs(f"./records/{title}-{author}-{date}")
    # 保存txt文件（复制）
    shutil.copyfile(txt_file_path,f"./records/{title}-{author}-{date}/{title}-{author}-{date}.txt")
    # copy pdf 文件
    shutil.copy2(f"{tex_filename}.pdf","D:/tempUseDir/Alldowns")
    # 保存tex与pdf文件（剪切）
    shutil.move(f"{tex_filename}.tex",f"./records/{title}-{author}-{date}/{title}-{author}-{date}.tex")
    shutil.move(f"{tex_filename}.pdf",f"./records/{title}-{author}-{date}/{title}-{author}-{date}.pdf")
    # 删掉剩下的垃圾
    os.system(f"cd \"{os.getcwd()}\" && del {tex_filename}*")

    return f"./records/{title}-{author}-{date}/{title}-{author}-{date}.pdf"
    

def get_format_tex_content_by_poem_or_essay(content_str,poem_or_essay):
    if poem_or_essay == 'poem':
        tex_file_paras=content_str.split('\n\n')
        for para_idx,para in enumerate(tex_file_paras):
            tex_file_lines_each_para=para.split('\n')
            for line_idx, line in enumerate(tex_file_lines_each_para):
                if line.replace(" ",'').replace("　",'') == '':
                    # 空行一律改成两个中文空格
                    line = '　　'
                line = line.replace("\n",'') + r'\\'+'\n'
                tex_file_lines_each_para[line_idx]=line
            tex_file_paras[para_idx]="".join(tex_file_lines_each_para)
        format_str = '\n\n'.join(tex_file_paras)
    elif poem_or_essay == 'essay':
        format_str = content_str
    return format_str

def get_final_file_str(info_dict:dict,template_path:str,poem_or_essay):
    with open(template_path,'r',encoding='utf-8') as f:
        template_line_s=f.read()
    for key,value in info_dict.items():
        if key.startswith('<Your'):
            template_line_s=template_line_s.replace(key,value)
    # 最终的文本体现
    final_file_str=template_line_s
    if poem_or_essay == 'essay':
        final_file_str=final_file_str.replace(r"\setlength\parindent{0pt}",'')
    return final_file_str

def get_para_type(para:str):
    # 章节段落单独标记为：crt
    return 'crt' if para.startswith("crtcrtcrt") else 'normal'

def get_latex_file_save_compile(title_info_dict,template_path):
    para_list = title_info_dict['para_list']
    for para_idx,para in enumerate(para_list):
        para_type = get_para_type(para)
        if para_type == 'crt':
            para='\n\n'+r"{\centering\section*{" + para.replace("crtcrtcrt",'').replace("\n",'') + '}}'+'\n\n'
            para_list[para_idx]=para
    paras_s="\n\n".join(para_list)
    content_str=get_format_tex_content_by_poem_or_essay(paras_s,title_info_dict["poem_or_essay"])
    title_info_dict['<Your-Content>']=content_str
    final_file_str=get_final_file_str(title_info_dict,template_path,title_info_dict["poem_or_essay"])
    # 生成编译用tex文件
    tex_filename=title_info_dict['filename'].replace(".txt","")
    with open(f"{tex_filename}.tex",'w',encoding='utf-8') as f:
        f.write(final_file_str)
    # 编译该文件
    comm = f"xelatex -interaction=nonstopmode {tex_filename}.tex"
    os.system(comm)
    # 保存应该保存的文件
    pdf_out_path=save_files(title_info_dict,title_info_dict["filepath"],tex_filename)
    return pdf_out_path

def main(txt_file_path):
    title_info_dict = get_title_infos(txt_file_path)
    txt_file_path = title_info_dict['filepath']
    pdf_out_path = get_latex_file_save_compile(title_info_dict,latex_template_path)
    pdf_out_path_collect_list.append(pdf_out_path)

if __name__ == '__main__':
    txt_file_path="D:\myFiles\forCoding\auto_article_latex_pdf_voice_video\text_files\samplesample.txt"
    main(txt_file_path)