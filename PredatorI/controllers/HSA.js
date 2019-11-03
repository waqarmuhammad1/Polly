$(document).ready(function () {
    // intialize_dt();
    // CollapsibleLists.apply()
    $('.modal').modal();
    $('select').formSelect();
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
        var file = document.getElementById("file");
        file.style.display = "block"
    });

    var file_name = null
    $('#upload-file-btn').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        var fileInput = document.getElementById('the-file');
        var file = fileInput.files[0];
        file_name = file.name.replace(/\.[^/.]+$/, "");
        $.ajax({
            type: 'POST',
            url: "http://0.0.0.0:5001/uploader",
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



    function get_file_name() {
        file_name += new Date().toISOString();
        return file_name;
    }




})



















