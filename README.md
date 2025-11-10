# 10ssonBase 批量下注脚本

## 功能概览
- 基于 USDC EIP-712 `TransferWithAuthorization`，批量签名并向 10ssoon 平台提交 `x420` 下注订单
- 自动按照钱包顺序交替提交 `up / down` 方向，支持多线程并在多轮循环中反复执行
- 通过 `CONFIG` 可配置目标合约、下注金额、线程数量、最大执行次数及代理地址

> ⚠️ **重要**：脚本需要使用明文私钥，请仅在可信的离线或隔离环境运行，并自行承担资金与账号安全风险。

## 仓库结构
| 文件 | 说明 |
| --- | --- |
| `main.py` | 核心脚本，读取私钥、构造 EIP-712 签名并调用 `https://api.10ssoon.com/payment/bet` |
| `pyproject.toml` | 依赖声明（Python >= 3.13，`curl-cffi` / `loguru` / `web3`）|
| `uv.lock` | `uv sync` 使用的锁定文件，确保每个人安装到相同版本 |
| `keys.txt` | 你的真实地址和私钥列表（运行前必须创建并放在仓库根目录）|


## 环境要求
- macOS / Linux / Windows (PowerShell) 均可，需联网访问 10ssoon API。
- Python 3.13 或更高版本（`pyproject.toml` 的最低要求；3.11+ 实测也能安装全部依赖）。
- 安装最新 Git（便于拉取代码）以及终端工具（bash / PowerShell）。
- `uv` 包管理工具（推荐）或 `pip`，二选一。

## 准备 `keys.txt`
1. 在仓库根目录创建 `keys.txt`。
2. 每行代表一个钱包，格式固定为：`钱包地址----私钥`，中间用四个连字符且不要加空格。
3. 示例：
   ```text
   0x1B279259B4A221d019C990BCD860ffA6BFDA9153----0x64080929b81767a643fdb105af161da0b581fb8a7af542e96bc0ebd5d6005c53
   0x1B279259B4A221d019C990BCD860ffA6BFDA9153----0x64080929b81767a643fdb105af161da0b581fb8a7af542e96bc0ebd5d6005c53
   ```
4. 空行或没有 `----` 的行会被跳过；如果私钥缺失脚本会报错。
5. `address.csv` 里的 `address`、`private key` 列等同于上面的信息，可用表格或脚本转换成 `keys.txt`。

## 配置项（`main.py` 顶部 `CONFIG`）
| 键 | 默认值 | 说明 |
| --- | --- | --- |
| `x420TokenAddress` | `0x0FE812a6BA666284e0c414646e694a53F1409393` | 下注时使用的合约地址，如有更新手动替换 |
| `UsdcAmount` | `"1"` | 单笔下注使用的 USDC 数量（字符串，6 位小数精度）|
| `threadCount` | `100` | 并发线程数；如果钱包数量少于该值会退化为钱包数 |
| `totalMintCount` | `100000` | 每轮最多处理的钱包数量（防止一次读取过多账户）|
| `proxy` | `None` | 可填 `http://user:pass@host:port` 等代理字符串，解决 429 或地区限制 |

脚本还定义 `ROUNDS = 10`，也就是会完整跑 10 轮；需要减少/增加可自行改动。

## 安装与运行
### 1. 获取源码
```bash
git clone <你的仓库地址>
cd 10ssonBase
```

### 2. 使用 `uv`（推荐）
1. **安装 `uv`**
   - macOS/Linux：`curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows (PowerShell)：`powershell -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"`
   - 安装后重新打开终端，并确认 `uv --version` 正常输出。
2. **创建并激活虚拟环境**
   ```bash
   uv venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```
3. **安装依赖**
   ```bash
   uv sync
   ```
   `uv sync` 会读取 `pyproject.toml + uv.lock` 自动安装 `curl-cffi`、`loguru`、`web3` 以及其依赖（会拉取 `eth-account`）。
4. **运行脚本**
   ```bash
   uv run python main.py
   ```

### 3. 不方便安装 `uv`？使用 `pip`

1. 安装基础工具并安装依赖：
   ```bash
   pip install curl-cffi loguru web3 eth-account
   ```
3. 运行：
   ```bash
   python main.py
   ```

## 运行时你会看到
- `loguru` 的多条 `Author: 0xNaixi` 提示表示脚本启动成功。
- `钱包数量...`：读取到了多少 `keys.txt` 中的钱包，并统计本轮会用几个线程。
- `✅ 下单成功...` / `❌ 下单失败...`：接口返回内容，会包含方向、价格、订单号或错误详情。
- 每轮结束后有 `成功/失败` 汇总，间隔 1 秒进入下一轮。

按 `Ctrl + C` 可中断运行；脚本不会自动重试被视为失败的钱包，可调低 `threadCount` 或 `ROUNDS` 做小额测试。

## 常见问题 & 建议
- **`curl_cffi` 安装失败**：请先安装 Rust 构建链（macOS: `xcode-select --install`，Windows: 安装 Build Tools）并确认使用的是 64 位 Python；或使用 `uv sync` 自动下载预编译 wheel。
- **Windows 找不到 `python` 命令**：在 PowerShell 使用 `py -3` 代替，并确保在“应用和功能”里勾选了 `Add python.exe to PATH`。
- **API 返回 `429 Too Many Requests`**：调小 `threadCount`、增加 `time.sleep`，或在 `CONFIG["proxy"]` 填写可用代理地址。
- **安全建议**：`keys.txt` 不要上传到任何版本库，完成操作后立即删除或移动到安全位置。

完成以上步骤后，你就可以在本地复现 `main.py` 的全部功能。祝使用顺利！
