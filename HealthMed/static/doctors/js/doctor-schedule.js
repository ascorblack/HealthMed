

window.ADD_FORM_EXISTS = false

var DOCTOR_SCHEDULE = $.ajax({
    type: "GET",
    url: "/doctor/api/getSchedule?doctor_id=" + DOCTOR_ID,
    headers: {'X-CSRFToken': csrfToken},
    dataType: "JSON",
    async: false
}).responseJSON;



async function createScheduleItem(time_start, time_end, state, schedule_id) {
    return "<div class='schedule-item'>" +
                "<p>" + time_start.slice(0, -3) + " - " + time_end.slice(0, -3) + "</p>" +
                "<p class='" + (state ? 'unavaible' : 'avaible') + "'>" + (state ? 'занято' : 'свободно') + "</p>" + 
                "<button onclick='deleteRecord(this)' type='button' class='schedule-del-btn' id='schedule-del-btn-" + schedule_id + "' " + (state ? 'disabled'  : '') + ">Удалить</button>" +
            "</div>"
}

async function createScheduleItemForm() {
    return "<div class='schedule-item-form' id='schedule-form'>" +
                "<div class='time-picker'>" +
                    "<input type='text' name='start_time' id='start_time' class='time' required>" +
                    // '<b-form-timepicker id="timepicker-sm" size="sm" locale="ge" class="mb-2"></b-form-timepicker>' +
                    "<input type='text' name='end_time' id='end_time' class='time' required>" +
                "</div>" +
                "<button onclick='addRecord(this)' type='button' class='schedule-add-btn'>Добавить</button>" +
            "</div>"
}

async function displayDoctorSchedules(date) {
    date_schedule = DOCTOR_SCHEDULE[date];
    $("#day-schedule").html("")
    $(".schedule-btn").prop("disabled", false)
    for (let schedule in date_schedule) {
        schedule_block = await createScheduleItem(
            time_start=date_schedule[schedule].start_time,
            time_end=date_schedule[schedule].end_time,
            state=date_schedule[schedule].state,
            schedule_id=date_schedule[schedule].schedule_id,
        )
        $("#day-schedule").append(schedule_block)
    }
}

async function getTimePickerValue(picker_id) {
    let value = $(picker_id).timepicker().val()
    
    if (value.split(":")[0].length == 1) {
        value = "0" + value
    }
    return value
}


async function addRecord(event) {
    let start_time = await getTimePickerValue('#start_time')
    let end_time = await getTimePickerValue("#end_time")
    let date = $('.calendar').datepicker("getFormattedDate")
    let button = $(".schedule-add-btn")

    let send_data = new FormData();
    send_data.append("start_time", start_time)
    send_data.append("end_time", end_time)
    send_data.append("date", date)

    if (start_time < end_time) {

        $.ajax({
            url: "/doctor/api/addScheduleRecord",
            data: send_data,
            processData: false,
            contentType: false,
            type: "POST",
            headers: {'X-CSRFToken': csrfToken},
            mode: 'same-origin',
            success: async function (data) {
                if (data.status_type === "UNSUCCESS_ADD_RECORD") {
                    button.css("background-color", "red");
                    setTimeout(async function (e) {
                        button.css("background-color", "");
                    }, 800);
                } else if (data.status_type === "SUCCESS_ADD_RECORD") {
                    button.css("background-color", "green");
                    setTimeout(async function (e) {
                        button.css("background-color", "");
                        await renderWorkspace(workspace_type=window.workspace_type)
                        $('.calendar').datepicker("setDate", new Date($('.calendar').datepicker("getDate")))
                    }, 800);
                }
            },
            error: async function (data) {
                button.css("background-color", "red");
                setTimeout(async function (e) {
                    button.css("background-color", "");
                }, 800);
            }
        });
    } else {
        $(".time-picker input").css("border", "2px solid red");
        setTimeout(async function (e) {
            $(".time-picker input").css("border", "");
        }, 400)
    }
}

async function deleteRecord(element) {
    schedule_id = element.id.split("-").slice(-1);

    let send_data = new FormData();
    send_data.append("schedule_id", schedule_id)

    $.ajax({
        url: "/doctor/api/deleteScheduleRecord",
        data: send_data,
        processData: false,
        contentType: false,
        type: "POST",
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
        success: async function (data) {
            $(element).css("background-color", "green");
            setTimeout(async function (e) {
                $(element).css("background-color", "");
                await renderWorkspace(workspace_type=window.workspace_type)
                $('.calendar').datepicker("setDate", new Date($('.calendar').datepicker("getDate")))
            }, 800);
        },
        error: async function (data) {
            $(element).css("background-color", "red");
            setTimeout(async function (e) {
                $(element).css("background-color", "");
            }, 800);
        }
    });
}


$(document).ready(function()
{   
    let current_date = (new Date()).toISOString().split('T')[0].split("-")

    let scheduleDays = {}
    for (let schedule in DOCTOR_SCHEDULE) {
        if (schedule !== "count_free_days") {
            date = schedule.split(".")
            scheduleDays[new Date( date[2] + "-" + date[1] + "-" + date[0] + " 00:00:00")] = DOCTOR_SCHEDULE[schedule]
        }
    }

    $('#schedule-calendar').datepicker({
        language: "ru", 
        calendarWeeks: true, 
        todayHighlight: true,
        inline: true,
        sideBySide: true,
        format: 'dd.mm.yyyy',
        startDate: current_date[2] + "." + current_date[1] + "." + current_date[0],
        beforeShowDay: function( date ) {
            if (scheduleDays[new Date(date)]) {
                return {"classes": "exists"}
            } else {
                return {"classes": "non-exists"}
            }
        }
    });

    $('.calendar').datepicker().on('changeDate', async function (ev) {
        window.ADD_FORM_EXISTS = false
        let selected_date = $(ev.target).datepicker('getFormattedDate');
        await displayDoctorSchedules(date=selected_date)
    });

    BODY.on("click", "#add-schedule", async function (e) {
        if (!window.ADD_FORM_EXISTS) {
            window.ADD_FORM_EXISTS = true
            $("#day-schedule").append(await createScheduleItemForm())
            $('.time-picker .time').timepicker({ 
                template: false,
                minuteStep: 60,  
                showMeridian: false,
                defaultTime: '00:00',
                showSeconds: false
            });
        }
    });


})
