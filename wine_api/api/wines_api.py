import flask
from flask import request, jsonify
from connect_db import Connection

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/wines/all_varieties', methods=['GET'])
def all_varieties():
	# create Neo4j connection
	conn = Connection()

	# make the transaction to take all varieties from Neo4j
	with conn.driver.session() as session:
		varieties = session.read_transaction(conn._all_varieties)

	# close connection
	conn.close()

	# sending the data and code OK
	return {'data': varieties}, 200

@app.route('/wines/all_grape_regions', methods=['GET'])
def grape_regions():
	# create Neo4j connection
	conn = Connection()

	# make the transaction to take all grapes and its growing regions from Neo4j
	with conn.driver.session() as session:
		grape_regions = session.read_transaction(conn._growing_grape_regions)
	
	# close connection
	conn.close()

	# sending the data and code OK
	return {'data': grape_regions}, 200

@app.route('/wines/all', methods=['GET'])
def wine_types():
	# create Neo4j connection
	conn = Connection()

	# make the transaction to take wine types from Neo4j
	with conn.driver.session() as session:
		wine_types = session.read_transaction(conn._wine_types)

	# close connection
	conn.close()

	# sending the data and the code OK
	return {'data': wine_types}, 200

@app.route('/wines', methods=['GET'])
def find_wine():

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

	# in case a wine is not found
	if wines_found:
		return {'data': wines_found}, 200
	else:
		return {'message': 'Wine not found using these parameter(s).'}, 404



if __name__ == '__main__':
	# run the api
    app.run()  