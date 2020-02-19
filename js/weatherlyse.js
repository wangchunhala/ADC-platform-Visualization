function WeatherGraph(graph) {
    var myChart = echarts.init(document.getElementById('chart_2'),"macarons");
    var categories = [];
    console.log(graph.nodes);
    console.log(graph.edges);
    categories[0] = {name: 'Airport'};
    categories[1] = {name: 'Type'};
    categories[2] = {name: 'Weather'};
    categories[3] = {name: 'Information'}
    categories[4] = {name: 'Infection Airport'}


    graph.edges.forEach(function (edge) {
        edge.lineStyle = {
            width:2,
            color:"#FFFAFA"
        };
        edge.type = 'dashed';
        edge.label={
            formatter:edge.name,
            position:'middle',
            show:true,
            fontSize:0.1
//            fontStyle:'italic'
        };
        edge.effect = {
            show:true,
            period:6,
            symbolSize: 3,
            color:"#fff",
            trailLength: 0.7
        };
    });

    var option = {
        title: {
            text: 'Route Point Relation',
            subtext: 'Default layout',
            top: 'bottom',
            left: 'right',
            textStyle : {
                color: '#fff'
            }
        },
        tooltip: {
            formatter: function(param){
                if(param.dataType === 'edge'){
                    return param.data.relationship;
                }
                else{
                    if(param.data.name != undefined){
                        return param.data.detail;
                    }
                    else{
                        return param.data.detail;
                    }
                }

            },
            position:"bottom",
            textStyle:{
                fontSize:10
            }
        },
        toolbox: {
            show : true,//是否显示工具箱
            feature : {
                magicType: ['line', 'bar'], // 图表类型切换，当前仅支持直角系下的折线图、柱状图转换，上图icon左数6/7，分别是切换折线图，切换柱形图
                restore: true, // 还原，复位原始图表，
                saveAsImage: true  // 保存为图片，
            }
        },
        legend: [{
            // selectedMode: 'single',
            type: 'scroll',
            orient: 'vertical',
            right: 10,
            top: 20,
            bottom: 20,
            textStyle:{color:'#fff'},
            selected:{
                'Massage':false
            },
            data: categories.map(function (a) {
                return a.name;
            })
        }],
        animation: true,
        series : [
            {
                name: 'Les Miserables',
                type: 'graph',
                layout: 'force',
                data: graph.nodes,
                links: graph.edges,
                categories: categories,
                edgeSymbol: ['','arrow'],
                edgeSymbolSize: [0,8],
                roam: true,
                draggable: true,
                focusNodeAdjacency: true,
                label: {
                    normal: {
                         fontSize:1,
                        show:true,

                        formatter: function(params){
                            return params.data.name;
                        }
                    }
                },
                force: {
                    repulsion: 500,
//                    edgeLength:70,
                    gravity:0.5
                }
            }
        ]
    };

    tmp_list = graph.infection;
    var length=0;
    for(var item in tmp_list){
        length++;
    }
    tmp_nodes = graph.nodes;

    if(length!=0){
        counter_flag = 0;
        setInterval(function() {
            if(counter_flag<length){
                tmp_nodes.push(tmp_list[counter_flag]);
                counter_flag++;
                myChart.setOption({
                series: [{
                    type: 'graph',
                    roam:true,
                    data:tmp_nodes,
                    links:graph.edges,
                }]
            });
            }
        },2500);
    }

    if (option && typeof option == "object"){
        myChart.setOption(option);
    }
}

