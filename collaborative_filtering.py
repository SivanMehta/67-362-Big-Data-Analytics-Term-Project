import os, glob, json, re
import 'bayesian_classification/bayes_votes'

from os.path import join
from math import sqrt
from pprint import pprint


class CollaborativeFilter(classifier):
    '''
    def docprob(self,item,cat):
    def prob(self,item,cat):

    def setthreshold(self,cat,t):
    def getthreshold(self,cat):

    def classify(self,item,default = None):

    def sim_distance( prefs, person1, person2 ):
    def sim_pearson( prefs, p1, p2 ):

    def topMatches( prefs, person, n=5, similarity=sim_pearson ):
    def getRecommendations( prefs, person, similarity=sim_pearson ):

    def transformPrefs( prefs ):

    def calculateSimilarItems( prefs, n=10 ):
    def getRecommendedItems( prefs, itemMatch, user ):

    def loadMovieLens_data( path='./ml-100k' ):
    def loadData(path='./ml-100k'):

    def sliceData(seg_n, seg_size, reviews):

    def rmse(sum_of_squares,n):
    def k_fold_cf(subset_perc):
    '''

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


    ###########################################################################
    # Euclidean distance
    ###########################################################################

    # Returns a distance-based similarity score for person1 and person2
    def sim_distance( prefs, person1, person2 ):
        # Get the list of shared_items
        si={}
        for item in prefs[person1]:
          if item in prefs[person2]: si[item]=1

        # if they have no ratings in common, return 0
        if len(si)==0: return 0

        # Add up the squares of all the differences
        sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                            for item in prefs[person1] if item in prefs[person2]])

        return 1/(1+sum_of_squares)
    #  return 1/(1+sqrt(sum_of_squares))

    ###########################################################################
    # Pearson correlation
    ###########################################################################

    # Returns the Pearson correlation coefficient for p1 and p2
    def sim_pearson( prefs, p1, p2 ):
      # Get the list of mutually rated items
      si={}
      for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1

      # if they are no ratings in common, return 0
      if len(si)==0: return 0

      # Sum calculations
      n=len(si)

      # Sums of all the preferences
      sumX=sum([prefs[p1][it] for it in si])
      sumY=sum([prefs[p2][it] for it in si])

      # Sums of the squares
      sumXSq=sum([pow(prefs[p1][it],2) for it in si])
      sumYSq=sum([pow(prefs[p2][it],2) for it in si])

      # Sum of the products
      sumXY=sum([prefs[p1][it]*prefs[p2][it] for it in si])

      # Calculate r (Pearson score)
      num=sumXY-(sumX*sumY/n)
      den=sqrt((sumXSq-pow(sumX,2)/n)*(sumYSq-pow(sumY,2)/n))
      if den==0: return 0

      r=num/den

      return r

    ###########################################################################
    # topmatches
    ###########################################################################

    # Returns the best matches for person from the prefs dictionary.
    # Number of results and similarity function are optional params.
    def topMatches( prefs, person, n=5, similarity=sim_pearson ):
      scores=[(similarity(prefs,person,other),other)
                      for other in prefs if other!=person]
      scores.sort()
      scores.reverse()
      return scores[0:n]

    ###########################################################################
    # getRecommendations
    ###########################################################################

    # Gets recommendations for a person by using a weighted average
    # of every other user's rankings
    def getRecommendations( prefs, person, similarity=sim_pearson ):
      totals={}
      simSums={}
      for other in prefs:
        # don't compare me to myself
        if other==person: continue
        sim=similarity(prefs,person,other)

        # ignore scores of zero or lower
        if sim<=0: continue
        for item in prefs[other]:

          # only score movies I haven't seen yet
          if item not in prefs[person] or prefs[person][item]==0:
            # Similarity * Score
            totals.setdefault(item,0)
            totals[item]+=prefs[other][item]*sim
            # Sum of similarities
            simSums.setdefault(item,0)
            simSums[item]+=sim

      # Create the normalized list
      rankings=[(total/simSums[item],item) for item,total in totals.items()]

      # Return the sorted list
      rankings.sort()
      rankings.reverse()
      return rankings

    ###########################################################################
    # transformPrefs
    ###########################################################################

    def transformPrefs( prefs ):
      result={}
      for person in prefs:
        for item in prefs[person]:
          result.setdefault(item,{})

          # Flip item and person
          result[item][person]=prefs[person][item]
      return result


    ###########################################################################
    # calculateSimilarItems
    ###########################################################################

    def calculateSimilarItems( prefs, n=10 ):
        # Create a dictionary of items showing which other items they
        # are most similar to.
        result={}
        # Invert the preference matrix to be item-centric
        itemPrefs = transformPrefs( prefs )
        c=0
        for item in itemPrefs:
          # Status updates for large datasets
          c+=1
          if c%100==0: print( "%d / %d" % (c,len(itemPrefs)) )
          # Find the most similar items to this one
          scores = topMatches( itemPrefs, item, n=n, similarity=sim_pearson )
          result[item] = scores
        return result

    ###########################################################################
    # getRecommendedItems
    ###########################################################################

    def getRecommendedItems( prefs, itemMatch, user ):
      userRatings=prefs[user]
      scores={}
      totalSim={}
      # Loop over items rated by this user
      for (item,rating) in userRatings.items( ):

        # Loop over items similar to this one
        for (similarity,item2) in itemMatch[item]:

          # Ignore if this user has already rated this item
          if item2 in userRatings: continue
          # Weighted sum of rating times similarity
          scores.setdefault(item2,0)
          scores[item2]+=similarity*rating
          # Sum of all the similarities
          totalSim.setdefault(item2,0)
          totalSim[item2]+=similarity

      # Divide each total score by total weighting to get an average
      rankings=[]
      for item,score in scores.items():
          total = totalSim[item]
          if total != 0:
              rankings.append((score/total,item))
          else:
              rankings.append((0,item))

      # rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

      # Return the rankings from highest to lowest
      rankings.sort( )
      rankings.reverse( )
      return rankings

    ###########################################################################
    # movie lens data set
    ###########################################################################

    # http://grouplens.org/datasets/movielens/

    def loadMovieLens_data( path='./ml-100k' ):
        # Get movie titles
        ml_movies={}
        for line in open( path+'/u.item', encoding="ISO-8859-1" ):
            print( line )
            id, title = line.split('|')[0:2]
            ml_movies[id]=title

        # Load data
        ml_recs={}
        for line in open(path+'/u.data'):
            # note that both user and movieid are retained as strings -not- numbers
            user, movieid, rating, ts = line.split('\t')
            ml_recs.setdefault( user, {} )
            ml_recs[user][ml_movies[movieid]] = float(rating)
        return ml_movies, ml_recs


    ###########################################################################

    from copy import deepcopy

    def loadData(path='./ml-100k'):
        movies = {}
        for line in open( path+'/u.item', encoding="ISO-8859-1" ):
            id, title = line.split('|')[0:2]
            movies[id]=title

        ml_ratings = []
        for line in open(path+'/u.data'):
            # note that both user and movieid are retained as strings -not- numbers
            user, movieid, rating, ts = line.split('\t')
            ml_ratings.append({"user":user, "movie":movies[movieid],
                "rating":float(rating), "ts":ts})

        return ml_ratings


    def transformToDict(ratings):
        recs={}
        for rating in ratings:
            user = rating["user"]
            movie = rating["movie"]
            rate = rating["rating"]
            ts = rating["ts"]

            recs.setdefault( user, {} )
            recs[user][movie] = rate

        return recs


    def sliceData(seg_n, seg_size, reviews):
        temp_ratings = deepcopy(reviews)

        start_index = seg_n*seg_size
        end_index = start_index+seg_size
        print("Segment %d (%d:%d)" % ((seg_n+1), start_index, end_index))

        if ((0<=start_index and start_index<len(temp_ratings)) and
            (0<end_index and end_index<len(temp_ratings)+seg_size)):
            seg = temp_ratings[start_index:end_index]
            temp_ratings = (temp_ratings[0:start_index] +
                temp_ratings[end_index:len(temp_ratings)])

            prefs = transformToDict(temp_ratings)

            return prefs, seg
        else:
            print(rmse_arr)
            print(start_index, end_index, len(temp_ratings))
            raise IndexError('Indices out of range; segment does not exist')


    def rmse(sum_of_squares,n):
        quotient = sum_of_squares/n
        rmse = quotient**0.5

        return rmse


    def k_fold_cf(subset_perc):
        ml_ratings = loadData()
        total_ratings = len(ml_ratings)
        rmse_arr = []
        item_sim = {}
        prefs = {}
        seg = []

        seg_size = int(subset_perc*total_ratings)
        total_segs = int(total_ratings/seg_size)

        if (total_ratings%seg_size!=0):
            total_segs += 1

        for i in range(0,total_segs):
            prefs, seg = sliceData(i,seg_size,ml_ratings)
            item_sim = calculateSimilarItems(prefs,n=len(prefs))

            recs = {}
            seen_recs = {}

            sumSquares = 0
            rmse_val = 0
            for rating in seg:
                user = rating["user"]
                movie = rating["movie"]

                if user in seen_recs:
                    recs = seen_recs[user]
                else:
                    recs = getRecommendedItems(prefs,item_sim,user)
                    seen_recs[user] = recs

                for (rate,title) in recs:
                    if title == movie:
                        predicted = rate
                        break

                actual = rating["rating"]

                squaredPminusA = ((predicted - actual)**2)
                sumSquares += squaredPminusA

            rmse_val = rmse(sumSquares,len(seg))
            print("rmse = {:.5f}".format(rmse_val))
            rmse_arr.append(rmse_val)

        return rmse_arr

    print(k_fold_cf(0.1))


