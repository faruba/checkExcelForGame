
"""
jpath
将匹配路径和值
"""
WILDCARD = '*'
SELF = '$'


def _get(obj, seg):
    if obj is None:
        return None

    try:
        nseg = int(seg)
    except ValueError:
        nseg = None

    if isinstance(obj, list):
        if nseg is not None and 0 <= nseg < len(obj):
            return obj[nseg]
        else:
            return None
    else:
        if seg in obj:
            return obj[seg]
        if nseg is not None and nseg in obj:
            return obj[nseg]

    return None


def _keys(obj):
    ret = []
    if isinstance(obj, dict):
        for key in obj.keys():
            if not key.startswith('_'):
                ret.append(key)
    elif isinstance(obj, list):
        for i in range(0, len(obj)):
            ret.append(i)
    return ret


def _iter_match(obj, segs, sid, pres, ret):
    seg = segs[sid]
    if isinstance(obj, list) or isinstance(obj, dict):
        if seg == WILDCARD:
            keys = _keys(obj)
            for k in keys:
                val = obj[k]
                if val is not None:
                    path = pres[0:]
                    path.append(str(k))
                    if sid == len(segs)-1:
                        path_str = '.'.join(path)
                        ret[path_str] = val
                    else:
                        _iter_match(val, segs, sid+1, path, ret)
        else:
            val = _get(obj, seg)
            if val is not None:
                pres.append(seg)
                if sid == len(segs)-1:
                    path_str = '.'.join(pres)
                    ret[path_str] = val
                else:
                    _iter_match(val, segs, sid+1, pres, ret)


def match(obj, path):
    """
    匹配对象和路径
    :param obj: 对象
    :param path: 路径 用.分割,"*"作为通配(例如"*.0"), 值本身用$表示
    :return: 返回匹配的值的字典(path: value)
    """
    ret = {}
    segs = path.split('.')
    if len(segs) == 1 and segs[0] == SELF:
        return {
            SELF: obj,
        }
    else:
        _iter_match(obj, segs, 0, [], ret)
    return ret


if __name__ == '__main__':
    test_cases = [
        ['*.0',   [[1, 10], [2, 20]]],
        ['*.1.*', [[1, 2, 3], [4, [5, 6], 7], [8, [[9, 10], 11], 12], 13]],
        ['a.*',   {'a': [1, 2]}],
        ['a',     {'a': [1, 2]}],
        ['$',     {'a': [1, 2]}],
        ['*.1',   {'a': [1, 2], '_b': [3, 4]}],
    ]
    print('run test')
    for t in test_cases:
        p = t[0]
        v = t[1]
        print('match(', v, ',', p, ')=', match(v, p))
    print('end test')
