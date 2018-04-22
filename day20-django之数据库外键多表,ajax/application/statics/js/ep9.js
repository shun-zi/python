(function ($) {
    //给菜单标签绑定click事件
    $('.menu-item').click(function () {
        //给点击到菜单标签改变背景颜色,其他菜单背景颜色隐藏
        $('.menu-item').css('background-color', '')
        $(this).css('background-color', 'red')

        //只显示相应菜单的内容
        var content_id = $(this).attr('content')
        $(".content-item").addClass('hide')
        $(".content-item[menu="+ content_id +"]").removeClass('hide')
    })
}(jQuery))