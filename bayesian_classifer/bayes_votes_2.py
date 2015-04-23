from pprint import pprint
# from matplotlib import pyplot as plt
import sys, time, math, os, json

class classifier:
    def __init__(self, getfeatures, filename=None):
        # Counts of feature/category combinations
        self.fc = {}
        # Counts of documents in each category
        self.cc = {}
        self.getfeatures = getfeatures
      
    # Increase the count of a feature/category pair
    def incf(self,f,cat):
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat,0)
        self.fc[f][cat]+=1

    # Increase the count of a category
    def incc(self,cat):
        self.cc.setdefault(cat,0)
        self.cc[cat]+=1

    # The number of times a feature has appeared in a category
    def fcount(self,f,cat):
        if f in self.fc and cat in self.fc[f]: 
            return float(self.fc[f][cat])
        return 0.0

    # The number of items in a category
    def catcount(self,cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    # The total number of items
    def totalcount(self):
        return sum(self.cc.values())

    # The list of all categories
    def categories(self):
        return self.cc.keys()

    def train(self,item, cat):
        features = self.getfeatures(item)
        # Increment the count for every feature with this category
        for f in features:
            self.incf(f,cat)

      # Increment the count for this category
        self.incc(cat)

    def fprob(self,f,cat):
        if self.catcount(cat)==0: return 0

      # The total number of times this feature appeared in this 
      # category divided by the total number of items in this category
        return self.fcount(f,cat)/self.catcount(cat)

    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        # Calculate current probability
        basicprob=prf(f,cat)

        # Count the number of times this feature has appeared in
        # all categories
        totals=sum([self.fcount(f,c) for c in self.categories()])

        # Calculate the weighted average
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp

class naivebayes(classifier):
    def __init__(self,getfeatures):
        classifier.__init__(self, getfeatures)
        self.thresholds={}

    def docprob(self,item,cat):
        features = self.getfeatures(item)

        # Multiply the probabilities of all the features together
        p = 1
        for f in features: p += math.log(self.weightedprob(f,cat,self.fprob))
        return -1*p

    def prob(self,item,cat):
        catprob = self.catcount(cat)/self.totalcount()
        docprob = self.docprob(item,cat)
        return 100.0 - (docprob * catprob)

    def setthreshold(self,cat,t):
        self.thresholds[cat]=t

    def getthreshold(self,cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]

    def classify(self,item,default = None):
        probs={}
        # Find the category with the highest probability

        max = 0.0
        for cat in self.categories():
          probs[cat] = self.prob(item,cat)
          if probs[cat] > max: 
            max = probs[cat]
            best = cat
        for cat in probs:
          if cat==best: continue
          if probs[cat]*self.getthreshold(best)>probs[best]: return default
        return best

def getVoteFeatures(vote_data):
    feature_dict = {}
    voter = vote_data[0]["id"]
    subject = vote_data[1]

    feature_dict[(voter, subject)] = 1

    return feature_dict


def parseFeatures(predictor, votePath):
     with open(votePath) as vote_file:
            vote_data = json.load(vote_file)
            if("Aye" not in vote_data["votes"].keys()): # if it was not voted on
                return

            try: 
                billPath = "data/bills_%d/%s/%s%d/data.json" % (
                    vote_data["bill"]["congress"],
                    vote_data["bill"]["type"],
                    vote_data["bill"]["type"],
                    vote_data["number"] )

                with open(billPath) as bill_file:
                    bill_data = json.load(bill_file)

                for status in vote_data["votes"].keys():
                    for vote in vote_data["votes"][status]:
                        for subject in bill_data["subjects"]:
                            # we are essentially how a particular voter has voted on each subject in the past
                            predictor.train((vote, subject), status)
            except:
                pass

def trainPredictor(predictor, votePath = "data/votes_111"):
    for path, dirs, files in os.walk(votePath):
        for data_file in files:
            if ".json" in data_file:
                parseFeatures(predictor, path + "/" + data_file)

def predictOutcomes(predictor):
    pass

vote_predictor = naivebayes(getVoteFeatures)
trainPredictor(vote_predictor)
predictOutcomes(congressional_predictor)

