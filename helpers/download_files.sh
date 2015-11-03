#/bin/bash

# download the files
rsync -avz --delete --delete-excluded --exclude **/text-versions/ govtrack.us::govtrackdata/congress/113/bills data

# remove the xml files
find . -name '*.xml' -type f -delete