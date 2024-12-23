# verifiyer
Blockchain CTF flag provider through standardized testnet on-chain contract interface

## Setup
1. Compile `templates/Setup.sol`
2. Spawn docker
```
docker run -t verifiyer -e SETUP_BYTECODE=0x... -e DIFFICULTY=6 -e CONSTRUCTOR_VALUE=1 -e PRIVATE_KEY=0x... -e RPC=... -e FLAG=flag{test} -e PORT=1337
```