from fim import compare

def test_compare():
    result = compare({"a":"1","b":"2"}, {"a":"x","c":"3"})
    assert result == {"added":["c"],"removed":["b"],"changed":["a"]}
