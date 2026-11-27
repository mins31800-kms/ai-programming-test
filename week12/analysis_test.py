import pandas as pd
from analysis import 정제, 반별평균

# 파일을 읽는 코드는 파일 맨 위에서 한 번만 실행한다.
본 = 정제(pd.read_csv("scores_2026.csv"))
미니 = 정제(pd.read_csv("mini.csv"))


def test_정제하면_100행이_남는다():
    # 행수 보존 검증
    assert len(본) == 100


def test_반은_두_종류만_남는다():
    # 공백 제거 및 고유값 검증
    assert sorted(본["반"].unique()) == ["1반", "2반"]


def test_그룹합이_전체합과_같다():
    # 합계 일치 검증
    assert 본.groupby("반")["점수"].sum().sum() == 본["점수"].sum()


def test_손계산과_일치한다():
    # mini.csv 손계산 대조 검증
    assert 반별평균(미니)["1반"] == 80.0