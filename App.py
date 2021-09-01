import pandas as pd
import matplotlib.pyplot as plt


def UpdateNetTotals():
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


def GenerateGraph():
    df = UpdateNetTotals()
    date = df["DATE"].max().date()
    df = df.set_index("DATE")
    fig = plt.figure(figsize=(20, 10))
    plt.plot(df["NSW"].ewm(span=7, adjust=False).mean(), color="r")
    plt.plot(df["VIC"].ewm(span=7, adjust=False).mean(), color="k")
    plt.legend(["NSW", "VIC"])
    plt.title(f"Daily Covid Cases (VIC vs NSW)\n7-Day Rolling Avg. | {date}")
    plt.show()
