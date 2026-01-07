#!/bin/bash
# mdtohtml.sh - Convert Gaussian Beams lab markdown files to HTML
#
# Prerequisites:
#   - pandoc (https://pandoc.org/installing.html)
#   - pandoc-xnos filter: pip install pandoc-xnos
#
# Usage:
#   cd raw-content
#   bash mdtohtml.sh
#
# This script converts the gaussian-beams markdown files to HTML includes
# using pandoc with the pandoc-xnos filter for equation/figure numbering.

pandoc gaussian-beams-1-raw.md -o ../_includes/gaussian-beams-1.html --toc --filter pandoc-xnos --mathjax -s -N --template Template.html
pandoc gaussian-beams-2-raw.md -o ../_includes/gaussian-beams-2.html --toc --filter pandoc-xnos --mathjax -s -N --template Template.html
pandoc gaussian-beams-3-raw.md -o ../_includes/gaussian-beams-3.html --toc --filter pandoc-xnos --mathjax -s -N --template Template.html
pandoc gaussian-beams-4-raw.md -o ../_includes/gaussian-beams-4.html --toc --filter pandoc-xnos --mathjax -s -N --template Template.html
