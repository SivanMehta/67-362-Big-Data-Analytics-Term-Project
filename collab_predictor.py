import os, glob, json, re, random
from os.path import join
from math import sqrt
from pprint import pprint

import collab_filter

votesdir = '/Users/suave/mprojects/termproject/data/votes'
exten = '.json'

# class MClassifier:
#   def __init__(self):
#     self.bills = {}
#     self.votes = []
#     self.congressmen = {}
#     self.features = {}

class Congressman:
  def __init__(self, mID, state, party):
      # self.votes = []
      self.id = mID
      self.state = state
      self.party = party
      self.prefs = {}

      # Counts of feature/category combinations
      self.fc = {}

  def getFeatureCount(self, feature, clas):
      if feature in self.fc.keys():
        return self.fc[feature][clas]
      else:
        return -1

  def incrFeatureCount(self, feature, clas):      
      self.fc.setdefault(feature, {})
      self.fc[feature].setdefault("yea", 0)
      self.fc[feature].setdefault("nea", 0)

      new_class = "yea" if (clas == "Aye" or clas == "Yay") else "nea"
      self.fc[feature][new_class] += 1

      self.updatePrefs(feature, "yea")

  def updatePrefs(self, feature, clas):
      # self.fc[feature].setdefault(clas, 0)
      fcount = self.fc[feature][clas]

      total = 0
      for key in self.fc[feature].keys():
        total += self.fc[feature][key]

      self.prefs[feature] = fcount / total


def mparseFeatures(votePath=votesdir):
  congressmen = []
  seen_congressmen = {}

  for dirpath, dirnames, files in os.walk(votePath):
    print("Found votes dir")
    for mfile in files:
      file_path = os.path.join(dirpath, mfile)

      if mfile.lower().endswith(exten):

        with open(file_path) as vote_file:
            print("Found vote file")
            vote_data = json.load(vote_file)
            if("Aye" not in vote_data["votes"].keys() and
              "Yay" not in vote_data["votes"].keys()): # if it was not voted on
                print("Did not find Aye or Yay")
                continue

            # try: 
            print("Find Aye or Yay")
            bill_path = "data/bills_%d/%s/%s%d/data.json" % (
                vote_data["bill"]["congress"],
                vote_data["bill"]["type"],
                vote_data["bill"]["type"],
                vote_data["number"] )

            with open(bill_path) as bill_file:
                print("Found bill file")
                bill_data = json.load(bill_file)
                # bill = Bill(bill_data["subjects"], bill_path)

            for status in vote_data["votes"].keys():
                for vote in vote_data["votes"][status]:
                    if vote["id"] in seen_congressmen.keys():
                        print("Found congressman")
                        congressman = seen_congressmen[vote["id"]]
                    else:
                        print("Making new congressman")
                        congressman = Congressman(vote["id"], vote["state"], vote["party"])
                        congressmen.append(congressman)
                        seen_congressmen[congressman.id] = congressman

                    for subject in bill_data["subjects"]:
                        congressman.incrFeatureCount(subject, status)
                    
            return congressmen

            # except:
            #     pass

def getVotesArr():
  congressmen = mparseFeatures()
  votes = []

  for congressman in congressmen:
      pprint(congressman.prefs)
      for feature in congressman.prefs.keys():
        v = {"congressman":congressman.id, "feature":feature, "vote_perc":congressman.prefs[feature]}
        votes.append(v)

  random.shuffle(votes)
  return votes


votes_arr = getVotesArr()
print(collab_filter.k_fold_cf(0.1,votes_arr))