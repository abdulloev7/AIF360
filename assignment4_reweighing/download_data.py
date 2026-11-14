"""Download the raw Adult, German and COMPAS files into the folder where AIF360 looks for them.

AIF360 does not ship the data; its loaders read from <aif360 package>/data/raw/<dataset>/.
Run once:  python download_data.py
"""
import os
import urllib.request
import aif360

RAW = os.path.join(os.path.dirname(aif360.__file__), "data", "raw")
UCI = "https://archive.ics.uci.edu/ml/machine-learning-databases"
FILES = {
    "adult": [f"{UCI}/adult/adult.data", f"{UCI}/adult/adult.test", f"{UCI}/adult/adult.names"],
    "german": [f"{UCI}/statlog/german/german.data", f"{UCI}/statlog/german/german.doc"],
    "compas": ["https://raw.githubusercontent.com/propublica/compas-analysis/master/compas-scores-two-years.csv"],
}

for folder, urls in FILES.items():
    os.makedirs(os.path.join(RAW, folder), exist_ok=True)
    for url in urls:
        dest = os.path.join(RAW, folder, url.rsplit("/", 1)[-1])
        if os.path.exists(dest):
            print("already there:", dest)
            continue
        print("downloading", url)
        urllib.request.urlretrieve(url, dest)
print("Done. Files are in", RAW)
