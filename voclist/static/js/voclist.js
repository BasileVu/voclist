$('.edit-button').click(function () {
    var tr = $(this).parents('tr');
    var modal = $('#update-entry-modal');

    modal.find('.modal-title').text("Update " + tr.children("td").first().text());
    modal.find('#update-modal-word').attr("value", tr.children("td:nth-child(2)").text());
    modal.find('#update-modal-translation').attr("value", tr.children("td:nth-child(3)").text());

    var tags = []
    tr.children("td:nth-child(4)").children("span").toArray().forEach(function (span) {
        tags.push($(span).text().trim());
    });

    modal.find('#update-modal-tags').attr("value", tags.join(", "));

    modal.find('#update-ok-button').click(function () {
        ajaxUpdate("/entry/" + tr.attr("entry-id"), {
            "word": modal.find('#update-modal-word').val(),
            "translation": modal.find('#update-modal-translation').val(),
            "tags": modal.find('#update-modal-tags').val()
        });
    });
    modal.modal("show");
});

$('.delete-button').click(function () {
    var tr = $(this).parents('tr');

    // FIXME Yes/No
    var resp = prompt("Delete '" + tr.children("td").first().text() + "' ? Type 'YES' if you are sure.")
    if (resp === "YES") {
        ajaxDelete("/entry/" + tr.attr("entry-id"));
    }
});

$('tr .label').click(function () {
    window.location.search = "?tag=" + $(this).text().trim();
});

$('h3 .label').click(function () {
    console.log($(this).text().trim())
    // TODO edit modal
});