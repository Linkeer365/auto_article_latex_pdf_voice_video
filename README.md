# auto_article_latex_pdf_voice_video

auto_article_latex 和 simple_video_generate 结合起来，修改了大量冗余的代码

因为records内容太多不好上传先删掉了，旧的可以到 auto_article_latex 和 simple_video_generate 去看看

## 整体逻辑

1. `text_files` 里面存放待处理的文章（按照一定规则约束并格式化），db存在check后，在`get_title_infos.py`当中提取文件标题、作者、行文日期 等信息

2. 以 `stable\poem_essay_template_new.tex` 为模板，生成tex文件并编译为pdf（写入db）

3. 将pdf文件按页抽取出文本+图片，同时通过文本获取音声文件。这些都放在`records\*\pic_mp3\`下面

> （例如对应pdf第1页：`文本文件001.txt`，`音声文件001.mp3`，`图片文件001.jpg`，这里pdf最多不超过1000页）

4. 将形如（音声文件001.mp3，图片文件001.jpg）的文件，通过ffmpeg合成为：`视频文件001.mp4`，命令如下：

> ffmpeg -loop 1 -i <your-pic-file-path> -i <your-audio-file-path> -vf "scale=2*trunc(iw/2):2*trunc(ih/2),setsar=1" -c:v h264_nvenc -b:v 10000k -c:a aac -b:a 192k -shortest <your-video-file-path> -y

5. 把形如（`视频文件001.mp4`，`视频文件002.mp4`...）的文件通过ffmpeg进行merge，形成最终文件