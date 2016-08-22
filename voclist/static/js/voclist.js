// FIXME
function getVoclistId() {
    return parseInt(window.location.pathname.match(/.*\/([0-9]+)$/)[1]);
}

function setModalValues(modal, title, word, translation, tags) {
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

    setModalValues(modal, "New entry", "", "", "");

    modal.find('form').on("submit", function (event) {
        event.preventDefault();
        ajaxPost("/voclist/" + getVoclistId(), getModalValues(modal));
    });

    modal.modal("show");
});

$('.edit-button').click(function () {
    var tr = $(this).parents('tr');
    var modal = $('#entry-modal');

    var tags = [];
    tr.children("td:nth-child(4)").children("span").toArray().forEach(function (span) {
        tags.push($(span).text().trim());
    });

    setModalValues(
        modal,
        "Update " + tr.children("td").first().text(),
        tr.children("td:nth-child(2)").text(),
        tr.children("td:nth-child(3)").text(),
        tags.join(", ")
    );

    modal.find('form').on("submit", function (event) {
        event.preventDefault();
        ajaxPut("/entry/" + tr.attr("entry-id"), getModalValues(modal));
    });

    modal.modal("show");
});

$('.delete-button').click(function () {
    var tr = $(this).parents('tr');

    if (confirm("Delete '" + tr.children("td").first().text() + "' ?")) {
        ajaxDelete("/entry/" + tr.attr("entry-id"));
    }
});

$('tr .label').click(function () {
    window.location.search = "?tag=" + $(this).text().trim();
});

$('#tag-value').click(function () {
    var tag = window.location.href.match(/tag=([^&]*)/)[1];

    $(this).replaceWith(
        '<form id="tag-edit-form" class="form-inline">' +
            '<div class="form-group">' +
                '<input id="input-tag-value" class="form-control" type="text" value="' + tag + '">' +
            '</div>' +
            '<div class="form-group">' +
                '<button type="submit" class="btn btn-primary">Ok</button>' +
            '</div>' +
        '</form>'
    );

    $('#tag-edit-form').on("submit", function (event) {
        event.preventDefault();

        var newValue = $('#input-tag-value').val();
        ajaxPut("/tags/" + tag, {
            value: newValue
        }, function () {
            console.log("success!");
            window.location.search = "?tag=" + newValue;
        });
    });
});
