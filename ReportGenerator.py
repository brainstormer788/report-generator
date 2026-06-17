from tkinter import Tk, filedialog, messagebox
import pandas as pd
from collections import defaultdict

def process_sheet(df):
    # Column J = 10th column
    dt_series = pd.to_datetime(
        df.iloc[:, 9],
        dayfirst=True,
        errors="coerce"
    )

    counts = defaultdict(int)

    for dt in dt_series.dropna():
        date_part = dt.strftime("%d/%m/%y")

        start_hour = dt.hour
        end_hour = (start_hour + 1) % 24

        bucket = f"{date_part} {start_hour:02d}--{end_hour:02d}"

        counts[bucket] += 1

    return counts

Tk().withdraw()

file_path = filedialog.askopenfilename(
    title="Select workbook containing LPG and ALP sheets",
    filetypes=[("Excel/ODS Files", "*.xlsx *.ods")]
)

if not file_path:
    raise SystemExit("No file selected")

try:

    if file_path.lower().endswith(".ods"):
        lpg = pd.read_excel(
            file_path,
            sheet_name="lpg",
            engine="odf",
            dtype=str
        )

        alp = pd.read_excel(
            file_path,
            sheet_name="alp",
            engine="odf",
            dtype=str
        )

    else:
        lpg = pd.read_excel(
            file_path,
            sheet_name="lpg",
            dtype=str
        )

        alp = pd.read_excel(
            file_path,
            sheet_name="alp",
            dtype=str
        )

    lpg_counts = process_sheet(lpg)
    alp_counts = process_sheet(alp)

    all_buckets = sorted(
        set(lpg_counts.keys()) | set(alp_counts.keys())
    )

    rows = []

    current_date = None
    date_lpg_total = 0
    date_alp_total = 0

    grand_lpg = 0
    grand_alp = 0

    for bucket in all_buckets:

        date_part = bucket.split()[0]

        if current_date is None:
            current_date = date_part

        if date_part != current_date:

            rows.append([
                f"TOTAL {current_date}",
                date_lpg_total,
                date_alp_total
            ])

            grand_lpg += date_lpg_total
            grand_alp += date_alp_total

            date_lpg_total = 0
            date_alp_total = 0

            current_date = date_part

        lpg_val = lpg_counts.get(bucket, 0)
        alp_val = alp_counts.get(bucket, 0)

        rows.append([
            bucket,
            lpg_val,
            alp_val
        ])

        date_lpg_total += lpg_val
        date_alp_total += alp_val

    if current_date is not None:

        rows.append([
            f"TOTAL {current_date}",
            date_lpg_total,
            date_alp_total
        ])

        grand_lpg += date_lpg_total
        grand_alp += date_alp_total

    rows.append([
        "G Total",
        grand_lpg,
        grand_alp
    ])

    output = pd.DataFrame(
        rows,
        columns=[
            "Time Slot",
            "LPG",
            "ALP"
        ]
    )

    output_file = "output.xlsx"

    with pd.ExcelWriter(output_file) as writer:
        output.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

    messagebox.showinfo(
        "Success",
        f"Output saved as {output_file}"
    )

except Exception as e:
    messagebox.showerror(
        "Error",
        str(e)
    )