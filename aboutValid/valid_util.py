# _ coding:utf-8 _*_

"""
本模块，提供参数校验，检查不符合条件请求参数
格式如下：
adb = {
    "id": {"type": int, "notnull": False, "format": {">": 0, "<": 255, "in": [1, 2, 3, 4]}},
    "name": {"type": basestring, "notnull": False, "format": {">": 2, "<": 255, "re.match":"[a-z]"}},
    "desc": {"type": datetime.datetime},
    "status": {"type": bool},
    "ss": {"type": list, "notnull": True, "format": {"size":{">": 2, "<": 255}, "lenth":{">": 2, "<": 255},"in":[], "re.match":"[a-z]"}},
    "ggg": {"type": dict},
    "cv": {"type": "ip"},
    "xcss": {"type": "email"}
}
type字段为必须定义
format 定义简单的数值大小及字段长度的检查，in表示只允许固定的一些值，为列表类型
notnull 代表是否不为null， True表示不为None

注：数据库自增型字段不要定义，或自动生成的字段不要定义

:return 处理后的字段，如有不符合条件的字段，则会抛出ValidationError异常
"""

import re
import datetime
from aboutValid.exceptions import ValidationError


args_type = {
    "int": "整数",
    "float": "浮点数",
    "list": "列表",
    "dict": "json类型",
    "basestring": "字符串类型",
    "str": "字符串类型",
    "unicode": "字符串类型",
    "bool": "布尔值",
    "datetime.datetime": "时间类型",
    "long": "长整型"
}


def _type_to_utf8(type):
    for ixe in args_type.keys():
        if type == eval(ixe):
            return args_type.get(ixe)


def str_to_time(date_str):
    if ":" in date_str:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    else:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')


def check_email_address(email_address):
    if re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email_address):
        return True
    else:
        return False


def check_params_with_model(dictstr, model, keep_extra_key=False, necessary=True):
    """
    注：参数中的两个字段required， notnull。
    如果有required， 并且值为True, 则是必传参数
    如果有notnull， 并且值为True，则传入的参数不能为空
    :param dictstr:
    :param model:
    :param necessary:
    :return:
    """
    if not isinstance(dictstr, dict):
        raise ValidationError("data不为json类型")
    if not isinstance(model, dict):
        raise ValidationError("model不为字典类型")
    if not dictstr or not model:
        return dictstr

    if necessary:
        for ixc in model.keys():
            if model.get(ixc).get("required"):
                if ixc not in dictstr.keys():
                    raise ValidationError("缺少必填参数: %s" % ixc)

    for ixc in model.keys():
        if model.get(ixc).get("notnull"):
            # 如果这个字段传入，但是值为None，则抛出异常，如果不传，则不处理
            if ixc in dictstr.keys():
                if dictstr.get(ixc) is None:
                    raise ValidationError("参数不能为空: %s" % ixc)

    _dict = {}
    for key in dictstr.keys():
        v = v_vv(key, dictstr.get(key), model)
        if v == "not__exist__in__model":
            if keep_extra_key is False:
                pass
            else:
                _dict[key] = dictstr.get(key)
            continue
        if v is None:
            continue
        _dict[key] = v
    return _dict


