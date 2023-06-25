# Open LLM Bridge

Open LLM Bridge is an open-source project that provides a unified interface for accessing various Language Model (LLM)
APIs. It allows users to configure and utilize different LLM APIs based on their preferences. The project is built using
Python 3.10, FastAPI framework, and runs on Uvicorn.

## Features

- **Stream Support**: Open LLM Bridge supports stream-based data transmission, enabling efficient processing of large
  text inputs.
- **OpenAI API Compatibility**: The project includes support for accessing Azure APIs using the OpenAI API format,
  facilitating seamless integration with Azure LLM services.
- **Language Expansion**: Open LLM Bridge is designed to be easily extendable to support additional LLM APIs for
  different programming languages.
- **Token-based Billing**: The project includes token-based billing functionality, allowing users to manage and track
  their API usage and costs effectively.

## Getting Started

```shell
# Clone the repository
git clone https://github.com/your-username/open-llm-bridge.git

# Install the required dependencies:
pip install -r requirements.txt

# Start the server using Uvicorn:
uvicorn main:app --host 127.0.0.1 --port 8000
```

## Project Progress and Future Roadmap

- **API Bridge Completion:**
  - OpenAI -> OpenAI: Stable
  - OpenAI -> AzureAI: Stable
  - AzureAI -> OpenAI: Preview
  - AzureAI -> AzureAI: Stable

- **Token Billing:**
  - OpenAI: Stable
  - AzureAI: Stable

- **Future Plans:**
  - Support for additional LLMs: Planned


### Contributing
Contributions to `Open LLM Bridge` are welcome! If you encounter any bugs, have suggestions for improvements, or would like to add support for additional LLM APIs, please open an issue or submit a pull request.

### Acknowledgements
Special thanks to the author of the [openai-proxy](https://github.com/fangwentong/openai-proxy.git) repository for providing inspiration and valuable insights during the development of this project.