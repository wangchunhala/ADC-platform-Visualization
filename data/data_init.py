def buildNodes(nodeRecord):
    if(len(nodeRecord._labels) != 0):
        data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0], "symbolSize": 15} #将集合元素变为list，然后取出值
        if(data['label'] == 'FlowControl'):
            data.update({'category': 1})
        else:
            data.update({'category': 0})
    else:
        data = {"id": nodeRecord._id}
    data.update(dict(nodeRecord._properties))
    if('title' in data):
        data["name"] = data["title"]
    data["detail"] = str(nodeRecord._properties)
    return data


def buildNodesforroute(nodeRecord):
    if(len(nodeRecord._labels) != 0):
        data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0], "symbolSize": 15}
        data_property = dict(nodeRecord._properties)
        if(data['label'] == 'FlightObject'):
            data.update({'category': 0})
        elif(data['label'] == 'RoutePoint'):
            data.update({'category': 3})
        elif(data['label'] == 'RouteSegment'):
            data.update({'category': 1})
        else:
            data.update({'category': 2})
    else:
        data = {"id": nodeRecord._id, "symbolSize": 20}
    data.update(dict(nodeRecord._properties))
    if ("bbox" in nodeRecord._properties.keys()):
        del nodeRecord._properties["bbox"]
    if('title' in data):
        data["name"] = data["title"]
    data["detail"] = str(nodeRecord._properties)
    return data


def buildweathernodes(nodeRecord):
    if (len(nodeRecord._labels) != 0):
        data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0], "symbolSize": 15}
        if (data['label'] == 'Airport'):
            data.update({'category': 0})
            data.update({"symbolSize": 30})
        elif (data['label'] == 'CurrentWeatherInformation'or data['label'] == 'FutureWeatherInformation'):
            data.update({'category': 3})
            data.update({"symbolSize": 15})
        elif (data['label'] == 'CurrentWeatherType'or data['label'] == 'FutureWeatherType'):
            data.update({'category': 1})
            data.update({"symbolSize": 20})
        elif (data['label'] == 'CurrentWeather'or data['label'] == 'FutureWeather'):
            data.update({'category': 2})
            data.update({"symbolSize": 25})
        else:
            data.update({'category': 4})
            data.update({"symbolSize": 15})
    else:
        data = {"id": nodeRecord._id, "symbolSize": 20}
    data.update(dict(nodeRecord._properties))
    if ('title' in data):
        data["name"] = data["title"]
    if("delete" in nodeRecord._properties.keys()):
        del nodeRecord._properties["delete"]
    if ("bbox" in nodeRecord._properties.keys()):
        del nodeRecord._properties["bbox"]
    data["detail"] = str(nodeRecord._properties)
    return data

def buildweathernodes_test(nodeRecord, cata):
    if (len(nodeRecord._labels) != 0):
        data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0], "symbolSize": 20}
        if (data['label'] in cata.keys()):
            data.update({'category': cata[data['label']]})
        else:
            length = len(cata)
            cata.update({data['label']: length})
            data.update({'category': length})
    else:
        data = {"id": nodeRecord._id, "symbolSize": 15}
    data.update(dict(nodeRecord._properties))
    if ('title' in data):
        data["name"] = data["title"]
    if("delete" in nodeRecord._properties.keys()):
        del nodeRecord._properties["delete"]
    if ("bbox" in nodeRecord._properties.keys()):
        del nodeRecord._properties["bbox"]
    data["detail"] = str(nodeRecord._properties)
    return data, cata
 
def buildEdges(relationRecord):
    data = {"id":relationRecord._id,
            "source": relationRecord.start_node._id,
            "target":relationRecord.end_node._id,
            "name": relationRecord.type,
            }
    return data


def intellNodes(nodeRecord, cata):
    if (len(nodeRecord._labels) != 0):
        data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0], "symbolSize": 15}
        i = 0
        for cata2 in cata:
            if (cata2 == data['label']):
                i = i + 1
        if (i == 0):
            cata.append(data['label'])
        for cata3 in cata:
            if (data['label'] == cata3):
                data.update({'category': cata.index(cata3)})

    else:
        data = {"id": nodeRecord._id, "label": 'others', "symbolSize": 15}
        i = 0;
        for cata2 in cata:
            if (cata2 == data['label']):
                i = i + 1
        if (i == 0):
            cata.append(data['label'])
        for cata3 in cata:
            if (data['label'] == cata3):
                data.update({'category': cata.index(cata3)})

    if ("id" in nodeRecord._properties.keys()):
        del nodeRecord._properties["id"]
    data.update(dict(nodeRecord._properties))

    if ('title' in data):
        data["name"] = data["title"]
    data["detail"] = str(nodeRecord._properties)
    return data, cata


def buildEdges(relationRecord):
    data = {"id": relationRecord._id,
            "source": relationRecord.start_node._id,
            "target": relationRecord.end_node._id,
            "name": relationRecord.type,
            }
    return data