$(function () {
  $("input[type=checkbox]").click(function() {
    var checked_length = $("input[type=checkbox]:checked").length;

    // 選択上限は3つまで
    if (checked_length >= 3) {
      $("input[type=checkbox]:not(:checked)").prop("disabled", true);
    } else {
      $("input[type=checkbox]:not(:checked)").prop("disabled", false);
    }
  });
});