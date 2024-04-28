// Функция обработки формы "Регистрация"
async function registerSubmit(e) {
    let form_data = await getFormData(REGISTER_FORM_ID);

    var response = $.ajax({
        url: "/user/api/registerPatient",
        data: form_data,
        processData: false,
        contentType: false,
        type: "POST",
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
        success: async function (data) {
            $.get("/static/main_pages/forms/success.html", function (data) {
                $(REGISTER_FORM_ID).remove();
                $(".fullscreen-form").append(data);
                $(".fullscreen-form #alert-text").html("Вы успешно зарегистрировались")
            })
            setTimeout(async function () {
                $(FULLSCREEN_FORM_CLASS).fadeOut(500, function () {
                    $(this).remove();
                })
                await replaceLoginBlock("/static/main_pages/forms/login_in.html", "login")
            }, 1500)
        },
        error: async function (data) {
            data.error_type = "";
            data = data.responseJSON;
            if (data.error_type === "USER_NOT_EXISTS") {
                await highlightAndAlert("email", "Такого пользователя не существует", "error", "red")
            } else if (data.error_type === "DATA_ENTRY_ERROR") {
                for (let key in data.error) { $(".fullscreen-form form #" + key).css("border-color", "red") }
                setTimeout(async function () {
                    for (let key in data.error) { $(".fullscreen-form form #" + key).css("border-color", "") }
                }, 1000)
            } else if (data.error_type === "USER_ALREADY_EXISTS") {
                await highlightAndAlert(data.error[0], "Пользователь с " + data.error[2] + " '" + data.error[1] + "' уже существует", "error", "red")
            }
        }
    });

    e.preventDefault()
}

$(REGISTER_FORM_ID).keypress(async function( event ) {
    if ( event.which === 13 ) {
      await registerSubmit(event)
    }
});

$(REGISTER_FORM_BTN).on("click", async function(e) { await registerSubmit(e) });