(function ($) {
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
})(jQuery)