"""
FastAPI application to split an image into a grid of rows and columns
"""
import io
import zipfile
import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from splitter import split_to_grid, white_stripes

load_dotenv()

origins = [os.getenv('FRONTEND_URL')]
print("Origins: ", origins)
app = FastAPI(
    title="Image Splitter API",
    description="""API for splitting images into a grid of rows and columns
    and applying white stripes to top and bottom.""",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow your front-end origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/health")
async def health_check():
    """Checks whether the service is online"""
    return {"Status": "Healthy"}

@app.post("/process-image/")
async def process_image(
    file: UploadFile = File(...),
    rows: int = Form(1),
    columns: int = Form(3),
    stripes: str = Form('false'),
    stripe_height: float = Form(1/6)
    ):
    """Process incoming image file by splitting it into a grid and optionally adding white stripes 
    to the top and bottom of each grid cell."""

    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    stripes = stripes.lower() in ['true', '1', 't', 'y', 'yes']

    print("File type: ", file.content_type)
    print("r: ", rows)
    print("c: ", columns)
    print("stripes: ", stripes)
    print("stripe height: ", stripe_height)

    # Read the image file
    image = Image.open(io.BytesIO(await file.read()))

    # Process the image
    processed_image = split_to_grid(image, rows, columns)

    if stripes:
        processed_image = [white_stripes(img, stripe_height) for img in processed_image]

    # Save the processed image to a bytes buffer
    input_format = file.content_type.split('/')[-1].upper()
    if input_format == 'JPG':
        input_format = 'JPEG'

    buf = io.BytesIO()

    with zipfile.ZipFile(buf, 'w') as zip_file:
        for i, img in enumerate(processed_image):
            img_buf = io.BytesIO()
            img.save(img_buf, format=input_format)
            img_buf.seek(0)
            zip_file.writestr(f'image_{i}.{input_format.lower()}', img_buf.read())

    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment;filename=processed_images.zip"}
        )
    