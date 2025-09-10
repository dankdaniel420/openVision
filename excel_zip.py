import io
import zipfile
import openpyxl
import csv
import base64
import logging


def compress(raw_data: str) -> str:
    wb = openpyxl.Workbook(write_only=True)  # write-only mode saves memory
    ws = wb.create_sheet("Validation_Errors")

    for line in raw_data.splitlines():
        # Skip empty lines
        if not line.strip():
            continue
        # Split by comma (basic CSV parsing; handle quotes manually if needed)
        row = []
        current = ""
        in_quotes = False
        for char in line:
            if char == "'":
                in_quotes = not in_quotes
            elif char == "," and not in_quotes:
                row.append(current)
                current = ""
            else:
                current += char
        row.append(current)
        ws.append(row)

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
