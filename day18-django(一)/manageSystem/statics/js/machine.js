(function ($) {
    //给菜单标签绑定click事件
    $('.menu-item').click(function () {
        //给点击到菜单标签改变背景颜色,其他菜单背景颜色隐藏
        $('.menu-item').css('background-color', '');
        $(this).css('background-color', 'green');

        //只显示相应菜单的内容
        var content_id = $(this).attr('content');
        $(".content-item").addClass('hide');
        $(".content-item[menu=" + content_id + "]").removeClass('hide');
    })

     //当鼠标移动到查看详情时,改变字体颜色
     $(".content .information tbody tr td:last-child").each(function () {
         $(this).mouseover(function () {
             $(this).css('color', 'blue');
         })
         $(this).mouseleave(function () {
             $(this).css('color', 'black');
         })
    })

    //给添加按钮绑定click事件
    $(".opreation :button[value='添加']").click(function () {
    $(".shadow").toggleClass('hide')
    $(".dialog").toggleClass('hide')
    })

    //给取消键绑定click事件
    $(".dialog :button[value='取消']").click(function () {
        $(".shadow").toggleClass('hide')
        $(".dialog").toggleClass('hide')
    })

    //给删除键绑定click事件
    $(".opreation :button[value='删除']").click(function () {
    $(".shadow").toggleClass('hide')
    $(".dialog1").toggleClass('hide')
    })
}(jQuery))
