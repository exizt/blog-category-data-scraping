import re
import json


class LazyJSONDecoder(json.JSONDecoder):
    """
    https://stackoverflow.com/questions/65910282/jsondecodeerror-invalid-escape-when-parsing-from-python
    JSONDecodeError; Invalid /escape 에 대한 조치
    """

    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)
