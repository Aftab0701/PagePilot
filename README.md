# PagePilot

PagePilot is an autonomous web navigation system that transforms BrowserUse into a calm, intentional, and production-grade application.

---

## 🎨 Design Philosophy & Aesthetic
PagePilot replaces bloated, emoji-cluttered interfaces with an original design language:
- **Calm, High-Contrast Palette**: Dual-mode (light obsidian and dark slate) with emerald success badges, subtle warm highlights, and crisp borders.
- **Dense, Functional Layout**: Asymmetric 2-column workspace putting task controls, thought reasoning, and discrete tool actions on the left, with an interactive live browser viewport on the right.
- **100% Token-Driven**: Zero hardcoded hex codes inside component rules. Every color, shadow, radius, and transition is governed by CSS variables in `tokens.css`.
- **Accessible & Motion-Respecting**: Comprehensive keyboard navigation, ARIA roles, high-visibility focus indicators, and `prefers-reduced-motion` compliance.

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Using uv (recommended)
uv venv --python 3.11
.venv\Scripts\activate   # Windows

# Install web server dependencies
uv pip install fastapi "uvicorn[standard]" websockets python-dotenv
```

### 2. Launch the Application
```bash
python webui.py --ip 127.0.0.1 --port 7788
```

Open your browser at **[http://127.0.0.1:7788](http://127.0.0.1:7788)**.

---

## 🧩 Architecture

```
PagePilot/
├── pagepilot/
│   ├── agent/                 # BrowserUse agent bridge & execution service
│   │   └── service.py
│   └── webui/                 # FastAPI backend & static assets
│       ├── server.py
│       └── static/
│           ├── index.html     # Semantic UI shell
│           ├── css/
│           │   ├── tokens.css # Design system variables
│           │   └── components.css # Primitives (Button, Composer, Drawer, Tabs, etc.)
│           └── js/
│               └── app.js     # State manager, WebSocket client, timeline & preview engine
├── webui.py                   # CLI entrypoint
├── pyproject.toml
└── PagePilot — Redesign.html  # Visual source of truth
```
