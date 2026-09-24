# Scheduler Web App — High-Level Design (HLD)

A when2meet-style group availability poll, built with Python + Flask.
Scope: trial version, zero cost.

---

## 1. Creating a poll (creator page)

The creator fills in:
- Poll name (e.g. "Informal Meeting")
- Creator name
- Creator password (stored hashed, never as plain text)
- Participant limit (includes the creator)
- Candidate dates (maximum 5)
- Response window in hours (e.g. 2 or 48)

Date validation:
- No past dates.
- No dates that fall before the deadline.

Submitting generates a **unique link** for the poll, which the creator shares.

## 2. Joining a poll (login page)

- The person enters their name.
- Names are the unique identifier and are **case-insensitive** ("Priya" = "priya" = "PRIYA").
- If the name matches the creator's, the same page asks for the **creator password**.
- A place in the participant limit is taken as soon as a name is entered.
  Returning under the same name does not take a new place.

## 3. Poll page

- Header at the top centre: **"Scheduling: <poll name>"**
- A **countdown** to the deadline.
- Grid in the middle of the page:
  - Columns: the dates the creator chose.
  - Rows: **4 AM – 11 PM IST** (labelled as IST), in one-hour labelled blocks split into half-hour cells.
- People select the cells when they are free.
- Updates: everyone's latest selections show when the page is **loaded or reloaded** (no live updates).

## 4. Rules

- Anyone beyond the participant limit can **see results only**.
- **Before the deadline:** people can come back and edit their selections any number of times.
- **After the deadline:** everyone sees results only.
- The **server rejects** submissions after the deadline; the countdown in the browser is only a display.
- Accepted trade-offs (trial version):
  - A second person with the same name must use a variation (e.g. "Priya K").
  - Anyone who knows a participant's name can open the page as that participant.

## 5. Creator powers (after password login)

- **End the poll early**, or **shorten the deadline**.
- **Raise the participant limit** at any time. It can never be lowered.
- **Remove any participant**, voted or not, **before the deadline only**.
  - Removing someone frees their place.
  - A removed person can rejoin and vote again under the same name.

## 6. Result (after the deadline)

- A "**Poll ended**" message and the result.
- Counts are taken among **the people who voted**.
- Minimum meeting length: **30 minutes** (a single cell counts).
- **All** qualifying slots are shown, with no cap.

Result tiers, in order:
1. **Tier 1:** slots where everyone who voted is free.
2. **Tier 2:** otherwise, slots where **at least half** of the voters are free (e.g. 2 of 4 counts).
3. **Tier 3:** otherwise, the most-selected slot(s). Ties: show all of them.
4. If nobody voted: **"Poll Ended: no slots voted."**

Merging cells into ranges:
- Adjacent cells merge into one range (e.g. "4 PM – 7 PM on 23/9") **only when exactly the same people are free throughout**.
- Otherwise each cell is listed separately.

---

## Notes to look up

- Password hashing: `werkzeug.security` (`generate_password_hash` / `check_password_hash`)
- Keeping the creator logged in across requests: Flask `session`
- Unguessable poll links: Python `secrets` module
- Timezones: `zoneinfo` (IST = `Asia/Kolkata`)
