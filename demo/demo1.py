#!/usr/bin/env python
#encoding=utf-8

import json
from flask import Blueprint, render_template, session, redirect, url_for, request, \
    Response, flash, g, jsonify, abort
from data.neo4j_database import database
from data.data_init import *
from data.map_database import map_data
from data.KGexpand import *
from data.prediction.svm_call import *
driver = database()

mod1 = Blueprint('demo1', __name__)

scatter_dict = {}

@mod1.route("/demo1")
def home1():
    return render_template('demo1.html')

@mod1.route("/demo1/graphdata")
def get_graph_data():
    with driver.session() as session:
        results=session.run('MATCH (p1)-[r1]->(p2{title:"Jerry Maguire"}) RETURN p1,p2,r1').values()
        nodeList=[]
        edgeList=[]
        for result in results:
            nodeList.append(result[0])
            nodeList.append(result[1])
            nodeList=list(set(nodeList))
            edgeList.append(result[2])
        
        edgeList=list(set(edgeList))
        nodes = list(map(buildNodes, nodeList))
        # edges= list(map(buildEdges,edgeList))
        edges=[]
        id_tmp=0
        for edge in edgeList:
            data = {"id":id_tmp,
            "source": str(edge.start_node._id),
            "target":str(edge.end_node._id),
            "name": str(edge.type)}
            id_tmp += 1
            edges.append(data)
    json_data = json.dumps({"nodes": nodes, "edges": edges})
    callback = request.args.get('callback')
    return Response('{}({})'.format(callback, json_data))

@mod1.route("/demo1/mapdata")
def get_map_data():
    name= [
        [{'name': '北京'}, {'name': '上海'}],
        [{'name': '北京'}, {'name': '广州'}],
        [{'name': '北京'}, {'name': '大连'}],
        [{'name': '北京'}, {'name': '南宁'}],
        [{'name': '北京'}, {'name': '南昌'}]
    ];
    json_data = json.dumps(name)
    callback = request.args.get('callback')
    return Response('{}({})'.format(callback, json_data))

@mod1.route("/demo1/neosearch",methods = ['POST'])
def neosearch():
    data = request.get_data()
    neoorder = json.loads(data)
    
    with driver.session() as session:
        results=session.run(neoorder).values()
        nodeList=[]
        edgeList=[]
        for result in results:
            nodeList.append(result[0])
            nodeList.append(result[1])
            nodeList=list(set(nodeList))
            edgeList.append(result[2])
        
        edgeList=list(set(edgeList))
        nodes = list(map(buildNodes, nodeList))
        # edges= list(map(buildEdges,edgeList))
        edges=[]
        id_tmp=0
        for edge in edgeList:
            data = {"id":id_tmp,
            "source": str(edge.start_node._id),
            "target":str(edge.end_node._id),
            "name": str(edge.type)}
            id_tmp += 1
            edges.append(data)
    json_data = json.dumps({"nodes": nodes, "edges": edges})
    callback = request.args.get('callback')
    return Response('{}({})'.format(callback, json_data))

@mod1.route("/demo1/statelyse",methods = ['POST'])
def state_analyse():
    data = request.get_data()
    str_input = json.loads(data)

    result_list=[]
    aim_dict = KGgenerate(str_input)
    aim_embed_code="'"+aim_dict["限流点"]+"_"+aim_dict["发布时间"]+"'"
    neoorder='MATCH (p1:FlowControl{code:%s})-[r1]->(p2) RETURN p1,p2,r1' % (aim_embed_code)

    with driver.session() as session:
        results=session.run(neoorder).values()
        nodeList=[]
        edgeList=[]
        for result in results:
            tmp_dict = (result[1]._properties)
            if(tmp_dict["name"] == 'null'):
                continue
            nodeList.append(result[0])
            nodeList.append(result[1])
            nodeList=list(set(nodeList))
            edgeList.append(result[2])
        
        edgeList=list(set(edgeList))
        nodes = list(map(buildNodes, nodeList))

        # print(nodes)
        # edges= list(map(buildEdges,edgeList))
        edges=[]
        id_tmp=0
        for edge in edgeList:
            data = {"id":id_tmp,
            "source": str(edge.start_node._id),
            "target":str(edge.end_node._id),
            "name": str(edge.type),
            "detail": str(edge.type)
            }
            id_tmp += 1
            edges.append(data)

    result_list.append({"nodes": nodes, "edges": edges})

    aim_embed_routepoint="'"+aim_dict["限流点"]+"'"
    neoorder = 'MATCH (p1)-[r1]->(p2:RoutePoint{code:%s}) RETURN p1,p2,r1'%(aim_embed_routepoint)

    with driver.session() as session:
        results = session.run(neoorder).values()

        scatter_dict.update({"results": results})

        nodeList=[]
        edgeList=[]
        for result in results:
            nodeList.append(result[0])
            nodeList.append(result[1])
            nodeList = list(set(nodeList))
            edgeList.append(result[2])
        edgeList = list(set(edgeList))
        cata = {}
        nodes = []
        for node in nodeList:
            tmp_node, cata = buildweathernodes_test(node, cata)
            nodes.append(tmp_node)
        # edges= list(map(buildEdges,edgeList))
        edges=[]
        id_tmp=0
        for edge in edgeList:
            data = {"id":id_tmp,
            "source": str(edge.start_node._id),
            "target":str(edge.end_node._id),
            "name": str(edge.type)}
            id_tmp += 1
            edges.append(data)


    result_list.append({"nodes": nodes, "edges": edges, "catas": list(cata.keys())})

    prediction_list = get_info(aim_dict["限流点"])
    # print(prediction_list)
    name = []
    for item in prediction_list:
        name.append([{'name': item[0]}, {'name': item[1]}])

    result_list.append(name)

    json_data = json.dumps(result_list)
    callback = request.args.get('callback')
    return Response('{}({})'.format(callback, json_data))

