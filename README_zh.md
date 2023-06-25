# Open LLM Bridge

Open LLM Bridge是一个开源项目，为访问各种语言模型（LLM）API提供了统一的接口。它允许用户根据自己的偏好配置和利用不同的LLM
API。该项目使用Python 3.10、FastAPI框架构建，并在Uvicorn上运行。

## 特点

- **Stream支持**：Open LLM Bridge支持`/chat/completion`的Stream数据传输。
- **跨LLM桥接**：该项目支持使用OpenAI API格式访问Azure API，方便与Azure LLM服务的无缝集成。
- **Token的计费**：该项目包括基于 [TikToken](https://github.com/openai/tiktoken) 的计费功能，允许用户有效地管理和跟踪其API使用和成本。

## 入门指南

### 安装
```shell
# 克隆存储库
git clone https://github.com/your-username/open-llm-bridge.git;

# 安装所需依赖：
pip install -r requirements.txt;

# 使用Uvicorn启动服务器：
uvicorn main:app --host 127.0.0.1 --port 8000;
```
### 配置

重命名 `.env.example` 为 `.env`
参考 [Config.md](./doc/CONFIG.md)



## 项目进展和未来计划

### API桥接

|                  | `/chat` | `/cmpl` | `/embdd` |
|------------------|:-------:|:-------:|:--------:|
| OpenAI -> OpenAI |   ✔️    |   ️✔️   |    ✔️    |
| OpenAI -> Azure  |   ✔️    |   ️✔️   |    ✔️    |
| Azure -> OpenAI  |   ✔️    |   ✔️    |    ✔️    |
| Azure -> Azure   |   ✔️    |   ✔️    |    ✔️    |

### 未来计划：

    - 支持其他LLM
    - 完善计费功能
    - 支持sk转换

### 贡献

欢迎为`Open LLM Bridge`做出贡献！如果您遇到任何错误，有改进建议，或者希望添加对其他LLM API的支持，请提交问题或拉取请求。