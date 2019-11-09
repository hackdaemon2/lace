var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
    // This function will display the specified tab of the form ...
    var x = document.getElementsByClassName("tab");

    if (n < 3) {
        x[n].style.display = "block";
    }


    // var id = x[n].id;
    // $(`#${id}`).fadeIn(800);
    // ... and fix the Previous/Next buttons:
    if (n == 0) {
        // $("#back").hide();
        document.getElementById("back").style.display = "none";
    } else if (n > 0 && n < x.length) {
        // $("#back").fadeIn(800);
        document.getElementById("back").style.display = "inline";
    }
    if (n >= x.length) {
        document.getElementById("next").value = "Submit";
        document.getElementById("back").style.display = "none";
    } else {
        document.getElementById("next").value = "Next";
    }
    // ... and run a function that displays the correct step indicator:
    fixStepIndicator(n)
}

function nextPrev(n) {
    // This function will figure out which tab to display
    var x = document.getElementsByClassName("tab");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    if (x[currentTab] != undefined) {
        x[currentTab].style.display = "none";
    }

    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;
    console.log(`current tab: ${currentTab}`);
    // if you have reached the end of the form... :
    if (currentTab >= 3) {
        //...the form gets submitted:

        document.getElementById("next").style.display = "none";
        document.getElementById("back").style.display = "none";
        document.getElementById("signup_submit").style.display = "block";
    }
    // Otherwise, display the correct tab:
    showTab(currentTab);
}

function validateForm() {
    // This function deals with validation of the form fields
    var x, y, i, valid = true;
    x = document.getElementsByClassName("tab");

    if (x[currentTab] == undefined) {
        return valid;
    }

    y = x[currentTab].getElementsByTagName("input");
    // A loop that checks every input field in the current tab:
    for (i = 0; i < y.length; i++) {
        // If a field is empty...
        if (y[i].value == "") {
            // add an "invalid" class to the field:
            y[i].className += " invalid";
            // and set the current valid status to false:
            valid = false;
        }
    }

    // if (currentTab > 0) {
    //     let mobile = document.getElementById("mobile_number_signup");
    //     let password = document.getElementById("password1")
    //     let password2 = document.getElementById("password2");

    //     if (currentTab > 1) {
    //         if (mobile !== null && mobile !== undefined) {
    //             if (mobile.value.length < 11) {
    //                 mobile.className += "invalid";
    //                 valid = false
    //             }
    //         }
    //     }

    //     // if (currentTab > 2) {
    //     //     if (password !== null && password !== undefined) {
    //     //         if (password.value.length < 8) {
    //     //             password.className += "invalid";
    //     //             valid = false
    //     //         }
    //     //     }

    //     //     if (password2 !== null && password2 !== undefined) {
    //     //         if (password2.value.length < 8) {
    //     //             password2.className += "invalid";
    //     //             valid = false
    //     //         }
    //     //     }

    //     //     if (password2 !== null && password2 !== undefined) {
    //     //         if (password2.value.length < 8) {
    //     //             password2.className += "invalid";
    //     //             valid = false
    //     //         }

    //     //         if (password.value.length < 8) {
    //     //             password.className += "invalid";
    //     //             valid = false
    //     //         }

    //     //         if (password !== password2) {
    //     //             password.className += "invalid";
    //     //             password2.className += "invalid";
    //     //             valid = false;
    //     //         }
    //     //     }
    //     // }
    // }

    // If the valid status is true, mark the step as finished and valid:
    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid; // return the valid status
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    //... and adds the "active" class to the current step:
    if (n < 3) {
        x[n].className += " active";
    }
}