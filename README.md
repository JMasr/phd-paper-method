# Closed-form readout versus parameter-efficient adaptation: data release

This repository releases the data behind the article *Closed-Form Depth-Fusion Readout versus Parameter-Efficient Adaptation of Speech Foundation Models for Low-Resource Clinical Screening from Voice* (J. M. Ramírez Sánchez, L. Docío-Fernández, C. García-Mateo; manuscript under review). The article compares a closed-form readout of frozen speech foundation models with five established parameter-efficient fine-tuning methods on clinical voice corpora of tens to hundreds of speakers, with speaker-disjoint partitions, speaker-level metrics and paired tests over blocks.

The experimental framework was run in two stages under one protocol, and each stage has its own folder:

| Folder | Stage in the article | Runs | Arms | Datasets | Blocks |
|---|---|---|---|---|---|
| [`screening_stage/`](screening_stage/) | screening stage | 828 | 23 | 4 | 12 |
| [`extension_stage/`](extension_stage/) | extension stage | 1197 | 13 | 7 | 18 |

Every number in the article's results is computed from these files. Each folder has its own README with the list of files, the arms and the datasets.

## Reading the data

A run is one training of one arm on one dataset, model and partition. A block is one independent corpus unit read through one model, and it is the unit of every statistical test: runs are paired by partition within a block, averaged within the block, and contrasts are Wilcoxon signed-rank tests over blocks with Benjamini–Hochberg correction within each family. The two COPERIA datasets, cough and sustained /a/, come from the same participants, so they form one corpus unit and one block per model. The confirmatory analysis keeps every run, including runs at or below the majority-class floor; the sensitivity analysis drops them, and `analysis_policies.csv` reports both. [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) defines every column.

## Integrity

Each folder's `MANIFEST.json` lists the SHA-256 of every file. To check them:

```bash
python3 -c "import hashlib,json,sys; from pathlib import Path
for d in ('screening_stage','extension_stage'):
    m=json.loads(Path(d,'MANIFEST.json').read_text())
    for f,v in m['files'].items():
        ok=hashlib.sha256(Path(d,f).read_bytes()).hexdigest()==v['sha256']
        print('ok ' if ok else 'BAD', d+'/'+f)"
```

## Reproducing the article's tables and figures

```bash
pip install -r requirements.txt
python3 tools/reproduce.py
```

The four scripts in [`tools/`](tools/) read the two stage folders, check every file against its manifest, and write the article's results tables, the macro files that carry every number quoted in the text, and the two data figures into `outputs/`. `reproduce.py` then compares each output with the copy the article compiles, kept in [`paper/`](paper/), and ends with `ALL REGENERATED OUTPUTS MATCH THE ARTICLE`. The main script also recomputes the analysis engine's own dfa–LoRA contrast in each stage and refuses to run if it does not reproduce it. [`paper/README.md`](paper/README.md) maps every file to its table or figure. The check passes with Python 3.8 and 3.11 and the library versions listed in [`requirements.txt`](requirements.txt).

The corpus and model descriptors (cohort construction, speaker partitions, age and sex, model sizes) are published in `paper/generated/` as the article prints them but are not regenerated, because they were measured from per-speaker metadata of the corpora, which cannot be redistributed.

## What is not here

The repository holds no audio, transcript, speaker identifier or per-speaker prediction, and not the training code or the analysis engine that produced the two packages from the training runs; the analysis here starts from the per-run results. The clinical corpora are governed by their originating agreements and cannot be redistributed: ADReSS is obtained through membership of the DementiaBank consortium, NeuroVoz from a restricted Zenodo record under its owners' data-use agreement, and Coswara from its public repository under CC BY 4.0; no public distribution point for PARCZ could be located; requests concerning COPERIA go to the corresponding author, and VISIA is access-restricted.

## Licence

The data are released under the Creative Commons Attribution 4.0 International licence ([`LICENSE-DATA`](LICENSE-DATA)). The code in `tools/` and `paper/figs/source/` is released under the MIT licence ([`LICENSE`](LICENSE)).

## Citation and contact

Please cite the article; [`CITATION.cff`](CITATION.cff) gives the release metadata, and a versioned archive with a DOI will be deposited on Zenodo. Correspondence: José Manuel Ramírez Sánchez, atlanTTic Research Center, Universidade de Vigo, jmramirez@gts.uvigo.es.
