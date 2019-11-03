$(document).ready(function () {
    // intialize_dt();
    // CollapsibleLists.apply()
    $('.modal').modal();
    $('select').formSelect();
    var excel_sheets = document.getElementById("excel_sheets")
    excel_sheets.style.display = 'none'
    function ajaxCallsFunc(type, url, processData, contentType, data, callback) {
        $.ajax({
            type: type,
            url: url,
            contentType: contentType,
            data: data,
            success: callback,
            processData: processData
        });
    };
    var selected_source = null;
    var first_sheet = null;
    var table = null;

    if(localStorage.getItem("user_name") === null){
        window.location = 'required.html'
    }

    $("#logout").click(function(){
        localStorage.removeItem('user_name')
        window.location = 'index.html'
    });

    $("#ds").change(function () {
        var db = document.getElementById("db");
        var file = document.getElementById("file");
        var csv_opt = document.getElementById("csv_opt");
        var excel_sheets = document.getElementById("excel_sheets")
        var db_items = document.getElementById("db_items");
        selected_source = $(this).val()
        if (table != null) {
            // for this version use fnDestroy() instead of destroy()
            table.fnDestroy();
            table = null;
            // empty in case the columns change
            $('#datatable').empty();
        }
        if (selected_source != 'excel' && selected_source != 'csv') {
            file.style.display = "none"
            csv_opt.style.display = "none"
            excel_sheets.style.display = 'none'
            db.style.display = "block";
            db_items.style.display = 'block'

        }
        else {
            if (selected_source == 'csv') {
                csv_opt.style.display = "block"
                excel_sheets.style.display = 'none'
            }
            else {
                csv_opt.style.display = "none"
                excel_sheets.style.display = 'block'
                console.log('changing_color')
            }
            db_items.style.display = 'none'
            db.style.display = "none";
            file.style.display = "block"
        }

    })
    var file_name = null
    $('#upload-file-btn').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        if (selected_source == 'csv') {
            delimiter = $('input[name=group1]:checked').attr('id')
            form_data.append('delimiter', delimiter)
        }
        var fileInput = document.getElementById('the-file');
        var file = fileInput.files[0];
        file_name = file.name.replace(/\.[^/.]+$/, "");
        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5000/uploader",
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                var toastHTML = '<span>' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
                populate_data();



            },
            error: function (data) {
                var toastHTML = '<span>Error: ' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
            }
        });

    });
    String.prototype.format = function () {
        a = this;
        for (k in arguments) {
            a = a.replace("{" + k + "}", arguments[k])
        }
        return a
    }

    function populate_data() {
        if (selected_source == 'excel') {

            ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_sheets", true, 'application/json', null, function (response) {
                var sheets = response['sheets']
                $("#sheet_select option").remove()
                var sheet_meta = create_sheet_options(sheets);
                var child_element = sheet_meta[0]
                var sheet_name = sheet_meta[1]
                $("#sheet_select").append(child_element);
                $('select').formSelect();

            });
        }
        else if (selected_source == 'csv') {
            $("#sheet_select option").remove()
            var request = JSON.stringify({

                'selected_table': null
            })

            ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_columns", true, 'application/json', request, function (response) {

                $("#training_vars option").remove();
                $("#target_vars option").remove();
                var child_elements = create_column_options(response['columns']);
                $("#training_vars").append(child_elements);
                $("#target_vars").append(child_elements)
                $("select").formSelect();

            });

            ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_data", true, 'application/json', request, function (response_data) {



                var data = response_data['data'];

                create_grid(data, null);

            });

        }


    }

    $("#sheet_select").change(function () {
        var selected_table = $(this).val()
        var request = JSON.stringify({
            'selected_table': selected_table
        });


        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_columns", true, 'application/json', request, function (response) {

            $("#training_vars option").remove();
            $("#target_vars option").remove();
            var child_elements = create_column_options(response['columns']);
            $("#training_vars").append(child_elements);
            $("#target_vars").append(child_elements)
            $("select").formSelect();


        });


        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_data", true, 'application/json', request, function (response_data) {

            var data = response_data['data'];

            create_grid(data, selected_table);

        });

    });

    $("#set_selected").click(function () {

        ajaxCallsFunc('POST', "http://0.0.0.0:5000/set_selected_data", true, 'application/json', null, function (response_data) {
            console.log(response_data)
            if(response_data == true)
                location.replace('stats.html')
            else{
                var toastHTML = '<span>' + response_data + '</span>';
                M.toast({ html: toastHTML }, 2000);
                populate_data();
            }

        });

    });

    function create_sheet_options(sheets) {
        for (var files in sheets) {
            var file_name = files;
            var child_element = " <option value=\"\" disabled selected>Choose your option</option> "
            sheet_names = sheets[file_name]
            first_sheet = sheet_names[0]

            for (var sheet_number in sheet_names) {
                var sheet_name = sheet_names[sheet_number]
                var temp_child = '<option value=\"{0}\"> {1} </option>'.format(sheet_name, sheet_name)

                child_element += " " + temp_child + " "
            }
        }

        return [child_element, first_sheet];
    }
    function create_column_options(columns) {
        var child_element = " <option value=\"\" disabled selected>Choose your option</option> "

        for (var column_number in columns) {
            var column_name = columns[column_number]
            var temp_child = '<option value=\"{0}\"> {1} </option>'.format(column_name, column_name)

            child_element += " " + temp_child + " "
        }

        return child_element
    }



    function create_grid(data, title) {

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
            $('#datatable').empty();
        }

        // Build dataTable with ajax, columns, etc.
        table = $('#datatable').dataTable({
            responsive: true,
            data: data,
            columns: column_names,
            // scrollY: 500,
            scrollX: 600,
            autowidth: true,
            ordering: false,
            searching: false,
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


    }
    function get_file_name() {
        file_name += new Date().toISOString();
        return file_name;
    }

    $("#connect-btn").click(function () {

        var host = $("#host").val()
        var port = $("#port").val()
        var username = $("#username").val()
        var password = $("#password").val()

        request = JSON.stringify({
            'host': host,
            'port': port,
            'user': username,
            'password': password
        })
        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5000/read_database",
            data: request,
            contentType: 'application/json',
            cache: false,
            processData: false,
            success: function (data) {
                var available_dbs = data['available_dbs']
                console.log(data)
                console.log(available_dbs)
                var child_element = " <option value=\"\" disabled selected>Choose your option</option> "
    
                for (var db_number in available_dbs) {
                    var db_name = available_dbs[db_number]
                    var temp_child = '<option value=\"{0}\"> {1} </option>'.format(db_name, db_name)
                    child_element += " " + temp_child + " "
                }
                //0.0.0.0
                $("#db_select option").remove();
                $("#db_select").append(child_element);
                $("select").formSelect();

            },
            error: function (data) {
                var toastHTML = '<span>Error: ' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
            }
        });

    });

    $("#db_select").change(function(){

        var db_name = $(this).val()

        var request = JSON.stringify({
            'db_name': db_name
        });

        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5000/get_database_tables",
            data: request,
            contentType: 'application/json',
            cache: false,
            processData: false,
            success: function (data) {
                var available_dbs = data['available_tables']
                console.log(data)
                console.log(available_dbs)
                var child_element = " <option value=\"\" disabled selected>Choose your option</option> "
    
                for (var db_number in available_dbs) {
                    var db_name = available_dbs[db_number]
                    var temp_child = '<option value=\"{0}\"> {1} </option>'.format(db_name, db_name)
                    child_element += " " + temp_child + " "
                }
                //0.0.0.0
                $("#table_select option").remove();
                $("#table_select").append(child_element);
                $("#table_select").prop("disabled", false);
                $("select").formSelect();

            },
            error: function (data) {
                var toastHTML = '<span>Error: ' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
            }
        });
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/get_columns", true, 'application/json', request, function (response) {

            $("#training_vars option").remove();
            $("#target_vars option").remove();
            var child_elements = create_column_options(response['columns']);
            $("#training_vars").append(child_elements);
            $("#target_vars").append(child_elements)
            $("select").formSelect();


        });

    });


    $("#table_select").change(function(){
        var table_name = $(this).val();

        var request = JSON.stringify({
            'table_name': table_name
        });

        ajaxCallsFunc('POST', "http://0.0.0.0:5000/read_table", true, 'application/json', request, function (response_data) {

            var data = response_data['data'];

            create_grid(data, null);

        });

    });

    $("#train_select").click(function () {

        var train_vars = $("#training_vars").val();
        var child_elements = create_badges(train_vars, 'green')
        $("#train_badges").empty();
        $("#train_badges").append(child_elements);

        var request = JSON.stringify({
            'train_vars': train_vars
        })

        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5000/update_train_vars",
            data: request,
            contentType: 'application/json',
            cache: false,
            processData: false,
            success: function (data) {
                var toastHTML = '<span>' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
                // populate_data();



            },
            error: function (data) {
                var toastHTML = '<span>Error: ' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
            }
        });

    });


    $("#target_select").click(function () {

        var target_vars = $("#target_vars").val();
        console.log(target_vars)
        var child_elements = create_badges(target_vars, 'orange')
        $("#target_badges").empty();
        $("#target_badges").append(child_elements);


        var request = JSON.stringify({
            'target_var': target_vars
        })

        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5000/update_target_vars",
            data: request,
            contentType: 'application/json',
            cache: false,
            processData: false,
            success: function (data) {
                var toastHTML = '<span>' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
                // populate_data();



            },
            error: function (data) {
                var toastHTML = '<span>Error: ' + data + '</span>';
                M.toast({ html: toastHTML }, 2000);
            }
        });


    });

    function create_badges(data, color, quote_name) {
        var child_elements = "";
        for (var data_number in data) {
            child_elements += "<span class=\"new badge {2} left\" data-badge-caption=\"{0}\">{1}</span>".format(data[data_number], (parseInt(data_number) + 1).toString() + ': ', color);
        }

        return child_elements;
    }

})



















