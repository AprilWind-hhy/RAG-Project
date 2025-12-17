import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DOWNLOAD_URL"] = "https://hf-mirror.com"

from camel.storages import QdrantStorage
from camel.embeddings import SentenceTransformerEncoder
from camel.storages import VectorRecord
from camel.types import VectorDistance

class QdrantDB:
    """简单的Qdrant向量数据库操作类"""
    #"sentence-transformers/all-MiniLM-L6-v2"
    def __init__(self, model_name: str = "TencentBAC/Conan-embedding-v1"):
        """
        初始化Qdrant数据库
        
        任务：
        1. 设置数据存储路径
        2. 初始化embedding模型
        3. 创建QdrantStorage实例
        
        参数:
            model_name: huggingface模型名称
        """
        
        # 完成：设置rootpath（数据存储根目录，存在当前文件夹的qdrant_data里）
        self.rootpath = os.path.join(os.path.dirname(__file__), "qdrant_data")
        os.makedirs(self.rootpath, exist_ok=True) # 确保目录存在
        
        # 完成：初始化SentenceTransformerEncoder
        self.embedding_instance = SentenceTransformerEncoder(model_name=model_name)
        
        # 完成：初始化QdrantStorage（vector_dim是模型的向量维度，这个模型固定是1792）
        self.storage_instance = QdrantStorage(
            vector_dim=1792,
            path=self.rootpath,
            distance=VectorDistance.COSINE ,
            collection_name="knowledge_collection"
        )
    
    def save_text(self, text: str, source_file: str = "unknown"):
        """
        保存单个文本到数据库
        
        任务：
        1. 将文本转换为向量
        2. 创建VectorRecord
        3. 保存到数据库
        
        参数:
            text: 要保存的文本
            source_file: 文本来源文件名
        """
        print(f"\n[QdrantDB] 准备保存文本 - source_file: {source_file}")
        print(f"[QdrantDB] 文本内容前50字符: {text[:50]}...")  # 只打印前50字符避免过长
        # 完成：使用embedding_instance将文本转换为向量
        vectors = self.embedding_instance.embed_list([text])  # 把文本变成数字密码
        vector = vectors[0]  # 取第一个结果（因为只传了一段文本）
        print(f"生成的向量维度：{len(vector)}") 
        # 完成：创建payload字典，包含text和source_file信息
        payload = {
            "text": text,
            "metadata": {  # 新增metadata层级
                "source_file": source_file  # source_file放在metadata里
            }
        }
        print(f"[QdrantDB] 存储的payload - source_file: {payload['metadata']['source_file']}")
        print(f"[QdrantDB] payload文本前50字符: {payload['text'][:50]}...")
        
        # 完成：创建VectorRecord对象
        record = VectorRecord(
            vector=vector,
            payload=payload
        )
        
        # 完成：使用storage_instance.add()保存记录
        self.storage_instance.add(records=[record])
        
        # 调试：确认保存完成
        print(f"[QdrantDB] 记录保存成功 (source_file: {source_file})")


"""
# 1. 创建数据库实例
db = QdrantDB()
# 2. 保存文本
db.save_text("这是第一段文本", "文档1.txt")
db.save_text("这是第二段文本", "文档2.txt")
print("文本保存完成！")
"""