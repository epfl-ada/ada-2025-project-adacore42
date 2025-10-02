LaTeX Setup Guide
=================

To compile .tex files into PDF you need:

1. A LaTeX distribution (compiler)
2. An editor (e.g., VS Code with LaTeX Workshop)

---------------------------------
1. Install LaTeX Distribution
---------------------------------

macOS:
  - Full: https://tug.org/mactex/
  - Brew (lightweight): brew install --cask mactex-no-gui
  - Add to PATH: export PATH="/Library/TeX/texbin:$PATH"

Linux:
  Ubuntu/Debian:  sudo apt install texlive-full
  Fedora:         sudo dnf install texlive-scheme-full
  Arch:           sudo pacman -S texlive-most

Windows:
  - MiKTeX (light, auto installs pkgs): https://miktex.org/download
  - TeX Live (full, stable): https://tug.org/texlive/

Check install:
  pdflatex --version

---------------------------------
2. VS Code Setup
---------------------------------
- Add extension: LaTeX Workshop (by James-Yu) 
- Recommended settings.json:

  "latex-workshop.latex.autoBuild.run": "onSave"
  "latex-workshop.view.pdf.viewer": "tab"

– Install the Live Share extension in VS Code.
    – One person hosts a session and shares it.
    – Others join via a link, see and edit the same code in real time.

---------------------------------
Done! You can now compile LaTeX files
directly in VS Code into PDFs.

P.S. 
Also, in this folder, you’ll find my latex.json with my snippets. I’ll be updating it over time.