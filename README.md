# verifiyer
Blockchain CTF flag provider through standardized testnet on-chain contract interface

## Setup
1. Compile `templates/Setup.sol`
2. Spawn docker
```
docker run -t verifiyer -e SETUP_BYTECODE=0x... -e DIFFICULTY=6 -e CONSTRUCTOR_VALUE=1 -e PRIVATE_KEY=0x... -e RPC=... -e FLAG=flag{test} -e PORT=1337
```
Or use docker compose
```yaml
services:
  challenge:
    image: hanzceo/verifiyer:0.3.0
    environment:
      - FLAG=
      - SETUP_BYTECODE=
      - CONSTRUCTOR_VALUE=
      - RPC=
      - PRIVATE_KEY=
      - PORT=
    ports:
      - "1337:1337"
```
