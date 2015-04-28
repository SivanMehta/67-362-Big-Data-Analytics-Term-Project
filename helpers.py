from pprint import pprint
# from matplotlib import pyplot as plt
import sys, time, math, os

###########################################################################
# sim_pearson
###########################################################################

class ColorError(LookupError): pass

def coloredMessage(message, color):
  if (type(message) != str or type(color) != str):
    raise TypeError("Both arguments of coloredMessage must be strings")

  if "\x1b[0;3" in message:
    raise ColorError("message is already colored")
    
  if color == "black":
    return "\033[0;30m%s\033[0m" % message
  elif color == "red":
    return "\033[0;31m%s\033[0m" % message
  elif color == "green":
    return "\033[0;32m%s\033[0m" % message
  elif color == "yellow":
    return "\033[0;33m%s\033[0m" % message
  elif color == "blue":
    return "\033[0;34m%s\033[0m" % message
  elif color == "magenta":
    return "\033[0;35m%s\033[0m" % message
  elif color == "cyan":
    return "\033[0;36m%s\033[0m" % message
  elif color == "white":
    return "\033[0;37m%s\033[0m" % message
  else:
    raise ColorError("%s is not an ANSI-specified color" % color)

# takes a hash in form of {subject: [count, passed]}
# and returns [(proportion, subject, count, passed)] sorted by proportion
def sortedHash(counts):
  by_proportion = []

  for subject in counts.keys():
    count, passed = counts[subject]
    if count < 50: continue # we don't care about insubstantial issues (were raised fewer than 50 times)
    by_proportion.append((passed/count, subject, count, passed))

  return(sorted(by_proportion))


def downloadFiles():
  # download files
  os.system("rsync -avz --delete --delete-excluded --exclude **/text-versions/ govtrack.us::govtrackdata/congress/111/bills data")

  # remove the files we won't ever read
  os.system("find . -name '*.xml' -type f -delete")
