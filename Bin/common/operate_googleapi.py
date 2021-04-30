import os
import pickle
import webbrowser
import pprint
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
# import stk00100_iniget as Ini

from common.make_log import setup_logger

logger = setup_logger(__name__)

class GoogleCommon():
    service = None
    def Authentication(self, TokenPikkle, CreadentialJson, Scopes, GoogleAPIType):

        GoogleVerDic = {'sheets':'v4', 'docs':'v1','Script': 'v1', 'Drive':'v3'}
        GoogleVersion = GoogleVerDic[GoogleAPIType]

        creds=None
        if os.path.exists(TokenPikkle):
            with open(TokenPikkle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except:
                    if not creds.requires_scopes:
                        os.remove(TokenPikkle)
                        flow = InstalledAppFlow.from_client_secrets_file(CreadentialJson, Scopes)
                        creds = flow.run_local_server(port=0)
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CreadentialJson, Scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TokenPikkle, 'wb') as token:
                pickle.dump(creds, token)
        self.service = build(GoogleAPIType, GoogleVersion, credentials=creds)


class SpreadSheet(GoogleCommon):
    def CheckExists(self, SpreadSheetId, SheetName):
        worksheets = self.service.spreadsheets().get(spreadsheetId=SpreadSheetId, fields="sheets").execute()
        for sheet in worksheets['sheets']:
            if SheetName == sheet['properties']['title']:
                return sheet['properties']['sheetId']
        return False

    def DeleteSheets(self, SpreadSheetId, ExistFile):
        requests = []
        requests.append({
            "deleteSheet": {
                "sheetId": ExistFile
                }
            })
        body = {'requests':requests}
        response = self.service.spreadsheets().batchUpdate(spreadsheetId=SpreadSheetId, body=body).execute()

    def AddSheets(self, SpreadSheetId, SheetName):
        # シートの作成
        requests = []
        requests.append({
            'addSheet':{
                "properties":{
                    "title": SheetName,
                    "index": "0",
                    }

                }
            })

        body = {'requests':requests}
        response = self.service.spreadsheets().batchUpdate(spreadsheetId=SpreadSheetId, body=body).execute()
        sheetid = response['replies'][0]['addSheet']['properties']['sheetId']
        return sheetid
    
    def Write(self, SpreadSheetId, StartCol, ColLength, StartRow, RowLength, Values):
        #セルに文字列を入れる
        EndRow = StartRow + (RowLength - 1)
        StartCol = StartCol + 64
        EndCol = StartCol + (ColLength - 1)
        if ColLength >= 27 or ColLength <= 0:
            try:
                raise ValueError("ValueError!")
            except ValueError as e:
                logger.error(e)
        body={}
        body['range'] = Ini.vgsSS_SheetName + "!" + chr(StartCol) +str(StartRow)+":"+chr(EndCol)+str(EndRow)
        body['majorDimension']="ROWS"
        body['values']=Values


        value_input_option = 'USER_ENTERED'
        insert_data_option = 'OVERWRITE'
        result = self.service.spreadsheets().values().update(spreadsheetId=SpreadSheetId, range=body['range'], valueInputOption=value_input_option, body=body).execute()

    def ChangeFormat(self, SpreadSheetId, vgsSheetId):
        requests = []#セルのフォーマットを変更する
        requests.append({
            "updateBorders":{
                "range": {
                    "sheetId": vgsSheetId,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 2,
                    },
                "bottom": {
                    "style": "SOLID",
                    "width": "1",
                    "color": { "red": 0, "green":0, "blue":0 },
                    },
                },
            })
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": vgsSheetId,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 2,
                    },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment" : "LEFT",
                        "textFormat": {
                            "fontSize": 11,
                            "bold": True,
                            "foregroundColor": {
                                "red": 1.0,
                                },
                            }
                        }
                    },
                "fields": "userEnteredFormat(textFormat,horizontalAlignment)"
                },
            })
        body = { 'requests': requests }
        response = self.service.spreadsheets().batchUpdate(spreadsheetId=SpreadSheetId, body=body).execute()

class Docs(GoogleCommon):
    def main(self, title, text):
        body = {
            "title":title
        }
        doc = self.service.documents().create(body=body).execute()
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': text
                }
            }
        ]
        document_id = doc.get('documentId')
        url = 'https://docs.google.com/document/d/' + document_id
        self.service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        webbrowser.open(url)

