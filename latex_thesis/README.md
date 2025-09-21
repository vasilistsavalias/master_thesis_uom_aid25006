# LaTeX Thesis

This directory contains all files related to the final thesis document, managed with LaTeX.

## Directory Structure (`src/`)
- `main.tex`: The root document. This file ties everything together.
- `preamble.tex`: Contains all package imports (`\usepackage`), custom commands, and document-wide settings.
- `bibliography.bib`: The BibTeX database file for all citations.
- `chapters/`: A subdirectory containing one `.tex` file per chapter.
- `figures/`: A subdirectory to store all plots, diagrams, and images used in the thesis.

## How to Compile
A standard LaTeX compilation workflow is required. If you are using a LaTeX editor (like TeXstudio, VS Code with LaTeX Workshop), you can typically just run the "Build" command.

For command-line compilation, the standard sequence is:
1.  `pdflatex main.tex`
2.  `biber main`
3.  `pdflatex main.tex`
4.  `pdflatex main.tex`

Run these commands from within the `src/` directory. The final compiled `main.pdf` will be generated there, and you can move it to the `output/` directory.

## Dependencies
You will need a full LaTeX distribution, such as:
- [TeX Live](https://www.tug.org/texlive/) (cross-platform)
- [MiKTeX](https://miktex.org/) (Windows)
- [MacTeX](https://www.tug.org/mactex/) (macOS)
Ensure that `biber` is included for bibliography management.