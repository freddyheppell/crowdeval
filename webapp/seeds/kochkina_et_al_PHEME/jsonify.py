# flake8: noqa

import os
import json

"""
Python 3 function to split rumour files into single JSON files.

Adapted from annotation conversion script by Elena Kochkina, Maria Liakata, and Arkaitz Zubiaga

https://doi.org/10.6084/m9.figshare.6392078.v1

"""


def convert_annotations(annotation, string=True):
    label = None
    if "misinformation" in annotation.keys() and "true" in annotation.keys():
        if int(annotation["misinformation"]) == 0 and int(annotation["true"]) == 0:
            if string:
                label = "unverified"
            else:
                label = 2
        elif int(annotation["misinformation"]) == 0 and int(annotation["true"]) == 1:
            if string:
                label = "true"
            else:
                label = 1
        elif int(annotation["misinformation"]) == 1 and int(annotation["true"]) == 0:
            if string:
                label = "false"
            else:
                label = 0
        elif int(annotation["misinformation"]) == 1 and int(annotation["true"]) == 1:
            print("OMG! They both are 1!")
            print(annotation["misinformation"])
            print(annotation["true"])
            label = None

    elif "misinformation" in annotation.keys() and "true" not in annotation.keys():
        # all instances have misinfo label but don't have true label
        if int(annotation["misinformation"]) == 0:
            if string:
                label = "unverified"
            else:
                label = 2
        elif int(annotation["misinformation"]) == 1:
            if string:
                label = "false"
            else:
                label = 0

    elif "true" in annotation.keys() and "misinformation" not in annotation.keys():
        print("Has true not misinformation")
        label = None
    else:
        print("No annotations")
        label = None

    return label


def generate_tweet_collection(event, subdir):
    tweet_path = os.path.join(event[1], subdir)

    tweets = [f.path for f in os.scandir(tweet_path) if f.is_dir()]

    tweets_list = []

    for tweet in tweets:
        this_tweet_path = os.path.join(tweet)
        source_tweet_path = os.path.join(this_tweet_path, "source-tweets")
        json_files = [
            f.path
            for f in os.scandir(source_tweet_path)
            if str(f.name).endswith(".json")
        ]

        if len(json_files) > 1:
            raise Exception("Two tweets found:" + str(json_files))

        with open(
            os.path.join(this_tweet_path, "annotation.json"), "r"
        ) as annotation_file:
            tweet_annotation = json.load(annotation_file)

        with open(json_files[0], "r") as f:
            tweet_json = json.load(f)
            tweet_json["VERACITY"] = convert_annotations(tweet_annotation)
            tweets_list.append(tweet_json)

    return tweets_list


if __name__ == "__main__":
    events = [(f.name, f.path) for f in os.scandir(os.getcwd()) if f.is_dir()]

    count = 0

    for event in events:
        if event[0] == "output":
            continue

        with open("output/" + event[0] + ".rumours.json", "w+") as file:
            collection = generate_tweet_collection(event, "rumours")
            count += len(collection)
            json.dump(collection, file)

        with open("output/" + event[0] + ".non-rumours.json", "w+") as file:
            collection = generate_tweet_collection(event, "non-rumours")
            count += len(collection)
            json.dump(generate_tweet_collection(event, "non-rumours"), file)

    print(count)
