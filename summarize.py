from pprint import pprint
import json, os, sys

class Analysis():
    def __init__(self):
        self.feature_dict = {}

        self.populateFeatureDict()


    def loadFile(self, path = 'bills/hconres/hconres1/data.json' ):
        skipped = 0
        with open(path) as data_file:
            data = json.load(data_file)

            try:
                self.feature_dict[data["bill_id"]] = data["subjects"] + \
                                                    [data["status"] == "ENACTED:SIGNED",
                                                    "VETO" in data["status"] and "OVERRIDE" not in data["status"]]
            except:
                sys.stdout.flush()
                sys.stdout.write("\rskipped %d files" % skipped)
                skipped += 1

    def populateFeatureDict(self, path = "bills"):
        for path, dirs, files in os.walk("bills"):
            for data_file in files:
                if data_file[-4:] == "json":
                    self.loadFile(path + "/" + data_file)

        # pprint(self.feature_dict)


Analysis()