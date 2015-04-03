from pprint import pprint
from summarize import Analysis

analysis = Analysis()

def top10Subjects():
    pprint(analysis.likelyFeatures()[:10])

top10Subjects()