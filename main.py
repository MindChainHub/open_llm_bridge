"""
Open LLM Bridge
"""
import json
import os
from datetime import datetime
from typing import Callable

# 没有的键值对代表model相同(注意,映射关系是单向,不可反向调用)
CVT_MODEL_NAME_OPENAI_AZURE = {
    "gpt-3.5-turbo": "gpt-35-turbo",
    # "text-embedding-ada-002": "text-embedding-ada-002",
}
CVT_MODEL_NAME_AZURE_OPENAI = {
    "gpt-35-turbo": "gpt-3.5-turbo",
    # "text-embedding-ada-003": "text-embedding-ada-002",
}

CVT_CONFIG_VARS = json.loads(os.environ.get(
    'CVT_CONFIG_VARS')) if os.environ.get('CVT_CONFIG_VARS') else {
    "openai_base": "https://api.openai.com",
    "openai_ctx": "/v1",
    "azure_base": "https://swarm.openai.azure.com",
    "azure_ctx": "/openai/deployments",
    "az_deploy_chat_cmpl": "/gpt-35-turbo",
    # azure的body内不允许 “model"字段, 因此可以通过使用同名的deployment,以便区分不同model
    "az_deploy_cmpl": "/text-davinci-002",
    "az_deploy_emb": "/text-embedding-ada-002",
}

