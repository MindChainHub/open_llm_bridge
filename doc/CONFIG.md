## Config

- BRG_CONFIG_VARS:
    - set LLM channel `base_url`, `ctx` ...

```json5
{
  "openai_base": "https://api.openai.com",
  "openai_ctx": "/v1",
  "azure_base": "https://swarm.openai.azure.com",
  "azure_ctx": "/openai/deployments",
  "az_deploy_chat_cmpl": "/gpt35",
  // **NOTE** set `deployment` instead `model`
  "az_deploy_cmpl": "/text-davinci-003",
  "az_deploy_emb": "/embedding",
}
```

- BRG_CONFIG:
    - set _match_config, _channel_route,_req_url

```json5
// BRG_CONFIG 
{
  // _match_config
  "/chat/completions": {
    // channel : <IN_Channel, OUT_Channel>
    "_channel_route": {
      "openai": "openai",
      "azure": "azure"
    },
    // _math_path:      <Channel, Target Path>
    "_req_url": {
      "openai": "{openai_base}{openai_ctx}/chat/completions",
      "azure": "{azure_base}{azure_ctx}{az_deploy_chat_cmpl}/chat/completions?api-version=2023-05-15",
    }
  },
  "/embeddings": {
    "_channel_route": {
      "openai": "openai",
      "azure": "azure"
    },
    "_req_url": {
      "openai": "{openai_base}{openai_ctx}/embeddings",
      "azure": "{azure_base}{azure_ctx}{az_deploy_emb}/embeddings?api-version=2023-05-15",
    }
  },
  "/completions": {
    "_channel_route": {
      "openai": "openai",
      "azure": "azure"
    },
    "_req_url": {
      "openai": "{openai_base}{openai_ctx}/completions",
      "azure": "{azure_base}{azure_ctx}{az_deploy_cmpl}/completions?api-version=2023-05-15",
    }
  },
  "-": {
    "_channel_route": {},
    "_req_url": {
      "openai": "{openai_base}",
      "azure": "{azure_base}",
    }
  }
}
```

## Test

```shell
curl http://127.0.0.1:9000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $YOUR_SK" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}]
  }'
```