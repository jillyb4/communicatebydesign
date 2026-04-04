# CbD Shared Inserts

Standalone reusable insert pages for all CbD products.
Built once here. Pull into any product as needed. Never bury in a unit.

## Files

| File | Purpose | Goes In |
|------|---------|---------|
| `CbD_Insert_Accessibility.docx` | WCAG 2.2 AA statement + known PDF limitation + contact | Every product |
| `CbD_Insert_About.docx` | About the Creator — Jill McCardel, CbD, capacity-building approach | Every product |
| `CbD_Insert_Terms.docx` | Terms of Use — what you can/cannot do, license, copyright | Every product |
| `CbD_Insert_Words_to_Add.docx` | Words to Add to the Device — student-led, continuous modeling (UFLI only) | UFLI products only |
| `CbD_Insert_VocabPreview_PictureBook.docx` | Vocabulary Preview Routine — 5-min pre-reading routine, unit-specific words filled in at build time | K–3 Picture Book Companions (Teacher Packet, Page 1) |

## Order in Products (LOCKED — CbD Standard)

End matter always appears in this order:
1. Accessibility Statement
2. About the Creator
3. Terms of Use

Words to Add to the Device goes in the Teacher Guide (UFLI), not the end matter.

## How to Use

1. Open the target product .docx in Word
2. Place cursor at the correct insert point
3. Go to Insert > Object > Text from File → select the insert .docx
4. It will drop in with its own formatting

OR copy/paste content from the insert file into the target document.

## How to Rebuild

Any approved change to locked language runs through the build script:

```bash
cd _Operations/_Shared_Inserts/
python3 build_shared_inserts.py              # rebuild all
python3 build_shared_inserts.py --insert about        # rebuild one
```

## HARD RULE
Do NOT change About, Terms, or Accessibility text without explicit instruction from Jill.
These are approved and locked. The build script is the single source of truth.
Words to Add content may be updated as CbD philosophy evolves — update the script first, then rebuild.
