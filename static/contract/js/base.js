function set_allowance_overtime_memo(id_time_max, id_allowance, id_comment) {
    time_max = $("#" + id_time_max).val();
    allowance = $("#" + id_allowance).val();
    obj_comment = $("#" + id_comment);

    comment = "＠" + allowance + "円/時間（" + time_max + "H以上支給とする）";
    obj_comment.val(comment)
}

function set_allowance_absenteeism_memo(id_time_max, id_allowance, id_comment) {
    time_max = $("#" + id_time_max).val();
    allowance = $("#" + id_allowance).val();
    obj_comment = $("#" + id_comment);

    comment = "＠" + allowance + "円/時間（" + time_max + "H未満の場合）";
    obj_comment.val(comment)
}