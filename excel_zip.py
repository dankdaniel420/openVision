import io
import zipfile
import openpyxl
import csv
import base64

def compress(raw_data: str) -> str:
    clean_data = raw_data.replace("\\r\\n", "\n").replace('\\"', '"')
        
    # Step 1: Build Excel workbook in memory
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Validation_Errors"

    reader = csv.reader(io.StringIO(clean_data), quotechar='"')
    for row in reader:
        ws.append(row)

    # Step 2: Save Excel to an in-memory buffer
    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)

    # Put Excel file into a ZIP archive (in memory)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("validation_errors.xlsx", excel_buffer.getvalue())
    zip_buffer.seek(0)

    return base64.b64encode(zip_buffer.getvalue()).decode("utf-8")

if __name__ == "__main__":
    print(download_errors())