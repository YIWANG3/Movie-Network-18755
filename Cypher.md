# Cypher Examples
### Label Actor/Director
```
MATCH (p:Person)-[:ACT_IN]->(movie) SET p:Actor
```
### Add Collaborate Relationship
Note that UNIQUE is necessary
```
MATCH (a:Person)-[:ACT_IN|:DIRECT]->(m:Movie)<-[:ACT_IN|:DIRECT]-(b:Person)
CREATE UNIQUE (a)-[r1:COLLABORATE]->(b),(b)-[r2:COLLABORATE]->(a)
RETURN count(r1)
```

### Transfer data to gephi
```
MATCH p=(n:Person)-[:ACT_IN|:DIRECT]->(m:Movie)
WITH p
WITH collect(p) AS ps
call apoc.gephi.add('http://localhost:8080','workspace1', ps) yield nodes, relationships, time
return nodes, relationships, time
```

### Export data to .graphml format
```
CALL apoc.export.graphml.all("movies.graphml", {format:"gephi"})
```

### Delete a relationship
```
MATCH ()-[r:COLLABORATE]-() 
DELETE r
```

### Delete all nodes and relationship
```
MATCH (n)
DETACH DELETE n
```

### Fuzzy Query
```
MATCH (n)
WHERE n.genres =~ '(?i).*Sci-Fi.*'
RETURN n
```

### Collect SciFi Only movies
```
MATCH x = (p:Person)-[r:ACT_IN|:DIRECT]->(m:SciFi)
WITH collect(x) AS ps
call apoc.gephi.add('http://localhost:8080','workspace1', ps) yield nodes, relationships, time
return nodes, relationships, time
```


### Only Choose 1 degree
```
MATCH (p:Person)-[r:ACT_IN|:DIRECT*1..2]-(m:StarWarsWorld) SET p:StarWarsWorld
```


### Set birthYear to Int
```
MATCH (n:Person) SET n.birthYear = toInt(n.birthYear) RETURN count(n)
```


### Collect Collaboration Network only 70s 
```
MATCH p=(n:_70S)-[:COLLABORATE]->(m:_70S)
WITH p
WITH collect(p) AS ps
call apoc.gephi.add('http://localhost:8080','workspace1', ps) yield nodes, relationships, time
return nodes, relationships, time
```


### Collect movies with at least 3 shared nodes
```
MATCH (a:Movie)<-[r1:ACT_IN|:DIRECT]-(p:Person)-[r2:ACT_IN|:DIRECT]->(b:Movie) 
WITH a,b,count(p) as rel_cnt 
WHERE rel_cnt > 3 
return a,b limit 10
```

Add Extra Relationship
```
MATCH (a:Movie)<-[r1:ACT_IN|:DIRECT]-(p:Person)-[r2:ACT_IN|:DIRECT]->(b:Movie) 
WITH a,b,count(p) as rel_cnt 
WHERE rel_cnt > 1 
CREATE UNIQUE (a)-[r3:CLOSE_MOVIES]->(b),(b)-[r4:CLOSE_MOVIES]->(a)
RETURN count(r3)
```

Transfer to gephi
```
MATCH p=(n:Movie)-[r:CLOSE_MOVIES]->(m:Movie)
WITH p
WITH collect(p) AS ps
call apoc.gephi.add('http://localhost:8080','workspace1', ps) yield nodes, relationships, time
return nodes, relationships, time
```