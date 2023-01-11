import os
import glob
import pandas as pd

from compare_pdfs import compare_pdf_files


def extract_data_from_result(pdf_result):
    """Extract report result from pdf comparison result"""
    data = {}
    for i, file_data in enumerate(pdf_result["files"]):
        for k, v in file_data.items():
            if k in ["filename", "n_pages", "n_suspicious_pages"]:
                data[k + str(i + 1)] = v
    data["pages_per_second"] = pdf_result["pages_per_second"]
    data["version"] = pdf_result["version"]
    data.update(pdf_result["elapsed_time_sec"])
    return data


if __name__ == "__main__":
    print(f"Starting Report Generation ----------")
    current_dir = os.getcwd()
    code_stage = "optimized"
    tmp_folder = "tmp"
    directory = os.path.join(current_dir, tmp_folder)
    report_file_path = os.path.join(directory, "Comparison Report 9 Jan.xlsx")

    file_names = glob.glob(directory + "/**/*.pdf", recursive=True)

    report = []
    for file_1 in file_names:
        for file_2 in file_names:
            result = compare_pdf_files(
                filenames=[file_1, file_2], pretty_print=False, regen_cache=True
            )
            output = extract_data_from_result(result)
            report.append(output)
    report_df = pd.DataFrame(report)
    report_df["code_stage"] = code_stage
    report_df.sort_index(inplace=True)
    report_df.to_excel(report_file_path, index=False)
    print(f"Report Generation Complete ----------")
