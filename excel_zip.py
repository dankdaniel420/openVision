import io
import zipfile
import openpyxl
import csv
import base64

def sanitize_cell(value):
    if value is None:
        return ""
    value = str(value)
    return "".join(c for c in value if c in "\t\n\r" or ord(c) >= 32)

def compress(raw_data: str) -> str:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Validation_Errors"

    reader = csv.reader(io.StringIO(raw_data), quotechar='"')
    for row in reader:
        ws.append([sanitize_cell(c) for c in row])

    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)

    zip_buffer, zip_bytes = io.BytesIO(), b""
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("validation_errors.xlsx", excel_buffer.getvalue())
        zip_bytes = zip_buffer.getvalue()

    return base64.b64encode(zip_bytes).decode("utf-8")

if __name__ == "__main__":
    with open("big.txt", "r", encoding="utf-8") as f:
        raw_data = f.read()
        print(compress(raw_data))
