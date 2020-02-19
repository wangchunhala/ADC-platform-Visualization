from data.neo4j_database import database

def infect_delete():
    driver = database()
    neoorder1 = "MATCH (p{delete:'instant'}) return p"
    neoorder2 = "MATCH (p{delete:'instant'}) detach delete p"
    with driver.session() as session:
        while(session.run(neoorder1).values()):
            session.run(neoorder2)