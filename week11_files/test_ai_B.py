import pytest
from load_scores import load_scores


def test_load_valid_csv(tmp_path):
    p = tmp_path / "scores.csv"
    p.write_text("이름,점수\n김철수,85\n이영희,92\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == [("김철수", 85), ("이영희", 92)]
    assert skipped == []


def test_blank_lines_are_skipped_without_record(tmp_path):
    p = tmp_path / "blank.csv"
    p.write_text("이름,점수\n김철수,85\n\n이영희,92\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert len(kept) == 2
    assert skipped == []


def test_header_only_file(tmp_path):
    p = tmp_path / "header_only.csv"
    p.write_text("이름,점수\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == []
    assert skipped == []


def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        load_scores("missing_file.csv")


def test_invalid_column_count_recorded(tmp_path):
    p = tmp_path / "bad_cols.csv"
    p.write_text("이름,점수\n김철수,85,추가\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == []
    assert len(skipped) == 1


def test_empty_name_or_score_recorded(tmp_path):
    p = tmp_path / "empty_val.csv"
    p.write_text("이름,점수\n,80\n김철수,\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == []
    assert len(skipped) == 2


def test_non_integer_score_recorded(tmp_path):
    p = tmp_path / "bad_int.csv"
    p.write_text("이름,점수\n김철수,점수없음\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == []
    assert len(skipped) == 1


@pytest.mark.parametrize(
    "score, expected_kept",
    [(-1, 0), (0, 1), (100, 1), (101, 0)],
)
def test_score_boundary_values(tmp_path, score, expected_kept):
    p = tmp_path / "boundary.csv"
    p.write_text(f"이름,점수\n학생,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert len(kept) == expected_kept
    assert len(skipped) == 1 - expected_kept


def test_duplicate_names_both_kept(tmp_path):
    p = tmp_path / "dup.csv"
    p.write_text("이름,점수\n박민수,60\n박민수,100\n", encoding="utf-8")
    kept, skipped = load_scores(p)
    assert kept == [("박민수", 60), ("박민수", 100)]
    assert skipped == []