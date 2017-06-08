function calculate_plus_minus(obj, name_base, name_min, name_max, name_minus, name_plus) {
    if (obj.id == "id_" + name_base) {
        price = parseFloat($("#id_" + name_base).val());
        min_hours = parseFloat($("#id_" + name_min).val());
        max_hours = parseFloat($("#id_" + name_max).val());
        plus_per_hour = Math.round(price / max_hours);
        minus_per_hour = Math.round(price / min_hours);
        // 残業手当
        $("#id_" + name_plus).val(plus_per_hour);
        // 残業手当メモ
        change_allowance_overtime($("#id_" + name_plus)[0], name_base, 'calculate_time_max', 'allowance_overtime_memo')
        // 欠勤手当
        $("#id_" + name_minus).val(minus_per_hour);
        // 欠勤手当メモ
        change_allowance_absenteeism($("#id_" + name_minus)[0], name_base, 'calculate_time_min', 'allowance_absenteeism_memo')

        // 基本給メモ
        obj_memo = $("#id_" + "allowance_base_memo");
        if (obj_memo != null) {
            obj_is_hourly_pay = $("#id_is_hourly_pay")
            obj_is_fixed_cost = $("#id_is_fixed_cost")
            is_hourly_pay = false;
            is_fixed_cost = false
            base_price_memo = "月額基本料金：\\" + toNumComma(price) + "円/月  (税金抜き)"
            // 時給の場合
            if (obj_is_hourly_pay && obj_is_hourly_pay.prop("checked") == true) {
                base_price_memo = "時間単価：\\" + toNumComma(price) + "/h  (消費税を含まない)"
            } else if (obj_is_fixed_cost && obj_is_fixed_cost.prop("checked") == true) {
                base_price_memo = "月額基本料金：\\" + toNumComma(price) + "円/月  (固定)"
            }
            obj_memo.val(base_price_memo);
        }
    } else {
        // Inlineの場合
        row_id = $(obj).parent().parent().attr("id");
        price = parseFloat($(obj).val());
        obj_min_hour = $("#id_" + row_id + "-" + name_min);
        obj_max_hour = $("#id_" + row_id + "-" + name_max);
        obj_plus = $("#id_" + row_id + "-" + name_plus);
        obj_minus = $("#id_" + row_id + "-" + name_minus);
        min_hours = parseFloat(obj_min_hour.val());
        max_hours = parseFloat(obj_max_hour.val());

        plus_per_hour = Math.round(price / max_hours);
        minus_per_hour = Math.round(price / min_hours);
        obj_plus.val(plus_per_hour);
        obj_minus.val(minus_per_hour);

        // 基本給メモ
        obj_memo = $("#id_" + row_id + "-allowance_base_memo");
        if (obj_memo != null) {
            obj_memo.val("月額基本料金：\\" + toNumComma(price) + "円/月  (税金抜き)");
        }
    }
}

function calculate_minus_from_min_hour(obj, name_base, name_min, name_max, name_minus, name_plus) {
    if (obj.id == "id_" + name_min) {
        price = parseFloat($("#id_" + name_base).val());
        min_hours = parseFloat($("#id_" + name_min).val());
        max_hours = parseFloat($("#id_" + name_max).val());
        minus_per_hour = Math.round(price / min_hours);
        $("#id_" + name_minus).val(minus_per_hour);

        //// 基準時間メモ
        //obj_memo = $("#id_" + "allowance_time_memo");
        //if (obj_memo != null) {
        //    obj_memo.val("※基準時間：" + min_hours + "～" + max_hours + "/月")
        //}
        // 欠勤手当メモ
        obj_memo_minus = $("#id_" + "allowance_absenteeism_memo");
        if (obj_memo_minus != null) {
            obj_is_show_formula = $("#id_" + "is_show_formula");
            is_show_formula = false;
            message = "不足単価：\\" + toNumComma(price) + "/" + min_hours + "h=\\" + toNumComma(minus_per_hour) + "/h"
            if (obj_is_show_formula && obj_is_show_formula.prop("checked") == false) {
                message = "不足単価：\\" + toNumComma(minus_per_hour) + "/h"
            }
            obj_memo_minus.val(message)
        }
    } else {
        // Inlineの場合
        row_id = $(obj).parent().parent().attr("id");
        obj_price = $("#id_" + row_id + "-" + name_base);
        obj_min_hour = $("#id_" + row_id + "-" + name_min);
        obj_minus = $("#id_" + row_id + "-" + name_minus);
        price = parseFloat(obj_price.val());
        min_hours = parseFloat(obj_min_hour.val());

        minus_per_hour = Math.round(price / min_hours);
        obj_minus.val(minus_per_hour);
    }
}

