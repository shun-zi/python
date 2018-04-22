(function ($) {
        function edit(th) {
            //取出原有内容
            var td_label = $(th).parent()
            var hostname = td_label.next().text()
            var ip = td_label.next().next().text()
            var status = td_label.next().next().next().text()
            var hostname_label = "<input type='text' value='" + hostname + "'>"
            var ip_label = "<input type='text' value='" + ip + "'>"
            if (status=='下线'){
                var status_label = "<select><option>下线</option><option>在线</option></select>"

            }
            else{
                var status_label = "<select><option>在线</option><option>下线</option></select>"
            }
            td_label.next().empty().append(hostname_label).next().empty().append(ip_label).next().empty().
            append(status_label)
        }

        function cancel_edit(th) {
            //取出文本框的内容
            var hostname = $(th).parent().next().find('input').val()
            var ip = $(th).parent().next().next().find('input').val()
            var status = $(th).parent().next().next().next().find('select').val()
            if(hostname.length!=0 && ip.length!=0 && status.length!=0){
                $(th).parent().next().empty().text(hostname).next().empty().text(ip).
                    next().empty().text(status)
            }
        }



        //给全选键加上事件,定位到checkbox,循环使用prop
        $(":button[value='全选']").click(function () {
            $(':checkbox').prop('checked', true)
        })

        //给取消键加上事件,定位到checkbox,循环使用prop
        $(":button[value='取消']").click(function () {
            $(':checkbox').prop('checked', false)
        })

        //给反选键加上事件
        $(":button[value='反选']").click(function () {
            $(':checkbox').each(function () {
                //勾上的勾选框取消勾选,未勾选的勾选框勾上.
                if($(this).prop('checked') == true){
                    $(this).prop('checked', false)
                }
                else{
                    $(this).prop('checked', true)
                }
            })
        })

        //为进入编辑模式绑定click事件
        $(":button[value='编辑模式']").click(function () {
            //判断是否为编辑模式
            var edit_status = $(this).attr('edit_status')
            if (edit_status=='0'){
                //进入编辑模式
                $(this).attr('edit_status', '1')
                //寻找勾上的选项,然后将后面hostname,ip,状态栏全设为文本框,将原有的文本内容放到文本框中.
                $(":checkbox").each(function () {
                    var checked = $(this).prop('checked')
                        if (checked){
                            edit(this)
                        }
                })

                //给勾选框绑定click事件
                $("table :checkbox").click(function () {
                    //找到每个勾选框标签,判断'checked''是否为true
                    var checked = $(this).prop('checked')
                    if (checked){
                        // console.log(this)
                        edit(this)
                    }else{
                        cancel_edit(this)
                    }
                })

                //改变编辑键的背景色
                $(this).css('background-color', '#5F9EA0')
            }
            else{
                //退出编辑模式
                $(this).attr('edit_status', '0')
                $(":checkbox").each(function () {
                    var checked = $(this).prop('checked')
                    if (checked){
                        //取出文本框的内容
                        var hostname = $(this).parent().next().find('input').val()
                        var ip = $(this).parent().next().next().find('input').val()
                        var status = $(this).parent().next().next().next().find('select').val()
                        if(hostname.length!=0 && ip.length!=0 && status.length!=0){
                            $(this).parent().next().empty().text(hostname).next().empty().text(ip).
                                next().empty().text(status)
                        }
                    }

                })
                //改变编辑键的背景色
                $(this).css('background-color', 'aqua')
            }
        })

})(jQuery)