#!/usr/bin/env python3

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.background import BackgroundTask
from utils import OverrideStreamResponse
import bridge

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 设置允许的来源（* 表示允许所有来源）
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许的 HTTP 方法（* 表示允许所有方法）
    allow_headers=["*"],  # 设置允许的 HTTP 头（* 表示允许所有头）
)


async def proxy_openai_api(request: Request):
    path = request.url.path

    body = await request.json() if request.method in {'POST', 'PUT'} else None
    ##
    req_cvt = bridge.ReqConverter(
        config_vars=bridge.CVT_CONFIG_VARS,
        config=bridge.CVT_CONFIG,
        # Replace to your sk convert logic
        on_get_key=lambda skp, out_chl: skp,
    )
    # 修改配置 IN_ openai -> OUT_ azure
    req_cvt.update_all_channel_route({"openai": "azure"})

    req_url, req_headers, request_body = req_cvt.build(
        path=path,
        query=request.url.query,
        headers={k: v for k, v in request.headers.items() if
                 k not in {'host', 'content-length', 'x-forwarded-for', 'x-real-ip', 'connection'}},
        body=body,
    )

    # =====
    client = httpx.AsyncClient()

    async def stream_api_response():
        try:
            st = client.stream(
                headers=req_headers,
                method=request.method,
                url=req_url,
                params=request.query_params,
                json=request_body,
            )
            async with st as res:
                response.status_code = res.status_code
                response.init_headers({k: v for k, v in res.headers.items() if
                                       k not in {'content-length', 'content-encoding', 'alt-svc'}})

                content = bytearray()
                async for chunk in res.aiter_bytes():
                    yield chunk
                    content.extend(chunk)

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=500,
                detail={"message": f"{type(exc)}#{exc}", "type": "MindAI Internal Error",
                        "code": "mindai_internal_error"}
            )

    async def update_log():
        # if you need log after request
        pass

    response = OverrideStreamResponse(stream_api_response(), background=BackgroundTask(update_log))
    return response


@app.route('/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def request_handler(request: Request):
    return await proxy_openai_api(request)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=9000, log_level="info", reload=True)
