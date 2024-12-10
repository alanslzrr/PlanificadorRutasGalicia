# journey.py
from neo4j import GraphDatabase
import logging

class Journey:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_all_stations(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Station) RETURN n.name AS name ORDER BY n.name")
            stations = [record["name"] for record in result]
            return stations

    def get_graph(self):
        with self.driver.session() as session:
            query = """
            MATCH (n:Station)-[r:CONNECTED_TO]->(m:Station)
            RETURN n.name AS from_station, m.name AS to_station, r.time AS time
            """
            result = session.run(query)
            edges = []
            for record in result:
                edges.append((record['from_station'], record['to_station'], record['time']))
            return edges
