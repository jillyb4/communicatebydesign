# CbD Skill Update To-Do
**Last updated:** 2026-04-05
**Location of skills on Mac:** `~/.claude/skills/communicate-by-design/`
**Note:** Skill files are read-only in Cowork sessions — all edits must be made directly on Mac in Finder/text editor, OR package a new .skill file and reinstall.

---

## ⚠️ Pending Updates (Cannot be done in session — read-only mount)

### 1. `references/products.md`

**UFLI Pricing table — replace entirely:**
```
OLD (delete all 4 rows):
| Teacher Guide + Communication Partner Guide | $5 |
| Individual Lesson Packet (Lessons 5–34) | $1 each |
| Lessons 5–34 Bundle | $25 (save $5) |
| Complete Set (Guide + All 30 Packets + Supplemental PDFs) | $28 (save $7) |

NEW:
| UFLI AAC Companion — Lessons 1–5 | FREE |
| UFLI AAC Companion — Lessons 6–34 + Teacher & Partner Guide | $20 |

Add below table:
**Old pricing ($1/lesson, $5 guide, $25 bundle, $28 set) is RETIRED. Do not reference it.**
```

**UFLI "Built, Not Yet Fully Listed" section — update status line:**
```
OLD: What's next: Cover design (Canva), preview PDFs, upload to TPT
NEW: Covers DONE in Canva. Blocker: formatting/consistency across lesson packets. Target May 2026.
     Airtable records: FREE = recCeJ479OD5BEHb5 · PAID = recas76MabrgRnmL1
```

**Picture Book Companions — replace "In Progress / Pipeline" entry with:**
```
### Picture Book Companions — 1 LIVE, 5 Building (Apr 2026)
| Title | Grade | Status | Price | Airtable ID |
|-------|-------|--------|-------|-------------|
| All the Way to the Top | K–3 | LIVE | $5 | recPx1oIQOMEUBP9E |
| A Friend for Henry | K–1 | Building | $5 | recRlyKIagsefExyM |
| I Talk Like a River | K–2 | Building | $5 | recN6ck156yzuPykm |
| Ian's Walk | K–1 | Building | $5 | recGCX4KbFeHmkbZ0 |
| Emmanuel's Dream | 1–2 | Building | $5 | recdW4e84IRXsKSHV |
| My Friend Isabelle | K–1 | Building | $5 | recZORJoyxVv4KacC |

Canva cover workflow (locked Apr 4 2026):
- Bulk template ID: DAHF6DObHZ4 ("(Bulk 1) Picture Book Square Template", 1080×1080, 6 pages)
- Text (title, standards, skill focus) = Lane B — auto-fills via bulk CSV
- Images (book cover + symbol preview + 3 worksheet previews) = Lane A — Jill places manually
- When cover done: check `Canva Cover ✓` in Airtable Products record
```

**Substack Status section — update to:**
```
- Post 1 (Welcome, March 2026) — LIVE
- Post 2 (Keiko behind-the-scenes, March 15) — LIVE
- Post 3 ("That Statistic Is 33 Years Old", March 25) — LIVE
- Post 4 ("AT Consideration Is a Legal Requirement…", April 2 2026) — LIVE
- Next up: "Tools I Wish Someone Had Handed Me" (Apr 7) · "IEP Goals for AAC Users" (Apr 8) · "My Student Has an AAC Device…" (Apr 10)
```

**Canva Design IDs table — add these rows:**
```
| Nonfiction Pinterest Pin template | DAHFdGbv7rs | 365×548 (2:3 pin) — 7 pages, one per nonfiction unit |
| IEP AT Consideration Toolkit AD | DAHEI1nmrPA | 365×548 (2:3 pin) — 5 pin variants |
| Fiction Long Format pin | DAHFeFD9LBk | 365×548 (2:3 pin) — Wonder, 1 page |
| Keiko FREE Pinterest pin | DAHEiSb8S7k | 365×548 (2:3 pin) |
| Picture Book Companion cover bulk template | DAHF6DObHZ4 | 1080×1080 — 6 pages (1 per companion). Text auto-fills via bulk CSV. Images placed manually by Jill. |
```

---

### 2. `references/ufli.md`

**Pricing table — replace entirely:**
```
OLD:
| Teacher Guide + Communication Partner Guide | $5 |
| Individual Lesson Packet (Lessons 5–34) | $1 each |
| Lessons 5–34 Bundle | $25 (save $5) |
| Complete Set (Guide + All 30 Packets + Supplemental PDFs) | $28 (save $7) |

NEW:
| UFLI AAC Companion — Lessons 1–5 | FREE |
| UFLI AAC Companion — Lessons 6–34 + Teacher & Partner Guide | $20 |

Add: **Old pricing ($1/lesson, $5 guide, $25 bundle, $28 set) is RETIRED.**
```

**Status section — update:**
```
OLD: What's next: Cover design (Canva), preview PDFs, upload to TPT
     Location: `Products/UFLI Phonics/Ready for TPT v3/` — 34 final files

NEW: Covers DONE in Canva (two covers: FREE + PAID).
     Blocker: formatting/consistency across lesson packets — must pass before listing either product.
     Airtable records: FREE = recCeJ479OD5BEHb5 · PAID = recas76MabrgRnmL1
     TPT listing copy: `Products/UFLI Phonics/TPT_Listings_UFLI_AAC_Companion.md` (bugs fixed Apr 5 2026)
     Phoneme patches applied: L5, L10, L11, L19 (Apr 4 2026) — configs now accurate to UFLI manual
```

---

### 3. `SKILL.md` frontmatter description

Add to the trigger list in the description field:
```
Add to existing trigger list: "picture book companion, poetry reading unit, PB companion, What the Voice Carries"
```

---

## ✅ Already Done This Session (2026-04-05)
- [x] Airtable UFLI records: 4 old retired, 2 new created (FREE + PAID $20)
- [x] PB Companion Canva Cover Link populated in all 6 Airtable records
- [x] TPT listing doc bugs fixed (title 81→80 chars, L10/L11/L19 label duplicates)
- [x] SESSION_STATE.md updated
- [x] TASKS.md updated with completed items

---

## How to Apply These Updates

**Option A — Edit on Mac directly:**
1. Open Finder → navigate to `~/.claude/skills/communicate-by-design/references/`
2. Right-click each file → Open With → TextEdit (or VS Code)
3. Apply the changes above

**Option B — Package a new .skill file in a future session:**
- Copy skill to writable location → apply edits → run `package_skill.py` → reinstall
- Ask Claude to do this at the start of any future session when the skill-creator is loaded
