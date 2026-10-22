# Reproduce the article's tables and figures from the released data.
#   make install     create .venv with the pinned dependencies (uv.lock)
#   make reproduce   regenerate everything and compare it with the article
# Run `make` or `make help` for every target. Requires uv: https://docs.astral.sh/uv/

UV  ?= uv
RUN := $(UV) run --frozen python

.DEFAULT_GOAL := help
.PHONY: help install verify-data tables figures outputs reproduce check-splits schematic clean distclean

help: ## List the targets
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "  make %-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.venv/.synced: pyproject.toml uv.lock
	@command -v $(UV) >/dev/null 2>&1 || { echo "uv is not installed: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
	$(UV) sync --frozen
	@touch $@

install: .venv/.synced ## Create .venv with the pinned dependencies (uv.lock)

verify-data: install ## Check every data file against the SHA-256 in its MANIFEST.json
	$(RUN) tools/verify_data.py

tables: install ## Write the results tables and the macro files to outputs/generated/
	$(RUN) tools/build_paper_sota.py
	$(RUN) tools/build_cost_macros.py
	$(RUN) tools/build_protocol_macros.py
	$(RUN) tools/build_sensitivity_macros.py

figures: install ## Write the data figures and the values they draw to outputs/figs/
	$(RUN) tools/build_paper_sota.py

outputs: tables ## Write every table, macro file and data figure (alias of tables)

reproduce: install ## Regenerate everything and compare it with the article in paper/
	$(RUN) tools/reproduce.py

check-splits: install ## Check the partition table's speaker columns against the protocol logs
	$(RUN) tools/check_splits.py

schematic: ## Render the methods schematic to outputs/figs/ (needs chromium and pdfcrop)
	@mkdir -p outputs/figs/schematic
	@cp paper/figs/source/* outputs/figs/schematic/
	bash outputs/figs/schematic/render_schematic.sh fig4_families
	@cp outputs/figs/schematic/fig4_families.pdf outputs/figs/

clean: ## Remove outputs/
	rm -rf outputs

distclean: clean ## Remove outputs/ and the environment
	rm -rf .venv
