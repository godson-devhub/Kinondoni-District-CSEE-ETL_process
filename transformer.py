import pandas as pd
import re


# school names
school_names = {
    "s0298": "Feza Girls Secondary School",
    "s2325": "Canossa Secondary School",
    "s0189": "Jangwani Secondary School",
    "p3097": "Dynamic Secondary School",
    "s4173": "St.Mary's Secondary School",
    "s5777": "Mivumoni Secondary School",
    "s6054": "Mbezi Secondary School",
    "s4210": "Kawe Ukwamani Secondary School",
    "s1022": "Kondo Secondary School",
    "s4026": "Bunju'A' Secondary School"
}


def extract_bmath(subjects):

    match = re.search(
        r"B/MATH\s*-\s*'([A-F])'",
        subjects
    )

    if match:
        return match.group(1)

    return None


def transform_data(data):

    df = pd.DataFrame(data)

    # extract B/MATH grade
    df["B_MATH"] = df["detailed_subjects"].apply(
        extract_bmath
    )

    # remove rows without B/MATH
    df = df.dropna(subset=["B_MATH"])

    # count grades per school
    summary = df.pivot_table(
        index="school_code",
        columns="B_MATH",
        aggfunc="size",
        fill_value=0
    )

    # ensure all grades exist
    for grade in ["A", "B", "C", "D", "F"]:

        if grade not in summary.columns:
            summary[grade] = 0

    # arrange columns
    summary = summary[
        ["A", "B", "C", "D", "F"]
    ]

    # total students
    summary["Total_Students"] = (
        summary["A"] +
        summary["B"] +
        summary["C"] +
        summary["D"] +
        summary["F"]
    )

    # failure rate percentage
    summary["Failure_Rate (%)"] = (
        summary["F"] /
        summary["Total_Students"]
    ) * 100

    # round percentages
    summary["Failure_Rate (%)"] = (
        summary["Failure_Rate (%)"]
        .round(2)
    )

    # add school names
    summary["School_Name"] = (
        summary.index.map(school_names)
    )

    # ranking based on F grades
    summary = summary.sort_values(
        by="F",
        ascending=True
    )

    # create ranking
    summary["Rank"] = range(
        1,
        len(summary) + 1
    )

    # reset index
    summary = summary.reset_index()

    # remove pivot table title
    summary.columns.name = None

    # rename columns
    summary = summary.rename(
        columns={
            "school_code": "School_Code",
            "A": "Grade_A",
            "B": "Grade_B",
            "C": "Grade_C",
            "D": "Grade_D",
            "F": "Grade_F"
        }
    )

    # final arrangement
    summary = summary[
        [
            "Rank",
            "School_Name",
            "School_Code",
            "Grade_A",
            "Grade_B",
            "Grade_C",
            "Grade_D",
            "Grade_F",
            "Total_Students",
            "Failure_Rate (%)"
        ]
    ]

    return summary