class Page(object):
    def __init__(self, show_pages):
        self.start_page = None
        self.end_page = None
        self.show_pages = show_pages

    def divide_page(self, counts, one_page_counts):
        # 计算总页数
        page_counts = int(counts / one_page_counts)
        remainder = counts % one_page_counts
        if remainder > 0:
            page_counts += 1
        return page_counts

    def start_and_end_page(self, select_page, half_show_pages, page_counts):
        # 页面显示的开始页数
        if (select_page-half_show_pages) < 1:
            self.start_page = 1
            self.end_page = self.start_page + self.show_pages - 1
        else:
            self.start_page = select_page - half_show_pages

            if (select_page + half_show_pages) > page_counts:
                self.end_page = page_counts
            else:
                self.end_page = select_page + half_show_pages

    def show_hosts(self, select_page, one_page_counts, counts, objs):
        # 选定页数要显示的主机信息
        start_index = (select_page-1) * one_page_counts
        if (start_index + one_page_counts) > (counts-1):
            end_index = counts
        else:
            end_index = start_index + one_page_counts
        return objs[start_index:end_index]
