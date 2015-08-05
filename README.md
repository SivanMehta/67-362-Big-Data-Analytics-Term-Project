# Predicting Congress

This project uses data from [here](https://www.govtrack.us/developers/data) and [here](https://github.com/unitedstates/congress) to attempt to predict Congressional results.

Currently, I am just exploring the data set. Here are some things that I am looking at right now:

* What type of bills get passed?
* Who is likely to sign a certain bill?
* What type of bill would theoretically have the best chance of getting passed?

#### Requirements

```shell
[~] python3 --version
Python 3.5.0a1
```

#### Usage

You can run a Bayesian classifer based on bills via the following command:

```shell
python3 bayesian_classifier/bayes_bills.py
```

This will train a classifer based off of the bills processed during the 111th and 112th congress, with the goal of trying to predict the results of 113th congress. As of 4/18/2015, we can predict whether or not a bill will be enacted into law with **an accuracy of 81.90663%**

The example output will be as follows:

```
[~] python3 bayesian_classifer/bayes_bills.py
Creating Classifier...
    Generating...
    Training classifier...
        trained 13675/13675 bills... finished data/bills_111
        trained 12299/12299 bills... finished data/bills_112
        --> done training!
Predicting Outcomes for 113th congress...
    classified bill 11203/11203...Done!

Accuracy --> 81.90663% for 11203 bills
```

However, if you have run the classifier in the past, the program will not re-train the classifer, but rather load it from a file called `predictor.bayes`

```
[~] python3 bayesian_classifer/bayes_bills.py
Creating Classifier...
    Loaded from file
Predicting Outcomes for 113th congress...
    classified bill 11203/11203...Done!

Accuracy --> 81.90663% for 11203 bills
```
