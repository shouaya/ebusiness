function set_allowance_overtime_memo(id_time_max, id_allowance, id_comment) {
    time_max = $("#" + id_time_max).val();
    allowance = $("#" + id_allowance).val();
    obj_comment = $("#" + id_comment);

    comment = "＠" + numberWithCommas(allowance) + "円/時間（" + time_max + "H以上支給とする）";
    obj_comment.val(comment)
}

function set_allowance_absenteeism_memo(id_time_max, id_allowance, id_comment) {
    time_max = $("#" + id_time_max).val();
    allowance = $("#" + id_allowance).val();
    obj_comment = $("#" + id_comment);

    comment = "＠" + numberWithCommas(allowance) + "円/時間（" + time_max + "H未満の場合）";
    obj_comment.val(comment)
}

function numberWithCommas(x) {
    if (x == '') {
        return 0
    } else {
        x = parseInt(x);
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
}

function gen_api_id(url) {
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.post(url, function(){
    }).done(function(data){
        location.reload();
    }).fail(function(data){
        alert('error!')
    })
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}