function calculate_plus_from_max_hour(obj, name_base, name_min, name_max, name_minus, name_plus) {
    if (obj.id == "id_" + name_max) {
        price = parseFloat($("#id_" + name_base).val());
        min_hours = parseFloat($("#id_" + name_min).val());
        max_hours = parseFloat($("#id_" + name_max).val());
        plus_per_hour = Math.round(price / max_hours);
        $("#id_" + name_plus).val(plus_per_hour);

        // 基準時間メモ
        //obj_memo = $("#id_" + "allowance_time_memo");
        //if (obj_memo != null) {
        //    obj_memo.val("※基準時間：" + min_hours + "～" + max_hours + "/月")
        //}
        // 残業手当メモ
        obj_memo_plus = $("#id_" + "allowance_overtime_memo");
        if (obj_memo_plus != null) {
            obj_is_show_formula = $("#id_" + "is_show_formula");
            is_show_formula = false;
            message = "超過単価：\\" + toNumComma(price) + "/" + max_hours + "h=\\" + toNumComma(plus_per_hour) + "/h"
            if (obj_is_show_formula && obj_is_show_formula.prop("checked") == false) {
                message = "超過単価：\\" + toNumComma(plus_per_hour) + "/h"
            }
            obj_memo_plus.val(message)
        }
    } else {
        // Inlineの場合
        row_id = $(obj).parent().parent().attr("id");
        obj_price = $("#id_" + row_id + "-" + name_base);
        obj_max_hour = $("#id_" + row_id + "-" + name_max);
        obj_plus = $("#id_" + row_id + "-" + name_plus);
        price = parseFloat(obj_price.val());
        max_hours = parseFloat(obj_max_hour.val());

        plus_per_hour = Math.round(price / max_hours);
        obj_plus.val(plus_per_hour);
    }
}

function change_hourly_pay_display(obj, name_base) {
    if (obj.id == "id_is_hourly_pay") {
        price = parseFloat($("#id_" + name_base).val());
        is_hourly_pay = $(obj).prop("checked");

        // 基本給メモ
        obj_memo = $("#id_" + "allowance_base_memo");
        if (obj_memo != null) {
            base_price_memo = "月額基本料金：\\" + toNumComma(price) + "円/月  (税金抜き)"
            // 時給の場合
            if (is_hourly_pay) {
                base_price_memo = "時間単価：\\" + toNumComma(price) + "/h  (消費税を含まない)"
            }
            obj_memo.val(base_price_memo);
        }
    } else {
        // Inlineの場合
    }
}

function change_fixed_cost_display(obj, name_base) {
    if (obj.id == "id_is_fixed_cost") {
        price = parseFloat($("#id_" + name_base).val());
        is_fixed_cost = $(obj).prop("checked");
        is_hourly_pay = $("#id_is_hourly_pay").prop("checked");

        // 基本給メモ
        obj_memo = $("#id_" + "allowance_base_memo");
        if (obj_memo != null && is_hourly_pay == false) {
            base_price_memo = "月額基本料金：\\" + toNumComma(price) + "円/月  (税金抜き)"
            // 時給の場合
            if (is_fixed_cost) {
                base_price_memo = "月額基本料金：\\" + toNumComma(price) + "円/月  (固定)"
            }
            obj_memo.val(base_price_memo);
        }
    } else {
        // Inlineの場合
    }
}

// ＢＰ契約画面で「計算式」チェックボックスの選択により変更
function change_formula_display(obj, name_base, name_min, name_max, name_minus, name_plus) {
    if (obj.id == "id_is_show_formula") {
        price = parseFloat($("#id_" + name_base).val());
        min_hours = parseFloat($("#id_" + name_min).val());
        max_hours = parseFloat($("#id_" + name_max).val());
        plus_per_hour = parseFloat($("#id_" + name_plus).val());
        minus_per_hour = parseFloat($("#id_" + name_minus).val());

        // 残業手当メモ
        obj_memo_plus = $("#id_" + "allowance_overtime_memo");
        obj_is_show_formula = $("#id_" + "is_show_formula");
        is_show_formula = true;
        if (obj_memo_plus != null) {
            message = "超過単価：\\" + toNumComma(price) + "/" + max_hours + "h=\\" + toNumComma(plus_per_hour) + "/h"
            if (obj_is_show_formula && obj_is_show_formula.prop("checked") == false) {
                message = "超過単価：\\" + toNumComma(plus_per_hour) + "/h"
            }
            obj_memo_plus.val(message)
        }
        // 欠勤手当メモ
        obj_memo_minus = $("#id_" + "allowance_absenteeism_memo");
        if (obj_memo_minus != null) {
            message = "不足単価：\\" + toNumComma(price) + "/" + min_hours + "h=\\" + toNumComma(minus_per_hour) + "/h"
            if (obj_is_show_formula && obj_is_show_formula.prop("checked") == false) {
                message = "不足単価：\\" + toNumComma(minus_per_hour) + "/h"
            }
            obj_memo_minus.val(message)
        }
    } else {
        // Inlineの場合
    }
}

