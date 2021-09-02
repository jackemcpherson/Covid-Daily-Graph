import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


def UpdateNetCaseTotals():
    vic_raw = pd.read_html(
        "https://covidlive.com.au/report/daily-cases/vic",
        attrs={"class": "DAILY-CASES"},
    )[0]
    nsw_raw = pd.read_html(
        "https://covidlive.com.au/report/daily-cases/nsw",
        attrs={"class": "DAILY-CASES"},
    )[0]
    raw = pd.merge(vic_raw[["DATE", "NET"]], nsw_raw[["DATE", "NET"]], on="DATE")
    raw[["DATE", "VIC", "NSW"]] = raw
    raw = raw.drop(["NET_x", "NET_y"], axis="columns")
    raw["DATE"] = raw["DATE"].apply(pd.to_datetime)
    raw[["VIC", "NSW"]] = raw[["VIC", "NSW"]].apply(pd.to_numeric, errors="coerce")
    return raw


def UpdateVaxTotals():
    vic_raw = pd.read_html(
        "https://covidlive.com.au/report/daily-vaccinations/vic",
        attrs={"class": "DAILY-VACCINATIONS"},
    )[0]
    nsw_raw = pd.read_html(
        "https://covidlive.com.au/report/daily-vaccinations/nsw",
        attrs={"class": "DAILY-VACCINATIONS"},
    )[0]
    raw = pd.merge(vic_raw[["DATE", "DOSES"]], nsw_raw[["DATE", "DOSES"]], on="DATE")
    raw[["DATE", "VIC", "NSW"]] = raw
    raw = raw.drop(["DOSES_x", "DOSES_y"], axis="columns")
    raw["DATE"] = raw["DATE"].apply(pd.to_datetime)
    raw[["VIC", "NSW"]] = raw[["VIC", "NSW"]].apply(pd.to_numeric, errors="coerce")
    return raw


def GenerateCasesGraph(window_size: int = 7):
    df = UpdateNetCaseTotals()
    date = df["DATE"].max().date()
    df = df.set_index("DATE")
    fig = plt.figure(figsize=(20, 10))
    plt.plot(df["NSW"].ewm(span=window_size, adjust=False).mean(), color="r")
    plt.plot(df["VIC"].ewm(span=window_size, adjust=False).mean(), color="k")
    plt.legend(["NSW", "VIC"])
    plt.title(
        f"Daily Covid Cases (VIC vs NSW)\n{window_size}-Day Rolling Avg. | {date}"
    )
    plt.show()


def GenerateVaxGraph():
    df = UpdateVaxTotals()
    date = df["DATE"].max().date()
    df = df.set_index("DATE").loc["2021-06-01":]
    fig, ax = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(20)
    ax.plot(df["NSW"], color="r")
    ax.plot(df["VIC"], color="k")
    ax.legend(["NSW", "VIC"])
    ax.set_title(f"Covid Vaccinations (VIC vs NSW) | {date}")
    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    plt.show()