def v_vv(key, value, model):

    if key not in model.keys():
        # 允许传多参数
        model.pop(key, None)
        # 这里返回一个标记，用于说明当前的参数不在model中
        return "not__exist__in__model"

    format_type = model.get(key).get("type")

    if format_type == datetime.datetime:
        if isinstance(value, str):
            if "/" in value:
                value = value.replace("/", "-")
            value = str_to_time(value)

    if format_type == int:
        if value is None:
            return value
        else:
            if not isinstance(value, int):
                raise ValidationError("%s 不是整数" % (key))

    if format_type == float:
        if value is None:
            return value
        else:
            if isinstance(value, int):
                # 如果是浮点数类型，如果value是整数，value转化为浮点数
                value = float(value)
            elif isinstance(value, float):
                pass
            else:
                raise ValidationError("%s 不是浮点数" % (key))

    if format_type == str:
        if value is None:
            return value
        else:
            if not isinstance(value, str):
                raise ValidationError("%s 不是字符串类型" % (key))

    if format_type == dict:
        if value is None:
            return value
        else:
            if not isinstance(value, dict):
                raise ValidationError("%s 不是字典类型" % (key))

    if format_type == list:
        if value is None:
            return value
        else:
            if not isinstance(value, list):
                raise ValidationError("%s 不是列表类型" % (key))

    if format_type == "email":
        res = check_email_address(value)
        if res:
            return value
        else:
            raise ValidationError("%s 不是合法的email地址" % (value))

    if isinstance(value, format_type):
        format_data = model.get(key).get("format", {})
        if format_data:
            if format_type == int:
                if format_data.get(">") is not None:
                    if not value > format_data.get(">"):
                        raise ValidationError(
                            "%s 非法值： %s, 参数值必须大于 %s" % (key, value, format_data.get(">")))
                if "<" in format_data:
                    if not value < format_data.get("<"):
                        raise ValidationError(
                            "%s 非法值： %s, 参数值必须小于 %s" % (key, value, format_data.get("<")))
                if ">=" in format_data:
                    if not value >= format_data.get(">="):
                        raise ValidationError("%s 非法值: %s，参数值必须大于等于%s" % (key, value, format_data.get(">=")))
                if "<=" in format_data:
                    if not value <= format_data.get("<="):
                        raise ValidationError("%s 非法值: %s，参数值必须小于等于%s" % (key, value, format_data.get("<=")))
                if "in" in format_data:
                    if value not in format_data.get("in"):
                        raise ValidationError("%s 非法值： %s, 允许的参数值为：%s" % (key, value, format_data.get("in")))
            if format_type == float:
                if format_data.get(">") is not None:
                    if not value > format_data.get(">"):
                        raise ValidationError(
                            "%s 非法值： %s, 参数值必须大于 %s" % (key, value, format_data.get(">")))
                if "<" in format_data:
                    if not value < format_data.get("<"):
                        raise ValidationError(
                            "%s 非法值： %s, 参数值必须小于 %s" % (key, value, format_data.get("<")))
                if ">=" in format_data:
                    if not value >= format_data.get(">="):
                        raise ValidationError("%s 非法值: %s，参数值必须大于等于%s" % (key, value, format_data.get(">=")))
                if "<=" in format_data:
                    if not value <= format_data.get("<="):
                        raise ValidationError("%s 非法值: %s，参数值必须小于等于%s" % (key, value, format_data.get("<=")))
                if "in" in format_data:
                    if value not in format_data.get("in"):
                        raise ValidationError("%s 非法值： %s, 允许的参数值为：%s" % (key, value, format_data.get("in")))
            if format_type == str:
                if format_data.get(">") is not None:
                    if not len(value) > format_data.get(">"):
                        raise ValidationError("%s 非法值： %s, 参数长度必须大于 %s" % (
                            key, len(value), format_data.get(">")))
                if "<" in format_data:
                    if not len(value) < format_data.get("<"):
                        raise ValidationError("%s 非法值： %s, 参数长度必须小于 %s" % (
                            key, len(value), format_data.get("<")))
                if format_data.get(">=") is not None:
                    if not len(value) >= format_data.get(">="):
                        raise ValidationError("%s 非法值： %s, 参数长度必须大于等于 %s" % (
                            key, len(value), format_data.get(">=")))
                if format_data.get("<=") is not None:
                    if not len(value) <= format_data.get("<="):
                        raise ValidationError("%s 非法值： %s, 参数长度必须小于等于 %s" % (
                            key, len(value), format_data.get("<=")))
                if format_data.get("==") is not None:
                    if not len(value) == format_data.get("=="):
                        raise ValidationError("%s 非法值： %s, 参数长度必须等于 %s" % (
                            key, len(value), format_data.get("==")))
                if "in" in format_data:
                    if value not in format_data.get("in"):
                        raise ValidationError("%s 非法值： %s, 允许的参数值为：%s" % (key, value, format_data.get("in")))

                if "re.match" in format_data:
                    if not re.match(r'%s' % format_data.get("re.match"), value):
                        raise ValidationError("%s 非法值： %s, 不符合规则" % (key, value))

            if format_type == list:
                if "size" in format_data:
                    size_data = format_data.get("size")
                    if size_data.get(">") is not None:
                        le_value = size_data.get(">")
                        for t_value in value:
                            if isinstance(t_value, int):
                                if not t_value > le_value:
                                    raise ValidationError("%s 非法值： %s, 参数值必须大于 %s" % (
                                        key, t_value, le_value))
                            if isinstance(t_value, str):
                                if not len(t_value) > le_value:
                                    raise ValidationError("%s 非法值： %s, 参数长度必须大于 %s" % (
                                        key, len(t_value), le_value))
                    if "<" in size_data:
                        le_value = size_data.get("<")
                        for t_value in value:
                            if isinstance(t_value, int):
                                if not t_value < le_value:
                                    raise ValidationError("%s 非法值： %s, 参数值必须小于 %s" % (
                                        key, t_value, le_value))
                            if isinstance(t_value, str):
                                if not len(t_value) < le_value:
                                    raise ValidationError("%s 非法值： %s, 参数长度必须小于 %s" % (
                                        key, len(t_value), le_value))
                if "length" in format_data:
                    lenth_data = format_data.get("length")
                    len_list = len(value)
                    if lenth_data.get(">") is not None:
                        if not len_list > lenth_data.get(">"):
                            raise ValidationError("%s 非法长度：%s 列表长度必须大于 %s" % (
                                key, len_list, lenth_data.get(">")))
                    if "<" in lenth_data:
                        if not len_list < lenth_data.get("<"):
                            raise ValidationError("%s 非法长度：%s 列表长度必须小于 %s" % (
                                key, len_list, lenth_data.get("<")))

                if "in" in format_data:
                    le_value = format_data.get("in")
                    for t_value in value:
                        if t_value not in le_value:
                            raise ValidationError("%s 非法值： %s, 允许的参数值为：%s" % (key, value, format_data.get("in")))

                if "re.match" in format_data:
                    rematch = format_data.get("re.match")
                    for t_value in value:
                        if not re.match(r'%s' % rematch, t_value):
                            raise ValidationError("%s 非法值： %s, 不符合规则" % (key, value))

        return value
    else:
        raise ValidationError("非法类型参数， 参数 %s 传入类型为 %s, 合法类型必须为： %s"
            % (key, _type_to_utf8(type(value)), _type_to_utf8(format_type)))

