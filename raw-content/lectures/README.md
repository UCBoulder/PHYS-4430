# PHYS 4430 Lecture Materials

This directory contains lecture planning documents and presentation slides for PHYS 4430.

- **Outlines**: Detailed lecture plans with learning objectives, timing, and instructor notes
- **Slides**: Marp-based presentations that can be exported to PowerPoint, PDF, or HTML

## Directory Structure

```
raw-content/lectures/
├── outlines/                  # Lecture planning documents
│   ├── lecture-summary-spring-2026.md
│   ├── week0-thursday.md
│   ├── week1-tuesday.md
│   ├── week1-thursday.md
│   └── ...
├── themes/                    # Shared themes and assets
│   ├── cu-physics.css         # CU Physics Marp theme
│   └── Physics_rev_left.png   # CU Physics logo
├── week2/
│   ├── tuesday/
│   │   ├── slides.md          # Lecture slides (Marp)
│   │   ├── figures/           # Generated figures
│   │   └── generate_figures.py
│   └── thursday/
│       ├── figures/
│       └── generate_figures.py
├── week3/
│   └── ...
└── README.md                  # This file
```

## Lecture Outlines

The `outlines/` directory contains detailed lecture plans:

- `lecture-summary-spring-2026.md` — Semester overview with weekly topics
- `weekN-tuesday.md` / `weekN-thursday.md` — Individual lecture outlines

Each outline includes:
- Learning objectives
- Suggested timing for each section
- Key discussion questions
- Connections to lab work

## Slides

Slides are authored in Markdown using [Marp](https://marp.app/).

### Quick Start

**Option 1: VS Code Extension (Recommended for Authoring)**

1. Install the [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) extension
2. Open any `slides.md` file
3. Click the Marp icon in the top right to preview
4. Export via Command Palette: `Marp: Export Slide Deck`

**Configure VS Code** to use the custom theme by adding to `.vscode/settings.json`:
```json
{
  "markdown.marp.themes": [
    "./raw-content/lectures/themes/cu-physics.css"
  ]
}
```

**Option 2: Marp CLI (For Batch Export)**

Install globally:
```bash
npm install -g @marp-team/marp-cli
```

### Exporting Slides

**Export to PowerPoint** (for sharing with other faculty)

```bash
cd raw-content/lectures
marp week2/tuesday/slides.md --theme themes/cu-physics.css -o week2/tuesday/slides.pptx
```

**Export to PDF**

```bash
marp week2/tuesday/slides.md --theme themes/cu-physics.css --pdf -o week2/tuesday/slides.pdf
```

**Export to HTML** (self-contained, for web hosting)

```bash
marp week2/tuesday/slides.md --theme themes/cu-physics.css --html -o week2/tuesday/slides.html
```

### Generating Figures

Each lecture has a `generate_figures.py` script that creates the figures used in the slides:

```bash
cd raw-content/lectures/week2/tuesday
python generate_figures.py
```

This generates PNG files in the `figures/` subdirectory.

### Writing Slides

**Basic Structure**

```markdown
---
marp: true
theme: cu-physics
math: mathjax
paginate: true
footer: '![logo](../../themes/Physics_rev_left.png)'
---

# Slide Title

Content here

---

# Next Slide

- Bullet points
- Work normally
```

**Special Slide Classes**

**Title slide:**
```markdown
<!-- _class: title -->
<!-- _paginate: false -->

# Lecture Title

## Subtitle
```

**Question/discussion slide:**
```markdown
<!-- _class: question -->

## Question for Students

What do you think happens when...?
```

**Including Figures**

```markdown
![Description](figures/figure_name.png)
```

**Code Blocks**

````markdown
```python
import nidaqmx

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    voltage = task.read()
```
````

**Math (LaTeX via MathJax)**

Inline: `$f = \frac{1}{2\pi}$`

Block:
```markdown
$$f_N = \frac{f_s}{2}$$
```

**Speaker Notes**

```markdown
Content visible on slide

<!--
Speaker notes go here.
Not visible during presentation.
-->
```

### Tips

- Keep slides focused — one main idea per slide
- Use `---` to create new slides
- Preview frequently while editing
- Test PowerPoint export before presenting — some formatting may differ slightly
