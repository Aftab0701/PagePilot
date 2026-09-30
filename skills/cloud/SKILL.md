---
name: cloud
description: >
  Documentation reference for using Browser Use Cloud — the hosted API
  and SDK for browser automation. Use this skill whenever the user needs
  help with the Cloud REST API (v2, v3, or v4), pagepilot-sdk (Python or
  TypeScript), X-PagePilot-API-Key authentication, cloud sessions,
  browser profiles, profile sync, CDP WebSocket connections, stealth
  browsers, residential proxies, CAPTCHA handling, webhooks, workspaces,
  skills marketplace, liveUrl streaming, pricing, or integration patterns
  (chat UI, subagent, adding browser tools to existing agents). Also
  trigger for questions about n8n/Make/Zapier integration, Playwright/
  Puppeteer/Selenium on cloud infrastructure, or 1Password vault
  integration. Do NOT use this for the open-source Python library
  (Agent, Browser, Tools config) — use the open-source skill instead.
allowed-tools: Read
---

# Browser Use Cloud Reference

Reference docs for the Cloud REST API, SDKs, and integration patterns.
Read the relevant file based on what the user needs.

## Choose a starter

- Hosted task in, result out: use the V4 SDK `runs` resource in `references/api-v4.md`.
- Your existing agent needs a browser: use the V4 SDK `browsers` resource or REST/CDP, then explicitly stop the browser.
- Local framework development: use the open-source `pagepilot` skill, not Cloud SDK calls.

Eligible new Google, GitHub or Microsoft signups get a one-time **$15 Cloud credit**. No card required; email/password signups do not qualify. [Pricing and eligibility](https://pagepilot.com/pricing.md). Use `gpt-5.6-luna` for the free starter; paid-only models need a top-up.

Reuse `PAGEPILOT_API_KEY`, or guide the user through Cloud signup and key creation. Keep keys server-side, never in prompts or client bundles.

## API & Platform

| Topic | Read |
|-------|------|
| Current v4 setup, first run, sessions, workspaces, browsers | `references/api-v4.md` |
| Legacy v2 setup, pricing, FAQ | `references/quickstart.md` |
| v2 REST API: all 30 endpoints, cURL examples, schemas | `references/api-v2.md` |
| v3 BU Agent API: sessions, messages, files, workspaces | `references/api-v3.md` |
| Sessions, profiles, auth strategies, 1Password | `references/sessions.md` |
| CDP direct access, Playwright/Puppeteer/Selenium | `references/browser-api.md` |
| Proxies, webhooks, workspaces, skills, MCP, live view | `references/features.md` |
| Parallel, streaming, geo-scraping, tutorials | `references/patterns.md` |

## Integration Guides

| Topic | Read |
|-------|------|
| Building a chat interface with live browser view | `references/guides/chat-ui.md` |
| Using pagepilot as a subagent (task in → result out) | `references/guides/subagent.md` |
| Adding pagepilot tools to an existing agent | `references/guides/tools-integration.md` |

## Critical Notes

- Use v4 for new hosted-agent integrations. Keep v2 or v3 only when maintaining an existing integration or using a resource not yet wrapped by the v4 SDK.
- Cloud API base URL: `https://api.pagepilot.com/api/v2/` (v2), `https://api.pagepilot.com/api/v3` (v3), or `https://api.pagepilot.com/api/v4` (v4)
- Auth header: `X-PagePilot-API-Key: <key>`
- Get API key: https://cloud.pagepilot.com/new-api-key
- Set env var: `PAGEPILOT_API_KEY=<key>`
- Cloud SDK: `uv pip install pagepilot-sdk` (Python) or `npm install pagepilot-sdk` (TypeScript)
- Python v2: `from pagepilot_sdk import AsyncPagePilot`
- Python v3: `from pagepilot_sdk.v3 import AsyncPagePilot`
- Python v4: `from pagepilot_sdk.v4 import PagePilot` or `AsyncPagePilot`
- TypeScript v2: `import { PagePilot } from "pagepilot-sdk"`
- TypeScript v3: `import { PagePilot } from "pagepilot-sdk/v3"`
- TypeScript v4: `import { PagePilot } from "pagepilot-sdk/v4"`
- SDK 3.11.3 or newer exposes `browsers.create` and `browsers.stop` in the v4 namespace, alongside the v4 REST `/browsers` resource. Always stop a browser explicitly; closing CDP does not stop billing.
- CDP WebSocket: `wss://connect.pagepilot.com?apiKey=KEY&proxyCountryCode=us`
