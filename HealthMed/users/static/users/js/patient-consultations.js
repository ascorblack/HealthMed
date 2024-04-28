
async function makeConsultationRequest(element) {
    var doctor_id = element.id.split("-").slice(-1);
    var date = $("#consult-date-" + doctor_id).val()
    let button = $(element);
    let send_data = new FormData();

    send_data.append("doctor_id", doctor_id)
    send_data.append("date", date)

    $.ajax({
        url: "/user/api/makeConsultationRequest",
        data: send_data,
        processData: false,
        contentType: false,
        type: "POST",
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
        success: async function (data) {
            if (data.status_type === "SUCCESS_ADD_REQUEST") {
                button.css("background-color", "green");
                setTimeout(async function (e) {
                    button.css("background-color", "");
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
    $(".consult-date input").attr('min', (new Date()).toISOString().split('T')[0])
});