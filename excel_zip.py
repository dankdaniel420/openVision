import io
import zipfile
import base64

def compress(raw_data: str) -> str:

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("validation_errors.csv", raw_data)

    return base64.b64encode(zip_buffer.getvalue()).decode("utf-8")

if __name__ == "__main__":
    with open("big.txt", "r", encoding="utf-8") as f:
        raw_data = f.read()
        print(compress(raw_data))
