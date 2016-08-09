$('td').click(function () {
    var id = $(this).parent().attr("entry-id");
});

$('.delete-button').click(function () {
    var tr = $(this).parent().parent();  // FIXME

    // FIXME
    var resp = prompt("Delete '" + tr.children("td").first().text() + "' ? Type 'YES' if you are sure.")
    if (resp === "YES") {
        $.ajax("/voclist/" + $('#voclist-id').attr("value") + "/", {
            type: "DELETE",
            contentType: "application/json",
            data: JSON.stringify({
                id: tr.attr('entry-id')
            })
        });
    }
});