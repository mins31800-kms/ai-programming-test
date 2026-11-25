import pytest
from load_scores import load_scores


def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5


def test_빈_줄은_건너뛴다(tmp_path):
    csv_file = tmp_path / "blank.csv"
    csv_file.write_text(
        "이름,점수\n김하나,88\n\n이둘,92\n\n",
        encoding="utf-8",
    )
    kept, skipped = load_scores(csv_file)
    assert kept == [("김하나", 88), ("이둘", 92)]
    assert skipped == []


def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    csv_file = tmp_path / "comma_name.csv"
    csv_file.write_text(
        '이름,점수\n"김,하나",88\n',
        encoding="utf-8",
    )
    kept, skipped = load_scores(csv_file)
    assert kept == [("김,하나", 88)]
    assert skipped == []


def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []


@pytest.mark.parametrize(
    "점수, 유효한가",
    [
        (-1, False),   # 경계 바로 아래
        (0, True),     # 아래쪽 경계
        (1, True),
        (99, True),
        (100, True),   # 위쪽 경계
        (101, False),  # 경계 바로 위
    ],
)
def test_점수_경계값(tmp_path, 점수, 유효한가):
    csv_file = tmp_path / "boundary.csv"
    csv_file.write_text(f"이름,점수\n테스트,{점수}\n", encoding="utf-8")
    kept, skipped = load_scores(csv_file)
    assert (len(kept) == 1) == 유효한가


def test_잘못된_형식의_줄은_건너뛰고_기록한다(tmp_path):
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(
        "이름,점수\n"
        "김하나,88,여분열\n"
        ",90\n"
        "이둘,\n"
        "박셋,팔십\n",
        encoding="utf-8",
    )
    kept, skipped = load_scores(csv_file)
    assert kept == []
    assert len(skipped) == 4


def test_동명이인은_둘_다_남긴다(tmp_path):
    csv_file = tmp_path / "duplicate.csv"
    csv_file.write_text(
        "이름,점수\n김하나,88\n김하나,95\n",
        encoding="utf-8",
    )
    kept, skipped = load_scores(csv_file)
    assert kept == [("김하나", 88), ("김하나", 95)]
    assert skipped == []
