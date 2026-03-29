import { useState } from "react";

const CHECKLIST = [
  {
    phase: "Before You Build",
    icon: "◈",
    color: "#006DA0",
    items: [
      { id: "b1", text: "Identify reading level target for audience (students, educators, families)" },
      { id: "b2", text: "Plan for at least 2 means of representation (visual + text, or text + symbol)" },
      { id: "b3", text: "Choose fonts ≥ 12pt for body; avoid decorative fonts for instructional text" },
      { id: "b4", text: "Color palette check: primary text meets 4.5:1 contrast ratio (use Coolors or WebAIM)" },
      { id: "b5", text: "Large text / headings meet 3:1 contrast ratio minimum" },
      { id: "b6", text: "No information conveyed by color alone (add icons, labels, or patterns)" },
    ],
  },
  {
    phase: "While Building in Canva",
    icon: "◉",
    color: "#E86A2E",
    items: [
      { id: "c1", text: "Use Heading / Body text styles consistently (not just size changes)" },
      { id: "c2", text: "Add alt text to every image, icon, and graphic element" },
      { id: "c3", text: "Decorative/purely visual elements: mark as decorative (alt = empty)" },
      { id: "c4", text: "Reading order is logical top-to-bottom, left-to-right" },
      { id: "c5", text: "Fillable form fields (if any) have visible, descriptive labels" },
      { id: "c6", text: "Tables have clear header rows; avoid merged cells where possible" },
      { id: "c7", text: "Page numbers or slide numbers included for navigation" },
      { id: "c8", text: "Document language metadata set (Canva: limited — note this as a known gap)" },
    ],
  },
  {
    phase: "Word Document (.docx) Build",
    icon: "◧",
    color: "#006DA0",
    items: [
      { id: "d1", text: "Heading hierarchy correct: H1 > H2 > H3, no skipped levels" },
      { id: "d2", text: "Document title set in File > Properties (not 'Document1')" },
      { id: "d3", text: "Document language set to English (Review > Language)" },
      { id: "d4", text: "All tables have header rows defined (Table Properties > Repeat as header row)" },
      { id: "d5", text: "No tables used for visual layout — only for data" },
      { id: "d6", text: "Lists use real bullet/number formatting (not manual dashes)" },
      { id: "d7", text: "Alt text on all informational images; decorative images marked decorative" },
      { id: "d8", text: "Run Word's Accessibility Checker (Review > Check Accessibility) — zero errors" },
      { id: "d9", text: "Test with Read Aloud (Review > Read Aloud) — content reads in correct order" },
      { id: "d10", text: "Accessibility Statement section included in teacher documents" },
    ],
  },
  {
    phase: "PDF Export Check",
    icon: "▣",
    color: "#C4A10A",
    items: [
      { id: "p1", text: "Export via Save As PDF (NOT Print to PDF) — printing strips all tags" },
      { id: "p2", text: "Enable 'Document structure tags for accessibility' checkbox during Save As" },
      { id: "p3", text: "Run Adobe Acrobat Accessibility Checker (if available)" },
      { id: "p4", text: "Check: Tags present (critical — untagged PDFs fail completely for AT users)" },
      { id: "p5", text: "Check: Reading order passes" },
      { id: "p6", text: "Check: Alt text present on all figures" },
      { id: "p7", text: "Check: Document title set in file metadata" },
      { id: "p8", text: "Note any known limitations in product listing accessibility note" },
    ],
  },
  {
    phase: "Video / Audio Content",
    icon: "◎",
    color: "#5B3FA6",
    items: [
      { id: "v1", text: "Captions added (YouTube auto-cap + manual correction, or Rev.com)" },
      { id: "v2", text: "Captions are accurate — proper nouns, AAC terms, names reviewed manually" },
      { id: "v3", text: "Audio description provided if visual content conveys critical information" },
      { id: "v4", text: "No auto-play — user controls playback" },
      { id: "v5", text: "No content flashes more than 3x per second (seizure safety)" },
    ],
  },
  {
    phase: "TPT Listing & Metadata",
    icon: "◆",
    color: "#006DA0",
    items: [
      { id: "t1", text: "Preview images have descriptive file names (not 'image001.jpg')" },
      { id: "t2", text: "Product description written in plain language (aim for 8th grade reading level)" },
      { id: "t3", text: "Accessibility note included in listing: what AT it supports, known limitations" },
      { id: "t4", text: "Tags include relevant AT/AAC/accessibility terms for searchability" },
      { id: "t5", text: "Thumbnail text is legible at small size (not image-only text)" },
    ],
  },
  {
    phase: "Social / Instagram",
    icon: "◐",
    color: "#E86A2E",
    items: [
      { id: "s1", text: "Alt text written for every post (Edit > Advanced Settings > Write Alt Text)" },
      { id: "s2", text: "Captions added to all Reels / video content" },
      { id: "s3", text: "Key information not buried in image text only — replicated in caption" },
      { id: "s4", text: "Hashtags written in CamelCase (#CommunicateByDesign not #communicatebydesign)" },
      { id: "s5", text: "Emojis used sparingly; placed at end of sentences (screen readers read emoji names)" },
    ],
  },
  {
    phase: "Substack / Website",
    icon: "◇",
    color: "#C4A10A",
    items: [
      { id: "w1", text: "All images have alt text; decorative images have null alt" },
      { id: "w2", text: "All links have descriptive text (not 'click here' or 'read more')" },
      { id: "w3", text: "Heading hierarchy used (H2 for sections, H3 for subsections — H1 is the post title)" },
      { id: "w4", text: "Embedded media has captions or transcripts" },
      { id: "w5", text: "CamelCase hashtags in all social shares" },
    ],
  },
];

