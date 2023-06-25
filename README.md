# Open LLM Bridge

[**简体中文**](./README_zh.md)

Open LLM Bridge is an open-source project that provides a unified interface for accessing various Language Model (LLM)
APIs. It allows users to configure and utilize different LLM APIs based on their preferences. The project is built using
Python 3.10, FastAPI framework, and runs on Uvicorn.

## Features

- **Stream Support**: Open LLM Bridge supports stream-based data transmission for `/chat/completion`.
- **LLM Bridging**: The project includes support for accessing Azure APIs using the OpenAI API format, facilitating seamless integration with Azure LLM services.
- **Token Billing**: The project includes token-based billing functionality based on [TikToken](https://github.com/openai/tiktoken), allowing users to effectively manage and track their API usage and costs.

## Getting Started

```shell
# Clone the repository
git clone https://github.com/your-username/open-llm-bridge.git;

# Install the required dependencies:
pip install -r requirements.txt;

# Start the server using Uvicorn:
uvicorn main:app --host 127.0.0.1 --port 8000;
```

## Project Progress and Future Roadmap

### API Bridge

|                  | `/chat` | `/cmpl` | `/embdd` |
|------------------|:-------:|:-------:|:--------:|
| OpenAI -> OpenAI |   ✔️    |   ️✔️   |    ✔️    |
| OpenAI -> Azure  |   ✔️    |   ️✔️   |    ✔️    |
| Azure -> OpenAI  |   ✔️    |   ✔️    |    ✔️    |
| Azure -> Azure   |   ✔️    |   ✔️    |    ✔️    |

### Future Plans:

- Support for additional LLMs
- Enhance billing functionality
- Support for SK conversion

### Contributing

Contributions to `Open LLM Bridge` are welcome! If you encounter any bugs, have suggestions for improvements, or would
like to add support for additional LLM APIs, please open an issue or submit a pull request.

### Acknowledgements

Special thanks to the author of the [openai-proxy](https://github.com/fangwentong/openai-proxy.git) repository for
providing inspiration and valuable insights during the development of this project.