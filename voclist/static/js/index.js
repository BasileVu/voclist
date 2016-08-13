// FIXME
function getSelectedId() {
    return $('#voclist-selection').val().match(/\[([0-9]+)\]/)[1];
}

$('#voclist-ok-button').click(function () {
    document.location.href = "/voclist/" + getSelectedId() + "/";
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