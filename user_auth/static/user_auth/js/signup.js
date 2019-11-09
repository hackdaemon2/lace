var signup_button = $("#signup_submit");
var signup_form = $("#signup_form");

const signup = () => {
    let url = signup_form.attr('data-signup-url');
    let csrftoken = get_cookie('csrftoken');
    let data = signup_form.serialize();
    let ajax_output = $("#ajax_output_signup");

    // register user
    $.ajax({
        type: 'POST',
        url: url,
        beforeSend: (xhr, settings) => {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            signup_button.attr({ disabled: "disabled" });
            ajax_output.html('Creating user account...');
        },
        data: data,
    }).done((response) => {
        signup_button.removeAttr("disabled");
        if (response.status === "success") {
            ajax_output.html(response.message);
            signup_form.reset();
        }
    }).fail((xhr, status, error) => {
        signup_button.removeAttr("disabled");
        let response = JSON.parse(xhr.responseText);

        ajax_output.html('Error: ' + response.message);

    });
};

signup_button.click((event) => {
    event.preventDefault();
    console.log("clicked");
    signup();
});