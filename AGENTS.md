# MyNoteTaking — Agent Guide

Personal note-taking app (COMP5241). Flask REST API + single-page UI in `src/static/index.html`. SQLite at repo-root `database/app.db`.

## Quick commands

From repository root (activate `venv` first if you use one):

```bash
python -m venv venv && source venv/bin/activate   # once
pip install -r requirements.txt                   # once
python src/main.py                              # dev server → http://localhost:5001
```

Optional shortcuts: `make install`, `make dev`, `make verify`.

## Architecture

| Layer | Location | Notes |
|-------|----------|--------|
| Entry | `src/main.py` | Registers blueprints, DB, static SPA fallback |
| Models | `src/models/` | Shared `db` in `user.py`; `Note` in `note.py` |
| API | `src/routes/` | Blueprints mounted at `/api` |
| UI | `src/static/index.html` | Inline CSS/JS; calls `/api/notes` (same origin) |
| DB | `database/app.db` | Created on first run; `*.db` is gitignored |

**Path bootstrap:** `main.py` inserts the repo root on `sys.path` — run and import as `from src.routes...`, not as a flat package.

**Do not change** the `sys.path.insert` block at the top of `main.py` unless explicitly fixing deployment layout.

## API (notes — primary product surface)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/notes` | List notes (newest `updated_at` first) |
| POST | `/api/notes` | Body: `{ "title", "content" }` |
| GET | `/api/notes/<id>` | Single note |
| PUT | `/api/notes/<id>` | Partial update via JSON |
| DELETE | `/api/notes/<id>` | 204 on success |
| GET | `/api/notes/search?q=` | Title/content substring search |
| POST | `/api/notes/translate` | Body: `{ "title", "content", "target_language" }` → OpenRouter translation |

User routes under `/api/users` exist as template scaffolding; the UI does not use them yet.

## Conventions for changes

1. **Scope:** Prefer minimal diffs. Notes feature is the user-facing path; extend `note` model/routes + `index.html` together when changing behavior.
2. **JSON:** Routes use `note.to_dict()` / `user.to_dict()`; keep ISO datetime strings for timestamps.
3. **Errors:** Follow existing pattern — 400 for validation, 404 via `get_or_404`, 500 with rollback on DB errors.
4. **Frontend:** No bundler; edit `index.html` in place. Preserve responsive layout and existing fetch URLs (`/api/...`).
5. **Secrets:** Do not commit real `SECRET_KEY` or `.env`. Use `.env.example` as reference only.
6. **Dependencies:** Pin in `requirements.txt`; avoid new packages unless the task requires them.
7. **Git:** `origin` → student fork; `upstream` → `HKPolyUSE/MyNoteTaking`. Do not force-push `main`. Commit only when the user asks.

## Verification (no test suite yet)

After backend changes:

```bash
make verify    # import app + list routes
make dev       # manual smoke: create/edit/delete/search in browser
```

Quick API smoke (server running):

```bash
curl -s http://localhost:5001/api/notes | head
```

## Common tasks

- **New note field:** Add column on `Note`, migration via `db.create_all()` only works for greenfield DBs — document if existing DBs need manual SQL or reset for course work.
- **New endpoint:** Add route on `note_bp`, mirror pattern in `index.html` fetch calls.
- **Auth / multi-user:** User model is stubbed; design before wiring UI.

## Docs map

- Human-oriented setup & features: `README.md`
- Cursor rules: `.cursor/rules/*.mdc`
- GitHub Copilot: `.github/copilot-instructions.md` (points here)
