import pandas as pd

# 전세계의 confirmed, deaths, recovered별 총합구하기
# total sum of confirmed, deaths, recovered
df = pd.read_csv("data/daily_report.csv")
totals_df = df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
totals_df = totals_df.rename(columns={"index": "condition"})

# 나라별 confirmed, deaths, recovered별 총합구하기
# country sum of confirmed, deaths, recovered
countries_df = df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
countries_df = countries_df.fillna(0)
countries_df = (
    countries_df.groupby("Country_Region")
    .sum()
    .sort_values(by="Confirmed", ascending=False)
    .reset_index()
)
# us의 recovered 수가 결측치로 되어 있어서 확진자 수에서 사망자를 제외한 숫자로 대체함
countries_df.iloc[0, 3] = countries_df.iloc[0, 1] - countries_df.iloc[0, 2]


# drop_down options
dropdown_options =countries_df.sort_values("Country_Region").reset_index()
dropdown_options = dropdown_options["Country_Region"]

conditions = ["confirmed", "deaths", "recovered"]

# 전세계의 confirmed, deaths, recovered별로 구하기
# make the column global of confirmed, deaths, recovered
def make_global_df():
    def make_df(condition):
        df = pd.read_csv(f"data/time_series_covid19_{condition}_global.csv")
        df = (
            df.drop(columns=["Province/State", "Country/Region", "Lat", "Long"])
            .sum()
            .reset_index(name=condition)
        )
        df = df.rename(columns={"index": "date"})
        return df

    final_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df


# 각 나라별 confirmed, deaths, recovered수 구하기
# make the column Each contry of confirmed, deaths, recovered
def make_country_df(country):
    def make_df(condition):
        df = pd.read_csv(f"data/time_series_covid19_{condition}_global.csv")
        df = df.loc[df["Country/Region"] == country]
        df = (
            df.drop(columns=["Province/State", "Country/Region", "Lat", "Long"])
            .sum()
            .reset_index(name=condition)
        )
        df = df.rename(columns={"index": "date"})
        return df

    final_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df