CVT_CONFIG = json.loads(os.environ.get(
    'CVT_CONFIG')) if os.environ.get('CVT_CONFIG') else {
    # _match_config: <...配置>
    "/chat/completions": {
        # channel 路由: <IN_Channel, OUT_Channel> (配置不同的 IN_和OUT_ 可能会因为返回值格式不同而导致错误)
        "_channel_route": {"openai": "openai", "azure": "azure"},
        # 路径配置:      <Channel, 匹配路径>
        "_req_url": {
            "openai": "{openai_base}{openai_ctx}/chat/completions",
            "azure": "{azure_base}{azure_ctx}{az_deploy_chat_cmpl}/chat/completions?api-version=2023-05-15",
        }
    },
    "/embeddings": {
        "_channel_route": {"openai": "openai", "azure": "azure"},
        "_req_url": {
            "openai": "{openai_base}{openai_ctx}/embeddings",
            "azure": "{azure_base}{azure_ctx}{az_deploy_emb}/embeddings?api-version=2023-05-15",
        }
    },
    "/completions": {
        "_channel_route": {"openai": "openai", "azure": "azure"},
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


class ReqConverter:

    # 暂不使用
    # default_model_route = {
    #     "gpt-3.5-turbo": "id_chn_llm_gpt35",
    #     "gpt-3.5-turbo-16k": "id_chn_llm_gpt35_16k",
    #     "gpt-3.5-turbo-0301": "id_chn_llm_gpt35",
    #     "gpt-3.5-turbo-0613": "id_chn_llm_gpt35",
    #     "gpt-3.5-turbo-16k-0613": "id_chn_llm_gpt35_16k",
    #     "gpt-4": "id_chn_llm_gpt4",
    #     "gpt-4-0314": "id_chn_llm_gpt4",
    #     "gpt-4-0613": "id_chn_llm_gpt4",
    #     "text-embedding-ada-002": "id_chn_llm_text_embedding_ada002"
    # }

    def __init__(
            self, config_vars: dict,
            config: dict,
            # model_route: dict,
            on_get_key: Callable[[str, str], str]
    ):
        """
        :param config_vars:
        :param config: 全局路由
        :param on_get_key: (headers, IN-channel, OUT-channel) -> (authed headers, wsk)
        ==
        channel: openai, azure; 用于区分源
        """
        self.config_vars: dict = config_vars
        self.config: dict = config
        self.on_get_key = on_get_key
        self._match_path: str  # 匹配路径 (/chat/completions, 等等)
        self._match_config: dict  # 匹配路径 对应的配置文件
        self._in_channel: str  # openai, azure
        self._in_model: str  # gpt-3.5-turbo, gpt-4, text-embedding-ada-002
        self._in_auth: str  # wsk
        self._in_headers: dict = {}  # 请求头
        self._in_body: dict = {}  # 请求体
        # self._in_query: str  # 请求参数, 如 api-version=2023-05-15
        self._out_channel: str
        self._out_model: str
        self._out_auth: str
        self._out_headers: dict = {}
        self._out_body: dict = {}
        self._out_url: str  # (base_path + path)

    def update_all_channel_route(self, channel_route: dict):
        for k, v in self.config.items():
            self.update_channel_route(k, channel_route)

    def update_channel_route(self, path: str, channel_route: dict):
        self.config[path]["_channel_route"] = channel_route

    def build(self, path: str, headers: dict, body: dict, query: str) -> (str, dict, dict):
        """
        接收http请求
        :param path: 请求路径(路径信息,deploymentId/model信息,)
        :param query: Azure会附带查询参数 ‘api-version=2023-5-15’
        :param headers: 请求头(Auth信息)
        :param body: 请求体(model信息)
        :return:
        """
        # == 环境准备
        self._config_match_config(path)
        self._config_channel(path)
        self._in_headers = headers
        self._in_body = body
        # == IN_ 处理
        if self._in_channel == "openai":
            self._set_in_openai()
        elif self._in_channel == "azure":
            self._set_in_azure(path=path)
        else:
            raise Exception(f"unknown in_channel[{self._in_channel}]")
        # == OUT_ 处理
        if self._out_channel == "openai":
            self._set_out_openai(path=path)
        elif self._out_channel == "azure":
            self._set_out_azure(path=path)
        else:
            raise Exception(f"unknown out_channel[{self._out_channel}]")
        print(f"### {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} OUT) {self._out_url}")
        # print(f"IN# {self._in_channel} {self._in_model} {self._in_auth}\n"
        #       f"OUT {self._out_channel} {self._out_model} {self._out_auth}")
        # print(f"{self._out_body}")
        return self._out_url, self._out_headers, self._out_body

    def _set_out_azure(self, path: str):
        self._out_auth = self.on_get_key(self._in_auth, self._out_channel)

        if self._in_channel != self._out_channel:
            self._out_model = CVT_MODEL_NAME_OPENAI_AZURE.get(self._in_model, self._in_model)
            self._out_headers = self._in_headers
            self._out_headers['api-key'] = self._out_auth
        else:
            self._out_model = self._in_model
            self._out_headers = self._in_headers

        if self._match_path == '/chat/completions' or self._match_path == '/embeddings':
            self._out_body = self._in_body
            self._out_url = self._match_config["_req_url"][self._out_channel].format(**self.config_vars)
        elif self._match_path == '/completions':
            for k, v in self._in_body.items():  # azure AI, completion无‘model’字段
                if k != "model":
                    self._out_body[k] = v
            self._out_url = self._match_config["_req_url"][self._out_channel].format(**self.config_vars)
        else:
            # 未配置路径,透明代理
            self._out_url = self._match_config["_req_url"][self._out_channel].format(**self.config_vars) + path

    def _set_out_openai(self, path: str):
        if self._in_channel != self._out_channel:
            self._out_model = CVT_MODEL_NAME_AZURE_OPENAI.get(self._in_model, self._in_model)
            self._out_headers = self._in_headers
            self._out_headers['authorization'] = f'Bearer {self._out_auth}'
        else:
            self._out_model = self._in_model
            self._out_headers = self._in_headers

        self._out_auth = self.on_get_key(self._in_auth, self._out_channel)
        self._out_headers = self._in_headers
        if ['/chat/completions', '/embeddings', '/completions'].__contains__(self._match_path):
            self._out_body = self._in_body
            self._out_body['model'] = self._out_model
            self._out_url = self._match_config["_req_url"][self._out_channel].format(**self.config_vars)
            # azure AI, completion无‘model’字段
            for k, v in self._in_body.items():
                if k != "model":
                    self._out_body[k] = v
            self._out_url = self._match_config["_req_url"][self._out_channel].format(**self.config_vars)
        else:
            # 未配置路径,透明代理
            self._out_url = self._match_config["_req_url"][self._out_channel].format(**self.config_vars) + path

    def _set_in_openai(self, ):
        # openai 3种 match_path都支持从body获得model
        self._in_model = self._in_body["model"]
        self._in_auth = self._in_headers.get("authorization", 'Bearer ')[7:]

    def _set_in_azure(self, path: str):
        if self._match_path == '/chat/completions' or self._match_path == '/embeddings':
            self._in_model = self._in_body["model"]
        elif self._match_path == '/completions':
            self._in_model = path[20:-12]  # /openai/deployments/text-davinci-002/completions
        self._in_auth = self._in_headers.get("api-key", '')

    def _config_match_config(self, path: str):
        self._match_path = path
        if path == '':
            self._match_path = '-'
        elif path.endswith("/chat/completions"):
            self._match_path = "/chat/completions"
        elif path.endswith("/embeddings"):
            self._match_path = "/embeddings"
        elif path.endswith("/completions"):
            self._match_path = "/completions"
        else:
            self._match_path = '-'
            print(f"未配置的路径, 透明代理处理[{path}]")
        self._match_config: dict = self.config.get(self._match_path, '-')
        if not self._match_config:
            raise Exception('请配置 透明路由[-] 规则')

    def is_transparent(self) -> bool:
        """是否透明代理"""
        return self._match_path == '-'

    def _config_channel(self, path: str) -> (str, str):
        """
        todo 当前是根据path来判断channel, 也可以考虑用 headers(sk附加信息), body参数 等来判断
        :param path:
        :return: (IN_channel, OUT_channel) (openai | azure)
        """
        self._in_channel = "azure" if path.__contains__("/openai/deployments") else "openai"

        self._out_channel = self._match_config['_channel_route'].get(self._in_channel, self._in_channel)
        return self._in_channel, self._out_channel

    def get_wsk(self):
        """在认证完成后, 会设置wsk, 用于日志记录"""
        return self._in_auth

    def get_match_path(self):
        return self._match_path

    def get_model(self):
        return self._in_model
