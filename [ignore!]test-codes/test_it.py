import os
import concurrent.futures
import psycopg2
from datetime import datetime
import uuid

def get_title_infos(txt_path):
    # 从文件中读取信息并生成新的内容
    with open(txt_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 假设我们从文件内容中提取信息
    title = "示例标题"  # 这里可以根据实际需要提取
    author = "示例作者"  # 这里可以根据实际需要提取
    date = "2024-08-22"  # 这里可以根据实际需要提取
    pe_type = "示例PE类型"  # 这里可以根据实际需要提取
    link = "http://example.com"  # 这里可以根据实际需要提取

    # 生成新的内容格式
    new_content = f"{title}\n{author}\n{date}\n{pe_type}\n{link}\n\n{content}"
    
    # 将新内容写入文件
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

    # 存储到数据库
    store_to_db(title, author, date, pe_type, link)

def store_to_db(title, author, date, pe_type, link):
    # 数据库连接参数
    db_config = {
        'dbname': 'lsyhome',
        'user': 'postgres',
        'password': 'xm111737',
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
    INSERT INTO lsyhome.article_infos (uuid, title, author, date, pe_type, link, create_datetime)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, (article_uuid, title, author, date, pe_type, link, create_datetime))

    # 提交事务并关闭连接
    conn.commit()
    cursor.close()
    conn.close()

def scan_txt_files(directory):
    # 扫描指定目录下的所有txt文件
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]

def main():
    # 获取用户输入的目录路径
    directory = input("请输入包含txt文件的目录路径: ")
    
    # 获取文件列表
    txt_files = scan_txt_files(directory)

    # 使用ProcessPoolExecutor进行多进程处理
    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
        executor.map(get_title_infos, txt_files)

if __name__ == "__main__":
    main()
