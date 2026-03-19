# Academic Paper Template

Modular, reproducible template for multi-journal academic publishing with Quarto.

## Quick start

```bash
make figures    # Render all PNGs (once, or when data changes)
make fp         # Family Practice PDF (two-column)
make draft      # One-column draft PDF
make docx       # Word document for submission
make all        # Everything
```

## Architecture

```
├── _quarto.yml              ← Shared: bibliography, language, Lua filter
├── bib.json                 ← Zotero → BBT export
├── Makefile                 ← Build commands
│
├── content/                 ← YOUR WRITING (pure markdown, zero LaTeX)
│   ├── en/                  ← English version
│   │   ├── 01-background.qmd
│   │   ├── 02-case.qmd
│   │   ├── 03-discussion.qmd
│   │   └── 04-backmatter.qmd
│   └── es/                  ← Spanish version (same structure)
│
├── figures/                 ← Pre-rendered PNGs + source scripts
│   ├── fig-timeline.png     ← 300dpi, used by all formats
│   ├── render_all.py        ← Generates all PNGs
│   └── (tab-results.png)    ← Tables as images if needed
│
├── assets/                  ← STYLE LAYER (set and forget)
│   ├── filters/
│   │   └── custom-blocks.lua  ← .box, .quote, .fig-wide → per-format
│   ├── fp/                    ← Family Practice style
│   │   ├── preamble.tex
│   │   └── titleblock.tex
│   ├── draft/                 ← Simple one-column style
│   │   └── preamble.tex
│   ├── docx/
│   │   └── reference.docx
│   └── vancouver-superscript.csl
│
├── index-fp.qmd             ← Assembly: FP two-column PDF
├── index-draft.qmd          ← Assembly: draft one-column PDF
├── index-docx.qmd           ← Assembly: Word document
│
├── reviews/                 ← Review tracking
│   ├── cover-letter.qmd
│   └── R1/, R2/...          ← Snapshots + reviewer responses
│
└── _output/                 ← Generated files (.gitignore)
```

## Custom blocks (Lua filter)

Write in pure markdown. The filter handles format-specific rendering:

```markdown
::: {.box title="Key messages"}
- First point
- Second point
:::

::: {.quote}
"Patient said something important."
:::

::: {.fig-wide}
![Caption](figures/fig-x.png){#fig-label}
:::
```

| Block | PDF | DOCX |
|-------|-----|------|
| `.box` | tcolorbox with thin rule | Bordered paragraph with bold title |
| `.quote` | mdframed with left rule, italic | Italic blockquote |
| `.fig-wide` | `figure*` (spans both columns) | Normal figure |

To add a new block type: add an entry to `handlers` in `custom-blocks.lua`.

## Adapting for a new paper

1. Duplicate this folder
2. Edit `assets/fp/titleblock.tex` (title, authors, abstract)
3. Edit the `title`/`author`/`abstract` in `index-draft.qmd` and `index-docx.qmd`
4. Write your sections in `content/en/*.qmd`
5. Replace `bib.json`
6. `make all`

## Adapting for a new journal

1. Create `assets/newjournal/` with `preamble.tex` and `titleblock.tex`
2. Define `custombox` and `customquote` environments in the preamble (the filter targets these)
3. Create `index-newjournal.qmd` referencing the new assets
4. Add a `make newjournal` target to the Makefile

## Dependencies

- [Quarto](https://quarto.org) ≥ 1.4
- TeX Live with LuaLaTeX
- Python 3 with matplotlib, pandas
- LaTeX packages: `orcidlink`, `fontspec`, `tcolorbox`, `mdframed`, `fancyhdr`, `titlesec`
