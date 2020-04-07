import json
import pandas as pd
import datetime

# idea
# first sort by spring/summer/fall/winter/all-season, as separate posts
# Check how many fish that is per post, to keep it properly spaced out
# if so, then we would probably do it by:
# 1. location, i.e. river, cliffside, sea, etc. as separate major headers
# 2. within those headers, sort it by all day fish, dayside fish, night fish
# 3. Sort those by price, with highest value at the top
# 4. If it's only available in one month, highlight that somehow

month_choices = [datetime.date(2020, i, 1).strftime('%B') for i in range(1, 13)]
this_month = datetime.date.today().month
month_list = [month_choices[int(i + this_month - 1) % 12] for i in range(12)]

def months_left(critter_months):
    month_count = 0
    for month in month_list:
        if month not in critter_months:
            return month_count
        else:
            month_count += 1
    return month_count

def months_until(critter_months):
    month_count = 0
    for month in month_list:
        if month in critter_months:
            return month_count
        else:
            month_count += 1
    return month_count

def group_critters():
    with open("wiki_data.json", "r") as fobj:
        data = json.load(fobj)

    hemi = next(iter(data.keys()))
    df = pd.DataFrame(data[hemi])
    df["months_left"] = df["months"].apply(months_left)
    df["months_until"] = df["months"].apply(months_until)
    df["price"] = pd.to_numeric(df["price"])
    df["name"] = df.apply(lambda row: f"<a href='{row.page}'>{row.name}</a>")
    # print(df.columns)
    # df["seasonality"] = df["months"].apply(len)
    # df["season"] = df["months"].apply(lambda lst: [s for s, ms in month_list
    #                                                if lst[0] in ms][0])
    df = df.sort_values(by=["months_until", "months_left", "location", "price"],
                        ascending=[True, True, True, False])
    return df

if __name__ == "__main__":
    import HTML
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    df = group_critters()
    print(df)
    df.to_csv("critters.csv")

    htmlcode = HTML.table(df)
    with open("critters.html", "w") as fobj:
        fobj.write(htmlcode)