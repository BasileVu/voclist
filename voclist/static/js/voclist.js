// FIXME
function getVoclistId() {
    return parseInt(document.location.href.match(/.*\/([0-9]+)$/)[1]);
}

function fillModalValues(modal, title, word, translation, tags) {
    modal.find('.modal-title').text(title);
    modal.find('#modal-word').attr("value", word);
    modal.find('#modal-translation').attr("value", translation);
    modal.find('#modal-tags').attr("value", tags);
}

function getModalValues(modal) {
    return {
       "word": modal.find('#modal-word').val(),
       "translation": modal.find('#modal-translation').val(),
       "tags": modal.find('#modal-tags').val()
    };
}

$('#add-entry-button').click(function () {
    var modal = $('#entry-modal');

    fillModalValues(modal, "New entry", "", "", "");

    modal.find('#entry-modal-ok-button').click(function () {
        ajaxPost("/voclist/" + getVoclistId(), getModalValues(modal));
    });

    modal.modal("show");
});

$('.edit-button').click(function () {
    var tr = $(this).parents('tr');
    var modal = $('#entry-modal');

    var tags = []
    tr.children("td:nth-child(4)").children("span").toArray().forEach(function (span) {
        tags.push($(span).text().trim());
    });

    fillModalValues(
        modal,
        "Update " + tr.children("td").first().text(),
        tr.children("td:nth-child(2)").text(),
        tr.children("td:nth-child(3)").text(),
        tags.join(", ")
    );

    modal.find('#entry-modal-ok-button').click(function () {
        ajaxUpdate("/entry/" + tr.attr("entry-id"), getModalValues(modal));
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