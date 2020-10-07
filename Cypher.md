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
