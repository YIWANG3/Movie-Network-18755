import csv
import os


def load_csv(path):
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        data = []
        for row in reader:
            data.append(row)
        return data


def export_csv(path, data):
    parent_path = '/'.join(path.split('/')[:-1])
    if '/' in path and not os.path.exists(parent_path):
        os.makedirs(parent_path)

    fieldnames = data[0].keys()
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def build_movie_set(movie_data):
    movie_set = set()
    for row in movie_data:
        movie_set.add(row["tconst"])
    return movie_set


def filter_data(raw_data, filter_func):
    res = []
    count = 0
    for row in raw_data:
        if filter_func(row):
            count += 1
            res.append(row)
    return res, count


def movie_filter_func(x):
    return x["titleType"] == "movie" and x["startYear"] != "\\N" and int(x["startYear"]) >= 1960 and x[
        "directors"] != "\\N" and int(x["numVotes"]) >= 4171


def people_filter_func(x):
    return x["tconst"] in filtered_movie_set and x["category"] in ["actress", "actor", "director"]


EXPORT_DATA_FOLDER = "../Data_V2"

# Filter movie data
movie_data = load_csv("../RawData/movie_data.csv")
filtered_movie_data, total = filter_data(movie_data, movie_filter_func)
print(f"Total Movie after filter: {total}")
export_csv(f"{EXPORT_DATA_FOLDER}/movie_data.csv", filtered_movie_data)

# Filter people data
filtered_movie_set = build_movie_set(filtered_movie_data)
people_data = load_csv("../RawData/people_data.csv")
filtered_people_data, total = filter_data(people_data, people_filter_func)
print(f"Total People with relation after filter: {total}")
export_csv(f"{EXPORT_DATA_FOLDER}/people_with_relation.csv", filtered_people_data)
