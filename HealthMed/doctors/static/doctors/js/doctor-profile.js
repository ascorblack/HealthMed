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
    let url = "/doctor/api/renderWorkspace?workspace=" + workspace_type
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


$(document).ready(function()
{   
    $(".user-info input").prop("disabled", true)

    BODY.on("click", ".nav-menu button", async function (element) {
        $(WORKSPACE_NAV_MENU + " button").removeClass("active");
        window.workspace_type = element.target.id;
        $(element.target).addClass("active");
        await renderWorkspace(workspace_type=window.workspace_type)
    });
});