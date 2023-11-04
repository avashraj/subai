from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/upload_file")
async def upload_file(file: UploadFile):

    # return the transcript of the file, save to db and return text.
    return {"filename": file.filename}


@router.get("/start_quiz")
async def start_quiz():
    return ""




