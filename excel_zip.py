import io
import zipfile
import openpyxl
import csv
import base64
import logging



def compress(raw_data: str) -> str:
    wb = openpyxl.Workbook(write_only=True)  # write-only mode saves memory
    ws = wb.create_sheet("Validation_Errors")

    reader = csv.reader(io.StringIO(raw_data), quotechar='"')
    for row in reader:
        ws.append(row)

    reader = csv.reader(io.StringIO(raw_data), quotechar='"')
    temp = 0
    for row in reader:
        ws.append(row)
        if temp < 5:
            print(row)
            temp += 1

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
