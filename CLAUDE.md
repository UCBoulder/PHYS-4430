# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based static website for CU Boulder's PHYS 4430 (Advanced Laboratory) course. It hosts lab guides, resources, and documentation for experimental physics labs. The project includes Python code for lab instrumentation (NI-DAQmx data acquisition, Thorlabs motor control) as part of an ongoing conversion from LabVIEW/Mathematica.

## Common Commands

### Local Development (Docker)
```bash
docker-compose build
docker-compose up
# Site accessible at http://localhost:4000/PHYS-4430/
```

### Converting Lab Guide Markdown to HTML
```bash
cd raw-content
bash mdtohtml.sh
```
This uses pandoc with pandoc-xnos filter for equation/figure numbering. The script converts `raw-content/*.md` files to HTML includes in `_includes/`.

### Python Lab Dependencies
```bash
cd resources/lab-guides/gaussian-laser-beams/python
pip install -r requirements.txt
```

## Architecture

### Content Pipeline
1. Raw markdown lab guides live in `raw-content/` (e.g., `gaussian-beams-1-raw.md`)
2. `mdtohtml.sh` converts them via pandoc to HTML in `_includes/`
3. Jekyll pages in `_pages/` include these HTML fragments
4. Jekyll builds the final site to `_site/`

### Key Directories
- `_pages/` - Main site content (Markdown)
- `_pages/lab-guides/` - Individual lab guide pages
- `raw-content/` - Source markdown for lab guides (edit these, not `_includes/`)
- `_includes/` - Generated HTML fragments (don't edit directly)
- `_layouts/` - Jekyll HTML templates
- `resources/lab-guides/` - Lab resources: PDFs, data files, Python scripts

### Python Lab Code
Lab instrumentation code is in `resources/lab-guides/<lab-name>/python/`. The Gaussian Beams lab has production-ready examples:
- `01_daq_basics.py` - NI-DAQmx introduction
- `02_fitting_example.py` - Curve fitting and data analysis
- `03_fft_analysis.py` - FFT signal processing
- `04_beam_profiler.py` - Thorlabs motor + DAQ automation

These scripts interface with:
- NI USB-6009 DAQ (via nidaqmx)
- Thorlabs KST101 stepper motor controller (via pythonnet + Kinesis SDK)

## Git Workflow

- `main` branch: Production (GitHub Pages builds from here)
- Create feature branches for development
- Current branch `python-conversion`: Converting labs from LabVIEW/Mathematica to Python

## Lab Guide Editing

Edit files in `raw-content/`, not in `_includes/`. After editing, run `mdtohtml.sh` to regenerate HTML. The `labX-raw.md` files are live on the site—use "old/new" naming convention for development versions.
