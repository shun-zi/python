(function ($) {
    //给添加按钮绑定click事件
    $(":button[value='添加']").click(function () {
    $(".shadow").toggleClass('hide')
    $(".dialog").toggleClass('hide')
    })

    //给取消键绑定click事件
    $(".dialog :button[value='取消']").click(function () {
        $(".shadow").toggleClass('hide')
        $(".dialog").toggleClass('hide')
    })

    //给对话框的确定键绑定click事件
    $(".dialog :button[value='确定']").click(function () {
        //获取文本框的位置
        var ip = $(".dialog input[name='hostname']").val()
        var port = $(".dialog input[name='port']").val()
        if (ip.length==0 || port.length==0 ){
            alert("text isn't None!")
        }
        else{
            var table = $("table").append("<tr></tr>")
            $("table tr:last").append("<td>" + ip + "</td><td>" + port + "</td>")
            $(".shadow").addClass('hide')
            $(".dialog").addClass('hide')
        }
    })
})(jQuery)