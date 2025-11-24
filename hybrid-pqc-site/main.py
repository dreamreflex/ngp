from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI()


class PQCFullInfo(BaseModel):
    # 协商结果
    tls_protocol: Optional[str]
    tls_cipher: Optional[str]
    tls_curve_raw: Optional[str]   # $ssl_curve 原始值
    tls_curve: Optional[str]       # 你映射后的友好名字
    pqc_status: str

    # 客户端能力
    client_ciphers: Optional[str]
    client_curves: Optional[str]

    # 附加 TLS 信息
    alpn: Optional[str]
    early_data: Optional[str]

    # 服务端配置（你在 nginx 里写死的）
    server_groups: Optional[str]

    # 一些方便展示的派生字段
    pqc_enabled: bool
    tls13: bool
    extra: Dict[str, str]


@app.get("/pqc-full", response_model=PQCFullInfo)
async def pqc_full(request: Request):
    h = request.headers

    tls_protocol   = h.get("x-tls-protocol")
    tls_cipher     = h.get("x-tls-cipher")
    tls_curve_raw  = h.get("x-tls-curve-raw")
    tls_curve      = h.get("x-tls-curve")          # pqc_group
    pqc_status     = h.get("x-pqc-status", "no_pqc")

    client_ciphers = h.get("x-tls-cipher-list")
    client_curves  = h.get("x-tls-curves-client")

    alpn           = h.get("x-tls-alpn")
    early_data     = h.get("x-tls-early-data")

    server_groups  = h.get("x-tls-server-groups")

    tls13_flag     = (tls_protocol == "TLSv1.3")
    pqc_enabled    = pqc_status != "no_pqc"

    return PQCFullInfo(
        tls_protocol=tls_protocol,
        tls_cipher=tls_cipher,
        tls_curve_raw=tls_curve_raw,
        tls_curve=tls_curve,
        pqc_status=pqc_status,
        client_ciphers=client_ciphers,
        client_curves=client_curves,
        alpn=alpn,
        early_data=early_data,
        server_groups=server_groups,
        pqc_enabled=pqc_enabled,
        tls13=tls13_flag,
        extra={
            "user_agent": h.get("user-agent", ""),
            "x_forwarded_for": h.get("x-forwarded-for", ""),
        }
    )
