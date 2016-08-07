$('#voclist-ok-button').click(function () {
    // FIXME
    var id = $('#voclist-selection').val().match(/\[([0-9]+)\]/)[1];

    document.location.href = "/voclist/" + id + "/";
});