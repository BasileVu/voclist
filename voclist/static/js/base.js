function ajaxUpdate(path, data) {
    $.ajax(path, {
        method: "UPDATE",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function () {
            document.location.reload();
        },
        error: function () {
            document.location.reload(); // FIXME error handling
        }
    });
}

function ajaxDelete(path) {
    $.ajax(path, {
        method: "DELETE",
        success: function () {
            document.location.reload();
        },
        error: function () {
            document.location.reload(); // FIXME error handling
        }
    });
}
