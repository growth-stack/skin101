import calendar
import base64
import logging
import json
import random
from datetime import datetime, timedelta
from xlrd import open_workbook,  xldate_as_tuple

from odoo import api, models, fields, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, date_utils
from odoo.exceptions import AccessError, UserError, ValidationError



_logger = logging.getLogger(__name__)

def format_to_odoo_date(date_str: str) -> str:
    """Formats date format mm/dd/yyyy eg.07/01/1988 to %Y-%m-%d
        OR  date format yyyy/mm/dd to  %Y-%m-%d
    Args:
        date (str): date string to be formated

    Returns:
        str: The formated date
    """
    if not date_str:
        return

    data = date_str.split('/')
    if len(data) > 2 and len(data[0]) ==2: #format mm/dd/yyyy
        try:
            mm, dd, yy = int(data[0]), int(data[1]), data[2]
            if mm > 12: #eg 21/04/2021" then reformat to 04/21/2021"
                dd, mm = mm, dd
            if mm > 12 or dd > 31 or len(yy) != 4:
                return
            return f"{yy}-{mm}-{dd}"
        except Exception:
            return

    if len(data) > 2 and len(data[0]) == 4: #format yyyy/mm/dd
        try:
            yy, mm, dd = int(data[0]), int(data[1]), data[2]
            if mm > 12: #eg 2021/21/04" then reformat to 2021/04/21"
                dd, mm = mm, dd
            if mm > 12 or dd > 31 or len(yy) != 4:
                return
            return f"{yy}-{mm}-{dd}"
        except Exception:
            return

def cast_to_integer(float_val):
    """Convert float to integer
    Args:
        val (float): The item to convert
    Returns:
        int: the converted item
    """
    return int(float_val) if isinstance(float_val, float) else float_val

def convert_excel_date(excel_date, workbook):
    if excel_date:
        if type(excel_date) is not str:
            try:
                dt = datetime(*xldate_as_tuple(excel_date, workbook.datemode))
            except Exception as ex:
                raise ValidationError(f"Invalid {excel_date}. The  must be a VALID EXCEL DATE format. " 
                "Please check the format of the date column  and also ensure you are uploading the correct template")
        else:
            dt = fields.Date.from_string(format_to_odoo_date(excel_date))

        return  dt
    else:
        return False
    
    

class Migration(models.TransientModel):
    _name = 'wizard.migration'
    _description = 'migration'

    @api.constrains('file')
    def _check_file(self):
        ext = str(self.file_name.split(".")[1])
        if ext and ext not in ('xls', 'xlsx'):
                raise ValidationError("You can only upload excel sheets")
            
            
    file = fields.Binary(string="Select File", required=True)
    file_name = fields.Char("File Name")
    
    
    def action_migrate(self):
        '''Reads and returns the file data 
        Appointment Id	Date of Diagnosis	Hospital	Patient	State	Findings
        '''
        if not self.file:
            raise ValidationError('Please select file and type of file')

        file_datas = base64.decodebytes(self.file)
        workbook = open_workbook(file_contents=file_datas)
        sheet = workbook.sheet_by_index(0)
        file_data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
        file_data.pop(0)
    
        for count, row in enumerate(file_data):
            if row[0] != "":
                _logger.info(f"importing row ... {count + 2}")
                appointment_no = row[0]
                date_diagnosis = convert_excel_date(row[1], workbook)
                hospital = row[2]
                patient = row[3]
                state = row[4]
                findings = row[5]
                
                patient = self.get_or_create_patient(patient)
                
                vals = {
                    'legacy_appointment_no': appointment_no,
                    'complaint_date': date_diagnosis,
                    'patient_id': patient.id,
                    'complaint': findings,
                    'complaint_subject': 'Patient complaint',
                }
                # Check if complaint already exists
                complaint = self.env['patient.complaint'].search([('legacy_appointment_no', '=', appointment_no)])  
                if not complaint:
                    self.env['patient.complaint'].create(vals)
                else:
                    complaint.write(vals)
        return True
    
    def get_or_create_patient(self, name):
        patient = self.env['medical.patient'].search([('partner_id.name', '=', name)], limit=1)
        if not patient:
            partner = self.env['res.partner'].create({'name': name})
            seq = self.env['ir.sequence'].next_by_code('medical.patient')
            patient = self.env['medical.patient'].create({'partner_id': partner.id, 'patient_id': seq})
        return patient
    
    