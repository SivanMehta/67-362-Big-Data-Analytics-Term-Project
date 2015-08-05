# Predicting Congress

This project uses data from [here](https://www.govtrack.us/developers/data) and [here](https://github.com/unitedstates/congress) to attempt to predict Congressional results.

Currently, I am just exploring the data set. Here are some things that I am looking at right now
* What type of bills get passed?
* Who is likely to sign a certain bill?
* What type of bill would theoretically have the best chance of getting passed?

You can run a Bayesian classifer based on bills via the following command:
```shell
python3 bayesian_classifier/bayes_bills.py
```
This will train a classifer based off of the bills processed during the 111th and 112th congress, with the goal of trying to predict the results of 113th congress. As of 4/18/2015, we can predict whether or not a bill will be enacted into law with **an accuracy of 92.30563%**

You can do some data exploration by running following commands:

```shell
python3 summarize.py
```
This will list each subject and the proportion of bills concerning that subject that have been enacted into law

```shell
python3 demo.py
```
This will do a similar thing as above, but only print out the top 10, and in a much prettier format

#### Requirements

```shell
[~] python3 --version
Python 3.5.0a1
```