import time
import sys
import os
import pickle
import math

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
        return 1 - best

def get_features(data):
    # needs to return feature dictionary, and the classification
    # in this case, we're going to map a bill to it's status
    sponsor = data[0]
    subjects = data[1]

    features = {}
    for subject in subjects:
        features[subject] = 1
    features[sponsor] = 1

    return features

def train_with_distilled(predictor, input_csv = "data_distilled/distilled_bills_1NF.csv"):
    csv_file = open(input_csv, "r")

    for line in csv_file.readlines():

        try:
            row = line.split("\t")
            sponsor = row[0]
            result = int(row[1])
            subjects = row[2][:-1].split("|") # we use the [:-1] because we don't want to include the new line
            data = [sponsor, subjects]
            predictor.train(data, result)

            seen += 1

            sys.stdout.flush()
            sys.stdout.write("\rTrained %d bills" % seen)
        except:
            pass
            
def predictOutcomes(predictor):
    print("Predicting Outcomes for 113th congress...")
    csv_file = open("data_distilled/data_distilled_113.csv", "r")

    outcomes = [0,0]

    seen = 0
    for line in csv_file.readlines():

        try:
            row = line.split("\t")
            sponsor = row[0]
            result = int(row[1])
            subjects = row[2][:-1].split("|") # we use the [:-1] because we don't want to include the new line
            data = [sponsor, subjects]
            predicted = predictor.classify(data)

            seen += 1
            outcomes[0] += 1 if (result == predicted) else 0
            outcomes[1] += 1
        except:
            pass

        sys.stdout.flush()
        sys.stdout.write("\rClassified %d bills... " % seen)
    
    print("Done!\n")
    print("Accuracy --> %.5f%% for %d bills" % (100*outcomes[0]/outcomes[1], outcomes[1]))

def main():
    start = time.time()

    predictor = "maybe?"

    if not os.path.isfile("distilled_predictor.bayes"):
        print("Generating...")
        predictor = naivebayes(get_features)
        train_with_distilled(predictor, "data_distilled/data_distilled_111.csv")
        train_with_distilled(predictor, "data_distilled/data_distilled_112.csv")

        save_file = open("distilled_predictor.bayes", "wb+")
        pickle.dump(predictor, save_file)
    else:
        save_file = open("distilled_predictor.bayes", "rb")
        predictor = pickle.load(save_file)
        print("Loaded from file")

    predictOutcomes(predictor)

if __name__ == "__main__":
    main()

