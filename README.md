# Pandoc-bootstrap template
Bootstrap 4 template for Pandoc - Converts markdown files into Twitter Bootstrap styled HTML.

```
pandoc gb2.md --toc --filter pandoc-xnos --mathjax -N -s --include-in-header header.html --include-before-body navbar.html --include-after-body footer.html --template template.html -o gb2.html

pandoc lab-issue.md --toc --filter pandoc-xnos --mathjax -s --include-in-header header.html --include-before-body navbar.html --include-after-body footer.html --template lab-issue-template.html -o lab-issue.html

pandoc index.md --toc --filter pandoc-xnos --mathjax -s --include-in-header header.html --include-before-body navbar.html --include-after-body footer.html --template home-template.html -o index.html

```
