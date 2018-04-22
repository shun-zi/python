(function ($) {

            //给machine_groups转链接加上click事件
            $(".menu-table li[role='presentation'] a:eq(2)").click(function () {
                    $(".table .groups").removeClass('hide');
                    $(".table .host").addClass('hide');
                    $(".table .header").addClass('hide');
                });

            //给host转链接加上click事件
            $(".menu-table li[role='presentation'] a:eq(1)").click(function () {
                    $(".table .host").removeClass('hide');
                    $(".table .groups").addClass('hide');
                    $(".table .header").addClass('hide');
                });
            //给主机分组添加按钮绑定click事件
            $(".content .table .groups .add :button:eq(0)").click(function () {
                    $(".shadow").toggleClass('hide');
                    $(".addApplication-box").toggleClass('hide');
            });

            //给主机添加按钮绑定click事件
            $(".content .table .host .add :button:eq(0)").click(function () {
                    $(".shadow").toggleClass('hide');
                    $(".addHost-box").toggleClass('hide');
            });


            //给主机分组添加模态框中的取消键绑定click事件
            $(".addApplication-box :button[value='取消']").click(function () {
                $(".shadow").toggleClass('hide');
                $(".addApplication-box").toggleClass('hide');
            });

            //给主机添加模态框中的取消键绑定click事件
            $(".addHost-box :button[value='取消']").click(function () {
                $(".shadow").toggleClass('hide');
                $(".addHost-box").toggleClass('hide');
            });

            //给主机分组删除键绑定click事件
            $(".content .table .groups .add :button:eq(1)").click(function () {
                $(".shadow").toggleClass('hide');
                $(".deleteApplication-box").toggleClass('hide');
            });

            //给主机删除键绑定click事件
            $(".content .table .host .add :button:eq(1)").click(function () {
                $(".shadow").toggleClass('hide');
                $(".deleteHost-box").toggleClass('hide');
            });

            //给主机分组删除模态框中的取消键绑定click事件
            $(".deleteApplication-box :button[value='取消']").click(function () {
                $(".shadow").toggleClass('hide');
                $(".deleteApplication-box").toggleClass('hide');
            });

            //给主机删除模态框中的取消键绑定click事件
            $(".deleteHost-box :button[value='取消']").click(function () {
                $(".shadow").toggleClass('hide');
                $(".deleteHost-box").toggleClass('hide');
            });

            allow_groupEdit = 1;
            // 给主机分组edit添加click点击事件
            $(".menu-table .groups .edit").click(function () {
                if(allow_groupEdit==1){
                    //取出主机分组的id和名字内容
                    //var id_old_label = $(this).parent().siblings(".group_th:eq(0)");
                    var host_list = [];
                    var name_old_label = $(this).parent().siblings(".group_th:eq(0)");
                    var host_old_label = $(this).parent().siblings(".group_th:eq(1)")
                    var span_label = host_old_label.children();
                    for (var i=0;i<span_label.length;i++){
                        var hid = span_label.eq(i).attr("hid");
                        host_list.push(hid);
                    }
                    console.log(host_list)


                    var id = $(this).parent().parent().attr("aid");
                    var name = name_old_label.text();
                    var action_url = "/application/host/?operation=update&db=application&id=" + id
                    var new_form = "<form id='update_form' action='/application/host/?operation=update' method='post'></form>";
                    //var new_id = "<input type='text' name='id' disabled='disabled' value=" + id + ">";
                    var new_name = "<input type='text' name='name' required='true' value=" + name + ">";
                    var new_hosts = "<select name='host_id' multiple>{% for host in hosts %}<option value='{{ host.id }}'>{{ host.hostname }}</option>{% endfor %}</select>"

                    // 插入表单
                    $(this).parent().parent().parent().parent().wrap(new_form).parent().attr("action", action_url);
                    //$(this).parent().parent().parent().parent().parent().attr("action", action_url)


                    //清空标签
                    name_old_label.empty();
                    host_old_label.empty();

                    //插入标签
                    name_old_label.append(new_name);
                    host_old_label.append(new_hosts);
                    host_old_label.find("select").val(host_list);

                    allow_groupEdit = 0;
                }
                else{
                  alert("正在编辑数据");
                }

            });

            allow_machineEdit = 1;
            // 给主机edit添加click点击事件
            $(".menu-table .host .edit").click(function () {
                if(allow_machineEdit==1){
                    // 取出主机分组的id和名字内容
                    var hostname_old_label = $(this).parent().siblings(".group_th:eq(0)");
                    var ip_old_label = $(this).parent().siblings(".group_th:eq(1)");
                    var port_old_label = $(this).parent().siblings(".group_th:eq(2)");
                    // var power_old_label = $(this).parent().siblings(".group_th:eq(3)");
                    var businessId_old_label = $(this).parent().siblings(".group_th:eq(3)");

                    var id = $(this).parent().parent().attr("hid");
                    var hostname = hostname_old_label.text();
                    var ip = ip_old_label.text();
                    var port = port_old_label.text();
                    // var power = power_old_label.text();
                    var business_id = businessId_old_label.attr("bid");

                    var action_url = "/application/host/?operation=update&db=host&id=" + id
                    var new_form = "<form id='update_form' action='/application/host/?operation=update' method='post'></form>";
                    //var new_id = "<input type='text' name='id' style='width:120px' disabled='disabled' value=" + id + ">";
                    var new_hostname = "<input type='text' style='width:120px' name='hostname' required='true' value=" + hostname + ">";
                    var new_ip = "<input type='text' style='width:120px' name='ip' required='true' value=" + ip + ">";
                    var new_port = "<input type='text' style='width:120px' name='port' required='true' value=" + port + ">";
                    //var new_power = "<input type='text' style='width:120px' name='power' required='true' value=" + power + ">";
                    var new_business = "<select name='business_id'>{% for b in business %}<option value='{{ b.id }}'>{{ b.caption }}</option>{% endfor %}</select>"

                    // 插入表单
                    $(this).parent().parent().parent().parent().wrap(new_form).parent().attr("action", action_url);
                    //$(this).parent().parent().parent().parent().parent().attr("action", action_url)


                    //清空标签
                    //id_old_label.empty();
                    hostname_old_label.empty();
                    ip_old_label.empty();
                    port_old_label.empty();
                    //power_old_label.empty();
                    businessId_old_label.empty();

                    //插入标签
                    //id_old_label.append(new_id);
                    hostname_old_label.append(new_hostname);
                    ip_old_label.append(new_ip);
                    port_old_label.append(new_port);
                    //power_old_label.append(new_power);
                    businessId_old_label.append(new_business);
                    businessId_old_label.find("select").val(business_id)


                    allow_machineEdit = 0;
                }
                else{
                  alert("正在编辑数据");
                }

            });

            //给主机添加框中的提交加上click事件
            $(".addHost-box #ajax_submit").click(function () {
                $.ajax({
                    url: "/application/host/?operation=add&db=host",
                    type: 'POST',
                    //data: {'hostname': $('#host').val(), 'ip': $('#ip').val(), 'port': $('#port').val(), 'b_id': $('#sel').val()},
                    data: $('.addHost-box #add_form').serialize(),
                    success: function(data){
                        var obj = JSON.parse(data);
                        if(obj.status){
                            location.reload();
                        }
                    }
                })
            })

            //给主机删除框中的提交加上click事件
            $(".deleteHost-box #ajax_submit").click(function () {
                $.ajax({
                    url: "/application/host/?operation=delete&db=host",
                    type: 'POST',
                    //data: {'hostname': $('#host').val(), 'ip': $('#ip').val(), 'port': $('#port').val(), 'b_id': $('#sel').val()},
                    data: $('.deleteHost-box #delete_form').serialize(),
                    success: function(data){
                        var obj = JSON.parse(data);
                        if(obj.status){
                            location.reload();
                        }
                    }
                })
            })

            //给应用添加框中的提交加上click事件
            $(".addApplication-box #ajax_submit").click(function () {
                $.ajax({
                    url: "/application/host/?operation=add&db=application",
                    type: 'POST',
                    //data: {'hostname': $('#host').val(), 'ip': $('#ip').val(), 'port': $('#port').val(), 'b_id': $('#sel').val()},
                    data: $('.addApplication-box #add_form').serialize(),
                    success: function(data){
                        var obj = JSON.parse(data);
                        if(obj.status){
                            location.reload();
                        }
                    }
                })
            })

            //给应用删除框中的提交加上click事件
            $(".deleteApplication-box #ajax_submit").click(function () {
                $.ajax({
                    url: "/application/host/?operation=delete&db=application",
                    type: 'POST',
                    //data: {'hostname': $('#host').val(), 'ip': $('#ip').val(), 'port': $('#port').val(), 'b_id': $('#sel').val()},
                    data: $('.deleteApplication-box #delete_form').serialize(),
                    success: function(data){
                        var obj = JSON.parse(data);
                        if(obj.status){
                            location.reload();
                        }
                    }
                })
            })

            //给主机save键添加click事件
            $(".host .save").click(function () {
                $.ajax({
                    url: $(".host #update_form").attr("action"),
                    type: 'POST',
                    //data: {'hostname': $('#host').val(), 'ip': $('#ip').val(), 'port': $('#port').val(), 'b_id': $('#sel').val()},
                    data: $('.host #update_form').serialize(),
                    success: function(data){
                        var obj = JSON.parse(data);
                        if(obj.status){
                            location.reload();
                        }
                    }
                })
            })

            //给应用save键添加click事件
            $(".groups .save").click(function () {
                $.ajax({
                    url: $(".groups #update_form").attr("action"),
                    type: 'POST',
                    //data: {'hostname': $('#host').val(), 'ip': $('#ip').val(), 'port': $('#port').val(), 'b_id': $('#sel').val()},
                    data: $('.groups #update_form').serialize(),
                    success: function(data){
                        var obj = JSON.parse(data);
                        if(obj.status){
                            location.reload();
                        }
                    }
                })
            })

        })(jQuery)