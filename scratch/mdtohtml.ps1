# List of lab guides to generate
# pandoc gb1.md --toc --filter pandoc-xnos -s -N  --template canvasTemplate.html --to html -o ../_includes/gbmark.html
pandoc gb1.md --toc --filter pandoc-xnos --mathjax="https://cdn.mathjax.org/mathjax/..." -s -N --template testTemplate.html -o ../_includes/gbmark.html