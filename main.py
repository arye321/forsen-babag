# uvicorn main:app --reload
import os
from fastapi import FastAPI, UploadFile,Form, Request
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse,HTMLResponse
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

uploadaddress = os.getenv('UPADD', '')
assert uploadaddress, "uploadaddress is empty"



class Item(BaseModel):
    key: str
if os.getenv('DEBUG'):
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)
    
app.mount("/babag", StaticFiles(directory="babag"), name="babag")
@app.post(f"/testform/")
async def testfor(key: str = Form(''),lol:int= Form(2)):
    return f'{key},{lol}'


@app.post(f"/{uploadaddress}/")
async def testupload(request: Request,key: str = Form(...), file: UploadFile | None = None):
    forsankey = os.getenv('FORSAN')
    ip = request.client.host
    if ip==os.getenv('IP') and forsankey and key == forsankey:
        return f"key = {key}, file={file.filename} host={request.client.host}"
    else:
        return f"something went wrong"
  

@app.post("/uploadfile/")
async def create_upload_file(key: str = Form(...), file: UploadFile | None = None):
    forsankey = os.getenv('FORSAN')
    if forsankey and key == forsankey:
        if not file:
            return {"message": "No upload file sent"}
        else:
            try:
                contents = await file.read()
                with open(f'./babag/{file.filename}', 'wb') as f:
                    f.write(contents)
                with open("streams.txt", "a") as f:
                    f.write(f"\n{file.filename}")
            except Exception:
                return {"message": "There was an error uploading the file"}
            finally:
                if file:
                    await file.close()
            return {"filename": file.filename}

    else:
        return "Something went wrong!"        

@app.post("/items/", response_class=PlainTextResponse)
async def create_item(item: Item):
    return f"ok, {item}"
    
@app.get("/")
async def root():

    links =''
    lines = ''
    try:
        with open("streams.txt") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
        for i in lines:
                htmlname = i.split('.')[0]
                links+=f'<a href="/r/{htmlname}">{htmlname}</a><br>'
    except Exception:
        return "Something went wrong"
    content = f"""
<body>
<script async defer data-website-id="3e4034d3-d98c-49ab-88ca-c021544e8194" src="https://babag.vercel.app/xd.js"></script>
{links}
<h1> Welcome to zombocom</h1>
</body>
        """
    # content = """
    # <!DOCTYPE html>
    #     <html>
    #         <script async defer data-website-id="3e4034d3-d98c-49ab-88ca-c021544e8194" src="https://babag.vercel.app/xd.js"></script>
    #         <h1> Welcome to zombocom</h1>
    #     </html>
    # """
    return HTMLResponse(content=content)

@app.get("/items/", response_class=PlainTextResponse)
async def lol():
    return 'lol'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.ico')# uvicorn main:app --reload

@app.get("/r/{stream}")
async def read_item(stream: str):
    if os.path.isfile(f'./babag/{stream}.html'):
        content=f"""
            <body>
                <iframe 
                    srcdoc="<h1>Loading...</h1>" 
                    onload="this.removeAttribute('srcdoc')" 
                    id="igraph" 
                    scrolling="no" 
                    style="border:none;" 
                    seamless="seamless" 
                    src="/babag/{stream}.html" 
                    height="525" width="100%">
                </iframe>
            </body>

        """
        return HTMLResponse(content=content)
    else:
        return "Something went wrong"
        

# uvicorn main:app --reload
#/workspaces/forsen-babag/babag/xd forsen 30-07-2022 21h52m53s.html