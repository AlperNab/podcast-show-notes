# Podcast Show Notes — Standalone Real GUI Implementation

This folder is now its own runnable project app. It does not depend on the root all-project dashboard at runtime.

## Run

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default URL: `http://127.0.0.1:9147`

## What is inside this project folder

- `app/` — FastAPI backend for this project.
- `static/` — elegant browser GUI.
- `plugins/podcast-show-notes.json` — this project’s own feature/customization/input schema.
- `project_config.json` — readable copy of the same project-specific configuration.
- `data/` — local SQLite jobs, uploads, exports.
- `tests/` — verifies this project has a registered real local engine.

## Project-specific scope

- Domain: `Creator / Podcast Ops`
- Target user: `Domain operator, business owner, analyst, or team member who needs this workflow executed reliably.`
- Core job: Audio/transcript → episode assets
- Suite: `Media Creator Suite`

## Deep features applied

- transcript cleanup
- chapters
- guest bio
- key quotes
- sponsor detection
- SEO description
- social/newsletter pack
- audiogram prompts

## Customization controls

- `execution_mode` — Execution mode (select)
- `show_style` — show style (select)
- `host_guest` — host/guest (text)
- `platform` — platform (select)
- `sponsor_rules` — sponsor rules (textarea)
- `timestamp_format` — timestamp format (select)
- `tone` — tone (text)
- `quote_style` — quote style (select)
- `output_format` — output format (select)
- `language` — language (select)
- `privacy_mode` — privacy mode (select)
- `confidence_threshold` — Confidence threshold (slider)

## Input fields

- `audio` — Audio (text) required
- `transcript` — transcript (text) required
- `work_brief` — Work brief / source text / URL / instructions (textarea) required

## External data policy

The local deterministic core is real and executable. Live external systems are not simulated. If Shopify, ATS, ERP, OCR/STT, maps, SERP, market data, medical databases, tax/customs databases, or other live systems are required, this project reports the missing connector/API requirement instead of inventing data.

---

## Final UX/UI Layer

This project now uses the **Creator Production Studio** pattern.

**UX workflow:** Brief → script/asset plan → timeline → publishing package

**Domain components:**
- Creative brief canvas
- Storyboard/timeline
- Transcript or caption editor
- Platform publish checklist
- Asset quality scorecards

**Quick actions:**
- Build storyboard
- Create caption package
- Check hook/thumbnail
- Prepare publishing checklist

**No fake-data policy:** external/live actions require real connectors or API keys. Missing connectors are reported instead of simulated.
