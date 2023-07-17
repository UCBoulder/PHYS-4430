
# Index/home page
pandoc index.md --toc --filter pandoc-xnos --mathjax -s --include-in-header header.html --include-before-body navbar.html --include-after-body footer.html --template templates/home-template.html -o index.html

# Lab issue page
pandoc lab-issue.md --toc --filter pandoc-xnos --mathjax -s --include-in-header header.html --include-before-body navbar.html --include-after-body footer.html --template templates/lab-issue-template.html -o lab-issue.html

# List of lab guides to generate