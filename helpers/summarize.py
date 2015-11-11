from helpers.analysis_utilities import *
import json, sys
from pprint import pprint

class Analysis():
    def __init__(self):
        self.feature_dict = {}
        self.populateFeatureDict()

    def loadFile(self, path = 'bills/hconres/hconres1/data.json' ):
        with open(path) as data_file:
            data = json.load(data_file)

            try:
                self.feature_dict[data["bill_id"]] = data["subjects"] + \
                                                    [data["status"] == "ENACTED:SIGNED"]
            except: pass

    def populateFeatureDict(self, path = "data"):
        print("loading files... ")
        count = 0
        for path, dirs, files in os.walk(path):
            for data_file in files:
                if data_file[-4:] == "json":
                    self.loadFile(path + "/" + data_file)

            count += 1
            sys.stdout.flush()
            sys.stdout.write("\rSeen %d documents" % count)
            
        print(coloredMessage("\tDone", "green"))

    # attempts to answer the question "what types of bills get passed"
    # by looking at the subjects and seeing what proportion of each get passed
    def likelyFeatures(self):

        seen = 0
        # compile the features into map with {subject: (count, passed)}
        subjects = {}
        for bill in self.feature_dict.keys():
            for subject in self.feature_dict[bill][:-1]:
                if subject not in subjects:
                    subjects[subject] = [0, 0]
                subjects[subject][0] += 1
                subjects[subject][1] += 1 if self.feature_dict[bill][-1] else 0

        # pprint(subjects)
        return(sortedHash(subjects)[::-1][:10])

if __name__ == '__main__':
    pprint(Analysis().likelyFeatures())

