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
    $("#logout").click(function(){
        localStorage.removeItem('user_name')
        window.location = 'index.html'
    });
    var file_name= null;
    window.onload = function () {
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_download_file_name", 'application/json',null, function (response) {
            
            file_name = response

        });
        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5000/get_selected_data",
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
                    var selected_data = data['selected_data']
                    create_grid(selected_data, 'datatable');
                }




            },
            error: function (data) {
                var toastHTML = '<span>Error: ' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
            }
        });

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

        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_available_algorithms", 'application/json', null, function (response) {
            console.log(response)
            data = response['available_algorithms']
            console.log(data)
            for (var algorithm in data) {
                $("#algo_select").append($('<option value=\"' + data[algorithm] + '\"> ' + data[algorithm] + ' </option>'))
                $('select').formSelect();
            }

        });

    }

    $("#update_select").click(function(){

        var selected_algos = $("#algo_select").val();

        var details = JSON.stringify({
            'selected_algorithms': selected_algos
        })
        console.log(details)
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/set_selected_algorithms", 'application/json',details, function (response) {
            window.location = 'tune.html'

        });


    })

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
                    filename: function () { return get_file_name();},
                    title: null
                },
                {
                    extend: 'pdfHtml5',
                    filename: function () { return get_file_name();},
                    title: null,
                    download: 'open'
                },
                {
                    extend: 'csvHtml5',
                    filename: function () { return get_file_name();},
                },
                'copy', 'print'
            ],
        });

        // $('table.display').DataTable();

    }
    function get_file_name() {
        file_name += new Date().toISOString();
        return file_name;
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