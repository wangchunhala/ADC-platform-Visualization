from data.extract_weather.extract_weather import work
from data.neo4j_database import database
from data.infection.KGInfect import *
from data.data_init import *
import json

def addWeatherToKG(content, airport, Affected_time=23, Affected_cap=33):
    dic = work(content)
    driver = database()
    reference_attribute_dic = {}
    reference_attribute_dic['Aircompany'] = ['name', 'mc']
    reference_attribute_dic['Route'] = ['code', 'name']
    reference_attribute_dic['RoutePoint'] = ['code', 'name']

    weather_property_dic={'云天气': 'CLOUD', '能见度':'CLEARANCE', '风天气':'WIND','雨天气':'RAIN', '雪天气':'SNOW', '霜天气':'FROST', '雷天气':'THUNDERSTORM'}


    timeslot=dic["预计天气信息"]

    nodeList = []
    infectionList = []
    infectionnode = []
    edgeList = []
    edges = []
    id_tmp = 0

    with driver.session() as session:
              result_list = []
              CurrentWeatherLabel = "MERGE (n:CurrentWeather{code:\""+airport+"\",time:\""+"目前"+"\",contents:\""+content+"\",delete:\""+"instant"+"\"})"
              CurrentWeatherRelation="match (a:Airport{code:\""+airport+"\"}),(w:CurrentWeather{code:\""+airport+"\"}) merge (a)-[r:CURRENTWEATHER]->(w)"
              for timeslot1 in timeslot:
                  FutureWWeatherRelation = "match (a:Airport{code:\"" + airport + "\"}) merge (a)-[r:FUTUREWEATHER{time:\"" + timeslot1['时间槽'] +"\"}]->(w:FutureWeather{code:\"" + airport + "\",time:\""+timeslot1['时间槽']+"\",contents:\""+content+"\",delete:\""+"instant"+"\"})"
                  session.run(FutureWWeatherRelation)
              session.run(CurrentWeatherLabel)
              session.run(CurrentWeatherRelation)


              neoorder1="match (a:Airport{code:\""+airport+"\"})-[r:CURRENTWEATHER]->(w) return a,w,r"

              results = session.run(neoorder1).values()
              for result in results:
                  nodeList.append(result[0])
                  nodeList.append(result[1])
                  nodeList = list(set(nodeList))
                  edgeList.append(result[2])
                  edgeList = list(set(edgeList))

              nodes = list(map(buildweathernodes, nodeList))





              neoorder0 = "match (a:Airport{code:\"" + airport + "\"})-[r:FUTUREWEATHER]->(w) return a,w,r"
              results = session.run(neoorder0).values()
              for result in results:
                      nodeList.append(result[1])
                      nodeList = list(set(nodeList))
                      edgeList.append(result[2])
                      edgeList = list(set(edgeList))

              nodes = list(map(buildweathernodes, nodeList))





              present_info_list = dic["目前天气信息"]
              for item in present_info_list:
                for key, value in item.items():
                    if key == "时间槽":
                        continue
                    CurrentWeatherType = "MERGE (n:CurrentWeatherType{code:\"" + airport + "_" + key + "\",delete:\""+"instant"+"\"})"
                    CurrentWeatherTypeRelation = "MATCH (n:CurrentWeather{code:\"" + airport + "\"}), (m:CurrentWeatherType{code:\"" + airport + "_" + key + "\"})" + " merge (n)-[r:" + weather_property_dic[key] + "]->(m)"
                    session.run(CurrentWeatherType)
                    session.run(CurrentWeatherTypeRelation)
                    neoorder2 = "MATCH (n:CurrentWeather{code:\"" + airport + "\"})-[r:" + weather_property_dic[key] + "]->(m:CurrentWeatherType{code:\"" + airport + "_" + key + "\"}) return n,m,r"
                    results = session.run(neoorder2).values()
                    for result in results:
                        nodeList.append(result[1])
                        nodeList = list(set(nodeList))
                        edgeList.append(result[2])
                        edgeList = list(set(edgeList))
                    nodes = list(map(buildweathernodes, nodeList))



                    for currentweatherkey in value:
                        if value[currentweatherkey]!=0 and value[currentweatherkey]!='null':
                            CurrentWeatherInformation="MERGE (n:CurrentWeatherInformation{code:\"" +airport+"_"+ currentweatherkey + "\",value:\""+str(value[currentweatherkey])+"\",delete:\""+"instant"+"\"})"
                            CurrentWeatherInformationRelation = "MATCH (n:CurrentWeatherType{code:\"" + airport+"_"+key  + "\"}), (m:CurrentWeatherInformation{code:\"" + airport+"_"+currentweatherkey + "\"})" + " merge (n)-[r:" + weather_property_dic[key] +"_VALUE" + "]->(m)"#add more information
                            session.run(CurrentWeatherInformation)
                            session.run(CurrentWeatherInformationRelation)

                            neoorder3 =" MATCH ( n:CurrentWeatherType {code:\"" + airport+"_"+key  + "\"})-[r:" + weather_property_dic[key] +"_VALUE" + "]->(m:CurrentWeatherInformation{code:\"" + airport+"_"+currentweatherkey + "\"}) return n,m,r"
                            results = session.run(neoorder3).values()
                            for result in results:
                                nodeList.append(result[1])
                                nodeList = list(set(nodeList))
                                edgeList.append(result[2])
                                edgeList = list(set(edgeList))
                            nodes = list(map(buildweathernodes, nodeList))



              future_info_list = dic["预计天气信息"]

              for item in future_info_list:
                for key, value in item.items():
                    if key == "时间槽":
                        continue
                    FutureWeatherType = "MERGE (n:FutureWeatherType{code:\"" + airport + "_" + key + "\",time:\"" + str(item["时间槽"]) + "\",delete:\""+"instant"+"\"})"
                    FutureWeatherTypeRelation = "MATCH (n:FutureWeather{code:\"" + airport + "\",time:\"" + str(item["时间槽"]) + "\"}), (m:FutureWeatherType{code:\"" + airport + "_" + key  + "\",time:\"" + str(item["时间槽"]) + "\"})" + " merge (n)-[r:" + weather_property_dic[key] + "]->(m)"
                    session.run(FutureWeatherType)
                    session.run(FutureWeatherTypeRelation)
                    neoorder4 = "MATCH (n:FutureWeather{code:\"" + airport + "\",time:\"" + str(item["时间槽"]) + "\"})-[r:" + weather_property_dic[ key] + "]->(m:FutureWeatherType{code:\"" + airport + "_" + key + "\",time:\"" + str(item["时间槽"]) + "\"}) return n,m,r"
                    results = session.run(neoorder4).values()
                    for result in results:
                        nodeList.append(result[1])
                        nodeList = list(set(nodeList))
                        edgeList.append(result[2])
                        edgeList = list(set(edgeList))
                    nodes = list(map(buildweathernodes, nodeList))

                    for futureweatherkey in value:
                        if value[futureweatherkey]!=0 and value[futureweatherkey]!='null':
                            FutureWeatherInformation="MERGE (n:FutureWeatherInformation{code:\"" +airport+"_"+ futureweatherkey +  "\",value:\""+str(value[futureweatherkey])+"\",time:\"" + str(item["时间槽"]) + "\",delete:\""+"instant"+"\"})"
                            FutureWeatherInformationRelation = "MATCH (n:FutureWeatherType{code:\"" + airport+"_"+key  + "\",time:\"" + str(item["时间槽"]) + "\"}), (m:FutureWeatherInformation{code:\""  + airport+"_" + futureweatherkey + "\",time:\"" + str(item["时间槽"]) + "\"})" + " merge (n)-[r:" + weather_property_dic[key] +"_VALUE" +"]->(m)"#add more information
                            session.run(FutureWeatherInformation)
                            session.run(FutureWeatherInformationRelation)

                            neoorder5 =" MATCH ( n:FutureWeatherType {code:\"" + airport+"_"+key  + "\",time:\"" + str(item["时间槽"]) + "\"})-[r:" + weather_property_dic[key] +"_VALUE" + "]->(m:FutureWeatherInformation{code:\"" + airport+"_"+futureweatherkey + "\",time:\"" + str(item["时间槽"]) + "\"}) return n,m,r"
                            results = session.run(neoorder5).values()
                            for result in results:
                                nodeList.append(result[1])
                                nodeList = list(set(nodeList))
                                edgeList.append(result[2])
                                edgeList = list(set(edgeList))
                            nodes = list(map(buildweathernodes, nodeList))

    edge_list, information_dict = infection(airport, Affected_time, Affected_cap)
    # print(information_dict)
    # print(edge_list)
    with driver.session() as session:
        airport_str = "'" + airport + "'"

        information_dict_section = information_dict[airport]
        information_detail = "capacity:%s,flow:%s,distribution:%s,overleft:%s" % (information_dict_section["capacity"],
                                                                                  information_dict_section["flow"],
                                                                                  information_dict_section["distribution"],
                                                                                  information_dict_section["overleft"])
        information_detail = "'" + information_detail + "'"

        neoorder = "MATCH (p:Airport{code:%s}) MERGE (p)-[r:InfectionRoot]->(q:InfectionPoint{name:%s,code:%s,information:%s,delete:'instant'}) RETURN p,q,r" % (
        airport_str, airport_str, airport_str, information_detail)
        results = session.run(neoorder).values()
        for result in results:
            infectionList.append(result[1])
            edgeList.append(result[2])
            edgeList = list(set(edgeList))
        infectionnode = list(map(buildweathernodes, infectionList))


        for pair_list in edge_list:
            origin_str = "'" + pair_list[0] + "'"
            destination_str = "'" + pair_list[1] + "'"

            destination = pair_list[1]
            information_dict_section = information_dict[destination]
            information_detail = "capacity:%s,flow:%s,distribution:%s,overleft:%s" % (
            information_dict_section["capacity"],
            information_dict_section["flow"],
            information_dict_section["distribution"],
            information_dict_section["overleft"])
            information_detail = "'" + information_detail + "'"

            check_order = "MATCH (p:InfectionPoint{name:%s}) RETURN p" % (destination_str)
            check_neoorder = "MATCH (p:InfectionPoint{name:%s}),(q:InfectionPoint{name:%s}) MERGE (p)-[r:Infection]->(q) return p,q,r" % (
                origin_str, destination_str)
            neoorder = "MATCH (p:InfectionPoint{name:%s}) MERGE (p)-[r:Infection]->(q:InfectionPoint{name:%s,code:%s,information:%s,delete:'instant'}) return p,q,r" % (
                origin_str, destination_str, destination_str, information_detail)
            results = session.run(check_order).values()
            # print(results)
            if (len(results) != 0):
                results = session.run(neoorder).values()
            else:
                results = session.run(neoorder).values()
            for result in results:
                infectionList.append(result[1])

                edgeList.append(result[2])
                edgeList = list(set(edgeList))
            infectionnode = list(map(buildweathernodes, infectionList))

    for edge in edgeList:
        data = {"id": str(id_tmp),
                "source": str(edge.start_node._id),
                 "target": str(edge.end_node._id),
                "name": str(edge.type),
                "detail": str(edge.type)
                }
        id_tmp += 1
        edges.append(data)
    result_list.append({"nodes": nodes, "edges": edges, "infection": infectionnode})
    return result_list

def generate_test1():
    content2 = "在北京机场西南60公里处有中等强度的分散对流云团，云团顶高8公里，以40公里/小时的速度向东北移动，强度不变，预计北京时间20日01:00 - 20日02:30影响南昌机场。其间南昌机场还将出现强降水，能见度1200米的低能见度等伴随天气。 "
    addWeatherToKG(content2, "ZGBH")


if __name__ == "__main__":
     generate_test1()
     # print(a)
     # infect_delete()


