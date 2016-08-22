function prepareObj(method, data, success, error, obj) {
    if (obj === undefined) {
        obj = {}
    }

    obj["method"] = method;
    obj["contentType"] = "application/json";
    obj["data"] = JSON.stringify(data);

    obj["success"] = success !== undefined ? success : function () {
        document.location.reload(); // FIXME notification
    };
    obj["error"] = error !== undefined ? error : function () {
        document.location.reload(); // FIXME notification
    };

    return obj;
}

function ajaxPost(path, data, success, error, obj) {
    $.ajax(path, prepareObj("POST", data, success, error, obj));
}

function ajaxPut(path, data, success, error, obj) {
    $.ajax(path, prepareObj("PUT", data, success, error, obj));
}

function ajaxDelete(path, data, success, error, obj) {
    $.ajax(path, prepareObj("DELETE", data, success, error, obj));
}
