$(document).ready(function () {
    if(localStorage.getItem("user_name") === null){
        window.location = 'required.html'
    }
    $('.tabs').tabs();
    $('.modal').modal();
    $('select').formSelect();
    $('.collapsible').collapsible();
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
        });
    };

    $("#view_change").click(function () {
        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5000/get_processed_data",
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
                    console.log(data)
                    var selected_data = data['processed']
                    console.log(selected_data)
                    create_grid_processed(selected_data, 'datatable2');
                    // location.reload()
                }




            },
            error: function (data) {
                var toastHTML = '<span>Error: ' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
            }
        });


    });

    $("#confirm_yes").click(function () {
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/overwrite_existing_data", 'application/json', null, function (response) {
            var success = response['success']

            if (success) {
                location.reload();
            }
            else {
                var msg = response['msg']
                if (response.includes('Error:')) {
                    const elem = document.getElementById('error_modal');
                    const instance = M.Modal.init(elem, { dismissible: false });
                    const error_msg = document.getElementById('error_msg')
                    new_data = msg.replace('Error:', ' ')
                    error_msg.innerText = new_data

                    instance.open();
                }
                else {
                    var toastHTML = '<span>' + msg + '</span>';
                    M.toast({ html: toastHTML }, 2000);
                }
            }
        });
    })

    var file_name = 'poka';

    function get_selected_data() {
        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5000/get_selected_data",
            data: null,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if ('Error' in data) {
                    error_msg = data['Error']


                    const elem = document.getElementById('error_modal');
                    const instance = M.Modal.init(elem, { dismissible: false });
                    const error_msg = document.getElementById('error_msg')
                    new_data = error_msg.replace('Error:', ' ')
                    error_msg.innerText = new_data
                    instance.open();
                }
                else {
                    var selected_data = data['selected_data']
                    create_grid(selected_data, 'datatable');
                }




            },
            error: function (data) {
                const elem = document.getElementById('error_modal');
                const instance = M.Modal.init(elem, { dismissible: false });
                const error_msg = document.getElementById('error_msg')
                new_data = data.replace('Error:', ' ')
                error_msg.innerText = new_data
                instance.open();
            }
        });
    }

    function get_data_description() {
        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5000/get_data_description",
            data: null,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if ('Error' in data) {
                    error_msg = data['Error']


                    const elem = document.getElementById('error_modal');
                    const instance = M.Modal.init(elem, { dismissible: false });
                    const error_msg = document.getElementById('error_msg')
                    new_data = error_msg.replace('Error:', ' ')
                    error_msg.innerText = new_data
                    instance.open();
                }
                else {
                    var selected_data = data['desc_data']
                    create_grid_desc(selected_data, 'datatable_desc');
                }


            },
            error: function (data) {
                var toastHTML = '<span>Error: ' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
            }
        });

    }

    function get_train_vars() {
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
    }

    function get_target_vars() {
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
    }

    function get_data_correlation() {
        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5000/get_data_correlation",
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
                    var selected_data = data['corr_data']
                    create_grid_corr(selected_data, 'datatable_corr');
                }


            },
            error: function (data) {
                var toastHTML = '<span>Error: ' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
            }
        });
    }

    function get_selected_columns() {

        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_selected_columns", 'application/json', null, function (branches) {


            data = branches['selected_columns']

            $("#hist_cols").empty().html(' ');
            $("#scatter_x").empty().html(' ');
            $("#scatter_y").empty().html(' ');
            $("#box_cols").empty().html(' ');
            console.log(data)
            if (typeof data != undefined) {
                if (data[0] != 'Indices') {
                    for (var x in data) {
                        $("#hist_cols").append($('<option value=\"' + data[x] + '\"> ' + data[x] + ' </option>'))
                        $("#scatter_x").append($('<option value=\"' + data[x] + '\"> ' + data[x] + ' </option>'))
                        $("#scatter_y").append($('<option value=\"' + data[x] + '\"> ' + data[x] + ' </option>'))
                        $("#box_cols").append($('<option value=\"' + data[x] + '\"> ' + data[x] + ' </option>'))
                        $('select').formSelect();
                    }
                }
                else {
                    $("#hist_cols").append($('<option value=\"No string column detected\">No String Column Detected </option>'))
                    $("#scatter_x").append($('<option value=\"No string column detected\">No String Column Detected </option>'))
                    $("#scatter_y").append($('<option value=\"No string column detected\">No String Column Detected </option>'))
                    $("#box_cols").append($('<option value=\"' + data[x] + '\"> ' + data[x] + ' </option>'))
                    $('select').formSelect();
                }
            }

        });

    }

    function get_string_columns() {
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_string_columns", 'application/json', null, function (branches) {

            data = branches['string_columns']
            $("#encod").empty().html(' ');
            console.log(data)
            if (data[0] != 'Indices') {
                for (var x in data) {
                    $("#encod").append($('<option value=\"' + data[x] + '\"> ' + data[x] + ' </option>'))
                    $('select').formSelect();
                }
            }
            else {
                $("#encod").append($('<option value=\"No string column detected\">No String Column Detected </option>'))
                $('select').formSelect();
            }

        });
    }

    function get_file_name() {
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_download_file_name", 'application/json', null, function (response) {


            file_name = response;

        });
    }

    function get_applied_methods() {
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_applied_methods", 'application/json', null, function (branches) {
            console.log(data)
            try {
                data = branches['applied_methods']
                var child_elements = create_badges(data, 'deep-orange accent-3')
                // $("#methods_badges").empty();
                $("#methods_badges").append(child_elements);
            }
            catch{

            }


        });
    }

    $("#logout").click(function(){
        localStorage.removeItem('user_name')
        window.location = 'index.html'
    });
    function get_attributes_encoded() {
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_attributes_encoded", 'application/json', null, function (branches) {

            try {
                data = branches['attributes_encoded']
                console.log(data)
                var child_elements = create_badges(data, 'blue')
                $("#attribute_badges").empty();
                $("#attribute_badges").append(child_elements);
            }
            catch{

            }


        });
    }
    window.onload = function () {

        get_selected_data();
        get_data_description();
        get_train_vars();
        get_target_vars();
        get_data_correlation();
        get_selected_columns();
        get_string_columns();
        get_file_name();
        get_applied_methods();
        get_attributes_encoded();
    }

    $("#filter_options").on('change', function () {
        $("#filter_na").prop("disabled", false);
        var selected_method = $(this).val();
        details = JSON.stringify({

            "selected_method": selected_method

        });

        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_columns_to_filter", 'application/json', details, function (branches) {


            data = branches['columns_to_filter']

            $("#filter_ na option").remove()
            $("#filter_na").empty().html(' ');
            for (var x in data) {
                $("#filter_na").append($('<option selected value=\"' + data[x] + '\"> ' + data[x] + ' </option>'))
                $('select').formSelect();
            }



        });
    });

    $("#filter_na").on('change', function () {

        $("#apply").removeClass('disabled')
    });

    $("#apply").click(function () {

        var selected_method = $("#filter_options").val()
        var selected_column = $("#filter_na").val()

        details = JSON.stringify({

            "selected_method": selected_method,
            "selected_column": selected_column
        })
        console.log(details)

        ajaxCallsFunc('POST', "http://0.0.0.0:5000/process_null_columns", 'application/json', details, function (data) {


            if (data.includes('Error:')) {
                const elem = document.getElementById('error_modal');
                const instance = M.Modal.init(elem, { dismissible: false });
                const error_msg = document.getElementById('error_msg')

                new_data = data.replace('Error:', ' ')
                error_msg.innerText = new_data

                instance.open();
            }
            else {
                var toastHTML = '<span>' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
                var badge_txt = []
                badge_txt.push(selected_method + ' [ ' + selected_column + ' ]')
        
                var child_elements = create_badges(badge_txt, 'deep-orange accent-3')
                // $("#methods_badges").empty();
                $("#methods_badges").append(child_elements);
                get_selected_columns();
                get_string_columns();
                get_attributes_encoded();
            }
        });

      

    });

    $("#apply_conv").click(function () {

        var selected_column = $("#encod").val()

        details = JSON.stringify({

            "selected_column": selected_column
        })

        ajaxCallsFunc('POST', "http://0.0.0.0:5000/process_attribute_encoding", 'application/json', details, function (data) {


            if (data.includes('Error:')) {
                const elem = document.getElementById('error_modal');
                const instance = M.Modal.init(elem, { dismissible: false });
                const error_msg = document.getElementById('error_msg')
                new_data = data.replace('Error:', ' ')
                error_msg.innerText = new_data

                instance.open();
            }
            else {
                var toastHTML = '<span>' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
                var badge_txt = []
                badge_txt.push(selected_column)
                var child_elements = create_badges(badge_txt, 'blue')
                $("#attribute_badges").empty();
                $("#attribute_badges").append(child_elements);
            }


        });

       

    });


    //####################################################################################################  GRAPH FUNCTIONS  #########################################################################################


    $("#hist_cols").on('change', function () {
        // $("#filter_na").prop("disabled", false);
        // $('select').formSelect();
        var col_name = $(this).val()
        var request_obj = []
        request_obj.push(col_name)
        details = JSON.stringify({

            "column_names": request_obj

        });
        console.log(details)
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_graph_data", 'application/json', details, function (branches) {

            if (typeof branches == undefined) {

            }
            else {
                var data = branches['graph_data']
                data = data[col_name]
                var x = [];
                for (var j in data) {
                    x[j] = data[j];
                }
                var trace = {
                    x: x,
                    type: 'histogram',
                };
                var layout = {
                    title: col_name
                }
                console.log(trace)
                var data = [trace];
                Plotly.newPlot('myDiv_histo', data, layout);
            }



        });
    });

    $("#box_cols").on('change', function () {
        // $("#filter_na").prop("disabled", false);
        // $('select').formSelect();
        var col_name = $(this).val()
        var request_obj = []
        request_obj.push(col_name)
        details = JSON.stringify({

            "column_names": request_obj

        });
        console.log(details)
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_graph_data", 'application/json', details, function (branches) {

            if (typeof branches == undefined) {

            }
            else {
                var data = branches['graph_data']
                data = data[col_name]
                var x = [];
                for (var j in data) {
                    x[j] = data[j];
                }
                var trace = {
                    y: x,
                    boxpoints: 'all',
                    jitter: 0.3,
                    pointpos: -1.8,
                    type: 'box',
                };
                var layout = {
                    title: col_name
                }
                console.log(trace)
                var data = [trace];
                Plotly.newPlot('myDiv_box', data, layout, { showSendToCloud: true });
            }



        });
    });


    $("#create_graph").click(function () {
        console.log($(this).val());
        // $("#filter_na").prop("disabled", false);
        // $('select').formSelect();
        var col_x = $("#scatter_x").val()
        var col_y = $("#scatter_y").val()

        var request_obj = []
        request_obj.push(col_x);
        request_obj.push(col_y)

        details = JSON.stringify({

            "column_names": request_obj

        });
        console.log(details)
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_graph_data", 'application/json', details, function (branches) {

            if (typeof branches == undefined) {

            }
            else {
                var data = branches['graph_data']
                var x_axis = [];
                for (var j in data[col_x]) {
                    x_axis.push(data[col_x][j]);
                }

                var y_axis = []
                for (var j in data[col_y]) {
                    y_axis.push(data[col_y][j])
                }

                var trace1 = {
                    x: x_axis,
                    y: y_axis,
                    mode: 'markers',
                    type: 'scatter',
                    name: 'Team A',
                    marker: { size: 12 }
                };


                var data = [trace1];

                var layout = {
                    title: {
                        text: 'Scatter ' + col_x + ' and ' + col_y,
                        font: {
                            family: 'Courier New, monospace',
                            size: 24
                        },
                        xref: 'paper',
                        //   x: 0.05,
                    },
                    xaxis: {
                        title: {
                            text: col_x,
                            font: {
                                family: 'Courier New, monospace',
                                size: 18,
                                color: '#7f7f7f'
                            }
                        },
                    },
                    yaxis: {
                        title: {
                            text: col_y,
                            font: {
                                family: 'Courier New, monospace',
                                size: 18,
                                color: '#7f7f7f'
                            }
                        }
                    }
                };

                console.log(trace1)
                var data = [trace1];
                Plotly.newPlot('myDiv_scatter', data, layout);
            }



        });
    });



    //####################################################################################################  USER DEFINED FUNCTIONS  ###############################################################################
    function create_grid(data, element_id) {

        var column_names = []
        var first_index = data[0]
        for (var column_name in first_index) {
            column_names.push({ data: column_name, 'title': column_name })
        }

        // Destroy the dataTable and empty because the columns may change!
        if (table != null) {
            // for this version use fnDestroy() instead of destroy()
            table.fnDestroy();
            table = null;
            // empty in case the columns change
            $('#' + element_id).empty();
        }

        // Build dataTable with ajax, columns, etc.
        table = $('#' + element_id).dataTable({
            responsive: true,
            data: data,
            columns: column_names,
            // scrollY: 500,
            scrollX: 600,
            autowidth: true,
            ordering: false,
            searching: false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    filename: function () { return get_file_name(); },
                    title: null
                },
                {
                    extend: 'pdfHtml5',
                    filename: function () { return get_file_name(); },
                    title: null,
                    download: 'open'
                },
                {
                    extend: 'csvHtml5',
                    filename: function () { return get_file_name(); },
                },
                'copy', 'print'
            ],
        });

        // $('table.display').DataTable();

    }
    var processed_tbl = null
    function create_grid_processed(data, element_id) {

        var column_names = []
        var first_index = data[0]
        for (var column_name in first_index) {
            column_names.push({ data: column_name, 'title': column_name })
        }

        // Destroy the dataTable and empty because the columns may change!
        if (processed_tbl != null) {
            // for this version use fnDestroy() instead of destroy()
            processed_tbl.fnDestroy();
            processed_tbl = null;
            // empty in case the columns change
            $('#' + element_id).empty();
        }

        // Build dataTable with ajax, columns, etc.
        processed_tbl = $('#' + element_id).dataTable({
            responsive: true,
            data: data,
            columns: column_names,
            // scrollY: 500,
            scrollX: 600,
            autowidth: true,
            ordering: false,
            searching: false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    filename: function () { return get_file_name(); },
                    title: null
                },
                {
                    extend: 'pdfHtml5',
                    filename: function () { return get_file_name(); },
                    title: null,
                    download: 'open'
                },
                {
                    extend: 'csvHtml5',
                    filename: function () { return get_file_name(); },
                },
                'copy', 'print'
            ],
        });

        // $('table.display').DataTable();

    }


    function create_grid_corr(data, element_id) {

        var column_names = []
        var first_index = data[0]
        var count = 0;
        var count2 = 0;
        for (var column_name in first_index) {
            if (column_name != 'Variables')
                count++;
            column_names.push({ data: column_name, 'title': column_name })
            count2++
        }
        var column_order = []
        column_order.push(count)

        for (var x = 0; x < count2; x++) {
            if (x != count) {
                column_order.push(x)
            }
        }
        // Destroy the dataTable and empty because the columns may change!
        if (table_corr != null) {
            // for this version use fnDestroy() instead of destroy()
            table_corr.fnDestroy();
            table_corr = null;
            // empty in case the columns change
            $('#datatable_corr').empty();
        }

        // Build dataTable with ajax, columns, etc.
        table_corr = $('#datatable_corr').dataTable({
            responsive: true,
            data: data,
            columns: column_names,
            // scrollY: 500,
            scrollX: 600,
            autowidth: true,
            ordering: false,
            searching: false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    filename: function () { return get_file_name(); },
                    title: null
                },
                {
                    extend: 'pdfHtml5',
                    filename: function () { return get_file_name(); },
                    title: null,
                    download: 'open'
                },
                {
                    extend: 'csvHtml5',
                    filename: function () { return get_file_name(); },
                },
                'copy', 'print'
            ],
            colReorder: {
                order: column_order
            }
        });
        // $('#datatable_corr').DataTable();

    }

    function create_grid_desc(data, element_id) {

        var column_names = []
        var first_index = data[0]
        var count = 0;
        var count2 = 0;
        for (var column_name in first_index) {
            if (column_name != 'Statistics')
                count++;
            column_names.push({ data: column_name, 'title': column_name })
            count2++
        }

        var column_order = []
        column_order.push(count)

        for (var x = 0; x < count2; x++) {
            if (x != count) {
                column_order.push(x)
            }
        }
        console.log(column_order)

        // Destroy the dataTable and empty because the columns may change!
        if (table_desc != null) {
            // for this version use fnDestroy() instead of destroy()
            table_desc.fnDestroy();
            table_desc = null;
            // empty in case the columns change
            $('#' + element_id).empty();
        }
        // Build dataTable with ajax, columns, etc.
        table_desc = $('#' + element_id).dataTable({
            responsive: true,
            data: data,
            columns: column_names,
            // scrollY: 500,
            scrollX: 600,
            autowidth: true,
            ordering: false,
            searching: false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    filename: function () { return get_file_name(); },
                    title: null
                },
                {
                    extend: 'pdfHtml5',
                    filename: function () { return get_file_name(); },
                    title: null,
                    download: 'open'
                },
                {
                    extend: 'csvHtml5',
                    filename: function () { return get_file_name(); },
                },
                'copy', 'print'
            ],
            colReorder: {
                order: column_order
            }
        });

        // $('table.display').DataTable();

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
    function get_file_name() {
        file_name += new Date().toISOString();
        return file_name;
    }
    String.prototype.format = function () {

        a = this;
        for (k in arguments) {
            a = a.replace("{" + k + "}", arguments[k])
        }
        return a
    }

});