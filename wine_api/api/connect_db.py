from neo4j import GraphDatabase

class Connection():

	# init the connection with db
	def __init__(self):
		self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j"))

	#  close the driver connection
	def close(self):
		self.driver.close()

	# take all varieties from db
	@staticmethod
	def _all_varieties(self, tx):

		query = "MATCH (v:Class)-[:SUBCLASSOF]->(:Class {label: 'varietal'}) RETURN v.label AS varietal"

		result = tx.run(query)

		varietals = [{'varietal': record["varietal"]} for record in result]

		return varietals

	# take all grapes and its growing region
	@staticmethod
	def _growing_grape_regions(self, tx):
	
		query = '''
				MATCH (g:Class)-[:SUBCLASSOF]->(:Class {label:'varietal'}) 
				MATCH (r1:Individual)<-[:grown_in]-(w:Class)-[:made_from]->(g:Class)
				MATCH (r2:Individual)<-[:region_of*1..]-(r1:Individual)
				RETURN DISTINCT g.label AS grape, r1.label AS region, r2.label as region_of
			'''
		result = tx.run(query)

		grape_regions = [{'grape': record["grape"], 'region': record["region"], 'region_of': record["region_of"]} for record in result]

		return grape_regions

	def _wine_types(self, tx):
		query = "MATCH (w:Class)-[:SUBCLASSOF*1..]->(:Class {label: 'wine'}) RETURN DISTINCT w.label AS wine"

		result = tx.run(query)

		wine_types = [{'wine': record["wine"]} for record in result]

		return wine_types

	def _find_wine(self,tx, colour, varietal, region):
		query = "MATCH (w:Class)-[:SUBCLASSOF*1..]->(:Class {label: 'wine'})"
		query_return = " RETURN DISTINCT w.label AS wine"

		to_filter = {}

		if colour:
			to_filter['colour'] = colour
			query += " MATCH (w:Class)-[:has_color]->(c:Class {label: $colour})-[:SUBCLASSOF]->(:Class {label:'color'})"
		if varietal:
			to_filter['varietal'] = varietal
			query += " MATCH (w:Class)-[:made_from]->(v:Class {label: $varietal})-[:SUBCLASSOF]->(:Class {label: 'varietal'})"
		if region:
			to_filter['region'] = region
			query += " MATCH (w:Class)-[:grown_in|region_of*1..]->(r:Individual {label: $region})"
		
		result = tx.run(query+query_return, to_filter)

		wine_found = [{'wine': record["wine"]} for record in result]

		return wine_found



        
        
   