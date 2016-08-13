function getSelectedName() {
    return $('#voclist-selection').val();
}

function getSelectedId() {
    // FIXME
    return getSelectedName().match(/\[([0-9]+)\]/)[1];
}

$('#voclist-ok-button').click(function () {
    document.location.href = "/voclist/" + getSelectedId() + "/";
});

$('#voclist-edit-button').click(function () {
    var modal = $('#update-voclist-modal');

    modal.find('.modal-title').text("Update " + getSelectedName());

    // FIXME
    var languages = getSelectedName().replace(/\[[0-9]+\]/, "").split("-")

    modal.find('#update-language-left').attr("value", languages[0].trim());
    modal.find('#update-language-right').attr("value", languages[1].trim());

    modal.find('#update-ok-button').click(function () {
        $.ajax("/voclists/" + getSelectedId() + "/", {
            type: "UPDATE",
            contentType: "application/json",
            data: JSON.stringify({
                "language-left": modal.find('#update-language-left').val(),
                "language-right": modal.find('#update-language-right').val()
            }),
            success: function () {
                document.location.reload();
            },
            error: function () {
                // FIXME
                document.location.reload();
            }
        });
    });
    modal.modal("show");
});

$('#voclist-delete-button').click(function () {
    var tr = $(this).parent().parent();  // FIXME

    // FIXME
    var resp = prompt("Delete '" + $('#voclist-selection').val() + "' ? Type 'YES' if you are sure.")
    if (resp === "YES") {
        $.ajax("/voclists/", {
            type: "DELETE",
            contentType: "application/json",
            data: JSON.stringify({
                id: getSelectedId()
            }),
            success: function () {
                document.location.reload();
            },
            error: function () {
                // FIXME
                document.location.reload();
            }
        });
    }
});