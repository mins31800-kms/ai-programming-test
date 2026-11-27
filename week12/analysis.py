import pandas as pd


def 정제(df):
    # 원본 df를 보호하기 위해 복사본을 생성한다.
    df = df.copy()
    print("시작:", len(df))

    # 1) 점수가 비어 있는 행을 삭제한다.
    df = df.dropna(subset=["점수"])
    print("빈 칸 제거:", len(df))

    # 2) 모든 열이 완전히 같은 중복 행은 하나만 남긴다.
    df = df.drop_duplicates()
    print("중복 제거:", len(df))

    # 3) 반과 과목 값의 앞뒤 공백을 제거한다.
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()

    # 4) 점수가 0~100 범위를 벗어난 행을 삭제한다.
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    print("범위 밖 제거:", len(df))

    return df


def 반별평균(df):
    # 반별 점수 평균을 소수 둘째 자리까지 반올림하여 반환한다.
    return df.groupby("반")["점수"].mean().round(2)


def 반별통계(df):
    # 반별로 개수, 평균, 중앙값, 최댓값을 한 표로 집계한다.
    return df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2)


if __name__ == "__main__":
    # 데이터 불러오기 및 정제
    raw_df = pd.read_csv("scores_2026.csv")
    df = 정제(raw_df)

    # STEP 3-① 필터링
    math_df = df[df["과목"] == "수학"]
    print("\n[필터링] 수학 과목 행 수:", len(math_df))

    # (응용) 1반이면서 90점 이상인 행만 남기기
    high_1ban_df = df[(df["반"] == "1반") & (df["점수"] >= 90)]
    print("[필터링 응용] 1반 90점 이상 행 수:", len(high_1ban_df))

    # STEP 3-② 그룹화
    print("\n[그룹화] 반별 평균:")
    print(반별평균(df))

    print("\n[그룹화] 과목 x 반별 평균:")
    print(df.groupby(["과목", "반"])["점수"].mean().round(2))

    # STEP 3-③ 통계
    print("\n[통계] 반별 요약표:")
    print(반별통계(df))

    # STEP 3 합계·개수 검증
    print("\n[검증] 그룹 합계의 합:", df.groupby("반")["점수"].sum().sum(), "/ 전체 합계:", df["점수"].sum())
    print("[검증] 그룹 개수의 합:", df.groupby("반")["점수"].count().sum(), "/ 전체 행 수:", len(df))