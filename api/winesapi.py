from flask import Flask, request, jsonify
from api.connect_db import Connection

app = Flask(__name__)

@app.route('/all_varietals', methods=['GET'])
def all_varietals():
	"""
	Creates connection with Neo4j and get all varietals
	:return: dict with varietals

	"""

	# create Neo4j connection
	conn = Connection()

	# make the transaction to get all varietals from Neo4j
	with conn.driver.session() as session:
		varietals = session.read_transaction(conn._all_varietals)

	# close connection
	conn.close()

	response = jsonify(data=varietals)
	response.status_code= 200

	# sending the data and code OK
	return response

@app.route('/all_grape_regions', methods=['GET'])
def grape_regions():
	"""
	Creates connection with Neo4j and get grapes and its growing regions
	:return: dict with grape, region and region_of

	"""

	# create Neo4j connection
	conn = Connection()

	# make the transaction to get all grapes and its growing regions from Neo4j
	with conn.driver.session() as session:
		grape_regions = session.read_transaction(conn._growing_grape_regions)
	
	# close connection
	conn.close()

	response = jsonify({'data': grape_regions})
	response.status_code = 200

	# sending the data and code OK
	return response

@app.route('/wines/all', methods=['GET'])
def wine_types():
	"""
	Creates connection with Neo4j and get all types of wine
	:return: dict with wine types
	"""

	# create Neo4j connection
	conn = Connection()

	# make the transaction to take wine types from Neo4j
	with conn.driver.session() as session:
		wine_types = session.read_transaction(conn._wine_types)

	# close connection
	conn.close()

	response = jsonify({'data': wine_types})
	response.status_code = 200

	# sending the data and the code OK
	return response

@app.route('/wines', methods=['GET'])
def find_wine():
	"""
	Creates connection with Neo4j and get arguments to filter wine
	:return: wines found

	"""

	# take args from the get request
	query_args = request.args

	colour = query_args.get('colour')
	varietal = query_args.get('varietal')
	region = query_args.get('region')

	if not (colour or varietal or region):
		return {'message': 'Wine not found! Please search a wine by colour, varietal or region.'}, 404

	# create Neo4j connection
	conn = Connection()

	# make transaction to find wine with parameters
	with conn.driver.session() as session:
		wines_found = session.read_transaction(conn._find_wine, colour, varietal, region)

	# close connection
	conn.close()

	response = {}

	# in case a wine is not found
	if wines_found:
		response = jsonify({'data': wines_found})
		response.status_code = 200
	else:
		response = jsonify({'message': 'Wine not found using these parameter(s).'})
		response.status_code = 404

	return response
