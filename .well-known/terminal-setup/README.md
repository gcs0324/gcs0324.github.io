# Terminal Setup Backup
# Generated: 2026-06-29
# Machine: macOS (Darwin 25.5.0, Apple Silicon)
#
# To restore:
#   1. Install Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
#   2. brew bundle --file=~/.config/terminal-setup-backup/Brewfile
#   3. Copy config files to their respective locations
#   4. Restart Ghostty

---

## Terminal Emulator

- **Ghostty** 1.3.1 (primary)
  - Config: `~/Library/Application Support/com.mitchellh.ghostty/config.ghostty`
  - Theme: Cobalt2 (via `auto/theme.ghostty`)

---

## Shell

- **Fish** 4.7.1 (primary interactive shell)
- **Zsh** (macOS default, login shell)

### Fish Config Files

| File | Purpose |
|------|---------|
| `~/.config/fish/config.fish` | Main config |
| `~/.config/fish/fish_variables` | Universal variables |
| `~/.config/fish/conf.d/fish_frozen_theme.fish` | Syntax highlighting theme (web-config) |
| `~/.config/fish/conf.d/uv.env.fish` | UV env (sources `~/.local/bin/env.fish`) |
| `~/.config/fish/functions/` | Custom functions (empty) |
| `~/.config/fish/completions/` | Custom completions (empty) |

### Fish Plugins

- **No plugin manager** (no Fisher, no Tide, no fish_plugins)

### Fish Universal Variables

- `fish_user_paths`: `/Users/cs/.mimocode/bin`

---

## Prompt: Starship

- **Starship** 1.25.1
- Config: `~/.config/starship-nerd.toml`
- Palette: Catppuccin Mocha
- Only active when `$TERM_PROGRAM = ghostty`
- Features:
  - Nerd Font symbols throughout
  - Left prompt: OS icon → username → directory → git branch/status → cmd duration → line break → character
  - Right prompt: conda / nodejs / python / java / rust / golang
  - Custom directory substitutions (Documents/Downloads/Music/Pictures/Developer with icons)
  - Cmd duration notifications at >= 45s

---

## Homebrew

### Formulae (52 packages)

| Package | Description |
|---------|-------------|
| bat | cat with syntax highlighting + Git integration |
| bottom | Cross-platform graphical process/system monitor |
| btop | Resource monitor (C++ bashtop/bpytop) |
| dust | More intuitive du (Rust) |
| eza | Modern ls replacement |
| fd | Simple, fast find alternative |
| fish | Shell |
| fzf | Fuzzy finder |
| gh | GitHub CLI |
| git | Version control |
| lsd | ls with colors and icons |
| maven | Java project management |
| procs | Modern ps replacement (Rust) |
| ripgrep | grep alternative |
| rtk | CLI proxy to minimize LLM token consumption |
| starship | Cross-shell prompt |
| tlrc | Official tldr client (Rust) |
| zoxide | Smarter cd |

### Casks (4)

| Cask | Description |
|------|-------------|
| cc-switch | Configuration manager for AI coding agents |
| claude-code | Claude Code CLI |
| codex | OpenAI Codex CLI |
| ghostty | Terminal emulator |

### Other (uv/npm)

| Tool | Package |
|------|---------|
| uv | claude-tap |
| npm | corepack |

---

## Claude Code

- Config: `~/.claude/settings.json`
- Model: deepseek-v4-pro (via Volces Ark API)
- Base URL: `https://ark.cn-beijing.volces.com/api/coding`
- Theme: dark

---

## Environment

- `HOMEBREW_NO_AUTO_UPDATE=1`
- Homebrew mirror: Tsinghua University (bottles + API)
- PATH includes: `~/.local/bin`, `~/.mimocode/bin`, `/usr/local/bin`, `/opt/homebrew/bin`

---

## Git Config

- HTTP version: 1.1

---

## GitHub CLI

- Protocol: HTTPS
- Aliases: `co` → `pr checkout`

---

## Key CLI Tools (non-Homebrew managed)

| Tool | Version |
|------|---------|
| Vim | 9.1 (macOS bundled) |

---

## Files in this Backup

| File | Restore To |
|------|-------------|
| `Brewfile` | `brew bundle --file=Brewfile` |
| `config.ghostty` | `~/Library/Application Support/com.mitchellh.ghostty/config.ghostty` |
| `theme.ghostty` | `~/Library/Application Support/com.mitchellh.ghostty/auto/theme.ghostty` |
| `config.fish` | `~/.config/fish/config.fish` |
| `fish_frozen_theme.fish` | `~/.config/fish/conf.d/fish_frozen_theme.fish` |
| `uv.env.fish` | `~/.config/fish/conf.d/uv.env.fish` |
| `env.fish` | `~/.local/bin/env.fish` |
| `starship-nerd.toml` | `~/.config/starship-nerd.toml` |
| `claude-settings.json` | `~/.claude/settings.json` |
| `gh-config.yml` | `~/.config/gh/config.yml` |
| `gitconfig` | `~/.gitconfig` |

## NOT Installed / Not Configured

- tmux (no .tmux.conf, no plugins)
- Neovim
- Alacritty / Kitty / iTerm2
- delta (git diff pager)
- lazygit
- Fisher plugin manager
- Tide prompt
- SSH config (empty)
