import os
import shutil
import uuid

from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse

from download_onedrive import baixar_arquivos_onedrive  # função que faz o ‘download’

app = FastAPI()


@app.post("/onedrive/download")
def baixar(url: str = Form(...)):
    pasta = f"/tmp/{uuid.uuid4()}"
    os.makedirs(pasta, exist_ok=True)

    print(url, pasta)

    arquivos = baixar_arquivos_onedrive(url, pasta)  # retorna lista de caminhos completos

    def gerar_streams():
        for arquivo in arquivos:
            yield f"--file-boundary\nContent-Disposition: attachment; filename=\"{os.path.basename(arquivo)}\"\n\n".encode()
            with open(arquivo, "rb") as f:
                shutil.copyfileobj(f, os)
            yield b"\n"

    return StreamingResponse(gerar_streams(), media_type="multipart/mixed; boundary=file-boundary")
