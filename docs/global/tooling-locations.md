## Clawdbot (Gateway Dashboard)

### CLI / Install
- Command: `clawdbot`
- Install (npm global):
  - `/Users/tradingwithpython/.npm-global/bin/clawdbot` (symlink)
  - `/Users/tradingwithpython/.npm-global/lib/node_modules/clawdbot/` (package root)

### Persistent State (DO NOT COMMIT)
- `~/.clawdbot/`
  - Config: `~/.clawdbot/clawdbot.json`
  - Agents: `~/.clawdbot/agents/`
  - Workspace: `~/.clawdbot/workspace/`
  - Credentials: `~/.clawdbot/credentials/`

### Runtime
- Start: `clawdbot gateway --port 18789`
- Dashboard: http://127.0.0.1:18789/
- UI branding: “CLAWDBOT — Gateway Dashboard”
- Preferred view: VS Code → Simple Browser