function DeleteGraph(graph) {
    var myChart = echarts.init(document.getElementById('chart_2'),"macarons");
    var categories = [];
    categories[0] = {name: 'Airport'};
    categories[1] = {name: 'Type'};
    categories[2] = {name: 'Weather'};
    categories[3] = {name: 'Information'}
    categories[4] = {name: 'Infection Airport'}


    graph.edges.forEach(function (edge) {
        edge.lineStyle = {
            width:2,
            color:"#FFFAFA"
        };
        edge.type = 'dashed';
        edge.label={
            formatter:edge.name,
            position:'middle',
            show:true,
            fontSize:0.1
//            fontStyle:'italic'
        };
        edge.effect = {
            show:true,
            period:6,
            symbolSize: 3,
            color:"#fff",
            trailLength: 0.7
        };
    });

    var option = {
        title: {
            text: 'Route Point Relation',
            subtext: 'Default layout',
            top: 'bottom',
            left: 'right',
            textStyle : {
                color: '#fff'
            }
        },
        tooltip: {
            formatter: function(param){
                if(param.dataType === 'edge'){
                    return param.data.relationship;
                }
                else{
                    if(param.data.name != undefined){
                        return param.data.detail;
                    }
                    else{
                        return param.data.detail;
                    }
                }

            },
            position:"bottom",
            textStyle:{
                fontSize:10
            }
        },
        toolbox: {
            show : true,//是否显示工具箱
            feature : {
                magicType: ['line', 'bar'], // 图表类型切换，当前仅支持直角系下的折线图、柱状图转换，上图icon左数6/7，分别是切换折线图，切换柱形图
                restore: true, // 还原，复位原始图表，
                saveAsImage: true  // 保存为图片，
            }
        },
        legend: [{
            // selectedMode: 'single',
            type: 'scroll',
            orient: 'vertical',
            right: 10,
            top: 20,
            bottom: 20,
            textStyle:{color:'#fff'},
            selected:{
                'Massage':false
            },
            data: categories.map(function (a) {
                return a.name;
            })
        }],
        animation: true,
        series : [
            {
                name: 'Les Miserables',
                type: 'graph',
                layout: 'force',
                data: graph.nodes,
                links: graph.edges,
                categories: categories,
                edgeSymbol: ['','arrow'],
                edgeSymbolSize: [0,8],
                roam: true,
                draggable: true,
                focusNodeAdjacency: true,
                label: {
                    normal: {
                         fontSize:1,
                        show:true,

                        formatter: function(params){
                            return params.data.name;
                        }
                    }
                },
                force: {
                    repulsion: 500,
//                    edgeLength:70,
                    gravity:0.5
                }
            }
        ]
    };

    myChart.setOption(option);
}

function WeatherAnalyse(){
    var tmp_state = $("#statetext").val();
    var tmp_code = $("#codetext").val();

    $.ajax({
        type: 'post',
        url: 'http://127.0.0.1:5000/demo2/weatherlyse',
        data: JSON.stringify([tmp_state, tmp_code]),
        dataType: "jsonp",
        contentType: "application/json; charset=utf-8",
        success: function (res) {
            WeatherGraph(res[0]);
        },
        error: function (msg) {
            console.log(msg);
        }
    });
}

function ClearAll(){
    var tmp_state = $("#statetext").val();
    var tmp_code = $("#codetext").val();

    $.ajax({
        type: 'post',
        url: 'http://127.0.0.1:5000/demo2/clearall',
        data: JSON.stringify([tmp_state, tmp_code]),
        dataType: "jsonp",
        contentType: "application/json; charset=utf-8",
        success: function (res) {
//            console.log(res);
//            DeleteGraph(res[0]);
            location.reload();
        },
        error: function (msg) {
            console.log(msg);
        }
    });
}

$("#upload").click(function(){
    $("#csvfile").click();
});

function csv(){
    $("input[name=csvfile]").csv2arr(function(arr){
        console.log( arr );
        //something to do here
        $.ajax({
            type: 'post',
            url: 'http://127.0.0.1:5000/demo2/csvload',
            data: JSON.stringify(arr),
            dataType: "jsonp",
            contentType: "application/json; charset=utf-8",
            success: function (res) {
                console.log(res);
            },
            error: function (msg) {
                console.log(msg);
            }
        });
    });
}