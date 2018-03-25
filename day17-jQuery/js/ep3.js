(function ($) {
    //菜单隐藏
    $("div[class='title']").click(function () {
        $("div[class='title']").next().addClass('hide')
        $(this).next().removeClass('hide')
    })
})(jQuery)