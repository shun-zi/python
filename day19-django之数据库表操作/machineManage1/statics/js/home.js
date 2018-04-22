(function ($) {

    //给machine_groups转链接加上click事件
    $(".menu-table li[role='presentation'] a:eq(2)").click(function () {
            $(".table .groups").removeClass('hide');
            $(".table .machines").addClass('hide');
            $(".table .header").addClass('hide');
        })

    //给machines转链接加上click事件
    $(".menu-table li[role='presentation'] a:eq(1)").click(function () {
            $(".table .machines").removeClass('hide');
            $(".table .groups").addClass('hide');
            $(".table .header").addClass('hide');
        })

    //给添加按钮绑定click事件
    $(".content .table .groups .add :button").click(function () {
        $(".shadow").toggleClass('hide');
        $(".add-box").toggleClass('hide');
    })


    //给取消键绑定click事件
    $(".add-box :button[value='取消']").click(function () {
        $(".shadow").toggleClass('hide');
        $(".add-box").toggleClass('hide');
    })

    //给删除键绑定click事件
    $(".content .table .groups .add :button:eq(1)").click(function () {
        $(".shadow").toggleClass('hide');
        $(".dialog1").toggleClass('hide');
    })

    allow_edit = 1;
    // 给edit添加click点击事件
    $(".menu-table .groups .edit").click(function (even) {
        if(allow_edit==1){
            //取出主机分组的id和名字内容
        var id_old_label = $(this).parent().siblings(".group_th:eq(0)");
        var name_old_label = $(this).parent().siblings(".group_th:eq(1)");
        var id = id_old_label.text();
        var name = name_old_label.text();
        var new_id = "<form><input type='text' name='id' disabled='disabled' required='true' value=" + id + "></form>"
        var new_name = "<form><input type='text' name='name' required='true' value=" + name + "></form>"

        //清空标签
        id_old_label.empty();
        name_old_label.empty();

        //插入标签
        id_old_label.append(new_id);
        name_old_label.append(new_name);
        allow_edit = 0;
        }
        else{
          alert("正在编辑数据")
        }

    })
})(jQuery)