// 残業手当だけを変更時、残業手当メモも変えるように
function change_allowance_overtime(obj, name_base, name_max, name_plus_memo) {
    if (obj.id == "id_allowance_overtime") {
        price = parseFloat($("#id_" + name_base).val());
        max_hours = parseFloat($("#id_" + name_max).val());
        plus_per_hour = parseFloat($(obj).val());

        // 残業手当メモ
        obj_memo_plus = $("#id_" + name_plus_memo);
        obj_is_show_formula = $("#id_" + "is_show_formula");
        is_show_formula = true;
        if (obj_memo_plus != null) {
            message = "超過単価：\\" + toNumComma(price) + "/" + max_hours + "h=\\" + toNumComma(plus_per_hour) + "/h"
            if (obj_is_show_formula && obj_is_show_formula.prop("checked") == false) {
                message = "超過単価：\\" + toNumComma(plus_per_hour) + "/h"
            }
            obj_memo_plus.val(message)
        }
    } else {
        // Inlineの場合
    }
}

// 欠勤手当だけを変更時、欠勤手当メモも変えるように
function change_allowance_absenteeism(obj, name_base, name_min, name_minus_memo) {
    if (obj.id == "id_allowance_absenteeism") {
        price = parseFloat($("#id_" + name_base).val());
        min_hours = parseFloat($("#id_" + name_min).val());
        minus_per_hour = parseFloat($(obj).val());

        // 残業手当メモ
        obj_memo_minus = $("#id_" + name_minus_memo);
        obj_is_show_formula = $("#id_" + "is_show_formula");
        is_show_formula = true;
        if (obj_memo_minus != null) {
            message = "不足単価：\\" + toNumComma(price) + "/" + min_hours + "h=\\" + toNumComma(minus_per_hour) + "/h"
            if (obj_is_show_formula && obj_is_show_formula.prop("checked") == false) {
                message = "不足単価：\\" + toNumComma(minus_per_hour) + "/h"
            }
            obj_memo_minus.val(message)
        }
    } else {
        // Inlineの場合
    }
}

// 基準時間　下限変更時、基準時間メモも一緒に変更する。
function change_allowance_time_min(obj, name_max, name_memo) {
    if (obj.id == "id_allowance_time_min") {
        min_hours = parseFloat($(obj).val());
        max_hours = parseFloat($("#id_" + name_max).val());

        // 基準時間メモ
        obj_memo = $("#id_" + name_memo);
        if (obj_memo != null) {
            obj_memo.val("※基準時間：" + min_hours + "～" + max_hours + "/月")
        }
    }
}

// 基準時間　上限変更時、基準時間メモも一緒に変更する。
function change_allowance_time_max(obj, name_min, name_memo) {
    if (obj.id == "id_allowance_time_max") {
        max_hours = parseFloat($(obj).val());
        min_hours = parseFloat($("#id_" + name_min).val());

        // 基準時間メモ
        obj_memo = $("#id_" + name_memo);
        if (obj_memo != null) {
            obj_memo.val("※基準時間：" + min_hours + "～" + max_hours + "/月")
        }
    }
}

// 開始日を変更時、営業日数も変更する。
function change_start_date(obj, name_base, name_min, name_max, name_minus, name_plus, name_type, name_days) {
    if (obj.id == "id_start_date") {
        start_date = new Date($(obj).val());
        obj_days = $("#id_" + name_days);

        days = get_business_days(start_date.getFullYear(), start_date.getMonth() + 1);
        if (parseInt(obj_days.val()) != days.length) {
            obj_days.val(days.length);
            change_business_days(obj_days[0], name_base, name_min, name_max, name_minus, name_plus, name_type)
        }
    }
}

// 営業日数変更時、計算用時間下限も一緒に変更する。
function change_business_days(obj, name_base, name_min, name_max, name_minus, name_plus, name_type) {
    if (obj.id == "id_business_days") {
        calc_type = $("#id_" + name_type).val();
        days = parseInt($(obj).val());
        if (days <= 0) {
            return;
        }
        obj_min = $("#id_" + name_min);
        if (calc_type === '01') {
            // 固定１６０時間
            obj_min.val(160);
            calculate_minus_from_min_hour(obj_min[0], name_base, name_min, name_max, name_minus, name_plus);
        } else if (calc_type === "02") {
            // 営業日数 × ８
            obj_min.val(days * 8);
            calculate_minus_from_min_hour(obj_min[0], name_base, name_min, name_max, name_minus, name_plus);
        } else if (calc_type === "03") {
            // 営業日数 × ７．９
            obj_min.val(parseInt(days * 7.9));
            calculate_minus_from_min_hour(obj_min[0], name_base, name_min, name_max, name_minus, name_plus);
        }
    }
}

// 計算種類を変更時、営業日数も変更する。
function change_calculate_type(obj, name_base, name_min, name_max, name_minus, name_plus, name_type, name_days) {
    if (obj.id == "id_calculate_type") {
        obj_days = $("#id_" + name_days);

        if (obj_days.val() != "" && parseInt(obj_days.val()) > 0) {
            change_business_days(obj_days[0], name_base, name_min, name_max, name_minus, name_plus, name_type, name_days);
        }
    }
}
