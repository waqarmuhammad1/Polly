$(document).ready(function () {
    if(localStorage.getItem("user_name") === null){
        window.location = 'required.html'
    }
    $('.tabs').tabs();
    $('.modal').modal();
    $('select').formSelect();
    var table = null;
    function ajaxCallsFunc(type, url, contentType, data, callback) {
        $.ajax({
            type: type,
            url: url,
            contentType: contentType,
            data: data,
            success: callback,
        });
    };
    var file_name = null;
    $("#logout").click(function(){
        localStorage.removeItem('user_name')
        window.location = 'index.html'
    });
    window.onload = function () {

        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5000/get_train_vars",
            data: null,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if ('Error' in data) {
                    var toastHTML = '<span>Error: ' + data['Error'] + '</span>';
                    M.toast({ html: toastHTML }, 2000);
                }
                else {
                    var train_vars = data['train_vars']
                    var child_elements = create_badges(train_vars, 'green')
                    $("#train_badges").empty();
                    $("#train_badges").append(child_elements);
                }


            },
            error: function (data) {
                var toastHTML = '<span>Error: ' + data['Error'] + '</span>';
                M.toast({ html: toastHTML }, 2000);
            }
        });

        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5000/get_target_vars",
            data: null,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if ('Error' in data) {
                    var toastHTML = '<span>Error: ' + data['Error'] + '</span>';
                    M.toast({ html: toastHTML }, 2000);
                }
                else {
                    var target_vars = data['target_vars']
                    var child_elements = create_badges(target_vars, 'orange')
                    $("#target_badges").empty();
                    $("#target_badges").append(child_elements);
                }


            },
            error: function (data) {
                var toastHTML = '<span>Error: ' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
            }
        });

        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_applied_methods", 'application/json', null, function (branches) {

            data = branches['applied_methods']
            var child_elements = create_badges(data, 'deep-orange accent-3')
            // $("#methods_badges").empty();
            $("#methods_badges").append(child_elements);

        });

        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_attributes_encoded", 'application/json', null, function (branches) {

            data = branches['attributes_encoded']
            console.log(data)
            var child_elements = create_badges(data, 'blue')
            $("#attribute_badges").empty();
            $("#attribute_badges").append(child_elements);

        });
        var analysis_mode = null;
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_analysis_mode", 'application/json', null, function (branches) {


            analysis_mode = branches['analysis_mode']
            console.log(analysis_mode)

        });
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_algorithm_results", 'application/json', null, function (branches) {

            console.log(branches)
            var data = branches['algorithm_results'];
            var fit_data = data['prediction_values']
            data = data['algorithm_results']

            console.log(data)
            console.log(fit_data)
            // var elapsed_time = branches['Elapsed']
            // console.log(branches['Elapsed'])
            var data = jQuery.parseJSON(JSON.stringify(data));

            var target_vars = []

            for (var x in data) {
                target_vars.push(x);
            }
            var algo_names = []

            for (var x in data[target_vars[0]]) {
                algo_names.push(x);
            }

            var metric_names = []
            var temp = target_vars[0];

            var temp2 = algo_names[0];
            var metric_pf = data[temp][temp2];

            for (var x in JSON.parse(metric_pf)) {
                metric_names.push(x);
            }
            var temp8 = []
            for (var h = 0; h < target_vars.length; h++) {
                temp8.push(data[target_vars[h]]);
            }
            var tab_count = 1;
            for (var i = 0; i < target_vars.length; i++) {
                var target_var = target_vars[i];
                var data_dict = [];
                // var tes1 = data[target_var];
                var tes1 = temp8[i];
                for (var j = 0; j < metric_names.length; j++) {
                    var metric_name = metric_names[j];
                    var algo_perf = {};
                    var x = []
                    var y = []

                    for (var k = 0; k < algo_names.length; k++) {
                        var algo_name = algo_names[k];
                        var metric_vals = JSON.parse(tes1[algo_name]);//data[target_var][algo_name]
                        metric_perf = metric_vals[metric_name];
                        algo_perf[algo_name] = metric_perf;
                        x.push(algo_name);
                        y.push(metric_perf);
                    }
                    data_dict.push({ 'x': x, 'y': y, 'name': metric_name, 'type': 'bar' });

                }

                $plot_title = $('#plots-title');
                var tab = "<li class=\"tab col s2\"><a class=\"active\" href=\"#plot" + tab_count.toString() + "\">" + target_var + "</a></li>";
                $plot_title.append(tab);

                if (analysis_mode == 'regression') {
                    var tab2 = "<li class=\"tab col 2\"><a href=\"#plot" + tab_count.toString() + "_scatter\">" + target_var + " Scatter</a></li>";
                    $plot_title.append(tab2);
                }


                $plot_content = $('#plots-content');
                var tab_content = "<div id=\"plot" + tab_count.toString() + "\" ></div>"
                var tab_content_scatter = "<div id=\"plot" + tab_count.toString() + "_scatter\" ></div>"
                $plot_content.append(tab_content);
                $plot_content.append(tab_content_scatter)

                var tab_content_div = document.getElementById("plot" + tab_count.toString());
                var tab_content_scatter_div = document.getElementById("plot" + tab_count.toString() + "_scatter");

                var actual = fit_data[target_var]['Actual']
                var pred = fit_data[target_var]['predicted']
                x = []
                y = []

                var scat_graph_data = [];
                for (var dp = 0; dp < actual.length; dp++) {
                    x.push(dp + 1);
                    y.push(actual[dp])
                }


                var act_graph = {
                    "x": x,
                    "y": y,
                    "mode": 'lines+markers',
                    // "connectgaps": true,
                    "name": target_var,
                    "line": { shape: 'linear', smoothing: 0 },
                    "type": "scatter"
                }

                scat_graph_data.push(act_graph);

                for (var y in pred) {
                    // console.log(x + " "+ target_var)
                    // console.log(pred[x])
                    var x = [];
                    for (var m = 1; m <= pred[y].length; m++) {
                        x.push(m);
                    }
                    scat_graph_data.push({

                        'x': x,
                        'y': pred[y],
                        'mode': 'lines+markers',
                        // 'connectgaps':true,
                        'name': y + " (" + target_var + ")",
                        "line": { shape: 'linear', smoothing: 0 },
                        "type": "scatter"

                    });
                }
                var title_graph = null;
                if (analysis_mode == "regression") {
                    title_graph = 'Algorithm Metric Comparison of: "' + target_var + '"';
                }
                else {
                    title_graph = 'Algorithms accuracy comparison for ' + target_var + '';
                }
                var layout = {
                    title: title_graph,
                    barmode: 'group',
                    bargap: 0.25,
                    bargroupgap: 0.1,
                    // barnorm: 'percent'

                };

                var layout2 = {
                    title: 'Algorithms Coverage of Target Variable: "' + target_var + '"',
                    xaxis: {
                        title: 'Test Sample Size',
                        titlefont: {
                            family: 'Courier New, monospace',
                            size: 18,
                            color: '#7f7f7f'
                        }
                        // x = [1,5]
                    },
                    yaxis: {
                        title: target_var + ' level',
                        titlefont: {
                            family: 'Courier New, monospace',
                            size: 18,
                            color: '#7f7f7f'
                        }
                        // visible:false
                    },

                    legend: {
                        y: [1, 5],
                        // traceorder: 'reversed',

                        font: {
                            size: 16
                        },
                        yref: 'paper'
                    }
                }


                console.log(target_var)
                var barDiv = $('#bar-chart');
                Plotly.newPlot(tab_content_div, data_dict, layout);
                if (analysis_mode == "regression") {
                    Plotly.newPlot(tab_content_scatter_div, scat_graph_data, layout2);
                }
                tab_count = tab_count + 1;

            }


        });

    }

    //####################################################################################################  USER DEFINED FUNCTIONS  ###############################################################################

    function create_badges(data, color) {
        var child_elements = "";
        for (var data_number in data) {
            try {
                child_elements += "<span class=\"new badge {1} left\" data-badge-caption=\"{0}\"> </span>".format(data[data_number], color);
            }
            catch{

            }
        }
        return child_elements
    }

    String.prototype.format = function () {

        a = this;
        for (k in arguments) {
            a = a.replace("{" + k + "}", arguments[k])
        }
        return a
    }

});