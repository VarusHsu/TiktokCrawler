
import openpyxl
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


def read_xlsx(file: str) -> dict:
    wb: Workbook = openpyxl.open(filename=file)
    ws: Worksheet = wb.worksheets[0]
    task_list = []
    row: int = 1
    while ws.cell(1, row).value is not None:
        task_list.append(ws.cell(1, row).value)
    return {
        'task_count': row,
        'task_list': task_list
    }