class GAS(GoogleCommon):
    def runGAS(self, script_id, function_name, function_params):
        import requests
        import json
        request = {
            "function": function_name, 
            "parameters": function_params,
            "devMode": True
            } # ← 関数名は自分が作ったもの
        response = self.service.scripts().run(body=request, scriptId=script_id).execute()

    def display_image_tmp(self, SS_id, SS_sheet_name, image_ids):
        image_length = len(image_ids)
        SS_info = dict()
        SS_info["SS_id"] = SS_id
        SS_info["SS_sheet_name"] = SS_sheet_name
        ROW_HEIGHT = 350
        Row_WIDTH= 600
        terget_cells_list = []  
        target_row_list = []
        images_list = []
        row_height_list = []
        row_width_list = []
        for i in range(image_length):
            terget_row_line = i + 1
            if i % 2 ==0:
                terget_cells_list.append("A" + str(i//2 + 1))
            else:
                terget_cells_list.append("B" + str(i//2 + 1))
            images_list.append("=image(\"https://drive.google.com/uc?export=view&id="
            + image_ids[i] +"\",1)")
            target_row_list.append(terget_row_line)
            row_height_list.append(ROW_HEIGHT)
            row_width_list.append(Row_WIDTH)

        SS_info["SS_cell_name"] = terget_cells_list
        SS_info["SS_function_value"] = images_list
        SS_info["SS_cell_row"] = target_row_list
        SS_info["SS_row_height"] = row_height_list
        SS_info["SS_row_Width"] = row_width_list

        return SS_info

    def display_image(self, GAS_id, SS_info, image_ids):
        image_length = len(image_ids)
        for i in range(image_length):
            SS_fucntion_params = [
                SS_info["SS_id"],
                SS_info["SS_sheet_name"],
                SS_info["SS_cell_name"][i],
                SS_info["SS_function_value"][i],
                4
            ]
            self.runGAS(GAS_id, "DisplayImage", SS_fucntion_params)

            SS_fucntion_params = [
                SS_info["SS_id"],
                SS_info["SS_sheet_name"],
                SS_info["SS_cell_name"][i],
                SS_info["SS_row_height"][i],
                SS_info["SS_row_Width"][i],
                5
            ]
            self.runGAS(GAS_id, "resizeCellSize", SS_fucntion_params)

class Drive(GoogleCommon):
    def list_drive_files(self, **kwargs):
        results = self.service.files().list(**kwargs).execute()
        return results

    def list_drive_fileids(self, folder_id):
        results = self.service.files().list(fields='*', q=f"'{folder_id}' in parents").execute()
        fileids = []
        filenames=[]
        for i in range(len(results['files'])):    
            filenames.append(results['files'][i]['name'])
            fileids.append(results['files'][i]['id'])
        return fileids

    def get_drive_fileid(self, folder_id, file_name):
        results = self.service.files().list(fields='*', q=f"'{folder_id}' in parents").execute()
        fileids = []
        for i in range(len(results['files'])):    
            if results['files'][i]['name'] == file_name:
                fileids.append(results['files'][i]['id'])
        return fileids
        

    def get_drive_folder_id(self, folder_path):
        """指定パスフォルダのfileIdを取得"""
        parent_id = 'root'
        for name in folder_path:
            res = self.list_drive_files(q=f"'{parent_id}' in parents and "
                                "mimeType = 'application/vnd.google-apps.folder' and "
                                f"name = '{name}'")
            if 'files' not in res or len(res['files']) < 1:
                return None
            parent_id = res['files'][0]['id']
    
        return parent_id
 
    def upload_file(self, local_file, remote_folder_id='root', mimetype='image/PNG'):
        media = MediaFileUpload(local_file, mimetype=mimetype)
        file = self.service.files().create(body={'name': os.path.basename(local_file),
                                            'parents': [remote_folder_id]},
                                    media_body=media,
                                    fields='id').execute()
        logger.info(f'File ID: {file.get("id")}')

    def delete_file(self, file_id):
        file = self.service.files().delete(fileId=file_id).execute()
     

if __name__ == '__main__':

    import sys
    sys.path.append(os.path.abspath("D:/User_Application/STK00100/Bin"))
    import stk00100_iniget as Ini
    from stk00100_iniget import vgfGetIni
    vgfGetIni()

    Type = "Drive"

    if Type == "Docs":
        Docs = Docs()
        Docs.Authentication(Ini.vgsDocs_TokenPikkleFile, Ini.vgsDocs_CreadentialJsonFile, Ini.vgsDocs_Scopes, 'docs')
        Docs.main('AA','BB')
    elif Type == "GAS":
        image_ids = [
            "15E1lgH_al6zN3nuZF2f2FV31xcGcBEuk",
            "15E1lgH_al6zN3nuZF2f2FV31xcGcBEuk",
            "15E1lgH_al6zN3nuZF2f2FV31xcGcBEuk"
        ]
        GAS_ID ="MjmckVh8J08SF7AsuqPnbxOyjeZo2-uJT"
        SS_SHEET_NAME = "シート1"   
        SS_ID = "1Y7uKyR2852oR9JCAmwZJoNgcG0hAioBWbiSCgZLmJUE"

        GAS = GAS()
        GAS.Authentication(Ini.vgsGAS_TokenPikkleFile, Ini.vgsGAS_CreadentialJsonFile, Ini.vgsGAS_Scopes, 'Script')

        SS_info_dict = GAS.display_image_tmp(SS_ID, SS_SHEET_NAME)
        GAS.display_image(GAS_ID, SS_info_dict)

    elif Type == "SpreadSheet":
        SS = SpreadSheet()
        SS.Authentication(Ini.vgsSS_TokenPikkleFile, Ini.vgsSS_CreadentialJsonFile, Ini.vgsSS_Scopes, 'sheets')
        SS.CheckExists("AA", "BB")

    elif Type == "Drive":
        drive = Drive()
        drive.Authentication(Ini.vgsDrive_TokenPikkleFile, Ini.vgsDrive_CreadentialJsonFile, Ini.vgsDrive_Scopes, 'Drive')


        # logger.error(image_ids)

        # for image_id in image_ids:
        #     drive.delete_file(image_id)

    
    else:
        logger.error("ERROR")

    
else:
    import stk00100_iniget as Ini


        
