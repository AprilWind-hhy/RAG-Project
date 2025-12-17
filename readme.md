# 智能RAG对话系统

## 项目简介

本项目是一个基于CAMEL-AI 框架的智能RAG对话系统，应用通过**向量数据库**存储相关知识，并结合大模型生成自然语言回答，提供直观的网页交互界面。

## 环境准备

### 第一步：创建并激活虚拟环境

确保使用 Python 3.10 版本以保证兼容性：

```
conda create -n your_env_name python=3.10
conda activate your_env_name
# 验证Python版本
python --version
# 预期输出类似：Python 3.10.19
```

### 第二步：安装核心依赖包

1. **安装 CAMEL-AI 框架**

```
pip install camel-ai[all]

# 验证安装
pip show camel-ai
# 预期输出包含：Version: 0.2.80

#CAMEL-AI技术指导：
#参考文档: https://docs.camel-ai.org/
#参考Tutorial: : https://fmhw1n4zpn.feishu.cn/docx/AF4XdOZpIo6TOaxzDK8cxInNnCe
#语⾔: Python 3.10-3.12
```

2. **安装 Qdrant 向量数据库客户端**

```
pip install qdrant-client
```

3. **安装句子嵌入模型工具**

```
pip install sentence-transformers
```

4. **安装 LLM 相关组件**

```
pip install transformers torch
```

5. **安装 Streamlit 前端框架**

```
pip install streamlit
```

## 项目结构

```
.
├── chat_app.py          # 主应用程序，包含聊天界面和核心逻辑
├── vector_retriever.py  # 向量检索器实现
├── qdrant.py            # Qdrant数据库操作类
├── load_data.py         # 数据加载脚本，用于将知识导入数据库
└── small_ocr_content_list.json  # 原始知识数据
```

## 运行步骤

1. **加载知识到数据库**

```
python load_data.py
# 程序会将small_ocr_content_list.json中的文本内容导入向量数据库
# 运行成功后会显示"全部存完啦！数据都放进数据库里了！"
```

2. **启动聊天应用**

```
streamlit run chat_app.py
# 程序会自动启动本地服务器，并在浏览器中打开聊天界面
# 若未自动打开，可手动访问终端中显示的本地地址（通常是http://localhost:8501）
```
3. **运行界面**

![image-20251217132303093](C:\Users\90511\AppData\Roaming\Typora\typora-user-images\image-20251217132303093.png)

4. **运行效果**

   ![image-20251217132443608](C:\Users\90511\AppData\Roaming\Typora\typora-user-images\image-20251217132443608.png)
## 使用说明

1. 应用启动后，界面会显示 5 个测试问题供参考。也可以脱离测试问题，问其他的问题。

1. 在底部输入框中输入您的问题，例如："什么是商品的使用价值？"

1. 系统会先检索相关知识，然后生成回答并显示来源。

1. 聊天记录会保存在页面中，方便查看历史对话。

## 核心功能

- 向量检索：通过 Qdrant 向量数据库快速查找与问题相关的知识。

- 智能回答：利用大模型将检索到的知识转化为通俗易懂的自然语言回答。

- 对话记忆：保存历史聊天记录，支持连续对话。

- 来源标注：显示回答所参考的知识来源，提高可信度。

## 注意事项

- 首次运行 load_data.py 时，会下载嵌入模型，可能需要较长时间（取决于网络状况）。
- 本项目提供了一份简单的数据文件，可以直接使用。也可以使用其它的的数据文件。
- 确保网络连接正常，以便模型能够正常加载和运行。
- 若遇到模型加载失败，可检查 MODELSCOPE_SDK_TOKEN 是否有效。"# RAG-Project" 
