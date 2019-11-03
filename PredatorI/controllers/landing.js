$(document).ready(function () {
    var canvas = document.getElementById("canvas"),
        ctx = canvas.getContext('2d');
    $('.modal').modal();
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight / 3;

    // var register_btn = document.getElementById("register");
    // var login_btn = document.getElementById("login");
    // var description = document.getElementById("desc");

    // description.style.top = window.innerHeight / 7;
    // description.style.left = window.innerWidth / 1.5;
    // register_btn.style.top = window.innerHeight / 4;
    // register_btn.style.left = window.innerWidth / 1.5;

    // login_btn.style.top = window.innerHeight / 4;
    // login_btn.style.left = window.innerWidth / 1.33;

    
    var canvas_items = document.getElementById("canvas_items");
    canvas_items.style.top = window.innerHeight / 7;
    canvas_items.style.left = window.innerWidth / 1.5;
    
    var regression_tab = document.getElementById('regression');
    var classification_tab = document.getElementById('classification');

    if(localStorage.getItem("user_name") === null){
        regression_tab.style.display = 'none';
        classification_tab.style.display = 'none'
        canvas_items.style.display = 'block'
    }
    else{
        canvas_items.style.display = 'none'
        regression_tab.style.display = 'block';
        classification_tab.style.display = 'block'
    }

    var stars = [], // Array that contains the stars
        FPS = 60, // Frames per second
        x = 100, // Number of stars
        mouse = {
            x: 0,
            y: 0
        };  // mouse location

    // Push stars to array

    for (var i = 0; i < x; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 1 + 1,
            vx: Math.floor(Math.random() * 50) - 25,
            vy: Math.floor(Math.random() * 50) - 25
        });
    }

    // Draw the scene

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.globalCompositeOperation = "xor";
        canvas.style.zIndex = -10
        for (var i = 0, x = stars.length; i < x; i++) {
            var s = stars[i];

            ctx.fillStyle = "#fff";
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.radius, 0, 2 * Math.PI);
            ctx.fill();
            ctx.fillStyle = 'black';
            ctx.stroke();
        }

        ctx.beginPath();
        for (var i = 0, x = stars.length; i < x; i++) {
            var starI = stars[i];
            ctx.moveTo(starI.x, starI.y);
            if (distance(mouse, starI) < 150) ctx.lineTo(mouse.x, mouse.y);
            for (var j = 0, x = stars.length; j < x; j++) {
                var starII = stars[j];
                if (distance(starI, starII) < 150) {
                    //ctx.globalAlpha = (1 / 150 * distance(starI, starII).toFixed(1));
                    ctx.lineTo(starII.x, starII.y);
                }
            }
        }
        ctx.lineWidth = 0.05;
        ctx.strokeStyle = 'white';
        ctx.stroke();
    }

    function distance(point1, point2) {
        var xs = 0;
        var ys = 0;

        xs = point2.x - point1.x;
        xs = xs * xs;

        ys = point2.y - point1.y;
        ys = ys * ys;

        return Math.sqrt(xs + ys);
    }

    // Update star locations

    function update() {
        for (var i = 0, x = stars.length; i < x; i++) {
            var s = stars[i];

            s.x += s.vx / FPS;
            s.y += s.vy / FPS;

            if (s.x < 0 || s.x > canvas.width) s.vx = -s.vx;
            if (s.y < 0 || s.y > canvas.height) s.vy = -s.vy;
        }
    }

    canvas.addEventListener('mousemove', function (e) {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    // Update and draw

    function tick() {
        draw();
        update();
        requestAnimationFrame(tick);
    }

    tick();
    $('.carousel').carousel();
    // $('.carousel.carousel-slider').carousel({ fullWidth: false });
    $('.slide-prev').click(function (e) {
        e.preventDefault();
        e.stopPropagation();
        $('.carousel').carousel('prev')
    });
    $('.slide-next').click(function (e) {
        e.preventDefault();
        e.stopPropagation();
        $('.carousel').carousel('next')
    });
    //this is for navigation using a new tab
    $('.share-btn').click(function (e) {
        var win = window.open('http://google.com', '_blank');
        win.focus();
    });

    function ajaxCallsFunc(type, url, contentType, data, callback) {
        $.ajax({
            type: type,
            url: url,
            contentType: contentType,
            data: data,
            success: callback
        });
    }

    $("#regression").click(function () {
        resp_obj = JSON.stringify({

            'analysis_mode': 'regression'
        });
        console.log(resp_obj)
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/set_analysis_mode", 'application/json', resp_obj, function (branches) {
            window.location = 'upload.html'
        });


    });


    $("#classification").click(function () {
        resp_obj = JSON.stringify({

            'analysis_mode': 'classification'
        });
        console.log(resp_obj)
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/set_analysis_mode", 'application/json', resp_obj, function (branches) {
            window.location = 'upload.html'

        });


    });


    $("#register").click(function () {
        const elem = document.getElementById('modal1');
        const instance = M.Modal.init(elem, { dismissible: false });
        instance.open();
    });

    $("#login").click(function () {
        const elem = document.getElementById('modal2');
        const instance = M.Modal.init(elem, { dismissible: false });
        instance.open();
    });

    $(document).keydown(function (event) {
        if (event.keyCode == 27) {
            const elem = document.getElementById('modal1');
            const instance = M.Modal.init(elem, { dismissible: false });
            instance.close();
        }
    });

    $("#sign_in").click(function(){

        var username = $("#username").val()
        var password = $("#password").val()

        var request = JSON.stringify({
            'username': username,
            'password': password
        });

        ajaxCallsFunc('POST', "http://0.0.0.0:5000/auth", 'application/json', request, function (response) {
            
            var toastHTML = '<span>' + response + '</span>';
            M.toast({ html: toastHTML }, 2000);
            
            if(response.includes('Invalid')){

            }
            else{
                const elem = document.getElementById('modal2');
                const instance = M.Modal.init(elem, { dismissible: false });
                instance.close();
    
                var regression_btn = document.getElementById('regression');
                var classification_btn = document.getElementById('classification');
                var canvas_items = document.getElementById('canvas_items');
    
                regression_btn.style.display = 'block';
                classification_btn.style.display = 'block';
                canvas_items.style.display = 'none';
                localStorage.setItem('user_name', username)
            }
            

        });

    });

    $("#register_reg").click(function(){

        var username = $("#username_reg").val()
        var password = $("#password_reg").val()
        var first_name = $("#first_name").val()
        var last_name = $("#last_name").val()
        var email = $("#email").val()

        var request = JSON.stringify({
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        });
        console.log(request)
        ajaxCallsFunc('POST', "http://0.0.0.0:5000/register", 'application/json', request, function (response) {
            
            var toastHTML = '<span>' + response + '</span>';
            M.toast({ html: toastHTML }, 2000);
            
        });


    });

})