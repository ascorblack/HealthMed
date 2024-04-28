// Функция обработки формы "Авторизация"
async function loginSubmit(e) {
    let form_data = await getFormData(LOGIN_FORM_ID);

    var response = $.ajax({
        url: "/user/api/loginPatient",
        data: form_data,
        processData: false,
        contentType: false,
        type: "POST",
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
        success: async function (data) {
            window.location.reload();
        },
        error: async function (data) {
            data = data.responseJSON;
            if (data.error_type === "USER_NOT_EXISTS") {
                await highlightAndAlert("email", "Такого пользователя не существует", "error", "red")
            } else if (data.error_type === "DATA_ENTRY_ERROR") {
                for (let key in data.error) { $(".fullscreen-form form #" + key).css("border-color", "red") }
                setTimeout(async function () {
                    for (let key in data.error) { $(".fullscreen-form form #" + key).css("border-color", "") }
                }, 1000)
            } else if (data.error_type === "PASSWORD_INCORRECT") {
                await highlightAndAlert("password", "Введён неверный пароль", "error", "red")
            }
        }
    });

    e.preventDefault()
}

$(LOGIN_FORM_ID).keypress(async function( event ) {
    if ( event.which === 13 ) {
      await loginSubmit(event)
    }
});


$(LOGIN_FORM_BTN).on("click", async function (e) { await loginSubmit(e) });
