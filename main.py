import base64
import json
import os
import time
from curl_cffi import requests
from decimal import Decimal, ROUND_DOWN
from eth_account import Account
from eth_account.messages import encode_typed_data, encode_defunct
from web3 import Web3
from loguru import logger
from multiprocessing.dummy import Pool
CONFIG = {
    "x420TokenAddress": "0xbDbddBEd6360e45a7FE0550a9A4F1fAE4C5074e7",
    "UsdcAmount": "1",
    "threadCount": 100,
    "totalMintCount": 100000,
    "proxy":None # 填你的代理
}

USDC_BASE_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
CHAIN_ID = 8453


# ============= EIP-712 结构 =============
EIP712_TYPES = {
    "EIP712Domain": [
        {"name": "name", "type": "string"},
        {"name": "version", "type": "string"},
        {"name": "chainId", "type": "uint256"},
        {"name": "verifyingContract", "type": "address"},
    ],
    "TransferWithAuthorization": [
        {"name": "from", "type": "address"},
        {"name": "to", "type": "address"},
        {"name": "value", "type": "uint256"},
        {"name": "validAfter", "type": "uint256"},
        {"name": "validBefore", "type": "uint256"},
        {"name": "nonce", "type": "bytes32"},
    ],
}

EIP712_DOMAIN = {
    "name": "USD Coin",
    "version": "2",
    "chainId": CHAIN_ID,
    "verifyingContract": USDC_BASE_ADDRESS,
}

PRIMARY_TYPE = "TransferWithAuthorization"

# ============= 工具函数 =============
def random_bytes32_hex() -> str:
    """生成 32 字节的 0x 前缀 hex 字符串"""
    return "0x" + os.urandom(32).hex()

def mint(thread_id: int, wallet:dict, direction:str):
    # 初始化账户
    if not wallet["private_key"]:
        raise ValueError("请导入钱包。")
    account = Account.from_key(wallet["private_key"])
    logger.info(f"线程 {thread_id}: 使用账户 {account.address} 开始铸造。 方向: {direction}")
    # USDC 6 位小数
    usdc_amount_raw = Web3.to_wei(Decimal(CONFIG["UsdcAmount"]), "mwei")  # 6900000

    # 时间窗口
    max_timeout_seconds = 3000
    now_sec = int(time.time())
    valid_after = now_sec - 600
    valid_before = now_sec + max_timeout_seconds

    # 随机 32 字节 nonce（bytes32）
    nonce_hex32 = random_bytes32_hex()

    # EIP-712 message
    message = {
        "from": account.address,
        "to": CONFIG["x420TokenAddress"],
        "value": str(usdc_amount_raw),
        "validAfter": str(valid_after),
        "validBefore": str(valid_before),
        "nonce": nonce_hex32,
    }

    # 组装 typed data
    typed_data = {
        "types": EIP712_TYPES,
        "domain": EIP712_DOMAIN,
        "primaryType": PRIMARY_TYPE,
        "message": message,
    }

    # 签名（等价于 viem account.signTypedData）
    encoded_data = encode_typed_data(full_message=typed_data)
    signed_message = account.sign_message(encoded_data)
    signature = f"0x{signed_message.signature.hex()}"
    # logger.info(f"线程 {thread_id}: 签名完成，发送交易中...")

    # 组装 payment JSON 并 base64
    payment = {
        "x402Version": 1,
        "scheme": "exact",
        "network": "base",
        "payload": {
            "signature": signature,
            "authorization": message,
        },
    }

    payload_str = json.dumps(payment, separators=(',', ':'), ensure_ascii=False)
    payment_base64 = base64.b64encode(payload_str.encode('utf-8')).decode('utf-8')
    # 发送
    result = send(payment_base64,direction)
    if isinstance(result, dict) and result.get("code") == 0:
        data = result.get("data", {}) or {}
        logger.info(
            f"✅ 下单成功 | 方向: {data.get('direction', direction)} | 价格: {data.get('betPrice')} | 订单号: {data.get('orderId')}"
        )
    else:
        logger.error(f"❌ 下单失败 | 返回内容: {result}")

def send(payment_base64: str, direction:str,max_retries: int = 3):
    url = "https://api.10ssoon.com/sd_payment/bet"

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'access-control-expose-headers': 'X-PAYMENT-RESPONSE',
        'cache-control': 'no-cache',
        'content-type': 'text/plain;charset=UTF-8',
        'origin': 'https://richsoon.ai',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://richsoon.ai/',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'x-payment': payment_base64,
    }
    data = f'{{"option":{direction}}}'
    # logger.debug(data)
    attempt = 0
    while attempt < max_retries:
        try:
            resp = requests.post(url, data=data,headers=headers, timeout=360,proxy=CONFIG["proxy"],impersonate="chrome136")
            text = resp.text
            # logger.debug(text)
            if "failed to submit payment" in text.lower():
                return text
            if "429 Too Many Requests" in text:
                attempt += 1
                continue
            # 返回 JSON（与原代码保持一致）
            try:
                return resp.json()
            except ValueError:
                # 非 JSON 则返回文本
                return resp.text
        except Exception as e:
            attempt += 1
            print(f"❌ 发送交易 (第 {attempt} 次): {e}")
            if attempt >= max_retries:
                print("🚨 已达到最大重试次数，推送失败。")
                return None
            time.sleep(0.1)

def read_keys(file_path="keys.txt"):
    keys = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "----" not in line:
                    continue  # 跳过空行或格式不对的行
                address, private_key = [part.strip() for part in line.split("----", 1)]
                keys.append({"address": address, "private_key": private_key})
    except FileNotFoundError:
        logger.error(f"❌ 文件未找到: {file_path}")
        return []
    except Exception as e:
        logger.error(f"❌ 读取文件时出错: {e}")
        return []

    logger.success(f"✅ 已加载 {len(keys)} 个钱包")
    return keys


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == "__main__":
    logger.warning("Author: 0xNaixi")
    logger.warning("Author: 0xNaixi")
    logger.warning("Author: 0xNaixi")
    logger.warning("https://x.com/0xNaiXi")
    logger.warning("验证码平台 https://www.nocaptcha.io/register?c=hLf08E")

    walletInfos = read_keys()
    wallet_count = len(walletInfos)
    max_mint_count = CONFIG["totalMintCount"]

    if wallet_count == 1:
        total = max_mint_count
        thread_count = CONFIG["threadCount"]  # 或者保持 1，看你需求
    else:
        total = min(max_mint_count, wallet_count)
        thread_count = total  # 每个钱包一个线程

    logger.info(f"钱包数量: {wallet_count}, 实际执行任务数: {total}, 并发数: {thread_count}")
    # 奇偶判断涨跌，一涨一跌
    # args = [(i, walletInfos[i], "up" if i % 2 == 0 else "down") for i in range(total)]

    args = [
        (
            i,
            walletInfos[i],
            i % 3,  # 取余 3，结果依次为 0, 1, 2, 0, 1, 2 ...
        )
        for i in range(total)
    ]

    ROUNDS = 3

    for round_idx in range(1, ROUNDS + 1):
        logger.info(f"🚀 开始第 {round_idx}/{ROUNDS} 轮任务...")

        with Pool(thread_count) as pool:
            results = pool.starmap(mint, args, chunksize=1)

        # 可选：统计结果
        success = sum(1 for r in results if r and r.get("ok"))
        failed = len(results) - success
        logger.info(f"✅ 第 {round_idx} 轮完成 | 成功 {success} | 失败 {failed}")
        time.sleep(1)

