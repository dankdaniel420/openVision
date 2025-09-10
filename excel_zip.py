import io
import zipfile
import openpyxl
import csv
import base64

def compress(raw_data: str) -> str:
    # Step 1: Build Excel workbook in memory
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Validation_Errors"

    reader = csv.reader(io.StringIO(raw_data), quotechar='"', )
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
    zip_bytes = zip_buffer.getvalue()

    return base64.b64encode(zip_bytes).decode("utf-8")

if __name__ == "__main__":

    with open("big.txt", "r", encoding="utf-8") as f:
        raw_data = f.read()
        print(compress(raw_data))