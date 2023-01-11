from py_book_util import util
from py_book_util.image_recognizer import ImageRecognizer
import os
import json
from myst_nb import glue
from PIL import Image

class PageRecognizer(object):
    def __init__(
        self, cur_pages_dir, cur_page_idx, cur_page_width=2561, cur_page_height=1206
    ):
        self.page_width = cur_page_width
        self.page_height = cur_page_height
        self.pages_dir = cur_pages_dir
        self.page_idx = cur_page_idx
        self.page_elements = {}
        dst_img_dir = self.dst_img_dir()
        if os.path.isdir(dst_img_dir) == False:
            os.mkdir(dst_img_dir)
        if os.path.exists(self.cur_img_file()):
            img = Image.open(self.cur_img_file())
            self.page_width = img.width
            self.page_height = img.height

    def cur_img_file(self):
        return "%s/%s.png" % (self.pages_dir, self.page_idx)

    def dst_img_dir(self):
        return "%s/%s" % (self.pages_dir, self.page_idx)

    def recognize_rect_w_h(
        self,
        cur_key_word,
        crop_img_left,
        crop_img_top,
        crop_img_width,
        crop_img_height,
        post_replace={},
        flag_force=False,
        ratio=2,
        flag_autocrop=True,
        app_name="img2txt",
    ):
        crop_img_bottom = self.page_height - crop_img_top - crop_img_height;
        crop_img_right = self.page_width - crop_img_left - crop_img_width;
        return self.recognize_rect_impl(cur_key_word, crop_img_top, crop_img_bottom, crop_img_left, crop_img_right, post_replace, flag_force, ratio, flag_autocrop, app_name)

    def recognize_rect(
        self,
        cur_key_word,
        crop_img_top,
        crop_img_bottom,
        crop_img_left,
        crop_img_right,
        post_replace={},
        flag_force=False,
        ratio=2,
        flag_autocrop=True,
        app_name="img2txt",
    ):
        crop_img_width = self.page_width - crop_img_left - crop_img_right
        crop_img_height = self.page_height - crop_img_top - crop_img_bottom
        if (app_name == "img2txt"):
            if flag_autocrop:
                if ratio == 2:
                    if flag_force == False:
                        print("Deprecidated please use recognize_rect_w_h(cur_key_word, %d, %d, %d, %d, %s)" %(crop_img_left, crop_img_top, crop_img_width , crop_img_height, post_replace));
                    else:
                        print("Deprecidated please use recognize_rect_w_h(cur_key_word, %d, %d, %d, %d, %s, %s)" %(crop_img_left, crop_img_top, crop_img_width , crop_img_height, post_replace, flag_force));
                else:
                    print("Deprecidated please use recognize_rect_w_h(cur_key_word, %d, %d, %d, %d, %s, %s, %d)" %(crop_img_left, crop_img_top, crop_img_width , crop_img_height, post_replace, flag_force, ratio));
            else:
                print("Deprecidated please use recognize_rect_w_h(cur_key_word, %d, %d, %d, %d, %s, %s, %d, %s)" %(crop_img_left, crop_img_top, crop_img_width , crop_img_height, post_replace, flag_force, ratio, flag_autocrop));
        else:
            print("Deprecidated please use recognize_rect_w_h(cur_key_word, %d, %d, %d, %d, %s, %s, %d, %s, '%s')" %(crop_img_left, crop_img_top, crop_img_width, crop_img_height, post_replace, flag_force, ratio, flag_autocrop, app_name));
        return self.recognize_rect_impl(cur_key_word, crop_img_top, crop_img_bottom, crop_img_left, crop_img_right, post_replace, flag_force, ratio, flag_autocrop, app_name)

    def recognize_rect_impl(
        self,
        cur_key_word,
        crop_img_top,
        crop_img_bottom,
        crop_img_left,
        crop_img_right,
        post_replace={},
        flag_force=False,
        ratio="2.0",
        flag_autocrop=True,
        app_name="img2txt",
    ):
        cur_rec = ImageRecognizer(
            "%s.png" % cur_key_word,
            crop_img_top,
            crop_img_bottom,
            crop_img_left,
            crop_img_right,
            self.cur_img_file(),
            self.dst_img_dir(),
            flag_force,
            ratio,
            flag_autocrop,
            app_name,
        )
        cur_rec_data = cur_rec.recognize_text(app_name)
        for single_replace_key in post_replace:
            cur_rec_data["recognize_text"] = cur_rec_data["recognize_text"].replace(
                single_replace_key, post_replace[single_replace_key]
            )  # ("\u2014", "-")
        glue(cur_key_word, cur_rec_data["recognize_text"])
        self.page_elements[cur_key_word] = cur_rec_data
        return cur_rec

    def generate_html_js(self, element_height={}, page_ratio_10x = 0):
        self.generate_js(element_height, page_ratio_10x)
        self.generate_html()

    def get_10x_page_ratio(self):
        return self.page_width * 10 / 1280

    def generate_js(self, element_height={}, page_ratio_10x = 0):
        file_name_page_js = "%s.js" % self.cur_img_file()
        if os.path.isfile(file_name_page_js):
            os.remove(file_name_page_js)
        cur_page_elements_js = ""
        cur_page_ratio = page_ratio_10x
        if (cur_page_ratio == 0):
            cur_page_ratio = self.get_10x_page_ratio()
        cur_page_element_top = 0
        cur_page_element_height = 0
        cur_page_element_idx = 0
        for single_element in self.page_elements:
            cur_page_element_idx = cur_page_element_idx + 1
            cur_page_element_top = cur_page_element_top + cur_page_element_height + 10
            cur_page_element_height = 60
            if single_element in element_height:
                cur_page_element_height = element_height[single_element]
            single_data = self.page_elements[single_element]
            print(single_element)
            print(single_data)
            cur_page_elements_js = (
                cur_page_elements_js
                + """
image_note.add(new DoneElement(%d * 10 / %d, %d * 10 / %d, %d * 10 / %d, %d * 10 / %d, "%s<br/>%s"));
"""
                % (
                    single_data["crop_img_left"],
                    cur_page_ratio,
                    single_data["crop_img_top"],
                    cur_page_ratio,
                    self.page_width
                    - single_data["crop_img_right"]
                    - single_data["crop_img_left"],
                    cur_page_ratio,
                    self.page_height
                    - single_data["crop_img_bottom"]
                    - single_data["crop_img_top"],
                    cur_page_ratio,
                    single_element,
                    single_data["recognize_text"],
                )
            )
            cur_page_elements_js = (
                cur_page_elements_js
                + """
image_note.add(new CommentElement(1300, 30+%d, 250, 44+%d, "Note_%s_%03d:<br/> - %s<br/> - %s"));
"""
                % (
                    cur_page_element_top,
                    cur_page_element_height - 44,
                    self.page_idx,
                    cur_page_element_idx,
                    single_element,
                    single_data["recognize_text"],
                )
            )
        file_content_page_js = """
var currentScript = $('script').last();

$(document).ready(function () {
	var image_file = "%s.png";
  var image_index = "000000";
  var image_note = new ImageNote(image_index, image_file, 0, 0);
  // <div style="width:730px; height:420px; position:absolute; left: 215px; top: 10px; color:#FFF; background:#0E0;filter:alpha(opacity=30); opacity:0.3; -moz-opacity=0.3; z-index:1;" id="Done_000000_001">&nbsp;</div>
  // <div style="width:250px; height:44px; position:absolute; left: 980px; top: 30px; color:#FFF; background:#0C3;filter:alpha(opacity=50); opacity:0.6; -moz-opacity=0.6; z-index:1;" id="Note_000000_001">Note_000000_001:<br/>Author is Carrieri, Enrico D</div>
  
  %s  

  image_note.create();
});
""" % (
            self.page_idx,
            cur_page_elements_js,
        )
        util.create_text_file(file_name_page_js, file_content_page_js)
        # util.display_code(file_name_page_js)
        # print("http://localhost:4507/xxx_dev_blog/%s/%s.png.html" % (self.pages_dir, self.page_idx))

    def generate_html(self):
        file_name_page_html = "%s.html" % self.cur_img_file()
        if os.path.isfile(file_name_page_html):
            os.remove(file_name_page_html)
        file_content_page_html = """<html>
  <head>
    <title>%s</title>
    <script src="../../static/note_common.js"></script>
    <script src="../../static/jquery-3.6.1.min.js"></script>
  </head>
  <body>
    <div style="width:1280px;">
      <div>
        <img width="1280" class="image_notes" src="%s.png"></img>
        <script src="%s.png.js"></script>
      </div>
    </div>
  </body>
</html>
""" % (
            self.page_idx,
            self.page_idx,
            self.page_idx,
        )
        util.create_text_file(file_name_page_html, file_content_page_html)
        # util.display_code(file_name_page_html)
        # print("http://localhost:4507/xxx_dev_blog/%s/%s.png.html" % (self.pages_dir, self.page_idx))
