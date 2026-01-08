---
title: "Python Workflows for PHYS 4430"
layout: textlay
sitemap: false
permalink: /python-workflows
---

# Python Workflows

You have several options for writing and running Python code in the lab. This guide helps you choose the right tool for each task.

---

## JupyterLab

JupyterLab provides an interactive environment where you write code in cells and see results immediately. This is ideal for:

- Learning new concepts
- Exploratory data analysis
- Creating documented analysis workflows
- Fitting data and making plots

**To start JupyterLab:**

```bash
py -m jupyter lab
```

This opens a browser window with the JupyterLab interface. Create a new notebook (`.ipynb` file) to get started.

**For the classic notebook interface:**

```bash
py -m jupyter notebook
```

### JupyterLab Tips

- **Run a cell:** Press `Shift+Enter`
- **Add a cell above:** Press `A` (in command mode)
- **Add a cell below:** Press `B` (in command mode)
- **Delete a cell:** Press `D` twice (in command mode)
- **Switch to Markdown:** Press `M` (for documentation cells)
- **Restart kernel:** Use the menu or press `0` twice

---

## VS Code

VS Code is a full-featured code editor, better suited for:

- Writing longer programs (like automation scripts)
- Debugging complex code
- Working with multiple files
- Version control with Git

### Recommended VS Code Extensions

Install these extensions for the best Python experience:

| Extension | Publisher | Purpose |
|-----------|-----------|---------|
| Python | Microsoft | Python language support |
| Pylance | Microsoft | Fast, feature-rich language server |
| Jupyter | Microsoft | Run notebooks in VS Code |

### Running Python in VS Code

**Option 1: Run a script**
- Open a `.py` file
- Click the play button (top right) or press `F5`
- Output appears in the terminal panel

**Option 2: Interactive window**
- Add `# %%` comments to create code cells in a `.py` file
- Run cells with `Shift+Enter`
- Results appear in an interactive window (like Jupyter)

**Option 3: Jupyter notebooks**
- Open a `.ipynb` file directly in VS Code
- Get notebook interactivity with VS Code's editing features

---

## Jupyter Notebooks in VS Code

VS Code can open and run Jupyter notebooks (`.ipynb` files) directly with the Jupyter extension installed. This gives you the best of both worlds:

- Notebook interactivity (run cells, see outputs inline)
- VS Code's powerful editing features (IntelliSense, debugging)
- Version control integration
- Multiple files open simultaneously

**To use:**
1. Install the Jupyter extension
2. Open any `.ipynb` file
3. Select your Python interpreter (bottom right)
4. Run cells with `Shift+Enter`

---

## When to Use Each

| Task | Recommended Environment |
|------|-------------------------|
| Learning a new concept | JupyterLab |
| Quick data exploration | JupyterLab |
| Fitting and plotting data | Either |
| Writing lab report figures | JupyterLab or VS Code notebooks |
| Real-time data acquisition | VS Code (Python script) |
| Automated measurements | VS Code (Python script) |
| Long-running experiments | VS Code (Python script) |
| Debugging complex code | VS Code |

### Why Scripts for Data Acquisition?

For real-time data acquisition and instrument control, standalone Python scripts (`.py` files) are preferred over notebooks because:

1. **Reliability:** Scripts run without the overhead of the Jupyter kernel
2. **Error handling:** Easier to implement proper cleanup if something goes wrong
3. **Automation:** Scripts can be run from the command line or scheduled
4. **Version control:** Plain text files are easier to track in Git

The provided automation scripts (like `04_beam_profiler.py`) are designed to run as standalone scripts, not in notebooks.

---

## File Organization

A suggested structure for your lab work:

```
phys4430/
├── week1/
│   ├── data/           # Raw data files (CSV)
│   ├── analysis.ipynb  # Jupyter notebook for analysis
│   └── figures/        # Saved plots
├── week2/
│   ├── data/
│   ├── analysis.ipynb
│   └── noise_characterization.ipynb
├── week4/
│   ├── data/
│   ├── beam_profiler.py  # Automation script (copy from resources)
│   └── analysis.ipynb
└── final_project/
    ├── data/
    ├── scripts/
    └── analysis/
```

---

[Back to Python Resources](/PHYS-4430/python-resources)
