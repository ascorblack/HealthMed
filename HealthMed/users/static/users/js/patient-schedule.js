async function openSchedule(element) {
    let schedule_block = $("#schedule-doctor-" + element.id.split("-").slice(-1));
    if (schedule_block.css("display") === "none") {
        schedule_block.show(400);
        schedule_block.css("display", "flex")
    } else {
        schedule_block.hide(400)
    }
};


var DOCTORS_SCHEDULE = $.ajax({
    type: "GET",
    url: "/doctor/api/getSchedule?special_id=" + window.special_id,
    headers: {'X-CSRFToken': csrfToken},
    dataType: "JSON",
    async: false
}).responseJSON;

async function createScheduleItem(time_start, time_end, state, schedule_id) {
    return "<div class='schedule-item'>" +
                "<p>" + time_start.slice(0, -3) + " - " + time_end.slice(0, -3) + "</p>" +
                "<p class='" + (state ? 'unavaible' : 'avaible') + "'>" + (state ? 'занято' : 'свободно') + "</p>" + 
                "<button onclick='makeAppointment(this)' type='button' class='schedule-btn' id='schedule-btn-" + schedule_id + "' " + (state ? 'disabled'  : '') + ">Записаться</button>" +
            "</div>"
}

async function displayDoctorSchedules(doctor_id, date) {
    date_schedule = DOCTORS_SCHEDULE[doctor_id][date];
    $("#day-schedule-" + doctor_id).html("")
    for (let schedule in date_schedule) {
        schedule_block = await createScheduleItem(
            time_start=date_schedule[schedule].start_time,
            time_end=date_schedule[schedule].end_time,
            state=date_schedule[schedule].state,
            schedule_id=date_schedule[schedule].schedule_id,
        )
        $("#day-schedule-" + doctor_id).append(schedule_block)
    }
}

async function makeAppointment(element) {
    var schedule_id = element.id.split("-").slice(-1);
    let send_data = new FormData();
    send_data.append("schedule_id", schedule_id)
    $.ajax({
        url: "/user/api/makeAppointment",
        data: send_data,
        processData: false,
        contentType: false,
        type: "POST",
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
        success: async function (data) {
            let button = $("#schedule-btn-" + schedule_id);
            if (data.status_type === "UNSUCCESS_APPOINTMENT") {
                button.css("background-color", "red");
                setTimeout(async function (e) {
                    button.css("background-color", "");
                }, 800);
            } else if (data.status_type === "SUCCESS_APPOINTMENT") {
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
};


$(document).ready(function()
{   
    let current_date = (new Date()).toISOString().split('T')[0].split("-")

    let scheduleDays = {}
    for (let doctor_id in DOCTORS_SCHEDULE ) {
        for (let schedule in DOCTORS_SCHEDULE[doctor_id]) {
            if (schedule !== "count_free_days") {
                date = schedule.split(".")
                scheduleDays[doctor_id] = scheduleDays[doctor_id] ? scheduleDays[doctor_id] : {}
                scheduleDays[doctor_id][new Date( date[2] + "-" + date[1] + "-" + date[0] + " 00:00:00")] = DOCTORS_SCHEDULE[doctor_id][schedule]
            }
        }

        $('#calendar-doctor-' + doctor_id).datepicker({
            language: "ru", 
            calendarWeeks: true, 
            todayHighlight: true,
            inline: true,
            sideBySide: true,
            format: 'dd.mm.yyyy',
            startDate: current_date[2] + "." + current_date[1] + "." + current_date[0],
            beforeShowDay: function( date ) {
                if (scheduleDays[doctor_id][new Date(date)]) {
                    return true
                } else {
                    return false
                }
            }
        });
    };

    $('.calendar').datepicker().on('changeDate', async function (ev) {
        let selected_date = $(ev.target).datepicker('getFormattedDate');
        let doctor_id = ev.target.id.split("-").slice(-1)
        await displayDoctorSchedules(doctor_id=doctor_id, date=selected_date)
    });
});