import os
from py_book_util import util
import json


class ImageRecognizer(object):
    def __init__(
        self,
        img_name,
        crop_img_top,
        crop_img_bottom,
        crop_img_left,
        crop_img_right,
        cur_img_file,
        dst_img_dir,
        flag_force=False,
        ratio="2.0",
        flag_autocrop=True,
        app_name="img2txt",
    ):
        self.img_name = img_name
        self.top = crop_img_top
        self.bottom = crop_img_bottom
        self.left = crop_img_left
        self.right = crop_img_right
        self.cur_img_file = cur_img_file
        self.dst_img_dir = dst_img_dir
        self.ratio = ratio
        self.flag_force = flag_force
        self.flag_autocrop = flag_autocrop
        self.app_name = app_name
        self.prepare_img()

    def get_dst_img_file(self):
        return self.dst_img_dir + os.path.sep + self.img_name

    def get_dst_img_file_json(self):
        return "%s.json" % self.get_dst_img_file()

    def checking_json_data(self):
        dst_img_file_json = self.get_dst_img_file_json()
        if os.path.isfile(dst_img_file_json):
            data = json.load(open(dst_img_file_json, "r", encoding="utf-8"))
            if ((data.__contains__("recognize_text") == False) or
                (len(data["recognize_text"])<=0) or
                (data.__contains__("app_name") == False) or
                (data["app_name"] != self.app_name) or
                (data.__contains__("flag_autocrop") == False) or
                (data["flag_autocrop"] != self.flag_autocrop) or
                (data.__contains__("ratio") == False) or
                (data["ratio"] != self.ratio) or
                (data.__contains__("crop_img_top") == False) or
                (data["crop_img_top"] != self.top) or
                (data.__contains__("crop_img_bottom") == False) or
                (data["crop_img_bottom"] != self.bottom) or
                (data.__contains__("crop_img_left") == False) or
                (data["crop_img_left"] != self.left) or
                (data.__contains__("crop_img_right") == False) or
                (data["crop_img_right"] != self.right)):
                os.remove(dst_img_file_json)
                return False
            else:
                return True
        else:
            return False

    def prepare_img(self):
        dst_img_file = self.get_dst_img_file()
        if self.flag_force:
            if os.path.isfile(dst_img_file):
                os.remove(dst_img_file)
        else:
            if os.path.isfile(dst_img_file):
                if self.checking_json_data() == False:
                    os.remove(dst_img_file)
        if os.path.isfile(dst_img_file) == False:
            # cargo install menyoki
            util.print_run_cmd(
                "menyoki edit %s --grayscale --crop %d:%d:%d:%d save %s"
                % (
                    self.cur_img_file,
                    self.top,
                    self.right,
                    self.bottom,
                    self.left,
                    dst_img_file,
                )
            )
            # util.print_run_cmd("menyoki edit %s --ratio 4.0 --filter gaussian save %s" % (dst_img_file, dst_img_file))
            if self.ratio != 1:
                util.print_run_cmd(
                    "menyoki edit %s --ratio %s --filter gaussian save %s"
                    % (dst_img_file, self.ratio, dst_img_file)
                )
            # cargo install auto-image-cropper
            if self.flag_autocrop:
                util.print_run_cmd(
                    "autocrop -i %s -o %s" % (dst_img_file, dst_img_file)
                )
        return dst_img_file

    def recognize_text(self, app_name="img2txt"):
        self.app_name = app_name
        dst_img_file_json = self.get_dst_img_file_json()
        # print(dst_img_file_json)
        if self.flag_force:
            if os.path.isfile(dst_img_file_json):
                os.remove(dst_img_file_json)
        else:
            self.checking_json_data()
        if os.path.isfile(dst_img_file_json) == False:
            # util.run_deno_cmd("js_book_util img2txt %s" % dst_img_file)
            # util.run_deno_cmd("js_book_util easyocr2txt %s" % dst_img_file)
            util.run_deno_cmd(
                "js_book_util %s %s" % (app_name, self.get_dst_img_file())
            )
            data = json.load(open(dst_img_file_json, "r", encoding="utf-8"))
            print(data["recognize_text"])
            data["crop_img_top"] = self.top
            data["crop_img_bottom"] = self.bottom
            data["crop_img_left"] = self.left
            data["crop_img_right"] = self.right
            data["flag_autocrop"] = self.flag_autocrop
            data["ratio"] = self.ratio
            data["app_name"] = app_name
            with (open(dst_img_file_json, "w") as fp):
                json.dump(data, fp)
        else:
            data = json.load(open(dst_img_file_json, "r", encoding="utf-8"))
        return data
