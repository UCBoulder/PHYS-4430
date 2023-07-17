
# Index/home page
pandoc ..\markdown\index.md --toc --filter pandoc-xnos --mathjax -s --include-in-header header.html --include-before-body navbar.html --include-after-body footer.html --template ..\templates\home-template.html -o ..\index.html

# Lab issue page
pandoc ..\markdown\lab-issue.md --toc --filter pandoc-xnos --mathjax -s --include-in-header header.html --include-before-body navbar.html --include-after-body footer.html --template ..\templates\lab-issue-template.html -o ..\lab-issue.html

# List of lab guides to generate
pandoc ..\lab-guides\Gaussian-Laser-Beams\gb1.md --toc --filter pandoc-xnos --mathjax -s -N --include-in-header header.html --include-before-body navbar.html --include-after-body footer.html --template ..\templates\lab-guide-template.html -o ..\gb1.html
