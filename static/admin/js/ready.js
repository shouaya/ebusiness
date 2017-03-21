$(document).ready(function() {
    setFinishedProjectMemberStyle();
    setPlanningProjectMemberStyle();
});

// 案件編集画面で作業終了したメンバーの表示スタイル
function setFinishedProjectMemberStyle() {
    inputs = $("div.inline-group input.finished");

    for (var i=0; i<inputs.length; i++) {
        tr = $(inputs.get(i)).parent().parent();
        tr.addClass('finished');
    }
}

// 案件編集画面で提案中のメンバーの表示スタイル
function setPlanningProjectMemberStyle() {
    inputs = $("div.inline-group select.planning");

    for (var i=0; i<inputs.length; i++) {
        tr = $(inputs.get(i)).parent().parent();
        tr.addClass('planning');
    }
}