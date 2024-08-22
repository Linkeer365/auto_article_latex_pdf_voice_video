import re
import os
import shutil
import sys
import psycopg2
import uuid
from datetime import datetime

def store_to_db(title, author, date, pe_type, link, content,txt_path):
    # 数据库连接参数
    db_config = {
        'dbname': 'lsyhome',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',  # 根据实际情况修改
        'port': '5432'        # 根据实际情况修改
    }
    # 创建UUID和当前时间
    article_uuid = str(uuid.uuid4())
    create_datetime = datetime.now().strftime('%y%m%d %H:%M:%S')
    # 连接到数据库
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    # 插入数据
    insert_query = """
    INSERT INTO article_infos (article_uuid, article_title, article_author, article_publish_date, article_pe_type, article_link,article_content, article_txt_path, create_datetime)
    VALUES                    (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, (article_uuid, title, author, date, pe_type, link,content, txt_path, create_datetime))
    # 提交事务并关闭连接
    conn.commit()
    cursor.close()
    conn.close()

def get_title_infos(txt_path):
    with open(txt_path,'r',encoding='utf-8') as f:
        lines = f.readlines()
    # 必须顶格：
    # 第一行必定为标题；副标题用括号括一下
    title=lines[0].replace("标题：","",1).replace("\n",'')
    # 第二行必定为作者；
    author=lines[1].replace("作者：","",1).replace("\n",'')
    # 第三行必定为发表日期
    date=lines[2].replace("日期：","",1).replace("\n",'')
    # 第四行必定为pe类型
    pe_type=lines[3].replace("PE：","",1).replace("\n",'')
    # 第五行必定为网页链接
    url=lines[4].replace("链接：","",1).replace("\n",'')
    # 第六行必定为【正文】，且在下两行才是真正的“正文”（正文8行起）
    content_s='\n'.join(lines[7:])
    # 把 para_list 直接做到这个里面
    para_list = content_s.split("\n\n")
    title_infos = {
        '<Your-Title>':title,
        '<Your-Author>':author,
        '<Your-Date>':date,
        'poem_or_essay':pe_type,
        'filename':os.path.basename(txt_path),
        'filepath':txt_path,
        '<Your-Url>': url,
        'raw_content': content_s,
        'para_list': para_list
    }
    # 写入本地数据库
    store_to_db(title,author,date,pe_type,url,content_s,txt_path)
    return title_infos

def get_title_infos_by_input():
    title=input("题目:")
    author=input("作者:")
    date=input("日期:（英文空格隔开）（都没有就直接回车）").replace(" ","-")
    pe_flag=0
    while pe_flag == 0:
        pe=input("p or e (poem or essay):")
        if pe == "e":
            poem_or_essay = "essay"
            pe_flag=1
        elif pe == "p":
            poem_or_essay = "poem"
            pe_flag=1
    filename=input("filename(no .txt prefix inside!):")
    url=input("网页链接：（最好是archive后的）")
    title_infos = {
        '<Your-Title>':title,
        '<Your-Author>':author,
        '<Your-Date>':date,
        'poem_or_essay':poem_or_essay,
        'filename':filename,
        '<Your-Url>':url,
    }
    return title_infos

def main():
    title_info_dict = get_title_infos()

if __name__ == '__main__':
    main()
    