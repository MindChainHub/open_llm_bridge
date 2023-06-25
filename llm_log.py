class LLMLog:
    req: dict = {}

    # req_at: int = 0
    req_url: str = ''
    req_header: dict = {}
    status_code: int = 0
    rsp_content: str = ''
    #
    model: str = ''  # rsp中不一定有,如azure的cmpl接口
    skp: str = ''
    chain: str = ''
    match_path: str = ''

    def log(self):
        print(f"""
        url {self.req_url}
        req {self.req}
        header {self.req_header}
        status {self.status_code}
        rsp {self.rsp_content}
        model {self.model}
        skp {self.skp}
        chain {self.chain}
        match {self.match_path}
        """)