const TOOLS = [
  { name: "WebAIM Contrast Checker", url: "https://webaim.org/resources/contrastchecker/", note: "Color contrast ratios" },
  { name: "Adobe Acrobat (free)", url: "https://www.adobe.com/acrobat/pdf-accessibility.html", note: "PDF accessibility check" },
  { name: "WAVE Browser Extension", url: "https://wave.webaim.org/extension/", note: "Website accessibility scan" },
  { name: "Hemingway App", url: "https://hemingwayapp.com", note: "Reading level check" },
  { name: "Coolors Contrast", url: "https://coolors.co/contrast-checker", note: "Design-friendly contrast tool" },
  { name: "NVDA Screen Reader", url: "https://www.nvaccess.org/download/", note: "Free screen reader for testing" },
];

export default function AccessibilityChecklist() {
  const [checked, setChecked] = useState({});
  const [expanded, setExpanded] = useState({ "Before You Build": true });

  const toggle = (id) => setChecked(prev => ({ ...prev, [id]: !prev[id] }));
  const toggleSection = (phase) => setExpanded(prev => ({ ...prev, [phase]: !prev[phase] }));

  const totalItems = CHECKLIST.reduce((sum, s) => sum + s.items.length, 0);
  const totalChecked = Object.values(checked).filter(Boolean).length;
  const pct = Math.round((totalChecked / totalItems) * 100);

  const resetAll = () => setChecked({});

  return (
    <div style={{
      fontFamily: "'Georgia', serif",
      background: "#FAF9F6",
      minHeight: "100vh",
      padding: "2rem 1.5rem",
      maxWidth: 760,
      margin: "0 auto",
      color: "#1a1a1a"
    }}>
      {/* Header */}
      <div style={{ borderBottom: "3px solid #006DA0", paddingBottom: "1.25rem", marginBottom: "1.5rem" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "0.5rem" }}>
          <div>
            <div style={{ fontSize: "0.7rem", letterSpacing: "0.18em", color: "#006DA0", textTransform: "uppercase", fontFamily: "sans-serif", marginBottom: "0.25rem" }}>
              Communicate by Design
            </div>
            <h1 style={{ margin: 0, fontSize: "1.6rem", fontWeight: 700, color: "#111" }}>
              Pre-Publish Accessibility Checklist
            </h1>
            <div style={{ marginTop: "0.3rem", fontSize: "0.82rem", color: "#666", fontFamily: "sans-serif" }}>
              WCAG 2.2 AA · ADA Title II · Section 508 · UDL-aligned
            </div>
          </div>
          <button
            onClick={resetAll}
            style={{
              background: "none", border: "1px solid #ccc", borderRadius: 4,
              padding: "0.35rem 0.75rem", fontSize: "0.75rem", cursor: "pointer",
              color: "#666", fontFamily: "sans-serif"
            }}
          >
            Reset
          </button>
        </div>

        {/* Progress */}
        <div style={{ marginTop: "1rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.35rem", fontFamily: "sans-serif", fontSize: "0.78rem", color: "#555" }}>
            <span>{totalChecked} of {totalItems} items</span>
            <span style={{ fontWeight: 600, color: pct === 100 ? "#006DA0" : "#555" }}>{pct}% complete</span>
          </div>
          <div style={{ background: "#E2E2E2", borderRadius: 99, height: 8 }}>
            <div style={{
              width: `${pct}%`, height: 8, borderRadius: 99,
              background: pct === 100 ? "#006DA0" : "#E86A2E",
              transition: "width 0.3s ease"
            }} />
          </div>
        </div>
      </div>

      {/* Sections */}
      {CHECKLIST.map((section) => {
        const sectionChecked = section.items.filter(i => checked[i.id]).length;
        const isOpen = expanded[section.phase];
        return (
          <div key={section.phase} style={{ marginBottom: "1rem", border: "1px solid #E0DDD8", borderRadius: 6, overflow: "hidden" }}>
            <button
              onClick={() => toggleSection(section.phase)}
              style={{
                width: "100%", display: "flex", justifyContent: "space-between", alignItems: "center",
                padding: "0.85rem 1rem", background: "#fff", border: "none", cursor: "pointer",
                textAlign: "left"
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "0.6rem" }}>
                <span style={{ color: section.color, fontSize: "1rem" }}>{section.icon}</span>
                <span style={{ fontWeight: 700, fontSize: "0.95rem", color: "#111" }}>{section.phase}</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
                <span style={{
                  fontFamily: "sans-serif", fontSize: "0.72rem",
                  color: sectionChecked === section.items.length ? "#006DA0" : "#888",
                  fontWeight: sectionChecked === section.items.length ? 700 : 400
                }}>
                  {sectionChecked}/{section.items.length}
                </span>
                <span style={{ color: "#aaa", fontSize: "0.85rem" }}>{isOpen ? "▲" : "▼"}</span>
              </div>
            </button>

            {isOpen && (
              <div style={{ borderTop: `2px solid ${section.color}`, background: "#FEFEFE", padding: "0.75rem 1rem" }}>
                {section.items.map((item) => (
                  <label
                    key={item.id}
                    style={{
                      display: "flex", alignItems: "flex-start", gap: "0.75rem",
                      padding: "0.55rem 0.25rem", cursor: "pointer",
                      borderBottom: "1px solid #F0EDEA",
                    }}
                  >
                    <input
                      type="checkbox"
                      checked={!!checked[item.id]}
                      onChange={() => toggle(item.id)}
                      style={{ marginTop: 3, accentColor: section.color, width: 15, height: 15, flexShrink: 0 }}
                    />
                    <span style={{
                      fontSize: "0.875rem", lineHeight: 1.5,
                      color: checked[item.id] ? "#999" : "#222",
                      textDecoration: checked[item.id] ? "line-through" : "none",
                      fontFamily: "sans-serif",
                      transition: "color 0.2s"
                    }}>
                      {item.text}
                    </span>
                  </label>
                ))}
              </div>
            )}
          </div>
        );
      })}

      {/* Tools Reference */}
      <div style={{ marginTop: "1.75rem", borderTop: "2px solid #E0DDD8", paddingTop: "1.25rem" }}>
        <h2 style={{ fontSize: "0.95rem", fontWeight: 700, marginBottom: "0.75rem", color: "#111" }}>
          Quick Reference Tools
        </h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: "0.6rem" }}>
          {TOOLS.map((tool) => (
            <a
              key={tool.name}
              href={tool.url}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: "block", padding: "0.6rem 0.85rem",
                background: "#fff", border: "1px solid #E0DDD8", borderRadius: 5,
                textDecoration: "none", color: "inherit"
              }}
            >
              <div style={{ fontFamily: "sans-serif", fontSize: "0.8rem", fontWeight: 600, color: "#006DA0" }}>{tool.name}</div>
              <div style={{ fontFamily: "sans-serif", fontSize: "0.72rem", color: "#888", marginTop: "0.15rem" }}>{tool.note}</div>
            </a>
          ))}
        </div>
      </div>

      {/* CbD Brand Color Reference */}
      <div style={{ marginTop: "1.5rem", borderTop: "2px solid #E0DDD8", paddingTop: "1.25rem" }}>
        <h2 style={{ fontSize: "0.95rem", fontWeight: 700, marginBottom: "0.75rem", color: "#111" }}>
          CbD Brand Colors — Contrast Verified
        </h2>
        <div style={{ fontFamily: "sans-serif", fontSize: "0.82rem", lineHeight: 1.8 }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.3rem" }}>
            <span style={{ display: "inline-block", width: 16, height: 16, background: "#1B1F3B", borderRadius: 2 }}></span>
            <span><strong>Navy #1B1F3B</strong> — 16.08:1 on white (AAA)</span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.3rem" }}>
            <span style={{ display: "inline-block", width: 16, height: 16, background: "#006DA0", borderRadius: 2 }}></span>
            <span><strong>Accessible Teal #006DA0</strong> — 5.68:1 on white, 5.25:1 on gray (AA)</span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.3rem" }}>
            <span style={{ display: "inline-block", width: 16, height: 16, background: "#FFB703", borderRadius: 2 }}></span>
            <span><strong>Amber #FFB703</strong> — borders/accents only (1.75:1 on white — never use as text on light bg)</span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.3rem" }}>
            <span style={{ display: "inline-block", width: 16, height: 16, background: "#00B4D8", borderRadius: 2, border: "1px solid #ccc" }}></span>
            <span style={{ color: "#999" }}><strong>Original Teal #00B4D8</strong> — RETIRED (2.46:1 on white — WCAG fail)</span>
          </div>
        </div>
      </div>

      {/* Footer note */}
      <div style={{ marginTop: "1.5rem", fontSize: "0.72rem", fontFamily: "sans-serif", color: "#aaa", textAlign: "center", lineHeight: 1.6 }}>
        CbD Accessibility Checklist · WCAG 2.2 AA baseline · Updated March 2026<br />
        "Where AT Meets Practice" means the practice starts with our own documents.
      </div>
    </div>
  );
}
