import os
os.environ["MODELSCOPE_CACHE"] = "./modelscope_cache"
from dotenv import load_dotenv 
load_dotenv()
MODELSCOPE_SDK_TOKEN = os.getenv("MODELSCOPE_SDK_TOKEN")  

import streamlit as st
from qdrant import QdrantDB
from vector_retriever import VecRetriever
from camel.models import ModelFactory

# 1. 初始化工具
@st.cache_resource  # 让工具只加载一次，不重复加载
def init_all_tools():
    # 创建数据库并连接
    db = QdrantDB()
    # 创建检索器
    retriever = VecRetriever(qdrant_db=db)
    # 创建翻译官（用modelscope平台的中文模型）
    llm = ModelFactory.create(
        model_platform="modelscope",  # 指定modelscope平台
        model_type="deepseek-ai/DeepSeek-R1-0528",  
        model_config_dict={  # 模型配置参数
            "temperature": 0.6
        }
    )
    return retriever, llm

# 2. 加载所有工具
retriever, llm = init_all_tools()

# 3. 设计聊天窗口界面
st.title("智能RAG对话系统")
st.markdown("""
测试问题1：什么是商品的使用价值？  
测试问题2：交换价值是什么？  
测试问题3：商品的价值是由什么决定的？  
测试问题4：什么是社会必要劳动时间？  
测试问题5：劳动的二重性指什么？
""")

# 4. 存储聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 显示之前的聊天记录
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 6. 让用户输入问题
if prompt := st.chat_input("请输入你的问题呀～"):
    # 记录用户的问题
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 7. 找知识：用检索器找抽屉里相关的3条知识
    st.write("小助手正在找答案...")
    retrieved_results = retriever.search(question=prompt, top_k=3)  # 找3条最相关的

    # 新增：显示应召回内容（检索到的原始文本）
    st.write("### 应召回内容：")
    for result in retrieved_results:
        st.write(f'"{result["content"]}"')  # 用引号包裹原始文本

    # 8. 整理找到的知识（给翻译官看）
    context = ""
    sources = []
    for idx, result in enumerate(retrieved_results, 1):
        context += f"相关知识{idx}：{result['content']}\n\n"
        sources.append(f"答案来源：{result['file_name']}")
    if not context:
        st.chat_message("assistant").write("哎呀，我没找到相关的知识呢～ 换个问题试试呀？")
        st.session_state.messages.append({"role": "assistant", "content": "没找到相关知识，换个问题试试～"})
        st.stop()  # 没有知识就停止后续处理

    # 9. 让翻译官把知识变成大白话
    prompt_for_llm = f"""
    请你用通俗易懂的话回答用户的问题，只说和问题相关的内容，不要说复杂术语，尽量简短。
    参考下面的相关知识：
    {context}
    用户的问题是：{prompt}
    """
    messages = [{"role": "user", "content": prompt_for_llm}]
    # 调用模型的客户端接口
    response = llm._client.chat.completions.create(
        model=llm.model_type,
        messages=messages,
        max_tokens=1024,
        **llm.model_config_dict
    )
    answer = response.choices[0].message.content.strip()

    # 10. 显示示例答案（带来源）
    st.write("### 示例答案：")
    final_answer = answer.strip() + "\n\n" + "\n".join(sources)
    st.chat_message("assistant").write(final_answer)
    st.session_state.messages.append({"role": "assistant", "content": final_answer})