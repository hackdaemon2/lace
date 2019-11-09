const csrfSafeMethod = (method) => {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

const get_cookie = (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

const login = () => {
    let url = $('#login').attr('data-auth-url');
    let redirect_url = $('#login').attr('data-redirect-url');
    let csrftoken = get_cookie('csrftoken');
    let submit_button = $("#login_submit");
    let data = $("#login").serialize();
    let ajax_output = $("#ajax_output");
    let register_link = $("#register_link");
    let password_reset_link = $("#password_reset_link");

    // authenticate user on client side
    $.ajax({
        type: 'POST',
        url: url,
        beforeSend: (xhr, settings) => {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            submit_button.fadeOut(500);
            password_reset_link.fadeOut(500);
            register_link.fadeOut(500);
            ajax_output.html('<i class="fa fa-spin fa-spinner"></i> Authenticating...');
        },
        data: data,
    }).done((response) => {
        if (response.status === "success") {
            ajax_output.html('<i class="fa fa-spin fa-spinner"></i> ' + response.message);
            setTimeout(() => {
                location.href = redirect_url;
            }, 500);
        }
    }).fail((xhr, status, error) => {
        submit_button.fadeIn(500);
        password_reset_link.fadeIn(500);
        register_link.fadeIn(500);
        let response = JSON.parse(xhr.responseText);
        ajax_output.html('Authentication Failed: ' + response.message);
    });
};

$(document).ready(function() {
    let login_form = $('#login');
    let mobile_number = $('#mobile_number');
    let password = $('#password');
    let ajax_output = $("#ajax_output");

    ajax_output.html('&nbsp;&nbsp;&nbsp;');

    $("#continue").click(() => {
        let form_set_2 = $('#form_set_2');

        if (!form_set_2.is(':visible')) {
            $('#form_set_1').fadeOut(800);
            $('#form_set_2').slideUp().fadeIn(800);
        }
    });

    $("#back").click(() => {
        let form_set_1 = $('#form_set_1');

        if (!form_set_1.is(':visible')) {
            $('#form_set_2').fadeOut(800);
            $('#form_set_1').slideDown().fadeIn(800);
        }
    });

    login_form.submit((event) => {
        event.preventDefault();

        if (mobile_number === '' && password === '') {
            ajax_output.html('Mobile number and password are required fields');
            return false;
        } else if (mobile_number === '') {
            ajax_output.html('Mobile number is a required field');
            return false;
        } else if (password === '') {
            ajax_output.html('Password is a required field');
            return false;
        }

        login();
    });
});