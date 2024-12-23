# verifiyer
Blockchain CTF flag provider through standardized testnet on-chain contract interface

## Setup
1. Deploy `templates/Setup.sol`
2. Spawn docker
```
docker run -t verifiyer -e SETUP_ADDRESS=0x... -e RPC=... -e FLAG=flag{test} -e PORT=1337
```