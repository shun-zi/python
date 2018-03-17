
function changeMenu(nid){
            var current_label = document.getElementsByClassName(nid)[0]
            var items_list = current_label.parentElement.parentElement.children;
            for (var i=0;i < items_list.length;i++){
                    var item = items_list[i].children[1];
                    item.classList.add('hide');
                    }
            current_label.nextElementSibling.classList.remove('hide');
            }