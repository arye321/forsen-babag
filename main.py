# uvicorn main:app --reload
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse,HTMLResponse
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles

class Item(BaseModel):
    name: str

app = FastAPI()
# app.mount("/babag", StaticFiles(directory="babag"), name="babag")

# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile | None = None):
#     if not file:
#         return {"message": "No upload file sent"}
#     else:
#         try:
#             contents = await file.read()
#             with open(file.filename, 'wb') as f:
#                 f.write(contents)
#         except Exception:
#             return {"message": "There was an error uploading the file"}
#         finally:
#             await file.close()
#         return {"filename": file.filename}

@app.post("/items/", response_class=PlainTextResponse)
async def create_item(item: Item):
    return f"ok, {item.name}"
    
@app.get("/")
async def root():
#     paths = sorted(Path("./babag").iterdir(), key=os.path.getmtime)
#     links =''
#     for i in paths:
#         links+=f'<a href="/babag/{i.name}">{i.name}<br>'
#     content = f"""
# <body>
# {links}
# </body>
#         """
    content = """
    <!DOCTYPE html>
        <html>
            <script async defer data-website-id="3e4034d3-d98c-49ab-88ca-c021544e8194" src="https://babag.vercel.app/xd.js"></script>
            <h1> Welcome to zombocom</h1>
        </html>
    """
    return HTMLResponse(content=content)

@app.get("/items/", response_class=PlainTextResponse)
async def lol():
    return 'lol'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.ico')# uvicorn main:app --reload
