import pytest
from load_scores import load_scores


def test_valid_scores(tmp_path):
    p = tmp_path / "valid.csv"
    p.write_text("이름,점수\n김하나,88\n이둘,75\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == [("김하나", 88), ("이둘", 75)]
    assert skipped == []


def test_utf8_bom_and_whitespace(tmp_path):
    p = tmp_path / "bom.csv"
    p.write_text("\ufeff이름,점수\n  김하나 , 90 \n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == [("김하나", 90)]
    assert skipped == []


def test_blank_lines_ignored(tmp_path):
    p = tmp_path / "blank.csv"
    p.write_text("이름,점수\n\n김하나,80\n\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == [("김하나", 80)]
    assert skipped == []


def test_header_only_returns_empty(tmp_path):
    p = tmp_path / "header.csv"
    p.write_text("이름,점수\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == []
    assert skipped == []


def test_file_not_found_raises():
    with pytest.raises(FileNotFoundError):
        load_scores("does_not_exist.csv")


def test_invalid_column_count_skipped(tmp_path):
    p = tmp_path / "cols.csv"
    p.write_text("이름,점수\n김하나,80,extra\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == []
    assert skipped == [(2, "김하나,80,extra", "열 개수가 2가 아님")]


def test_empty_name_and_empty_score_skipped(tmp_path):
    p = tmp_path / "empty_fields.csv"
    p.write_text("이름,점수\n,85\n김하나,\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == []
    assert skipped == [
        (2, ",85", "이름이 비어 있음"),
        (3, "김하나,", "점수가 비어 있음"),
    ]


def test_non_integer_score_skipped(tmp_path):
    p = tmp_path / "non_int.csv"
    p.write_text("이름,점수\n김하나,abc\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == []
    assert skipped == [(2, "김하나,abc", "점수가 정수가 아님")]


@pytest.mark.parametrize(
    "score, is_valid",
    [(-1, False), (0, True), (100, True), (101, False)],
)
def test_score_boundaries(tmp_path, score, is_valid):
    p = tmp_path / "bound.csv"
    p.write_text(f"이름,점수\n홍길동,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    if is_valid:
        assert kept == [("홍길동", score)]
        assert skipped == []
    else:
        assert kept == []
        assert skipped[0][2] == "점수가 0~100 밖"


def test_duplicate_names_kept(tmp_path):
    p = tmp_path / "dup.csv"
    p.write_text("이름,점수\n김하나,70\n김하나,90\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == [("김하나", 70), ("김하나", 90)]
    assert skipped == []