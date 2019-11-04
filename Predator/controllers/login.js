$(document).ready(function () {

    var attempt = 3; // Variable to count number of attempts.
    $("#login").click(function(){
        console.log('poka')
        validate()
    })
    
    // Below function Executes on click of login button.
    function validate() {
        var username = document.getElementById("emal").value;
        var password = document.getElementById("passwd").value;
        if (username == "muhammadw@slu.edu" && password == "admin") {
            window.location = "landing.html"; // Redirecting to other page.
            return false;
        }
        else {
            attempt--;// Decrementing by one.
            alert("You have left " + attempt + " attempt;");
            // Disabling fields after 3 attempts.
            if (attempt == 0) {
                document.getElementById("emal").disabled = true;
                document.getElementById("passwd").disabled = true;
                document.getElementById("login").disabled = true;
                return false;
            }
        }
    }


})