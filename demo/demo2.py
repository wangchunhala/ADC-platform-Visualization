#!/usr/bin/env python
#encoding=utf-8

import sys
from flask import Blueprint, render_template, session, redirect, url_for, request, \
    Response, flash, g, jsonify, abort
import json
from data.extract_weather.extract_weather import work
from data.data_init import *
from data.extract_weather.addtoKG import *
from data.neo4j_database import database
from data.cypher_script import infect_delete
driver = database()

mod2 = Blueprint('demo2', __name__)

@mod2.route("/demo2")
def home2():
    return render_template('demo2.html')

@mod2.route("/demo2/weatherlyse",methods = ['POST'])
def weather_analyse():
    data = request.get_data()
    str_input = json.loads(data)

    # flag
    neoorder = "match (n:Airport) where n.name =~\'.*%s.*\' return n.code" % (str_input[1])
    results = driver.session().run(neoorder).values()

    result_list = addWeatherToKG(str_input[0], results[0][0])

    json_data = json.dumps(result_list)
    callback = request.args.get('callback')
    return Response('{}({})'.format(callback, json_data))

@mod2.route("/demo2/clearall",methods = ['POST'])
def clear_all():

    data = request.get_data()
    str_input = json.loads(data)
    airport_code = "'"+str_input[1]+"'"
    infect_delete()

    callback_str = "Clear All!"
    print(callback_str)

    result_list = []
    nodeList = []
    edgeList = []
    edges = []
    infectionnode = []
    # print(airport_code)
    with driver.session() as session:
        neoorder = "match (n:Airport{code:%s}) return n" % (airport_code)
        results = session.run(neoorder).values()
        for result in results:
            nodeList.append(result[0])
            nodeList = list(set(nodeList))
        nodes = list(map(buildweathernodes, nodeList))
        # print(nodes)

    result_list.append({"nodes": nodes, "edges": edges, "infection": infectionnode})

    json_data = json.dumps(result_list)
    callback = request.args.get('callback')
    return Response('{}({})'.format(callback, json_data))


@mod2.route("/demo2/csvload",methods = ['POST'])
def weather_csv_approach():
    data = request.get_data()
    data_input = json.loads(data)

    print(data_input)

    json_data = json.dumps([1, 2, 3])
    callback = request.args.get('callback')
    return Response('{}({})'.format(callback, json_data))