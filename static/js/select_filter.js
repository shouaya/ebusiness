function select_filter(id_select, id_input) {
    var myfilter = new filterlist(document.getElementById(id_select));
    $("#" + id_input).keyup(function() {
        myfilter.set(this.value)
    })
}

function replaceToFilter(id_select, id_input) {
    if (document.getElementById(id_select).selectedIndex == 0) {
        obj = $("#" + id_select);
        if (obj.length == 1) {
            obj.attr("size", "9");
            obj.css("width", "400px");
            obj.css("height", "17.2em");
            obj.before("<p id='id_members_filter' style='margin-left: 0px; padding-left:3px;' class='selector-filter'>" +
            "<label style='width: 12px;'>" +
            "    <img src='/static/admin/img/selector-search.gif'></img>" +
            "</label>" +
            "<input id='" + id_input + "' type='text' placeholder='フィルター' style='width: 367px;' />" +
            "</p>");

            select_filter(id_select, id_input);
        }
    }
}

function replaceToFilterForSubRow(rowClass, tdClass) {
    rows = $("." + rowClass);
    for (var i=0; i<rows.length; i++) {
        row_id = rows[i].id;
        id_input = "input_" + row_id;
        obj = $("#" + row_id + " td." + tdClass + " select");
        id_select = obj.id;
        obj.attr("size", "9");
        obj.css("width", "100px");
        obj.css("height", "7em");
        obj.before("<p id='id_members_filter' style='margin-left: 0px; padding-left:3px;' class='selector-filter'>" +
        "<label style='width: 12px;'>" +
        "    <img src='/static/admin/img/selector-search.gif'></img>" +
        "</label>" +
        "<input id='" + id_input + "' type='text' placeholder='フィルター' style='width: 70px;' />" +
        "</p>");

        select_filter(id_select, id_input);
    }
}

$(document).ready(function() {
    replaceToFilter("id_project", "input_project");
    replaceToFilter("id_member", "input_member");
    replaceToFilter("id_client", "input_client");
    replaceToFilter("id_subcontractor", "input_subcontractor");

//    replaceToFilterForSubRow("dynamic-projectmember_set", "field-member")
});
