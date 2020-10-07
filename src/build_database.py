import csv
from py2neo import Graph, Node, Relationship, NodeMatcher


def load_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        data = []
        for row in reader:
            data.append(row)
        return data


def format_movie_item(raw_data):
    return {
        "id": raw_data["tconst"],
        "name": raw_data["primaryTitle"],
        "tconst": raw_data["tconst"],
        "averageRating": raw_data["averageRating"],
        "numVotes": raw_data["numVotes"],
        "title": raw_data["title"],
        "region": raw_data["region"],
        "language": raw_data["language"],
        "types": raw_data["types"],
        "attributes": raw_data["attributes"],
        "isOriginalTitle": raw_data["isOriginalTitle"],
        "titleType": raw_data["titleType"],
        "primaryTitle": raw_data["primaryTitle"],
        "originalTitle": raw_data["originalTitle"],
        "startYear": raw_data["startYear"],
        "endYear": raw_data["endYear"],
        "runtimeMinutes": raw_data["runtimeMinutes"],
        "length": raw_data["runtimeMinutes"],
        "genres": raw_data["genres"],
        "directors": raw_data["directors"],
        "writers": raw_data["writers"]
    }


def format_people_item(raw_data):
    return {
        "id": raw_data["nconst"],
        "name": raw_data["primaryName"],
        "nconst": raw_data["tconst"],
        "birthYear": raw_data["birthYear"],
        "deathYear": raw_data["deathYear"],
        "primaryProfession": raw_data["primaryProfession"],
        "knownForTitles": raw_data["knownForTitles"]
    }


def insert_movie_data(g, movie_data):
    tx = g.begin()
    visited = set()
    for i in range(len(movie_data)):
        temp = format_movie_item(movie_data[i])
        if temp["id"] in visited:
            print(f"{i}: Skip {temp['id']}, {temp['primaryTitle']}")
        else:
            visited.add(temp["id"])
            print(f"{i}: Insert Movie {temp['id']}, {temp['primaryTitle']}")
            for key in temp.keys():
                if temp[key] == "\\N":
                    temp[key] = ""
            tx.create(Node("Movie", **temp))
    tx.commit()
    # Add Index to accelerate query, important!
    g.run("CREATE INDEX ON :Movie(id)")


def insert_people_data(g, people_data):
    tx = g.begin()
    visited = set()
    for i in range(len(people_data)):
        temp = format_people_item(people_data[i])
        if temp["id"] in visited:
            print(f"{i}: Skip {temp['id']}, {temp['name']}")
        else:
            visited.add(temp["id"])
            print(f"{i}: Insert Person {temp['id']}, {temp['name']}")
            for key in temp.keys():
                if temp[key] == "\\N":
                    temp[key] = ""
            a = Node("Person", **temp)
            tx.create(a)
    tx.commit()
    g.run("CREATE INDEX ON :Person(id)")


def insert_relationship(g, people_data):
    nodes = NodeMatcher(g)
    tx = g.begin()

    RELATIONSHIPS = {
        "actor": Relationship.type("ACT_IN"),
        "actress": Relationship.type("ACT_IN"),
        "director": Relationship.type("DIRECT"),
        "producer": Relationship.type("PRODUCE"),
    }

    visited = set()

    for i in range(len(people_data)):
        person_id, movie_id = people_data[i]["nconst"], people_data[i]["tconst"]
        if (person_id, movie_id) not in visited:
            print(f"{i} Insert Relation: {person_id},{movie_id}")
            visited.add((person_id, movie_id))
            person = nodes.match("Person", id=person_id).first()
            movie = nodes.match("Movie", id=movie_id).first()
            this_relation = people_data[i]["category"]
            if person and movie:
                tx.create(RELATIONSHIPS[this_relation](person, movie))
        else:
            print(f"{i} Skip: {person_id},{movie_id}")
        if i % 1000 == 0:
            print("Committing ...")
            tx.commit()
            tx = g.begin()
    tx.commit()


def add_extra_info(g):
    g.run("MATCH (p:Person)-[:ACT_IN]->(movie) SET p:Actor")
    g.run("MATCH (p:Person)-[:DIRECT]->(movie) SET p:Director")
    # Add Collaborate relationship
    # g.run("MATCH (a:Person)-[:ACT_IN|:DIRECT]->(m:Movie)<-[:ACT_IN|:DIRECT]-(b:Person) "
    #       "CREATE UNIQUE (a)-[r1:COLLABORATE]->(b),(b)-[r2:COLLABORATE]->(a) "
    #       "RETURN count(r1)")


# DB Connection
# bolt -- protocol
# neo4j -- username
# 1234 -- db password
# localhost:7687 -- db url
g = Graph("bolt://neo4j:1234@localhost:7687")

# Clean DB first
g.run("MATCH (n) DETACH DELETE n")

EXPORT_DATA_FOLDER = "../Data_V1"
movie_data = load_csv(f"{EXPORT_DATA_FOLDER}/movie_data.csv")
insert_movie_data(g, movie_data)

people_data = load_csv(f"{EXPORT_DATA_FOLDER}/people_with_relation.csv")
insert_people_data(g, people_data)

insert_relationship(g, people_data)

add_extra_info(g)
