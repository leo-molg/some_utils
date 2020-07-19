# coding: utf-8
from aboutValid.valid_util import check_params_with_model


# check model
def test_model(self):
    base_define = {
        "name": {"type": str, "notnull": True, "required": True, "format": {">": 0, "<=": 64}},
        "age": {"type": int, "notnull": True, "required": True, "format": {">=": 0}},
        "comment": {"type": str, "notnull": False, "required": False, "format": {">=": 0, "<=": 256}},
    }
    return base_define


_data = {
    "name": "ssss",
    "age": 23,
    "comment": "test"
}

try:
    request_data = check_params_with_model(_data, test_model(), keep_extra_key=False)
except Exception as e:
    # error message
    print(e.message)




