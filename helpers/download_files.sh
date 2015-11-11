#/bin/bash

#make a place to put it
mkdir data

# download the files
rsync -avz --delete --delete-excluded --exclude **/text-versions/ govtrack.us::govtrackdata/congress/$1/bills data/bills_$1

# remove the xml files
find . -name '*.xml' -type f -delete

# remove unneeded json files
find . -name 'text-versions.' -type f -delete