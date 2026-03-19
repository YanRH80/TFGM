# ═══════════════════════════════════════════════════════════════
# Makefile — Paper build system
# ═══════════════════════════════════════════════════════════════

.PHONY: fp draft docx figures clean snapshot help

# Default target
help:
	@echo "Usage:"
	@echo "  make figures   — Render all figure PNGs (run first)"
	@echo "  make fp        — Build Family Practice PDF (two-column)"
	@echo "  make draft     — Build draft PDF (one-column)"
	@echo "  make docx      — Build DOCX for submission"
	@echo "  make all       — Build everything"
	@echo "  make snapshot  — Save current outputs to reviews/"
	@echo "  make clean     — Remove generated files"

# ── Figures (run before any render) ───────────────────────────
PYTHON ?= python3
figures:
	$(PYTHON) figures/render_all.py

# ── PDF outputs ───────────────────────────────────────────────
fp: figures
	quarto render index-fp.qmd

draft: figures
	quarto render index-draft.qmd

# ── DOCX output ───────────────────────────────────────────────
docx: figures
	quarto render index-docx.qmd

# ── All ───────────────────────────────────────────────────────
all: figures fp draft docx

# ── Snapshot for review tracking ──────────────────────────────
snapshot:
	@ROUND=$$(ls -d reviews/R* 2>/dev/null | wc -l | tr -d ' '); \
	NEXT=$$((ROUND + 1)); \
	DIR=reviews/R$$NEXT; \
	mkdir -p $$DIR; \
	cp _output/index-fp.pdf $$DIR/submitted-v$$NEXT.pdf 2>/dev/null || true; \
	echo "Snapshot saved to $$DIR/"

# ── Clean ─────────────────────────────────────────────────────
clean:
	rm -rf _output/
	rm -f figures/*.png
