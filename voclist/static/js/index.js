$('#voclist-ok-button').click(function () {
    // var voclistIds = $('#voclist-ids').text().match(/[0-9]+/g);

    // FIXME find selected item position o find id + change url accordingly
    var id = 1;

    document.location.href = "/voclist/" + id + "/";
});