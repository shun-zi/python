(function ($) {
    //给添加键绑定click事件
    $(":button[value='添加']").click(function () {
        //将文本框的内容添加到列表末尾
        var content = $(":text").val()
        if(content.length==0)
        {
            alert("The text isn't None")
        }
        else{
            $("ul li:last").after("<li>" + content + "</li>")
        }
    })
    //给删除键绑定click事件
    $(":button[value='删除']").click(function () {
        // 根据文本框的value值去匹配列表,将相应的标签移除.
        var content = $(":text").val()
        if(content.length==0)
        {
            alert("The text isn't None")
        }
        else{
            $("li:contains(" + content + ")").remove()
        }
    })
    //给复制键绑定click事件
    $(":button[value='复制']").click(function () {
        // 根据文本框的value值去匹配列表,将相应的标签移除.
        var content = $(":text").val()
        if(content.length==0)
        {
            alert("The text isn't None")
        }
        else{
            $("li:contains(" + content + ")").clone().insertAfter('li:last')
        }
    })
})(jQuery)