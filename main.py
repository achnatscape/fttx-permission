from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pymssql

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_conn():
    return pymssql.connect(
        server='your-sql-server',     # 🔁 เปลี่ยนตรงนี้
        user='your-username',
        password='your-password',
        database='FTTx_db'
    )

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
async def submit_form(
    AWO_Work_Permission: str = Form(...),
    Region: str = Form(...),
    Province: str = Form(...),
    Route_Name: str = Form(...),
    Project_Name: str = Form(...),
    Contractor: str = Form(...),
    Distance_Meter: float = Form(...),
    Pole_Box_Count: int = Form(...),
    Submit_NBTC_Date: str = Form(...),
):
    conn = get_conn()
    cursor = conn.cursor()

    sql = """
        INSERT INTO FTTX_Permission (
            AWO_Work_Permission,
            Region,
            Province,
            Route_Name,
            Project_Name,
            Contractor,
            Distance_Meter,
            Pole_Box_Count,
            Submit_NBTC_Date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (
        AWO_Work_Permission,
        Region,
        Province,
        Route_Name,
        Project_Name,
        Contractor,
        Distance_Meter,
        Pole_Box_Count,
        Submit_NBTC_Date
    ))

    conn.commit()
    conn.close()

    return {"status": "success", "message": "บันทึกข้อมูลเรียบร้อยแล้ว!"}
