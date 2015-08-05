from pprint import pprint
from summarize import Analysis
import csv
from pprint import pprint

analysis = Analysis()

def top10Subjects():
    top10 = analysis.likelyFeatures()
    out = [['proportion', 'subject', 'enacted', 'proposed']]

    # message = "## Top 10 Most Passed Subjects ##"
    # out += "#" * len(message) + "\n" + message + "\n" + "#" * len(message) + "\n"
    # header = ("%10s" % "proportion") + ("%51s" % "subject") + ("%8s" % "enacted") + ("%9s" % "proposed")  + "\n"
    # out += header

    # for piece in top10:
    #     out += ("%.8f" % piece[0] + "%50s" % piece[1] + "%7d" % piece[2] + "%8d" % piece[3])

    # print(out)
    # with open("report.txt", "w") as f:
    #     f.close()
    for piece in top10:
            out += [list(piece)]

    with open('report.tsv', 'w+') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t')
        for row in out:
            spamwriter.writerow(row)
        

    # pprint(out)

top10Subjects()