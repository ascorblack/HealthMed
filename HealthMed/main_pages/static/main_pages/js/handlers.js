const HEADER_CONTAINER = $(".header__container");
const PAGE_INDEX = $(".page-index");
const BODY = $("body")
const LOGIN_BTN_ID = "#login-button"
const REGISTRATION_BTN_ID = "#register-button"
const BUTTON_PERSONAL_CABINET_ID = "#personal-profile"
const FULLSCREEN_FORM_CLASS = ".fullscreen-form"
const CLOSE_FORM_ID = "#close-form"
const LOGIN_FORM_ID = "#login-form"
const LOGIN_FORM_BTN = "#login-submit-btn"
const REGISTER_FORM_BTN = "#register-submit-btn"
const REGISTER_FORM_ID = "#register-form"
window.current_form = null;
const TOGGLE_LOGIN_BLOCK = {
    registration: ["login", "login_in.html"],
    login: ["registration", "registration.html"]
}

function header_watcher() {
    if (window.innerWidth <= 600) {
        HEADER_CONTAINER.css("flex-direction", "column");
        HEADER_CONTAINER.css("height", "unset");
        let height = HEADER_CONTAINER.innerHeight();
        PAGE_INDEX.css("margin-top", height + "px")
    } else {
        HEADER_CONTAINER.css("flex-direction", "");
        HEADER_CONTAINER.css("height", "");
        PAGE_INDEX.css("margin-top", "")
    }
}

async function replaceLoginBlock(form_link, new_status_fom) {
    window.current_form = new_status_fom

    let new_login_block = $.get(form_link, function (data) {
        $(FULLSCREEN_FORM_CLASS).remove();
        $("body").append(data);
        $(FULLSCREEN_FORM_CLASS).css("display", "flex")
    })
}

async function getFormData(form_id) {
    let form_data = $(form_id).serializeArray().reduce(function(obj, item) {obj[item.name] = item.value; return obj}, {});
    let new_form_data = new FormData();
    for (let key in form_data) {
        new_form_data.append(key, form_data[key])
    }
    return new_form_data
}


async function highlightAndAlert(input_id, message, alert_type, color) {
    $(".fullscreen-form form #" + input_id).css("border-color", color)
     await makeAlert(message, alert_type)
    setTimeout(async function () {
        $(".fullscreen-form form #" + input_id).css("border-color", "")
    }, 1000)
}

$(document).ready(function()
{   
    var resizeDelay = 200;
    var doResize = true;

    var resizer = function () {
      if (doResize) {

        header_watcher();

        doResize = false;
      }
    };
    var resizerInterval = setInterval(resizer, resizeDelay);
        resizer();

        $(window).resize(function() {
          doResize = true;
    });

    BODY.on("click", CLOSE_FORM_ID, function ( e ) {
        $(FULLSCREEN_FORM_CLASS).fadeOut(200, function () {
            $(this).remove();
        })
    });

    BODY.on("click", LOGIN_BTN_ID, async function (e) {
        await replaceLoginBlock("/static/main_pages/forms/login_in.html", "login")
    });

    BODY.on("click", REGISTRATION_BTN_ID, async function (e) {
        await replaceLoginBlock("/static/main_pages/forms/registration.html", "registration")
    });

    BODY.on("click", CLOSE_FORM_ID, function ( e ) {
        $(FULLSCREEN_FORM_CLASS).fadeOut(200, function () {
            $(this).remove();
        })
    });

    BODY.on("click", "#toggle-login-block", async function (e) {
        let toggle_block = TOGGLE_LOGIN_BLOCK[window.current_form]
        window.current_form = toggle_block[0]
        await replaceLoginBlock("/static/main_pages/forms/" + toggle_block[1], toggle_block[0])
    });

    BODY.on("click", "#logout-button", async function (e) {
        $.ajax({
                url: "/user/api/logOut",
                type: "POST",
                headers: {'X-CSRFToken': csrfToken},
                mode: 'same-origin',
                async: false,
                success: function (data) {
                         window.location.href = "/"
                }
            }
        );

    });

    BODY.on("click", ".show-article-btn", async function (e) {
        let article_text = $("#article-text-" + e.target.id.split("-").slice(-1));
        let button = $(e.target);
        article_text.css("display") == "none" ? article_text.show(600) : article_text.hide(600)
        button.html() == "Раскрыть статью" ? button.html("Скрыть статью") : button.html("Раскрыть статью")
    });
});