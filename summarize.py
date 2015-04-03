from pprint import pprint
import json, os, sys

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

    def populateFeatureDict(self, path = "bills"):
        print("loading files... ")
        for path, dirs, files in os.walk("bills"):
            for data_file in files:
                if data_file[-4:] == "json":
                    self.loadFile(path + "/" + data_file)
        print("\tDONE")

        # pprint(self.feature_dict)

    # attempts to answer the question "what types of bills get passed"
    # by looking at the subjects and seeing what proportion of each get passed
    def likelyFeatures(self):

        # compile the features into map with {subject: (count, passed)}

        subjects = {}
        for bill in self.feature_dict.keys():
            for subject in self.feature_dict[bill][:-1]:
                if subject not in subjects:
                    subjects[subject] = [0, 0]
                subjects[subject][0] += 1
                subjects[subject][1] += 1 if self.feature_dict[bill][-1] else 0

        pprint(subjects)

Analysis().likelyFeatures()
