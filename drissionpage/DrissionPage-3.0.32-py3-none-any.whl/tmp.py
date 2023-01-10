# -*- coding:utf-8 -*-
class ChromiumFrame1(object):
    """frame元素的类。
    frame既是元素，也是页面，可以获取元素属性和定位周边元素，也能跳转到网址。
    同域和异域的frame处理方式不一样，同域的当作元素看待，异域的当作页面看待。"""

    def __init__(self, page, ele):
        """
        :param page: frame所在页面对象
        :param ele: frame容器元素对象
        """
        self.page = page
        self.frame_ele = ele
        node = page.run_cdp('DOM.describeNode', nodeId=ele.node_id, not_change=True)['node']
        self.frame_id = node.get('frameId', None)

        if self._is_inner_frame():
            self._is_diff_domain = False
            self.frame_page = None
            # self.backend_id = node.get('contentDocument', None).get('backendNodeId', None)
            # obj_id = self.page.driver.DOM.resolveNode(backendNodeId=self.backend_id)['object']['objectId']
            self.cc = cc(page.address, page.tab_id, page.timeout, self.frame_id, self.page, self.frame_ele)
            self.cc._debug = True
            # self._doc_ele = ChromiumElement(page, obj_id=obj_id)
            self._doc_ele = self.cc.doc_ele

        else:  # 若frame_id不在frame_tree中，为异域frame
            self._is_diff_domain = True
            self._doc_ele = None
            self.frame_page = ChromiumBase(page.address, self.frame_id)
            self.frame_page.set_page_load_strategy(self.page.page_load_strategy)
            self.frame_page.timeouts = self.page.timeouts

    def __call__(self, loc_or_str, timeout=None):
        """在内部查找元素                                             \n
        例：ele2 = ele1('@id=ele_id')                               \n
        :param loc_or_str: 元素的定位信息，可以是loc元组，或查询字符串
        :param timeout: 超时时间
        :return: ChromiumElement对象或属性、文本
        """
        return self.ele(loc_or_str, timeout)

    def __repr__(self):
        attrs = self.frame_ele.attrs
        attrs = [f"{attr}='{attrs[attr]}'" for attr in attrs]
        return f'<ChromiumFrame {self.frame_ele.tag} {" ".join(attrs)}>'

    def _is_inner_frame(self):
        """返回当前frame是否同域"""
        return self.frame_id in str(self.page.run_cdp('Page.getFrameTree', not_change=True)['frameTree'])

    @property
    def tag(self):
        """返回元素tag"""
        return self.frame_ele.tag

    @property
    def url(self):
        """返回frame当前访问的url"""
        if self._is_diff_domain:
            return self.frame_page.url
        else:
            r = self.page.run_cdp('DOM.describeNode', nodeId=self.frame_ele.node_id)
            return r['node']['contentDocument']['documentURL']

    @property
    def html(self):
        """返回元素outerHTML文本"""
        if self._is_diff_domain:
            tag = self.tag
            out_html = self.page.run_cdp('DOM.getOuterHTML',
                                         nodeId=self.frame_ele.node_id, not_change=True)['outerHTML']
            in_html = self.frame_page.html
            sign = search(rf'<{tag}.*?>', out_html).group(0)
            return f'{sign}{in_html}</{tag}>'

        else:
            return self.frame_ele.html

    @property
    def title(self):
        """返回frame内网页title"""
        d = self.frame_page if self._is_diff_domain else self.frame_ele
        ele = d.ele('xpath://title')
        return ele.text if ele else None

    @property
    def cookies(self):
        """以dict格式返回cookies"""
        return self.frame_page.cookies if self._is_diff_domain else self.page.cookies

    @property
    def inner_html(self):
        """返回元素innerHTML文本"""
        return self.frame_page.html if self._is_diff_domain else self.frame_ele.inner_html

    @property
    def attrs(self):
        """返回frame元素所有attribute属性"""
        return self.frame_ele.attrs

    @property
    def frame_size(self):
        """返回frame内页面尺寸，格式：(长, 高)"""
        if self._is_diff_domain:
            return self.frame_page.size
        else:
            h = self.frame_ele.run_script('return this.contentDocument.body.scrollHeight;')
            w = self.frame_ele.run_script('return this.contentDocument.body.scrollWidth;')
            return w, h

    @property
    def size(self):
        """返回frame元素大小"""
        return self.frame_ele.size

    @property
    def obj_id(self):
        """返回frame元素的object id"""
        return self.frame_ele.obj_id

    @property
    def node_id(self):
        """返回cdp中的node id"""
        return self.frame_ele.node_id

    @property
    def backend_id(self):
        """返回cdp中的node id"""
        return self.frame_ele.backend_id

    @property
    def location(self):
        """返回frame元素左上角的绝对坐标"""
        return self.frame_ele.location

    @property
    def is_displayed(self):
        """返回frame元素是否显示"""
        return self.frame_ele.is_displayed

    @property
    def xpath(self):
        """返回frame的xpath绝对路径"""
        return self.frame_ele.xpath

    @property
    def css_path(self):
        """返回frame的css selector绝对路径"""
        return self.frame_ele.css_path

    def get(self, url, show_errmsg=False, retry=None, interval=None, timeout=None):
        """访问目标网页，url为同域名时只有url参数生效                 \n
        :param url: 目标url
        :param show_errmsg: 是否显示和抛出异常
        :param retry: 重试次数
        :param interval: 重试间隔（秒）
        :param timeout: 连接超时时间
        :return: 目标url是否可用
        """
        # todo: 处理同域名跳转到异域，及同域跳转到异域的情况
        if self._is_diff_domain:
            r = self.frame_page.get(url, show_errmsg, retry, interval, timeout)
        else:
            r = self.cc.get(url, show_errmsg, retry, interval, timeout)

            # self.frame_ele.run_script(f'this.contentWindow.location="{url}";')
        return r

    def refresh(self):
        """刷新frame页面"""
        if self._is_diff_domain:
            raise RuntimeError('refresh()仅支持同域frame。')
        else:
            try:
                self.frame_ele.run_script('this.contentWindow.location.reload();')
            except RuntimeError:
                return RuntimeError('非同源域名无法执行refresh()。')

    def forward(self, steps=1):
        """在浏览历史中前进若干步    \n
        :param steps: 前进步数
        :return: None
        """
        if self._is_diff_domain:
            raise RuntimeError('forward()仅支持同域frame。')
        else:
            try:
                self.frame_ele.run_script(f'this.contentWindow.history.go({steps});')
            except RuntimeError:
                return RuntimeError('非同源域名无法执行forward()。')

    def back(self, steps=1):
        """在浏览历史中后退若干步    \n
        :param steps: 后退步数
        :return: None
        """
        if self._is_diff_domain:
            raise RuntimeError('back()仅支持同域frame。')
        else:
            try:
                self.frame_ele.run_script(f'this.contentWindow.history.go({-steps});')
            except RuntimeError:
                return RuntimeError('非同源域名无法执行back()。')

    def ele(self, loc_or_str, timeout=None):
        """在frame内查找单个元素                         \n
        :param loc_or_str: 定位符或元素对象
        :param timeout: 查找超时时间
        :return: ChromiumElement对象
        """
        d = self.frame_page if self._is_diff_domain else self.cc.doc_ele
        return d.ele(loc_or_str, timeout)

    def eles(self, loc_or_str, timeout=None):
        """获取所有符合条件的元素对象                         \n
        :param loc_or_str: 定位符或元素对象
        :param timeout: 查找超时时间
        :return: ChromiumElement对象组成的列表
        """
        d = self.frame_page if self._is_diff_domain else self.cc.doc_ele
        return d.eles(loc_or_str, timeout)

    def s_ele(self, loc_or_str=None):
        """查找第一个符合条件的元素以SessionElement形式返回，处理复杂页面时效率很高       \n
        :param loc_or_str: 元素的定位信息，可以是loc元组，或查询字符串
        :return: SessionElement对象或属性、文本
        """
        if isinstance(loc_or_str, ChromiumElement):
            return make_session_ele(loc_or_str)
        else:
            return make_session_ele(self, loc_or_str)

    def s_eles(self, loc_or_str=None):
        """查找所有符合条件的元素以SessionElement列表形式返回                       \n
        :param loc_or_str: 元素的定位信息，可以是loc元组，或查询字符串
        :return: SessionElement对象组成的列表
        """
        return make_session_ele(self, loc_or_str, single=False)

    def attr(self, attr):
        """返回frame元素attribute属性值                           \n
        :param attr: 属性名
        :return: 属性值文本，没有该属性返回None
        """
        return self.frame_ele.attr(attr)

    def set_attr(self, attr, value):
        """设置frame元素attribute属性          \n
        :param attr: 属性名
        :param value: 属性值
        :return: None
        """
        self.frame_ele.set_attr(attr, value)

    def remove_attr(self, attr):
        """删除frame元素attribute属性          \n
        :param attr: 属性名
        :return: None
        """
        self.frame_ele.remove_attr(attr)

    def run_script(self, script, as_expr=False, *args):
        # todo:
        pass

    def parent(self, level_or_loc=1):
        """返回上面某一级父元素，可指定层数或用查询语法定位              \n
        :param level_or_loc: 第几级父元素，或定位符
        :return: 上级元素对象
        """
        return self.frame_ele.parent(level_or_loc)

    def prev(self, filter_loc='', index=1, timeout=0):
        """返回前面的一个兄弟元素，可用查询语法筛选，可指定返回筛选结果的第几个        \n
        :param filter_loc: 用于筛选元素的查询语法
        :param index: 前面第几个查询结果元素
        :param timeout: 查找元素的超时时间
        :return: 兄弟元素
        """
        return self.frame_ele.prev(filter_loc, index, timeout)

    def next(self, filter_loc='', index=1, timeout=0):
        """返回后面的一个兄弟元素，可用查询语法筛选，可指定返回筛选结果的第几个        \n
        :param filter_loc: 用于筛选元素的查询语法
        :param index: 后面第几个查询结果元素
        :param timeout: 查找元素的超时时间
        :return: 兄弟元素
        """
        return self.frame_ele.next(filter_loc, index, timeout)

    def before(self, filter_loc='', index=1, timeout=None):
        """返回当前元素前面的一个元素，可指定筛选条件和第几个。查找范围不限兄弟元素，而是整个DOM文档        \n
        :param filter_loc: 用于筛选元素的查询语法
        :param index: 前面第几个查询结果元素
        :param timeout: 查找元素的超时时间
        :return: 本元素前面的某个元素或节点
        """
        return self.frame_ele.before(filter_loc, index, timeout)

    def after(self, filter_loc='', index=1, timeout=None):
        """返回当前元素后面的一个元素，可指定筛选条件和第几个。查找范围不限兄弟元素，而是整个DOM文档        \n
        :param filter_loc: 用于筛选元素的查询语法
        :param index: 后面第几个查询结果元素
        :param timeout: 查找元素的超时时间
        :return: 本元素后面的某个元素或节点
        """
        return self.frame_ele.after(filter_loc, index, timeout)

    def prevs(self, filter_loc='', timeout=0):
        """返回前面全部兄弟元素或节点组成的列表，可用查询语法筛选        \n
        :param filter_loc: 用于筛选元素的查询语法
        :param timeout: 查找元素的超时时间
        :return: 兄弟元素或节点文本组成的列表
        """
        return self.frame_ele.prevs(filter_loc, timeout)

    def nexts(self, filter_loc='', timeout=0):
        """返回后面全部兄弟元素或节点组成的列表，可用查询语法筛选        \n
        :param filter_loc: 用于筛选元素的查询语法
        :param timeout: 查找元素的超时时间
        :return: 兄弟元素或节点文本组成的列表
        """
        return self.frame_ele.nexts(filter_loc, timeout)

    def befores(self, filter_loc='', timeout=None):
        """返回当前元素后面符合条件的全部兄弟元素或节点组成的列表，可用查询语法筛选。查找范围不限兄弟元素，而是整个DOM文档        \n
        :param filter_loc: 用于筛选元素的查询语法
        :param timeout: 查找元素的超时时间
        :return: 本元素前面的元素或节点组成的列表
        """
        return self.frame_ele.befores(filter_loc, timeout)