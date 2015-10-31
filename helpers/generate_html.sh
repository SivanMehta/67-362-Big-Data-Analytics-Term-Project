#/bin/bash

# generate the document
pandoc README.md -o index.html

# add header
cat helpers/header.html | cat - index.html > temp && mv temp index.html

# add footer
cat helpers/footer.html >> index.html