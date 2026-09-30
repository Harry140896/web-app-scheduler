# Scheduler Web App — Build Milestones

Companion to `HLD.md` (what the app does) and `LLD.md` (how it's structured).

**How to use this file**
- Build one milestone at a time, top to bottom. Each one depends on the ones before it.
- Each milestone is a **vertical slice**: page (template) + route (Flask) + database, finished when you can click it and see it work.
- Tick the boxes as you go (`[ ]` → `[x]`).
- **Decisions** are yours to make when you reach them; write them into `LLD.md` as you go.
- After each milestone: stage → commit → `git push`.
- Stuck? Read the whole traceback first, then bring it to Claude (PLAN mode: problem explained, fix only if asked).

---

## Milestone 0 — Setup

**Goal:** a "hello" page running from your own project, tracked in Git and on GitHub.

- [x] Virtual environment `app1` created
- [x] Venv activated (`(app1)` shows in the prompt)
- [x] Git repository started, `.gitignore` created
- [x] First commit made and pushed to GitHub (`web-app-scheduler`)
- [ ] Confirm `app1/` is **not** on GitHub
- [ ] Flask installed inside `app1`
- [ ] `requirements.txt` created
- [ ] Hello page visible at `127.0.0.1:5000`

**Concepts:** terminal vs shell (PowerShell / Command Prompt / bash) · venv · `pip` · `pip freeze` · Git: stage, commit, remote, push, upstream

**References**
- Python venv: https://docs.python.org/3/library/venv.html
- PowerShell execution policies: https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_execution_policies
- Flask Quickstart ("A Minimal Application"): https://flask.palletsprojects.com/en/stable/quickstart/
- `.gitignore`: https://git-scm.com/docs/gitignore
- Pro Git book (chapters 1–2): https://git-scm.com/book/en/v2
- Pushing to GitHub: https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository

---

## Milestone 1 — The database

**Goal:** a Python script that creates the four tables (Poll, PollDate, Participant, Selection) in a SQLite file.

- [ ] Script connects to (and creates) a SQLite database file
- [ ] All four tables created, matching the LLD data model
- [ ] Primary keys and foreign keys in place
- [ ] Participant names unique **within a poll**, case-insensitive
- [ ] Running the script twice doesn't crash or duplicate tables
- [ ] Tables inspected in DB Browser for SQLite
- [ ] Database file is ignored by Git

**Decisions**
- Where does the database file live in the project folder, and what's it called? Ans: database folder.
- Column types for each field (SQLite has only a few; how do dates, times and true/false fit?)
- Is creating the tables a standalone script, or a function the app calls on startup?
Ans: Let it be stand alone script one time for now, then we can consider about incorporating it into the main function later.

**Concepts:** `sqlite3` connection & cursor · `CREATE TABLE` · `IF NOT EXISTS` · `PRIMARY KEY` · `FOREIGN KEY` · composite `UNIQUE` · `COLLATE NOCASE` · `PRAGMA foreign_keys` · `commit`

**References**
- Python `sqlite3` (tutorial section first): https://docs.python.org/3/library/sqlite3.html
- SQLite `CREATE TABLE`: https://www.sqlite.org/lang_createtable.html
- SQLite data types: https://www.sqlite.org/datatype3.html
- SQLite foreign keys: https://www.sqlite.org/foreignkeys.html
- DB Browser for SQLite: https://sqlitebrowser.org/
- Flask's own tutorial uses plain `sqlite3`; see "Define and Access the Database": https://flask.palletsprojects.com/en/stable/tutorial/database/

---

## Milestone 2 — Create poll

**Goal:** the Create poll page saves a new poll to the database.

- [ ] Page with: creator name, poll name, participant limit, 5 date boxes, response window (hours), password, Submit
- [ ] Route shows the page (GET) and receives the form (POST)
- [ ] Server-side validation: required fields, limit is a positive number, 1–5 dates, no duplicates, no past dates, none before the deadline
- [ ] Clear error message shown on the same page when validation fails (form keeps what was typed)
- [ ] On success, saved in one transaction: Poll row, PollDate rows, creator's Participant row (`is_creator` = true)
- [ ] Password stored as a **hash**
- [ ] Poll ID is unguessable
- [ ] Start time and deadline stored in IST, ISO 8601
- [ ] After success: redirect to the login page with the poll ID filled in


Remaining to do: 

B. Step 4: validate on the server (add rules one at a time)

 Required text fields aren't empty, after trimming spaces
 Participant limit and response window convert to whole numbers, within your minimums
 Date range: split into two dates. Both present, start not in the past, end ≥ start, at most 5 days, and none before the deadline (now + response window)
 On an error: show a message on the same page, with the form keeping what was typed (this is where Jinja placeholders come in)

C. Step 5: prepare the data

 Poll ID: a random token (secrets)
 The creator's participant ID
 The password → hash (generate_password_hash)
 creation_date_time = now, in IST, as ISO text
 Expand the date range into a list of individual dates (timedelta)

D. Step 6: save

 A database connection in app.py. The path starts from the project root now, not scripts/. Foreign keys on.
 In one transaction: the Poll row, one PollDate row per day, and the creator's Participant row (is_creator = 1)
 Check the rows in DB Browser

E. Step 7: redirect

 Send the creator to the login page with the poll ID. It can be a placeholder page for now (milestone 3 builds the real one).

F. Wrap up

 Commit and push, and tick milestone 2 in MILESTONES.md


**Decisions**
- Project folder structure (Flask expects `templates/` and `static/` folders; where does database code go?) app.py is in the Root folder along with two folders: templates and static.
- URL for this page DONE: create_scheduler
- Poll ID format: the database's number, or a random token? (What does each reveal in a shared link?) Possibly a random Token.
- How errors reach the page

**Concepts:** templates (Jinja) · `render_template` · `request.form` · GET vs POST · Post/Redirect/Get · `redirect` · `url_for` · `<input type="date">` · password hashing · `secrets` · `datetime` · `zoneinfo` · transactions

**References**
- Flask templates: https://flask.palletsprojects.com/en/stable/templating/
- Jinja template syntax: https://jinja.palletsprojects.com/en/stable/templates/
- Flask Quickstart (routing, HTTP methods, redirects): https://flask.palletsprojects.com/en/stable/quickstart/
- Message flashing (for errors): https://flask.palletsprojects.com/en/stable/patterns/flashing/
- HTML forms (MDN): https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms
- `<input type="date">` (MDN): https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date
- Password hashing (Werkzeug): https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security
- `secrets` module: https://docs.python.org/3/library/secrets.html
- `datetime`: https://docs.python.org/3/library/datetime.html
- `zoneinfo` (IST = `Asia/Kolkata`; on Windows you may need the `tzdata` package): https://docs.python.org/3/library/zoneinfo.html

---

## Milestone 3 — Login (main page)

**Goal:** people can join a poll by name; the creator logs in with a password.

- [ ] Main page: name, poll ID, Submit, and a "Create new poll" button
- [ ] Two routes: poll ID in the URL (pre-filled) and no poll ID (typed)
- [ ] Unknown poll ID → clear error
- [ ] New name → Participant row created, if the limit allows
- [ ] Returning name (any case) → no new row, no new place taken
- [ ] Poll full → results only, no voting
- [ ] Creator's name → page reloads with a password box; name and poll ID stay filled
- [ ] Wrong password → error; right password → logged in as creator
- [ ] Who is logged in is remembered across pages
- [ ] Deadline passed → results only

**Decisions**
- URLs for the two versions of this page
- What exactly goes into the session (participant ID? poll ID? creator flag?)
- Where the secret key lives (it must not go to GitHub)

**Concepts:** variable rules (dynamic routes) · `request.args` · HTML `value` attribute · Flask `session` · `SECRET_KEY` · `.env` files

**References**
- Flask variable rules & sessions (Quickstart): https://flask.palletsprojects.com/en/stable/quickstart/
- Flask configuration (secret key): https://flask.palletsprojects.com/en/stable/config/
- Flask tutorial, blueprints & auth (a login example with `sqlite3`): https://flask.palletsprojects.com/en/stable/tutorial/views/
- `python-dotenv` (loading `.env`): https://pypi.org/project/python-dotenv/

---

## Milestone 4 — Poll page (read-only)

**Goal:** the poll page draws everything from the database, without saving yet.

- [ ] Only reachable when logged in to this poll
- [ ] Header "Scheduling: <poll name>"
- [ ] Grid: one column per date; rows 4 AM – 11 PM IST, hour labels, half-hour cells (38 per date)
- [ ] Grid is labelled IST
- [ ] Your own saved cells shown as selected
- [ ] Everyone's selections visible (e.g. a count or shading per cell)
- [ ] Countdown to the deadline, ticking in the browser

**Decisions**
- Who builds the list of slots: Python (passed to the template) or the template itself?
- How each cell is identified in the HTML (date + slot start)
- How "everyone's selections" are displayed per cell
- HTML table or CSS Grid for the layout

**Concepts:** Jinja loops · `timedelta` · generating time slots · HTML `<table>` / CSS Grid · `data-*` attributes · JavaScript `setInterval` · SQL `GROUP BY` + `COUNT`

**References**
- Jinja `for` loops: https://jinja.palletsprojects.com/en/stable/templates/#for
- `timedelta`: https://docs.python.org/3/library/datetime.html#timedelta-objects
- CSS Grid (MDN): https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout
- `data-*` attributes (MDN): https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Solve_HTML_problems/Use_data_attributes
- `setInterval` (MDN): https://developer.mozilla.org/en-US/docs/Web/API/Window/setInterval
- SQLite `SELECT` (incl. `GROUP BY`): https://www.sqlite.org/lang_select.html
- SQL basics tutorial: https://www.sqlitetutorial.net/

---

## Milestone 5 — Save selections

**Goal:** clicking cells and pressing Save stores your availability.

- [ ] Clicking a cell toggles it on/off in the browser
- [ ] Save sends the selected cells to the server
- [ ] Server rejects saves after the deadline
- [ ] Server rejects saves from people not logged in to this poll
- [ ] Old selections deleted and new ones inserted **in one transaction**
- [ ] Poll ID on each Selection row taken from the participant's own poll
- [ ] After saving, the page shows the saved state
- [ ] Saving with nothing selected works (clears your availability)

**Decisions**
- How the grid sends data: a normal form submit (e.g. hidden inputs or checkboxes) or JavaScript `fetch` with JSON?
- Click-to-toggle only, or also click-and-drag?

**Concepts:** DOM events (`click`, pointer events) · checkboxes / hidden inputs · `request.form.getlist` · `fetch` · `request.get_json` · `jsonify` · transactions (`commit` / `rollback`)

**References**
- Handling events (MDN): https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Events
- Using `fetch` (MDN): https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
- Pointer events (MDN): https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events
- Flask `request` object: https://flask.palletsprojects.com/en/stable/api/#flask.Request
- SQLite transactions: https://www.sqlite.org/lang_transaction.html
- `sqlite3` transaction control: https://docs.python.org/3/library/sqlite3.html#sqlite3-controlling-transactions

---

## Milestone 6 — Result

**Goal:** after the deadline, the poll page shows "Poll ended" and the result, following the HLD rules.

- [ ] Grid becomes read-only after the deadline
- [ ] Voters = participants with at least one selection
- [ ] Tier 1: slots where every voter is free
- [ ] Tier 2 (otherwise): slots where at least half the voters are free
- [ ] Tier 3 (otherwise): most-selected slot(s), all ties shown
- [ ] No voters → "Poll Ended: no slots voted."
- [ ] Adjacent cells merged into a range **only if exactly the same people** are free throughout
- [ ] Ranges shown readably (e.g. "4 PM – 7 PM on 23/9")
- [ ] Result logic tested on made-up examples (including ties and the "exactly half" case)

**Decisions**
- How much of the logic is SQL and how much is Python?
- Keep the result logic in its own module/function, separate from Flask? (Much easier to test.)
- Test with plain `assert`s or `pytest`?

**Concepts:** sets (comparing "same people") · sorting · grouping consecutive items · `strftime` · separating logic from web code · unit tests

**References**
- Python sets: https://docs.python.org/3/tutorial/datastructures.html#sets
- `itertools.groupby`: https://docs.python.org/3/library/itertools.html#itertools.groupby
- `strftime` format codes: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
- pytest getting started: https://docs.pytest.org/en/stable/getting-started.html
- Testing Flask apps: https://flask.palletsprojects.com/en/stable/testing/

---

## Milestone 7 — Creator powers

**Goal:** the creator's left and right panels and the four actions work.

- [ ] Panels visible **only** to the logged-in creator
- [ ] Left panel shows the share link (login page with poll ID filled in)
- [ ] Right panel lists participants, each with a Remove button
- [ ] **Remove participant:** Selection rows first, then the Participant row, in one transaction; only before the deadline; creator can't remove themselves
- [ ] **Raise limit:** only increases allowed
- [ ] **Shorten deadline:** only earlier, never later
- [ ] **End poll now:** deadline set to now
- [ ] Every creator route checks on the **server** that the requester is the creator
- [ ] A removed person can rejoin under the same name

**Decisions**
- URLs for the four actions
- How each action reports errors (e.g. "limit can only go up")

**Concepts:** Jinja `if` blocks · small forms per action (POST) · authorization checks in routes · decorators (optional: look up `functools.wraps`) · building full URLs with `url_for(..., _external=True)`

**References**
- Jinja `if`: https://jinja.palletsprojects.com/en/stable/templates/#if
- `url_for`: https://flask.palletsprojects.com/en/stable/api/#flask.url_for
- View decorators (e.g. "login required"): https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/

---

## Milestone 8 — Tidy up the trial version

**Goal:** the local app is complete and understandable.

- [ ] Full walkthrough with 2–3 browser windows (e.g. one normal, one private) acting as different people
- [ ] Basic styling in `static/` (readable grid, panels, errors)
- [ ] `README.md`: what it does, how to run it locally
- [ ] `requirements.txt` up to date
- [ ] **Rewrite `LLD.md`** to match what was actually built

**References**
- Flask static files: https://flask.palletsprojects.com/en/stable/quickstart/#static-files
- Writing a README (GitHub): https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

---

## Milestone 9 — Deploy (later)

**Goal:** the app runs on the internet: Vercel (code from GitHub) + Turso (hosted SQLite).

- [ ] Turso account, free plan checked, database created
- [ ] Connection code switched from the local file to Turso (the SQL stays the same)
- [ ] Secrets (secret key, Turso token) set as Vercel environment variables, never in Git
- [ ] Vercel project linked to the GitHub repo
- [ ] Tested end-to-end on the live URL
- [ ] Deadline and "now" checked for IST on the server (servers usually run in UTC)

**References**
- Vercel Python runtime: https://vercel.com/docs/functions/runtimes/python
- Vercel environment variables: https://vercel.com/docs/environment-variables
- Is SQLite supported in Vercel?: https://vercel.com/kb/guide/is-sqlite-supported-in-vercel
- Turso docs (Python SDK): https://docs.turso.tech
