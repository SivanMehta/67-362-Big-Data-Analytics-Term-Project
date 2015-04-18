from pprint import pprint
from summarize import Analysis

analysis = Analysis()

def top10Subjects():
    top10 = analysis.likelyFeatures()[:10]

    message = "## Top 10 Most Passed Subjects ##"
    print("#" * len(message) + "\n" + message + "\n" + "#" * len(message))
    header = ("%10s" % "proportion") + ("%51s" % "subject") + ("%8s" % "enacted") + ("%9s" % "proposed") 
    print(header)

    for piece in top10:
        print("%.8f" % piece[0], "%50s" % piece[1], "%7d" % piece[2], "%8d" % piece[3])

top10Subjects()