from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j"))

def get_growing_grape_regions(tx):
    regions = []
    result = tx.run("MATCH (r:Individual)-[:INSTANCEOF]->(:Class {label: 'region'}) RETURN r.label AS region")

    for record in result:
        regions.append(record["region"])
        
    return {'data': regions }, 200

def get_all_varietal(tx):
    varietals = []
    result = tx.run("MATCH (v:Class)-[:SUBCLASSOF]->(:Class {label: 'varietal'}) RETURN v.label AS varietal")

    for record in result:
        varietals.append(record["varietal"])

    return varietals

def get_wine(tx, colour, varietal, region):
    query = '''
        MATCH (:Class {label: 'wine'})<-[:SUBCLASSOF*1..2]-(w:Class)
        MATCH (w:Class)-[:has_color]->(c:Class)-[:SUBCLASSOF]->(:Class {label:'color'})
        MATCH (w:Class)-[:made_from]->(v:Class)-[:SUBCLASSOF]->(:Class {label: 'varietal'})
        MATCH (w:Class)-[:grown_in]->(r:Individual)-[:INSTANCEOF]->(:Class {label: 'region'})
        WHERE c.label = $colour and v.label = $varietal and r.label = $region
        RETURN DISTINCT w.label AS wine
    '''

    wines = []
    result = tx.run(query, colour=colour, varietal=varietal, region=region)

    for record in result:
        wines.append(record["wine"])

    return wines


with driver.session() as session:
    regions = session.read_transaction(get_growing_grape_regions)
    print(' '.join(regions))

    varietals = session.read_transaction(get_all_varietal)
    print(' '.join(varietals))

    wines = session.read_transaction(get_wine,'white','Chardonnay','Chablis')
    print(' '.join(wines))

driver.close()