@mod1.route("/demo1/csvload",methods = ['POST'])
def csv_approach():
    data = request.get_data()
    data_input = json.loads(data)

    result_list=[]
    data_length=len(data_input)
    for data_id in range(1,data_length):
        data_list_item = data_input[data_id]
        data_string_item = str(data_list_item)[1:-1]
        aim_dict = KGgenerate(data_string_item.replace("'","\""))
        print(data_string_item)

    aim_embed_code="'"+aim_dict["限流点"]+"_"+aim_dict["发布时间"]+"'"
    neoorder='MATCH (p1:FlowControl{code:%s})-[r1]->(p2) RETURN p1,p2,r1'%(aim_embed_code)

    with driver.session() as session:
        results = session.run(neoorder).values()
        nodeList=[]
        edgeList=[]
        for result in results:
            tmp_dict = (result[1]._properties)
            if (tmp_dict["name"] == 'null'):
                continue
            nodeList.append(result[0])
            nodeList.append(result[1])
            nodeList=list(set(nodeList))
            edgeList.append(result[2])
        
        edgeList=list(set(edgeList))
        nodes = list(map(buildNodes, nodeList))
        # edges= list(map(buildEdges,edgeList))
        edges=[]
        id_tmp=0
        for edge in edgeList:
            data = {"id":id_tmp,
            "source": str(edge.start_node._id),
            "target":str(edge.end_node._id),
            "name": str(edge.type)}
            id_tmp += 1
            edges.append(data)

    result_list.append({"nodes": nodes, "edges": edges})

    aim_embed_routepoint="'"+aim_dict["限流点"]+"'"
    neoorder = 'MATCH (p1)-[r1]->(p2:RoutePoint{code:%s}) RETURN p1,p2,r1'%(aim_embed_routepoint)

    with driver.session() as session:
        results = session.run(neoorder).values()

        scatter_dict.update({"results": results})

        nodeList=[]
        edgeList=[]
        for result in results:
            nodeList.append(result[0])
            nodeList.append(result[1])
            nodeList=list(set(nodeList))
            edgeList.append(result[2])
        edgeList = list(set(edgeList))
        cata = {}
        nodes = []
        for node in nodeList:
            tmp_node, cata = buildweathernodes_test(node, cata)
            nodes.append(tmp_node)
        edges=[]
        id_tmp=0
        for edge in edgeList:
            data = {"id":id_tmp,
            "source": str(edge.start_node._id),
            "target":str(edge.end_node._id),
            "name": str(edge.type)}
            id_tmp += 1
            edges.append(data)
    
    result_list.append({"nodes": nodes, "edges": edges, "catas": list(cata.keys())})

    prediction_list = get_info(aim_dict["限流点"])
    # print(prediction_list)
    name = []
    for item in prediction_list:
        name.append([{'name': item[0]}, {'name': item[1]}])
    # print(name)
    # name = [
    #     [{'name': '北京'}, {'name': '上海'}],
    #     [{'name': '北京'}, {'name': '广州'}],
    #     [{'name': '北京'}, {'name': '大连'}],
    #     [{'name': '北京'}, {'name': '南宁'}],
    #     [{'name': '北京'}, {'name': '南昌'}]
    # ];

    result_list.append(name)

    json_data = json.dumps(result_list)
    callback = request.args.get('callback')
    return Response('{}({})'.format(callback, json_data))

@mod1.route("/demo1/click",methods = ['POST'])
def graph_click():
    data = request.get_data()
    data_input = json.loads(data)
    # print(data_input[1])
    click_point_data = data_input[0]

    # print(click_point_data)
    aim_name = "'" + click_point_data["name"] + "'"
    neoorder1 = 'MATCH (p1)-[r1]->(p2:%s{name:%s}) RETURN p1,p2,r1' % (click_point_data["label"], aim_name)
    neoorder2 = 'MATCH (p1:%s{name:%s})-[r1]->(p2) RETURN p1,p2,r1' % (click_point_data["label"], aim_name)

    nodeList = []
    edgeList = []
    with driver.session() as session:
        old_results = scatter_dict["results"]
        results1 = session.run(neoorder1).values()
        results2 = session.run(neoorder2).values()
        results = results1 + results2 + old_results
        scatter_dict.update({"results": results})
        for result in results:
            nodeList.append(result[0])
            nodeList.append(result[1])
            nodeList = list(set(nodeList))
            edgeList.append(result[2])
            edgeList = list(set(edgeList))

        tmp_nodeList = []
        tmp_nodeId = []
        tmp_edgeList = []
        tmp_edegId = []

        for item in nodeList:
            if item._id in tmp_nodeId:
                continue
            else:
                tmp_nodeList.append(item)
                tmp_nodeId.append(item._id)
        nodeList = tmp_nodeList

        for item in edgeList:
            if item._id in tmp_edegId:
                continue
            else:
                tmp_edgeList.append(item)
                tmp_edegId.append(item._id)
        edgeList = tmp_edgeList

        cata = {}
        nodes = []
        for node in nodeList:
            tmp_node, cata = buildweathernodes_test(node, cata)
            nodes.append(tmp_node)
        edges = []
        id_tmp = 0
        for edge in edgeList:
            data = {"id": id_tmp,
                    "source": str(edge.start_node._id),
                    "target": str(edge.end_node._id),
                    "name": str(edge.type)}
            id_tmp += 1
            edges.append(data)
    result_list = []

    result_list.append({"nodes": nodes, "edges": edges, "catas": list(cata.keys())})

    json_data = json.dumps(result_list)
    callback = request.args.get('callback')
    return Response('{}({})'.format(callback, json_data))