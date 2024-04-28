const FORM_ALERTS_ID = "#form-alerts"


async function makeAlert(text, alert_type) {
    let alert_form = $(FORM_ALERTS_ID);
    alert_form.html(
        "<p class='" + alert_type + "'> " + text + " </p>"
    )
    alert_form.css("display", "flex")
    setTimeout(async function () {
        alert_form.fadeOut(300, async function() { $(this).html("") })
    }, 1600)
}
