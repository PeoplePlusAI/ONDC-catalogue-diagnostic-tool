from utils.file_utils import xlsx_to_csv, load_csv


def validate_catalogue(csv_file_path, requirements):
    csv_file_path = xlsx_to_csv(csv_file_path)
    df = load_csv(csv_file_path)
    df.fillna("")
    requirements = requirements.split("\n")
    return {
        "passed": False,
        "reason": "Not implemented yet",
        "rows_failed": [1,2,3]
    }

   



