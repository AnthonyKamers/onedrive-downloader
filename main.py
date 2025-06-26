import io
import os
import shutil
import uuid
import zipfile

from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse

from download_onedrive import baixar_arquivos_onedrive  # função que faz o ‘download’

app = FastAPI()


@app.post("/onedrive/download")
def baixar(url: str = Form(...)):
    load_dotenv()
    is_docker = os.getenv("IS_DOCKER") == "True"

    folder = "/downloads" if is_docker else "./downloads"

    folder = f"{folder}/{uuid.uuid4()}"
    os.makedirs(folder, exist_ok=True)

    print(url, folder)

    arquivos = baixar_arquivos_onedrive(url, folder)  # retorna lista de caminhos completos

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for caminho in arquivos:
            zip_file.write(caminho, arcname=os.path.basename(caminho))
    zip_buffer.seek(0)

    return StreamingResponse(zip_buffer, media_type="application/zip", headers={
        "Content-Disposition": "attachment; filename=arquivos_onedrive.zip"
    })
