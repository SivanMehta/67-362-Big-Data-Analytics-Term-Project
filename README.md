# Predicting Congress

This project uses data from [here](https://www.govtrack.us/developers/data) and [here](https://github.com/unitedstates/congress) to attempt to predict Congressional results.

As of 11/11/2015, we can predict whether or not a bill will be enacted into law with **an accuracy of 96.88%**


## Requirements

```
$ python3 --version ; pandoc --version
Python 3.5.0a1
pandoc 1.15.0.6
```

## Usage

I recommend using the `bayesian_classifier` module, which contains both a normal version and a distilled version. They do the same thing, but run off two different datasets. The distilled version comes in this repo, you have to download the more bloated version (`~600MB`), by using the command provided when you try to run the file `bayesian_classifer/bayes_bills.py`.


You can run the distilled classifer based on bills via the following command. This will train a classifer based off of the bills processed during the 111th and 112th congress, with the goal of trying to predict the results of 113th congress.

The example output will be as follows:

```
$ python3 bayesian_classifer/bayes_bills_distilled.py
Generating...
Predicting Outcomes for 113th congress...
Classified 1764 bills... Done!

Accuracy --> 96.88209% for 1764 bills
```

However, if you have run the classifier in the past, the program will not re-train the classifer, but rather load it from a file called `distilled_predictor.bayes`

```
$ python3 bayesian_classifer/bayes_bills_distilled.py
Loaded from file
Predicting Outcomes for 113th congress...
Classified 1764 bills... Done!

Accuracy --> 96.88209% for 1764 bills
```