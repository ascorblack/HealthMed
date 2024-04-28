const WORKSPACE_NAV_MENU = ".nav-menu"
const WORKSPACE_VIEWER = "#workspace-viewer"


$.fn.datepicker.dates['ru'] = {
    days: ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
    daysShort: ["Воск", "Понед", "Втор", "Сред", "Четв", "Пятн", "Суб", "Воск"],
    daysMin: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
    months: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
    monthsShort: ["Янв", "Фев", "Мар", "Апр", "Май", "Июнь", "Июль", "Авг", "Сен", "Окт", "Нояб", "Дек"],
    today: "Сегодня"
};


async function renderWorkspace(workspace_type, specialization_id=false) {
    let url = "/user/api/renderWorkspace?workspace=" + workspace_type
    if (specialization_id) {
        url += "&specialization_id=" + specialization_id
    }

    $.ajax({
        url: url,
        processData: false,
        contentType: false,
        type: "GET",
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
        success: async function (data) {
            $(WORKSPACE_VIEWER).html(data)
        },
        error: async function (data) {
            $(WORKSPACE_VIEWER).html("")
        }
    });
}

async function denyAppointment(element) {
    var schedule_id = element.id.split("-").slice(-1);
    let send_data = new FormData();
    send_data.append("schedule_id", schedule_id)
    $.ajax({
        url: "/user/api/denyAppointment",
        data: send_data,
        processData: false,
        contentType: false,
        type: "POST",
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
        success: async function (data) {
            let button = $("#deny-schedule-" + schedule_id);
            if (data.status_type === "UNSUCCESS_DISAPPOINTMENT") {
                button.css("background-color", "red");
                setTimeout(async function (e) {
                    button.css("background-color", "");
                }, 800);
            } else if (data.status_type === "SUCCESS_DISAPPOINTMENT") {
                button.css("background-color", "green");
                setTimeout(async function (e) {
                    button.css("background-color", "");
                    await renderWorkspace(workspace_type=window.workspace_type,
                        specialization_id=window.special_id)
                }, 800);
            }
        },
        error: async function (data) {
            data = data.responseJSON;
            $(element).css("background-color", "red");
            setTimeout(async function (e) {
                $(element).css("background-color", "");
            }, 800);
        }
    });
}


async function userInfoEdit(element) {
    $(".user-info input").prop("disabled") ? $(".user-info input").prop("disabled", false) : $(".user-info input").prop("disabled", true)
    $(".user-info").toggleClass("disabled");
    let button = $("#edit-info-btn")
    button.toggleClass("in-edit");
    if (button.html() === "Редактировать") {
        button.html("Подтвердить")
    } else {
        button.html("Редактировать")
        send_data = new FormData();
        send_data.append("birthdate", $("#user-birthdate").val())
        send_data.append("email", $("#user-email").val())
        // send_data.append("phone", $("#user-phone").val())
        send_data.append("passport", $("#user-passport").val())
        send_data.append("med_policy", $("#user-med_policy").val())

        $.ajax({
            url: "/user/api/editInfo",
            data: send_data,
            processData: false,
            contentType: false,
            type: "POST",
            headers: {'X-CSRFToken': csrfToken},
            mode: 'same-origin',
            success: async function (data) {
                $("#edit-info-btn").css("border", "1px solid rgb(255 255 255 / 89%)")
                $("#edit-info-btn").css("background-color", "rgb(56 255 0)")
                $("#edit-info-btn").css("color", "rgb(0 0 0 / 89%)")
                setTimeout(async function() {
                    window.location.reload()
                }, 600)
            },
            error: async function (data) {
                data = data.responseJSON;
                for (let key in data.error) { $(".user-field #user-" + key).css("border-color", "red") }
                setTimeout(async function() {
                    for (let key in data.error) { $(".user-field #user-" + key).css("border-color", "") }
                }, 600)
            }
        });
    }
}


async function deleteConsultation(element) {
    var consultation_id = element.id.split("-").slice(-1);
    let button = $(element);
    let send_data = new FormData();

    send_data.append("consultation_id", consultation_id)

    $.ajax({
        url: "/user/api/deleteConsultation",
        data: send_data,
        processData: false,
        contentType: false,
        type: "POST",
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
        success: async function (data) {
            if (data.status_type === "SUCCESS_DELETE") {
                button.css("background-color", "green");
                setTimeout(async function (e) {
                    button.css("background-color", "");
                    await renderWorkspace(workspace_type=window.workspace_type)
                }, 400);
            }
        },
        error: async function (data) {
            button.css("background-color", "red");
            setTimeout(async function (e) {
                button.css("background-color", "");
            }, 400);
        }
    });
};


$(document).ready(function()
{   
    $(".user-info input").prop("disabled", true)

    BODY.on("click", ".nav-menu button", async function (element) {
        $(WORKSPACE_NAV_MENU + " button").removeClass("active");
        window.workspace_type = element.target.id;
        $(element.target).addClass("active");
        await renderWorkspace(workspace_type=window.workspace_type)
    });

    BODY.on("click", ".spec-item", async function (element) {
        let specialization_id = parseInt(element.target.id.replace("spec-", "")) ;
        window.special_id = specialization_id;
        await renderWorkspace(workspace_type=window.workspace_type, specialization_id=specialization_id);
    });
});