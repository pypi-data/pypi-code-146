# -*- encoding:utf-8 -*-

class JType:
    @staticmethod
    def is_number(s):
        """判断是否是数字，包括浮点型"""
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    @staticmethod
    def is_equal(a, b):
        """判断两个数值是否相等，只支持数字和字符串"""
        print("> is_equal:", a, b)
        aa = str(a).strip() if JType.is_number(a) else a.strip()
        bb = str(b).strip() if JType.is_number(b) else b.strip()
        return aa == bb








