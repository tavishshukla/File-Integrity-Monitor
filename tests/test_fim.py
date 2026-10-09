from fim import compare

def test_compare():
    result = compare({"a":"1","b":"2"}, {"a":"x","c":"3"})
    assert result == {"added":["c"],"removed":["b"],"changed":["a"]}


def test_scan_detects_changed_file(tmp_path):
    from fim import scan, compare
    target = tmp_path / "example.txt"
    target.write_text("before", encoding="utf-8")
    baseline = scan(tmp_path)
    target.write_text("after", encoding="utf-8")
    changes = compare(baseline, scan(tmp_path))
    assert str(target) in changes["changed"]
