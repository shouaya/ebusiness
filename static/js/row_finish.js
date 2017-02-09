$(document).ready(function() {
    inputs = $("div.inline-group input.finished");

    for (var i=0; i<inputs.length; i++) {
        tr = $(inputs.get(i)).parent().parent();
        tr.addClass('finished');
    }
});
