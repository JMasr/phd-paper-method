# What the article prints, and where it comes from

This folder holds the files the article compiles: the LaTeX tables and macro files in [`generated/`](generated/) and the figures in [`figs/`](figs/). They are the reference that [`tools/reproduce.py`](../tools/reproduce.py) compares its own outputs against. Run it from the repository root:

```bash
make install
make reproduce
```

It writes `outputs/` (not tracked) and ends with `ALL REGENERATED OUTPUTS MATCH THE ARTICLE` when every regenerated file agrees with the one here.

## Tables

| File | In the article | Written by | Data |
|---|---|---|---|
| `sota_tab_screen_perf.tex` | Results: performance in the screening stage | `build_paper_sota.py` | screening stage |
| `sota_tab_screen.tex` | Results: contrasts of the screening stage | `build_paper_sota.py` | screening stage |
| `sota_tab_perarm.tex` | Results: performance in the extension stage | `build_paper_sota.py` | extension stage |
| `sota_tab_contrasts.tex` | Results: contrasts of the extension stage | `build_paper_sota.py` | extension stage |
| `sota_tab_corpus.tex` | Results: the dfa–LoRA difference by corpus unit | `build_paper_sota.py` | extension stage |
| `sota_tab_regime.tex` | Results: exploratory breakdown by elicited material | `build_paper_sota.py` | extension stage |
| `sota_tab_controls.tex` | Results: readout controls | `build_paper_sota.py` | extension stage |
| `sota_tab_cost.tex` | Results: cost and reliability | `build_paper_sota.py` | extension stage |
| `supps_tab_stages.tex` | Supplementary Table S1: reproducibility across the two stages | `build_paper_sota.py` | both stages |
| `supps_tab_all_two.tex` | Supplementary Table S2: every arm of the extension stage | `build_paper_sota.py` | extension stage |
| `supps_tab_all_one.tex` | Supplementary Table S3: every arm of the screening stage | `build_paper_sota.py` | screening stage |
| `supps_tab_extra.tex` | Supplementary Table S4: arms outside the main comparison | `build_paper_sota.py` | extension stage |
| `supps_tab_blocks_two_auroc.tex`, `supps_tab_blocks_two_macrof.tex` | Supplementary Tables S5–S6: per-block values, extension stage | `build_paper_sota.py` | extension stage |
| `supps_tab_blocks_one_auroc.tex`, `supps_tab_blocks_one_macrof.tex` | Supplementary Tables S7–S8: per-block values, screening stage | `build_paper_sota.py` | screening stage |
| `supps_tab_stats.tex` | Supplementary Table S9: full statistics of every contrast | `build_paper_sota.py` | both stages |

Supplementary Table S12 (implementation details of the compared arms) and Table S13 (sensitivity analyses) are written in the supplement's source; every number of Table S13 comes from `sensitivity_macros.tex`.

## Macro files

| File | Numbers it carries | Written by | Read from |
|---|---|---|---|
| `sota_macros.tex` | every result quoted in the text | `build_paper_sota.py` | both stages |
| `cost_macros.tex` | end-to-end cost per cell and search budgets | `build_cost_macros.py` | `extension_stage/cell_wall_clock.csv`, both `hpo_trials.csv` |
| `protocol_macros.tex` | partition and learning-rate search as executed | `build_protocol_macros.py` | both `protocol_runs.csv` and `protocol_logs.csv`, `tools/protocol_constants.json` |
| `sensitivity_macros.tex` | sensitivity analyses of the readout | `build_sensitivity_macros.py` | `extension_stage/sensitivity_readout.json` |

## Figures

| File | In the article | Written by |
|---|---|---|
| `figs/fig_blocks.pdf` | Results: paired block-level differences, both stages | `build_paper_sota.py` |
| `figs/fig_rank_curve.pdf` | Supplementary Figure S1: performance against rank | `build_paper_sota.py` |
| `figs/fig4_families.pdf` | Methods: components of the compared strategies (schematic, no data) | `figs/source/render_schematic.sh` from `fig4_families.html` |

`fig_blocks_data.csv` and `fig_rank_curve_data.csv` hold the values each data figure draws; the check compares them, because text and line rendering change between matplotlib versions. With matplotlib 3.3 the rendered pages are also identical to the article's. The schematic is rendered from HTML with Chromium and `pdfcrop`: `bash paper/figs/source/render_schematic.sh fig4_families`.

## Recorded, not regenerated

`datasets_macros.tex`, `models_macros.tex`, `tab_cohorts.tex` (Supplementary Table S10), `tab_splits.tex` (Supplementary Table S11) and `tab_demographics.tex` (age and sex of the speakers used) describe the corpora and the models. They were measured from the per-speaker metadata of the corpora, which cannot be redistributed, and from the public model checkpoints, so no script here regenerates them; they are published as the article prints them. The speaker columns of `tab_splits.tex` are the partition as executed, and `tools/check_splits.py` (run by `make reproduce`) checks them against the protocol logs of both stages.
