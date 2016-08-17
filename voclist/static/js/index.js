function getSelectedName() {
    return $('#voclist-selection').val();
}

function getSelectedId() {
    // FIXME
    return getSelectedName().match(/\[([0-9]+)\]/)[1];
}

$('#ok-button').click(function () {
    document.location.href = "/voclist/" + getSelectedId();
});

function setModalValues(modal, title, left, right) {
    modal.find('.modal-title').text(title);
    modal.find('#language-left').attr("value", left);
    modal.find('#language-right').attr("value", right);
}

function getModalValues(modal) {
    return {
       "language-left": modal.find('#language-left').val(),
       "language-right": modal.find('#language-right').val()
    };
}

$('#add-voclist-button').click(function () {
    var modal = $('#voclist-modal');

    setModalValues(modal, "New voclist", "", "");

    modal.find('#voclist-modal-ok-button').click(function () {
        ajaxPost("/voclists/", getModalValues(modal));
    });

    modal.modal("show");
});

$('#edit-button').click(function () {
    var modal = $('#voclist-modal');

    // FIXME
    var languages = getSelectedName().replace(/\[[0-9]+\]/, "").split("-")
    setModalValues(modal, "Update " + getSelectedName(), languages[0].trim(), languages[1].trim());

    modal.find('#voclist-modal-ok-button').click(function () {
        ajaxUpdate("/voclists/" + getSelectedId(), getModalValues(modal));
    });

    modal.modal("show");
});

$('#delete-button').click(function () {
    var resp = prompt("Delete '" + $('#voclist-selection').val() + "' ? Type 'YES' if you are sure.")
    if (resp === "YES") {
        ajaxDelete("/voclists/" + getSelectedId());
    }
});