# AGENTS.md — Cloud Agent Instructions

## Project Overview

This repository contains two distinct parts:

1. **Clawd on Desk** — An Electron desktop pet app that reacts to Claude Code sessions (Node.js / Electron)
2. **FoneSquare PRD** — Product Requirements Documents (interactive HTML prototypes) for a cross-border B2B mobile device trading platform

## Repository Structure

```
├── src/                    # Electron app source
├── agents/                 # Agent registry (codex, claude-code, copilot)
├── hooks/                  # Auto-start hooks for IDE agents
├── extensions/             # VSCode extension files
├── specs/                  # FoneSquare technical specs (Markdown)
│   ├── i18n/              # Language packs (en, zh-CN, zh-HK) for APP & Web
│   ├── app/               # APP-side specs (auth, login, KYC)
│   ├── web/               # Web admin specs
│   └── shared/            # Shared specs (i18n, timezone, etc.)
├── FoneSquare-PRD-v2.html # Main PRD document (Web admin, interactive prototype)
├── fonesquare-login.html  # APP login flow prototype
├── fonesquare-kyc.html    # APP KYC verification flow prototype
├── public/                # GitHub Pages deploy directory
├── deploy-prd.sh          # GitHub Pages deployment script
├── prd-server.py          # Local dev server (Python, handles POST for notes saving)
├── tools/                 # One-off refactoring scripts
├── i18n-table.html        # i18n language pack comparison table
└── i18n-table.csv         # i18n data export
```

## Tech Stack

- **Electron App**: Node.js, Electron 41, electron-builder
- **PRD Documents**: Self-contained HTML files with embedded CSS/JS, Mermaid.js diagrams, interactive prototypes
- **Specs**: Markdown documents
- **i18n**: JSON language packs (`en.json`, `zh-CN.json`, `zh-HK.json`)
- **Local Server**: Python 3 (`prd-server.py`) — serves HTML files and handles note-saving POST requests
- **Deployment**: `deploy-prd.sh` → GitHub Pages at `https://joannqiao.github.io/fonesquare-prd/`

## How to Run

### Electron App
```bash
npm install
npm start
```

### PRD Local Server
```bash
python3 prd-server.py
# Serves at http://localhost:8080
# Supports GET (static files) and POST /save, /save-notes (persists edits)
```

### Tests
```bash
npm test
```

## Key Conventions

### Language & Locale
- Locale codes: `zh-CN` (Simplified Chinese), `zh-HK` (Hong Kong Traditional Chinese), `en` (English)
- Never use `zh-Hans`, `zh-Hant`, or `zh-TW` — always use region-specific codes above

### Timezone
- Server stores UTC+8
- APP and Web admin both display in user's device local timezone
- Special display cases are noted explicitly in specs

### Terminology
- Use "维护人" (not "销售") in Chinese for account advisors
- Use "Advisor" or "Consultant" (not "Owner" or "Sales") in English

### PRD Documents
- All PRD HTML files are self-contained (single file, no external dependencies except CDN)
- Interactive prototypes are embedded directly in the HTML
- Product notes are saved to `*.notes.json` files via the local server
- The `public/` directory mirrors what gets deployed to GitHub Pages

### i18n JSON Files
- Located in `specs/i18n/{app,web}/{en,zh-CN,zh-HK}.json`
- Flat key-value structure with dot-notation keys (e.g., `login.btn`, `profile.title`)
- Keys are grouped by page/screen prefix

## Deployment

### GitHub Pages (PRD)
```bash
# 1. Ensure public/ has latest files
cp FoneSquare-PRD-v2.html public/
cp fonesquare-login.html fonesquare-kyc.html public/
cp *.notes.json public/

# 2. Deploy
bash deploy-prd.sh
# Pushes to gh-pages branch → https://joannqiao.github.io/fonesquare-prd/
```

### Git Remotes
- `origin` → `git@github.com:rullerzhou-afk/clawd-on-desk.git` (main repo)
- `pages` → `git@github.com:JoannQiao/fonesquare-prd.git` (GitHub Pages)

## Cloud Agent Specific Instructions

- When editing PRD HTML files, preserve the self-contained nature — do not extract CSS/JS to external files
- When modifying i18n keys, update ALL three language files (en, zh-CN, zh-HK) simultaneously
- After PRD changes, always copy updated files to `public/` for deployment readiness
- The `prd-server.py` is for local development only; Cloud Agent should edit files directly
- Respond in Chinese (中文) unless the user explicitly requests English
