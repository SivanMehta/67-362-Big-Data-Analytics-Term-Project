import os, glob, json, re, random
from os.path import join
from math import sqrt
from pprint import pprint

import collab_filter

votesdir = '/Users/suave/mprojects/termproject/data'
exten = '.json'

class Classifier:
  def __init__(self, classID, vID, vState, vParty):
      self.id = classID
      self.prefs = {}

      self.vID = vID
      self.vstate = vState
      self.vparty = vParty

      # Counts of feature/category combinations
      self.fc = {}

  def setFeatureDefault(self, feature):
      if feature not in self.fc.keys():
        self.fc.setdefault(feature, {})
        self.fc[feature].setdefault("yea", 0)
        self.fc[feature].setdefault("nea", 0)

  def getFeatureCount(self, feature, vote):
      if feature in self.fc.keys():
        if vote in self.fc[feature].keys():
          return self.fc[feature][vote]
      else:
        self.setFeatureDefault(feature)
        return 0

  def incrFeatureCount(self, feature, vote):
      new_vote = "yea" if (vote == "Aye" or vote == "Yay") else "nea"
      self.fc[feature][new_vote] = self.getFeatureCount(feature, new_vote) + 1
      self.updatePrefs(feature, "yea")

  def updatePrefs(self, feature, vote):
      fcount = self.getFeatureCount(feature,vote)

      total = 0
      for key in self.fc[feature].keys():
        total += self.fc[feature][key]

      # print("yeas: %s, total: %s" % (fcount, total))

      self.prefs[feature] = fcount / total


def mparseFeatures(votePath=votesdir):
  classes = []
  seen_class = {}

  for path, dirs, files in os.walk(votePath):
      # file_count = len(dirs) * len(files)
      for data_file in files:
          file_path = path + '/' + data_file

          # ".json" in data_file
          if re.match(".+(votes).+\.json", file_path):
            with open(file_path) as vote_file:
                # print("Found vote file")
                vote_data = json.load(vote_file)
                if("Aye" not in vote_data["votes"].keys() and
                  "Yay" not in vote_data["votes"].keys()): # if it was not voted on
                    # print("Did not find Aye or Yay")
                    continue

                try: 
                  # print("Found Aye or Yay")
                  bill_path = "/Users/suave/mprojects/termproject/data/bills_%d/%s/%s%d/data.json" % (
                      vote_data["bill"]["congress"],
                      vote_data["bill"]["type"],
                      vote_data["bill"]["type"],
                      vote_data["number"] )

                  with open(bill_path) as bill_file:
                      # print("Found bill file")
                      bill_data = json.load(bill_file)

                  for status in vote_data["votes"].keys():
                      for vote in vote_data["votes"][status]:
                          class_id = vote["state"]
                          if class_id in seen_class.keys():
                              # print("Found clas")
                              clas = seen_class[class_id]
                          else:
                              # print("Making new clas")
                              clas = Classifier(class_id, vote["id"], vote["state"], vote["party"])
                              classes.append(clas)
                              seen_class[class_id] = clas

                          for subject in bill_data["subjects"]:
                              clas.incrFeatureCount(subject, status)
                  bill_file.close()
                  vote_file.close()

                except:
                    continue
  return classes

def getVotesArr():
  classes = mparseFeatures()
  votes = []
  stats = []

  for clas in classes:
      # pprint(clas.prefs)
      highest = {"h":0, "feat":""}
      lowest = {"l":100, "feat":""}

      for feature in clas.prefs.keys():
        perc = clas.prefs[feature]

        # if 0 < perc and perc < 1:

        if perc < lowest["l"]:
          lowest["l"] = perc
          lowest["feat"] = feature
        if highest["h"] < perc:
          highest["h"] = perc
          highest["feat"] = feature

        v = {"id":clas.id, "feature":feature, "vote_perc":clas.prefs[feature],
              "vID":clas.vID, "vstate":clas.vstate, "vparty":clas.vparty}
        votes.append(v)

      stats.append({"id":clas.id, "vstate":clas.vstate, "vparty":clas.vparty,
        "lowest":lowest["l"], "highest":highest["h"], "low_feat":lowest["feat"],
        "high_feat":highest["feat"]})

  random.shuffle(votes)
  # print("Size of votes_arr: %s" % len(votes))
  return votes, stats



votes_arr, stats = getVotesArr()
with open('id_stats.txt', 'w+') as outfile:
  for v in stats:
    low_str = v["low_feat"].replace(',', ':')
    high_str = v["high_feat"].replace(',', ':')
    s = ("%s, %s, %s, %s, %s, %s, %s" % (v["id"], v["vstate"],
         v["vparty"], v["lowest"], low_str, v["highest"], high_str))
    print(s, file=outfile)
outfile.close()
pprint(votes_arr[0:20])
votes_slice = votes_arr[0:500000]
print(collab_filter.k_fold_cf(0.1,votes_arr))