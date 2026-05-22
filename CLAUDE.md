# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> 内容写作规范见 [WRITING.md](WRITING.md)，新增或修改文章前先读一遍。

## Project Overview

Static GitHub Pages site (`gcs0324.github.io`) — no build tools, no package manager, no frameworks. All files are plain HTML/CSS/JS deployed directly from the `main` branch.

To preview locally: open any `.html` file in a browser, or use any static file server:
```bash
python3 -m http.server 8080
```

## Architecture

### Two distinct page types

**Dashboard pages** (`index.html`, `doc/index.html`):
- Fully self-contained with all CSS inlined in `<style>` tags
- Dark-only theme with warm accent palette (no light/dark toggle)
- Fonts: Syne (headings) + DM Mono (body), loaded from Google Fonts

**Knowledge/doc pages** (`doc/*.html`, except `doc/index.html`):
- Import `../shared/theme.css` for unified CSS variables
- Load `../shared/theme.js` in `<head>` (synchronous, before any content) to avoid flash of unstyled content
- Support light/dark toggle; preference persisted in `localStorage` under key `docTheme`
- Fonts: Inter (body) + IBM Plex Mono (code/labels), loaded via `@import` in CSS

### Shared assets (`shared/`)

- **`theme.css`**: CSS custom properties for both light and dark modes. Defines two parallel naming conventions that must stay in sync — short aliases (`--tx`, `--bd`, `--bg`) and long aliases (`--text`, `--border`, `--bg`). Also defines named semantic colors (`--red`, `--blue`, `--yellow`, etc.) each with `-bg` and `-b` (border) variants.
- **`theme.js`**: Immediately-invoked script that reads `localStorage` or `prefers-color-scheme` and sets `data-theme` on `<html>` before the page renders. Also injects a toggle button (☀/◑) on `DOMContentLoaded`.

### CSS conventions in doc pages

Doc pages use a dense utility-class pattern with very short class names (`.fw`, `.fwh`, `.fwb`, `.sec`, `.sb`, etc.) defined inline per file. When adding a new doc page, follow the existing pattern of that file rather than inventing new class names. The `.sec` class marks major section headings and doubles as scroll-margin anchor targets (`scroll-margin-top: 55px` to clear the sticky nav).

### Adding a new doc page

1. Copy the structure from an existing doc page (e.g. `kafka-mq-reliability.html`)
2. Keep `<link rel="stylesheet" href="../shared/theme.css">` and `<script src="../shared/theme.js"></script>` in `<head>` — the script must be synchronous (no `defer`/`async`)
3. Add a sticky `<nav>` with anchor links for in-page navigation
4. Register the page in the dashboard (`index.html`) card grid
