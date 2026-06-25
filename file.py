'''
File Upload @Stattic Files
1. Upload files
2. Serve Image/files
'''
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
import os 
import shutil  #Use for file Operation

app =  FastAPI()

#step -1  Ensure upload folder exist
UPLOAD_DIR = "upload"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Step -2 static file set-up
# URL:  HTTP:/   /127.0.0.1:8000/FILES/<FILENAME>
app.mount("/files",StaticFiles(directory=UPLOAD_DIR),name ="files")

#Step-3 :upload file api
@app.post("/upload")
def upload_file(file:UploadFile= File(...)):
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR,filename)

    if not filename:
        raise HTTPException(
            status_code= 400,
            detail="FIle not found error"
        )
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

        return{
            "message": "file uploaded succesfully",
            "Filename": filename,
            "file_url": f"http://127.0.0.1:8000/files/{filename}"
        }

#Step-4:GET file url ApI
@app.get("/files/{filename}")
def get_files(filename:str):
    file_path = os.path.join(UPLOAD_DIR,filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code= 404,
            detail= "File not found error"
        )
    return {"file_url": f"http://127.0.0.1:8000/files/{filename}"
    }
@app.get("/")
def message():
    return "This is a files"