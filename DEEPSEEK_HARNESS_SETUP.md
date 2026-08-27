# DeepSeek Harness — Setup & Usage Guide

**Added:** 2026-08-20  
**Repo:** [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)  
**License:** MIT

---

## What is DeepSeek Harness?

DeepSeek Harness (`dsh`) is an open-source AI agent harness by DeepSeek AI. It connects to DeepSeek's LLM API and provides a Web UI where you can chat with an AI agent that can:

- **Read and edit** all `.pa.yaml` source files in the repo
- **Run terminal commands** (repack msapp, run verification tools, git operations)
- **Maintain a plan** across multiple sessions
- **Delegate work** to sub-agents for complex tasks

---

## Prerequisites

| Requirement | Version | Install |
|-------------|---------|---------|
| Node.js | v22+ | `nvm install 22` |
| pnpm | v11+ | `npm install -g pnpm` |
| DeepSeek API Key | — | Free at [platform.deepseek.com](https://platform.deepseek.com/) |

---

## Quick Start

### 1. Get a DeepSeek API Key (Free)

1. Go to **https://platform.deepseek.com/**
2. Sign up / Log in
3. Navigate to **API Keys**
4. Create a new key
5. Copy it

### 2. Clone & Install (already done)

```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
```

### 3. Set Your API Key

```bash
# Option A: Export in your shell
export DEEPSEEK_API_KEY="sk-your-key-here"

# Option B: Create a .env file in the repo root
echo 'DEEPSEEK_API_KEY=sk-your-key-here' > deepseek-harness/.env
```

### 4. Launch the Web UI

```bash
# From the deepseek-harness directory
DSH_HOME=$(pwd) pnpm dsh web --no-open --port 3080
```

Open **http://127.0.0.1:3080** in your browser.

### 5. Configure in the Web UI

1. **Settings → Models** → Enter your DeepSeek API key → Save
2. **Choose workspace** → Add the `APP_MRMS_Project` directory → Select it
3. Start a session

---

## Usage for APP-MRMS

Once connected to the workspace (the APP-MRMS repo), the agent can:

### Read & Understand the Codebase
> "Summarize the scoping logic across all screens and identify inconsistencies."

### Fix Issues
> "Find all AccessibleLabel properties set to empty strings and add appropriate labels."

### Run Verification
> "Run the verify_powerfx.py and check_screen_registry.py tools and fix any errors."

### Rebuild the App
> "Rebuild the .msapp file using repack_msapp.py as the latest version."

### Documentation
> "Update KNOWN_ISSUES.md with the current status of all open items."

### Performance Analysis
> "Identify all ForAll/Sequence patterns in the codebase and suggest optimizations."

---

## Command Reference

| Command | Description |
|---------|-------------|
| `pnpm dsh web` | Start Web UI on http://127.0.0.1:3080 |
| `pnpm dsh web --port 8080` | Start on custom port |
| `pnpm dsh web --no-open` | Start without opening browser |
| `pnpm dsh --profile headless "task"` | Run one task and exit |
| `pnpm dsh plugin --profile web install` | Manage profile plugins |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | Yes | Your DeepSeek API key |
| `DEEPSEEK_BASE_URL` | No | Custom API endpoint (default: DeepSeek's) |
| `DSH_HOME` | No | Harness home directory (default: current dir) |

---

## Files Created by DeepSeek Harness

These files/directories are created at runtime under `DSH_HOME`:

| Path | Description |
|------|-------------|
| `profiles/web/` | Web profile configuration |
| `.credentials.yaml` | Encrypted API keys (git-ignored) |
| `settings.yaml` | User settings and model config |
| `.sessions/` | Session history and logs |

**Note:** Add `.credentials.yaml`, `settings.yaml`, and `.sessions/` to `.gitignore` to avoid committing secrets.

---

## Troubleshooting

### "Port 3080 already in use"
```bash
# Kill any existing dsh process
pkill -f "dsh web"
# Or use a different port
pnpm dsh web --port 3081
```

### "DEEPSEEK_API_KEY not set"
```bash
export DEEPSEEK_API_KEY="sk-your-key-here"
```

### Build fails with "globSync not found"
You need Node.js v22+:
```bash
nvm install 22
nvm use 22
```

### Server starts but port not responding
The server may need a few seconds to start. Wait 10-15 seconds, then try:
```bash
curl -sI http://127.0.0.1:3080/
```

---

## Resources

- [DeepSeek Harness GitHub](https://github.com/deepseek-ai/deepseek-harness)
- [DeepSeek Platform (API Keys)](https://platform.deepseek.com/)
- [Web UI Guide](https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/user/guide/index.md)
- [Discord Community](https://discord.gg/Ycq5dCaS4)
