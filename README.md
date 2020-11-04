# Semantic Dev Tech Test  [![Build Status](https://travis-ci.com/EBISPOT/semantic_dev_tech_test.svg?branch=main)](https://travis-ci.com/EBISPOT/semantic_dev_tech_test)

Technical test for semantic dev.

This GitHub Repository has:

 *  An OWL file with an ontology of wines (src/resources/wine.owl)
 *  A script for loading OWL files into a customised Neo4j database.
 *  A `.travis.yml` file that launches a containerised Neo4j database and loads the OWL file into it.
 

### Exercise 1:

Explore the OWL file in Protege and run a reasoner.

![image](https://user-images.githubusercontent.com/112839/97699007-60bd2f00-1aa1-11eb-8e1a-ab8a5b1c98ac.png)

* **Please explain, in a few clear sentences, why the reasoner classifies Barolo as an Italian wine.**

The reasoner finds this inference because the class Barolo is a subclass of the property *grown_in* with the value Piedmont and the former has the property *region_of* with the value Italy. Therefore, the reasoner classifies Barolo as an Italian wine because of the transitive property *region_of* that is a subproperty of *grown_in*.

---


Launch a local copy of the DB and load the ontology

```sh
docker run -p:7474:7474 -p 7687:7687 --env-file ./src/resources/env.list matentzn/vfb-prod
```
Then in a separate terminal window, run:

```sh
python src/load_db.py "https://raw.githubusercontent.com/EBISPOT/semantic_dev_tech_test/main/src/resources/wine.owl"
```

You should be able to browse at http://localhost:7474

* **Compare the original OWL representation of the wine ontology and its representation as a Neo4j labelled property graph and document the transformation in your own words. How do the representations differ? How was the OWL representation mapped into the Neo4j representation?**

The main difference between the OWL representation and its corresponding property graph in Neo4j is the transformation of some definitions and relations in nodes and relations' properties. For instance, in Neo4j every node and relation has the properties *iri*, used in OWL to identify an entity, and *label*. In the case of a Class node, the label is used to define its type in OWL.

The most significant OWL representations mapped in Neo4j is the use of definitions, *NamedIndividual* and *SubClassOf*, as a different relationship that doesn't have properties and is written in upper case, *INSTANCEOF* and *SUBCLASSOF*.  The Object Properties created in OWL are written in lower case in Neo4j and link the same classes and instances. However, the only *Data property year* used by the instance *Barolo_Villero_2015* is not mapped in Neo4j. 

Moreover, the mapping transforms every OWL component (class, property, or individual) into a node. Transforming properties in nodes introduce redundancy in the property graph, as the properties are already accounted for in the relations.

Finally, some of the inferences which create a hierarchy in the class wine in OWL are included explicitly in Neo4j. For example, the class Chablis\_wine has the relation *SUBCLASSOF* with the class French\_wine. However, the class definition using equivalence was not mapped. For instance, in Neo4j, the class French\_wine doesn't have the relation *grown_in* with the class France, but it has the relation *SUBCLASSOF* with the class wine. The same happens with the class Italian\_wine.

### Exercise 2: 

Using a forked copy of this repo as a base, write an API library in Python to query the database with methods to:

* List all grape growing regions (in the ontology)
* List all varietals  (in the ontology)
* List all types (classes) of wine  (in the ontology)
* Query for wine types and individual wines by: colour, varietal, region

Your code should:
  * have at least 3 unit tests, ideally with continuous integration via Travis or GitHub Actions
  * be well documented

If you prefer, you may base your API on SPARQL queries of the OWL ontology in place of Cypher queries of the Neo4J database.

**You should include clear documentation on how to use your API.**

To use Wine API, follow the next steps after having Neo4j with wine ontology running at http://localhost:7474.

To run the API follow these steps:

```sh
$ export FLASK_APP="api/winesapi"
$ flask run
```

In PowerShell:

```sh
> $env:FLASK_APP="api/winesapi"
> python -m flask run
```

The Wine API should be accessible at http://127.0.0.1:5000/


* To get all grape growing regions use the endpoint `/all_grape_regions`

* To get all varietals use the endpoint `/all_varietals`

* To get all types of wine use the endpoint `/wines/all`

* To query for a wine by colour, varietal and region use the endpoint `/wines?colour=<colour_name>&varietal=<varietal_name>&region=<region_name>`

You can use any combination of these three arguments to query a wine, for example:

* `/wines?varietal=<varietal_name>`
* `/wines?colour=<colour_name>&region=<region_name>`
* `/wines?colour=<colour_name>&varietal=<varietal_name>`


### Exercise 3:

**Write a couple of paragraphs on how you might extend the OWL modeling and content to build a knowledge base of individual wines that would be useful to consumers trying to decide what wine to buy.**

Include the 5 characteristics of wine: sweetness, acidity, tannin levels, fruity flavor, light, or full-bodied.

Include other types of wine: Dessert Wine and Sparkling Wine.

Include other types of varietal: Pinot noir, Pinot Grigio, Riesling, Cabernet Sauvignon, etc..

Include dishes that go with specific types of wine.