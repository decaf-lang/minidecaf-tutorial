$("body").on("click", ".click_reveal > span",function() {
    $(this).parent().children("div").show();
    $(this).remove();
});