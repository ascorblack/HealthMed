
async function createArticle(element) {
    var title = $("#article-title").val()
    var text = $("#article-text").val()
    let button = $(element);
    let send_data = new FormData();

    send_data.append("title", title)
    send_data.append("text", text)
    $.ajax({
        url: "/doctor/api/createArticle",
        data: send_data,
        processData: false,
        contentType: false,
        type: "POST",
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
        success: async function (data) {            
            if (data.status_type === "SUCCESS_CREATE") {
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


async function articleAction(element, action) {
    var article_id = element.id.split("-").slice(-1);
    let button = $(element);
    let send_data = new FormData();

    send_data.append("article_id", article_id)

    $.ajax({
        url: "/doctor/api/" + action + "Article",
        data: send_data,
        processData: false,
        contentType: false,
        type: "POST",
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
        success: async function (data) {
            if (data.status_type === "SUCCESS_" + action.toUpperCase()) {
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
    $(".consult-date input").attr('min', (new Date()).toISOString().split('T')[0])
});
