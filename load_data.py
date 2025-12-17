# 把数据字典（small_ocr_content_list.json）里的内容，批量存进数据库
from qdrant import QdrantDB
import json
import os

# 1. 找到数据字典文件
json_file_path = "small_ocr_content_list.json"
if not os.path.exists(json_file_path):
    print("没找到small_ocr_content_list.json文件。")
    exit()

# 2. 打开数据字典，读里面的内容
with open(json_file_path, "r", encoding="utf-8") as f:
    data_list = json.load(f)  # 把字典里的所有数据读出来

# 3. 创建数据库实例（调用之前改好的QdrantDB）
db = QdrantDB()

# 4. 把每一条数据都存进数据库
print("开始往数据库里存知识啦...总共要存", len(data_list), "条数据")
for idx, data in enumerate(data_list):
    # 1：读取json里的「text」字段
    text = data.get("text", "").strip()  # 去掉文本前后的空格
    # 2：读取页码（page_idx是数字，+1变成咱们习惯的“第X页”）
    page_num = data.get("page_idx", 0) + 1  # 比如page_idx=0 → 第1页
    if not text:  # 跳过空文本（json里有些text是""，不用存）
        continue
    # 3：来源文件名设为“第X页”
    source_file = f"第{page_num}页"
    
    # 调试：打印准备存储的数据信息
    print(f"\n[load_data] 处理第{idx+1}条数据")
    print(f"[load_data] page_idx原始值: {data.get('page_idx')} → 转换后页码: {page_num}")
    print(f"[load_data] source_file生成: {source_file}")
    print(f"[load_data] 文本内容前50字符: {text[:50]}...")
    
    
    db.save_text(text=text, source_file=source_file)
    if (idx + 1) % 10 == 0:  # 每存10条提示一下
        print(f"已经存了{idx+1}条啦...")

print("全部存完啦！数据都放进数据库里了！")