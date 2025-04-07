from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import json
import uvicorn
from pathlib import Path

app = FastAPI()


@app.get("/linear/available-languages/{req_lang}")
async def get_available_languages(req_lang: str):
    if req_lang == 'ru':
        return JSONResponse(
            content={
                "list": [
                    {
                        "id": 1,
                        "name": "Грузинский",
                        "acronym": "ka",
						"source": "ru",
                        "emoji": "🇬🇪",
						"type": "linear",
                        "available": True
                    }
                ]
            },
            status_code=200
        )
    elif req_lang == 'en':
        raise HTTPException(detail=f"{req_lang.capitalize} endpoint is not implemented yet.", status_code=501)
    else:
        raise HTTPException(detail=f"{req_lang.capitalize} does not exist.", status_code=404)


@app.get("/linear/{lang_acronym}/{req_lang}")
async def get_language_info(lang_acronym: str, req_lang: str):
    if req_lang == 'ru':
        if lang_acronym == 'el' or lang_acronym == 'ka':
            json_file_path = Path(__file__).parent / "langs" / "linear" / f"{lang_acronym}-{req_lang}.json"
            # Check if the file exists
            if not json_file_path.exists():
                raise HTTPException(status_code=404, detail="Language file not found")
            
            # Open and read the JSON file
            with open(json_file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)

            # Return the content of the file as JSON response
            return JSONResponse(
                status_code=200,
                content=content
            )
        else:
            raise HTTPException(detail=f"{lang_acronym.capitalize} does not exist.", status_code=404)
    elif req_lang == 'en':
        raise HTTPException(detail=f"{req_lang.capitalize} endpoint is not implemented yet.", status_code=501)
    else:
        raise HTTPException(detail=f"{req_lang.capitalize} does not exist.", status_code=404)


@app.get("/file/{filename}")
async def get_file(filename: str):
	file_path = Path(__file__).parent / "files" / filename
	if not file_path.exists() or not file_path.is_file():
		raise HTTPException(status_code=404, detail="File not found")
	return FileResponse(
		path=file_path,
		filename=filename
	)


if __name__ == '__main__':
	uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=443,
        ssl_keyfile="/ssl/privkey.pem",
        ssl_certfile="/ssl/fullchain.pem"
    )
