---
title: "Python Workflows for PHYS 4430"
layout: textlay
sitemap: false
permalink: /python-workflows
---

# Python Workflows

In this course you'll use two types of Python files: **notebooks** for analysis and **scripts** for data acquisition. Understanding when to use each is more important than which tool you use to open them.

---

## Notebooks vs Scripts

### Notebooks (.ipynb)

Notebooks combine code, output, and documentation in a single file. You write code in cells and run them one at a time, seeing results immediately. Use notebooks for:

- Learning new concepts and experimenting
- Exploratory data analysis
- Curve fitting and making plots
- Creating documented analysis workflows
- Figures for lab reports

### Scripts (.py)

Scripts are plain text files containing Python code that runs from start to finish. Use scripts for:

- Real-time data acquisition
- Automated measurements
- Long-running experiments
- Code that controls hardware

### Why Scripts for Data Acquisition?

For data acquisition and instrument control, scripts are preferred over notebooks because:

1. **Reliability:** Scripts run without the overhead of the Jupyter kernel
2. **Error handling:** Easier to implement proper cleanup if something goes wrong
3. **Automation:** Scripts can be run from the command line
4. **Version control:** Plain text files are easier to track in Git

The provided automation scripts (like `04_beam_profiler.py`) are designed to run as standalone scripts, not in notebooks.

### Quick Reference

| Task | Use |
|------|-----|
| Learning a new concept | Notebook |
| Quick data exploration | Notebook |
| Fitting and plotting data | Notebook |
| Writing lab report figures | Notebook |
| Real-time data acquisition | Script |
| Automated measurements | Script |
| Long-running experiments | Script |
| Controlling hardware | Script |

---

## Recommended Tools

### VS Code (Recommended)

VS Code handles both notebooks and scripts, making it our recommended environment. It's already installed on the lab computers. If you want to install it on your personal computer, download it from [code.visualstudio.com](https://code.visualstudio.com/).

**To run a notebook:** Open any `.ipynb` file and run cells with `Shift+Enter`.

**To run a script:** Open a `.py` file and click the play button (top right) or press `F5`.

#### Required Extensions

Install these extensions (click the Extensions icon in the left sidebar or press `Ctrl+Shift+X`):

| Extension | Publisher | Purpose |
|-----------|-----------|---------|
| Python | Microsoft | Python language support |
| Pylance | Microsoft | Fast, feature-rich language server |
| Jupyter | Microsoft | Run notebooks in VS Code |

#### Useful Shortcuts

- **Run cell:** `Shift+Enter`
- **Select Python interpreter:** Click the Python version in the bottom status bar
- **Open terminal:** `` Ctrl+` ``
- **Command palette:** `Ctrl+Shift+P`
- **Go to definition:** `F12` or `Ctrl+Click`

### JupyterLab (Alternative)

JupyterLab is a browser-based environment for running notebooks. It's a good alternative if you prefer the classic notebook experience.

**To start JupyterLab:**

```bash
py -m jupyter lab
```

This opens a browser window where you can create and run notebooks.

#### Useful Shortcuts

- **Run cell:** `Shift+Enter`
- **Add cell above/below:** `A` / `B` (in command mode)
- **Delete cell:** `D D` (in command mode)
- **Switch to Markdown:** `M` (in command mode)

> **Note:** JupyterLab only runs notebooks. For scripts, use VS Code.

### Google Colab (Alternative)

[Google Colab](https://colab.research.google.com/) runs notebooks in your browser with no software installation required. It's a good option if you're already familiar with it or want to work from a computer without Python installed.

**To use Colab:**
1. Go to [colab.research.google.com](https://colab.research.google.com/)
2. Sign in with your Google account
3. Create a new notebook or upload an existing `.ipynb` file

> **Limitation:** Colab runs on Google's servers, so it cannot communicate with lab hardware. Use Colab only for data analysis—you'll need to collect data using the lab computers and then upload your data files to Colab for analysis.

---

## File Organization

Here's an example structure for organizing your lab work. Create a folder for each lab and keep your data, analysis notebooks, and scripts together:

```
phys4430/
├── gaussian-beams/
│   ├── data/              # Raw data files (CSV)
│   ├── beam_profiler.py   # Script for data acquisition
│   ├── analysis.ipynb     # Notebook for analysis
│   └── figures/           # Saved plots
├── lab-2/
│   ├── data/
│   ├── analysis.ipynb
│   └── ...
└── ...
```

---

[Back to Python Resources](/PHYS-4430/python-resources)
