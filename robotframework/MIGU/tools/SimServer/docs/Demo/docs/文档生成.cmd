pandoc readme.md -s -o readme.html
rem pandoc readme.md -s -o readme.docx

rem PPT����
pandoc readme.md -s --webtex  -t slidy -o readme_ppt_slidy.html
pandoc readme.md -s --webtex  -t revealjs -o readme_ppt_revealjs.html
