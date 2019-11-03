$(document).ready(function () {

    $('.tabs').tabs();
    $('.modal').modal();
    $('select').formSelect();
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    $("#loader").hide()
    var table = null;
    var table_desc = null;
    var table_corr = null;
    function ajaxCallsFunc(type, url, contentType, data, callback) {
        $.ajax({
            type: type,
            url: url,
            contentType: contentType,
            data: data,
            success: callback,
            error: function (data) {
                var toastHTML = '<span>Error: ' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
            }

        });
    };
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


        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_algorithm_params", 'application/json', null, function (branches) {


            var algo_params = branches['algorithm_params'];
            for (var x in algo_params) {

                var params = algo_params[x].split(",")
                var input_ele = "";
                var i = 0;
                var bol = false;
                for (var y in params) {
                    var temp = params[y].split("=");
                    param_name = temp[0].trim();
                    param_val = temp[1].trim().split("|")[0].trim();
                    param_name = param_name.replace("\"", "")
                    param_val = param_val.replace("\"", "")
                    param_name = param_name.replace("'", "")
                    param_val = param_val.replace("'", "")
                    if (i % 2 == 0) {
                        input_ele = input_ele + "<div class=\"row\">\
                                    <div class=\"col s6 m4\">\
                                        <label for=\""+ param_name + "\">" + param_name + "</label>\
                                        <input id=\""+ param_name + "\" type=\"text\" class=\"validate\" value=\"" + param_val + "\">\
                                    </div>"
                        bol = true;
                    }
                    else {
                        input_ele = input_ele + "<div class=\"col s6 m4 offset-m2\">\
                                        <label for=\""+ param_name + "\">" + param_name + "</label>\
                                        <input id=\""+ param_name + "\" type=\"text\" class=\"validate\" value=\"" + param_val + "\">\
                                    </div>\
                                    </div>"
                        bol = false;
                    }
                    i++;
                }

                if (bol == false) {
                    input_ele = input_ele += "</div>"
                }
                var xtra_elem = "<li>\
                    <div class=\"collapsible-header grey darken-2 white-text\" >\
                      <i class=\"material-icons\">settings</i>"+ x + "\
                    </div>\
                    <div class=\"collapsible-body\" id=\""+ x + "\">" + input_ele + "\
                    </div>\
                  </li>";

                $("#md").append(xtra_elem)
            }




        });

    }

    $("#update_select").click(function(){
        // console.log('here')
        window.location = 'results.html'
    });
    $("#logout").click(function(){
        localStorage.removeItem('user_name')
        window.location = 'index.html'
    });
    if(localStorage.getItem("user_name") === null){
        window.location = 'required.html'
    }
    $("#update").click(function () {


        var tune_params = new Object();
        var got_error = false
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_algorithm_params", 'application/json', null, function (branches) {

            var algo_params = branches['algorithm_params'];

            for (var x in algo_params) {
                var params = algo_params[x].split(",")
                tune_params[x] = null;
                var temp_params = new Object();
                for (var y in params) {
                    var temp = params[y].split("=");
                    param_name = temp[0].trim();
                    param_dt = temp[1].trim().split("|")[1].trim();
                    param_name = param_name.replace("\"", "")
                    param_name = param_name.replace("'", "")

                    var user_data = getRequiredParams(x, param_name)
                    var user_value = user_data['value']
                    var elem = user_data['elem']

                    var output = checkType(user_value, param_dt)
                    if (output == undefined || output == 'error') {
                        // console.log(param_name + " Parsed(" + output + ") Actual(" + user_value + ") DT(" + temp + ")")
                    }
                    if (output == 'error') {
                        var elems = document.getElementById(x).getElementsByTagName('*');
                        for (var i = 0; i < elems.length; i++) {
                            if (elems[i].id == param_name) {
                                elems[i].style.color = 'red';
                                var toastHTML = '<span>Error: ' + param_name + ' incorrect value, values passed: ' + user_value + ' values expected: ' + temp + '</span>';
                                M.toast({ html: toastHTML }, 2000);
                            }
                        }
                        got_error = true
                    }
                    else {
                        var elems = document.getElementById(x).getElementsByTagName('*');
                        for (var i = 0; i < elems.length; i++) {
                            if (elems[i].id == param_name) {
                                elems[i].style.color = 'black';
                                break;
                            }
                        }
                        temp_params[param_name] = output
                    }
                }
                tune_params[x] = temp_params
            }
            if (got_error == false) {
                $("#main_div").hide();
                $("next_btn").hide();
                $("#loader").show();
                resp_obj = JSON.stringify({

                    'updated_algorithms': tune_params
                });
                // console.log('calling apply algos')
                console.log(tune_params)
                ajaxCallsFunc('POST', "http://0.0.0.0:5000/apply_selected_algorithms", 'application/json', resp_obj, function (branches) {

                    var toastHTML = '<span>' + branches + '</span>';
                    M.toast({ html: toastHTML }, 2000);
                    $("#main_div").show();
                    $("#loader").hide();
                    $("#next").removeClass("disabled");
                });
            }




        });




        // window.location.replace('results.html');

    });


    //####################################################################################################  USER DEFINED FUNCTIONS  ###############################################################################

    function getRequiredParams(algoName, paramName) {
        var elems = document.getElementById(algoName).getElementsByTagName('*');
        for (var i = 0; i < elems.length; i++) {
            if (elems[i].id == paramName) {
                return { 'elem': elems[i], 'value': elems[i].value };
            }
        }
    }

    function checkType(user_value, accepted_type) {

        var constant_val = null;
        var is_array = false;

        var type = accepted_type.split('/');
        if (type.length == 3) {
            constant_val = type[1];
        }
        if (type[0] == 'int') {
            return isNumber(user_value);
        }
        else if (type[0] == 'string') {
            return isString(user_value);
        }
        else if (type[0] == 'bool') {
            var output = isBool(user_value);
            if (output == 'error' && constant_val != null) {
                return constant_val
            }
            else {
                return output
            }
        }
        else if (type[0] == 'float') {
            return isFloat(user_value);
        }
        else if (type[0] == 'None') {
            return null
        }

    }

    function isNumber(param_value) {

        try {

            param_value = param_value.trim()
            var parsed_val = parseFloat(param_value)
            return parsed_val
        } catch (err) {

            if (param_value.toLowerCase() == 'none' || param_value.toLowerCase() == 'null') {
                return null
            }
            else {
                return 'error'
            }
        }
    }

    function isFloat(param_value) {
        try {

            if (param_value == "auto_deprecated" || param_value == 'auto') {
                return  param_value
            }
            param_value = param_value.trim()
            var parsed_val = parseFloat(param_value)
            // console.log(param_value)
            return parsed_val
        } catch (err) {

            if (param_value.toLowerCase() == 'none' || param_value.toLowerCase() == 'null') {
                return null
            }
            else {
                return 'error'
            }
        }
    }

    function isBool(param_value) {
        try {
            param_value = param_value.toString().trim()
            if (param_value.toLowerCase() == 'true' || param_value.toLowerCase() == 'false') {
                if (param_value.toLowerCase() == 'true') {
                    return true
                }
                else {
                    return false
                }
            }
            else {
                return 'error'
            }
        } catch (err) {
            return 'error'
        }
    }

    function isString(param_value) {
        try {
            return param_value.trim()
        }
        catch (err) {
            return 'error'
        }
    }


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