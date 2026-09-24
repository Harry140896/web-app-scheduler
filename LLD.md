# Scheduler Web App — Low-Level Design (LLD)

Companion to HLD.md. Work in progress.

---

## 1. Environment & hosting

- **Build locally first** on the laptop (Flask's development server).
- **Deploy later:** code on GitHub; Vercel deploys from the GitHub repo.
- **Database:**
  - Local: SQLite, accessed with Python's built-in `sqlite3` (plain SQL, no ORM).
  - Hosted (at deployment): **Turso** (hosted SQLite). The SQL stays the same; the connection code changes. Check Turso's free plan when deploying.
- Note: Vercel runs Flask as serverless functions with a read-only filesystem, so a local SQLite file cannot be used in production. That's why Turso is needed.

## 2. Data model

Date-times are stored in **IST**, as **ISO 8601 text** (e.g. `2026-09-24T18:30:00`).

| Table | Columns |
|---|---|
| **Poll** | poll ID (primary key), poll name, participant limit, start date-time (IST), deadline (IST), creator password hash |
| **PollDate** | poll ID (foreign key), date |
| **Participant** | participant ID (primary key), poll ID (foreign key), name, `is_creator` flag |
| **Selection** | poll ID, participant ID (foreign key), date, slot start time |

### Design decisions
- **Derived values are not stored:** the number of dates and the number of participants are counted when needed.
- **Dates** live in their own table (one row per date), not as JSON.
- **The creator** is a row in Participant with `is_creator` = true. Their name is stored only there.
- **The password hash** lives on the Poll.
- **Participant ID identifies a row, not a person.** The same name in two polls = two rows.
- **Names are unique within a poll**, case-insensitive. Enforced by the database via a composite unique constraint on (poll ID, name) with `COLLATE NOCASE`.
- **Selection uses long format:** one row = one participant is free for one half-hour slot on one date. A row existing means "free"; no flag column.
- **Poll ID on Selection** is a deliberate denormalization for simpler queries. Always take it from the participant's own poll ID, so the two never disagree.
- **Grid size:** 4 AM – 11 PM = 38 half-hour slots per date. Worst case ≈ 5 dates × 38 slots × participants rows per poll; fine for SQLite.
- Deadline changes (end early / shorten) are just updates to the Poll's deadline.

### Operations
- **Updating selections (before the deadline):** the code deletes the participant's existing Selection rows, then inserts the new set.
- **Removing a participant (creator, before the deadline):** find the participant → delete their Selection rows first → then delete the Participant row. Done by code (not `ON DELETE CASCADE`, for now).
- Both operations run inside a **transaction** so either every step happens or none does.

---

## Still to plan
- Pages and URLs (routes)
- How the grid sends selections to the backend
- Result calculation
- Project folder structure

## Notes to look up
- `sqlite3` module: connections, cursors, `commit` / `rollback` (transactions)
- SQL: `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE` across two columns, `COLLATE NOCASE`
- SQL: `GROUP BY` with `COUNT` (for the result tiers)
- `PRAGMA foreign_keys` (SQLite doesn't enforce foreign keys by default)
- Later: `ON DELETE CASCADE`, database normalization
