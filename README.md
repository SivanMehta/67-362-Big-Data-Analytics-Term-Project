# Predicting Congress

This project uses data from [here](https://www.govtrack.us/developers/data) to attempt to predict Congressional results

Currently, I am just exploring the data set. Here are some things that I am looking at right now
* What type of bills get passed?
* Who is likely to sign a certain bill?
* What type of bill would theoretically have the best chance of getting passed?

As of right now, you can do some preliminary data exploration by running following commands:

```bash
python summarize.py
```
This will list each subject and the proportion of bills concerning that subject that have been enacted into law

```bash
python demo.py
```
This will do a similar thing as above, but only print out the top 10, and in a much prettier format

**Note:** These files use **Python 3**, *not* Python 2