def mtrainPredictor(predictor, votePath = "data/votes_111"):
    for path, dirs, files in os.walk(votePath):
        for data_file in files:
            if ".json" in data_file:
                parseFeatures(predictor, path + "/" + data_file)


mvote_predictor = CollaborativeFilter(getVoteFeatures)
mtrainPredictor(vote_predictor)





topdir = '/Users/suave/mprojects/termproject/data'
votesdir = '/Users/suave/mprojects/termproject/data/votes'
exten = '.json'

mdata = {"hconres":{},"hjres":{},"hr":{},"hres":{},"s":{},"sconres":{},
  "sjres":{},"sjres":{},"sres":{}}
ndata = {}

bills = []
congressmen = {}

class Bill:
  def __init__(self, subjects, filepath=None):
      self.subjects = subjects
      self.filepath = filepath
      
      # Counts of feature/category combinations
      self.fc = {}
      # Counts of documents in each category
      self.cc = {}
      self.getfeatures = getfeatures

class Congressman:
  def __init__(self, id):
      self.votes = []

  def addVote(, ):



def mparseFeatures(votePath=votesdir):
  with open(votePath) as vote_file:
      vote_data = json.load(vote_file)
      if("Aye" not in vote_data["votes"].keys() and
        "Yay" not in vote_data["votes"].keys()): # if it was not voted on
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
                  if vote["id"] in congressmen.keys():
                      congressman = congressmen[vote["id"]]
                  else:
                    congressman = Congressman(vote["id"])
                    congressmen[vote["id"]] = 


                      congressman.addVote(status, )
                      vote["id"]
                  for subject in bill_data["subjects"]:
                      # we are essentially how a particular voter has voted on each subject in the past
                      predictor.train((vote, subject), status)
      except:
          pass


def remap():
  for dirpath, dirnames, files in os.walk(topdir):

    for mfile in files:
      file_path = os.path.join(dirpath, mfile)

      if mfile.lower().endswith(exten):

        with open(file_path) as data_file:

          subdir = os.path.basename(os.path.normpath(dirpath))
          num = re.sub("\D", "", subdir)
          key = re.sub("\d", "", subdir)

          tdata = json.load(data_file)
          match = re.match("(pass)|(enacted)", temp_data[status], re.I)

          if match:
            tbill = Bill(temp_data["subjects"],file_path)
            bills.append(tbill)

            for 
            mdata[key][num] = tdata

  # pprint(mdata)
  with open('/Users/suave/mprojects/termproject/map.txt', 'w') as outfile:
    json.dump(mdata, outfile)

remap()