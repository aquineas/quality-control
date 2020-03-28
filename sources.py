from typing import List, Dict
from loguru import logger
import pandas as pd

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY_PATH = "credentials-scanner.json"

class GoogleWorksheet():

    def __init__(self, trace= True):
        logger.info("load credentials")

        # pylint: disable=no-member
        self.creds = service_account.Credentials.from_service_account_file(
            KEY_PATH,
            scopes=SCOPES)

        self.trace = trace
        if self.trace:        
            logger.info(f"  email {self.creds.service_account_email}")
            logger.info(f"  project {self.creds.project_id}")
            logger.info(f"  scope {self.creds._scopes[0]}")
            logger.info("")
            logger.warning(" **** The private key for this identify is published in a public Github Repo")
            logger.warning(" **** DO NOT ALLOW ACCESS TO SENSITIVE/PRIVATE RESOURCES")
            logger.warning(" **** DO NOT ALLOW WRITE ACCESS ANYTHING")
            logger.info("")

        if self.trace: logger.info("connect")
        service = build('sheets', 'v4', credentials=self.creds)
        self.sheets = service.spreadsheets()


    def get_sheet_id_by_name(self, name: str) -> str:
        items = {
            "dev": {
                "id": "1MvvbHfnjF67GnYUDJJiNYUmGco5KQ9PW0ZRnEP9ndlU",
                "url": "https://docs.google.com/spreadsheets/d/1MvvbHfnjF67GnYUDJJiNYUmGco5KQ9PW0ZRnEP9ndlU/edit#gid=1777138528"
            },
            "instructions": {
                "id": "1lGINxyLFuTcCJgVc4NrnAgbvvt09k3OiRizfwZPZItw",
                "url": "https://docs.google.com/document/d/1lGINxyLFuTcCJgVc4NrnAgbvvt09k3OiRizfwZPZItw/edit"
            },
            "pubished": {
                # not sure if this ID is right - Josh
                "id": "2PACX-1vRwAqp96T9sYYq2-i7Tj0pvTf6XVHjDSMIKBdZHXiCGGdNC0ypEU9NbngS8mxea55JuCFuua1MUeOj5",
                "url": "https://docs.google.com/spreadsheets/u/2/d/e/2PACX-1vRwAqp96T9sYYq2-i7Tj0pvTf6XVHjDSMIKBdZHXiCGGdNC0ypEU9NbngS8mxea55JuCFuua1MUeOj5/pubhtml"
            }
        }

        rec = items.get(name)
        if rec == None:
            raise Exception("Invalid name {name}, should be one of " + ", ".join([x for x in items]))
        return rec["id"]


    def read_values(self, sheet_id: str, cell_range: str) -> List[List]:
        " read results as a list of lists"
        
        if self.trace: logger.info(f"read {cell_range}")
        result = self.sheets.values().get(spreadsheetId=sheet_id, range=cell_range).execute()
        #if self.trace: logger.info(f"  {result}")

        values = result.get('values', [])
        return values

    def read_as_frame(self, sheet_id: str, cell_range: str) -> pd.DataFrame:
        " read results as a data frame, first row is headers"
        
        values = self.read_values(sheet_id, cell_range)
    
        header = values[0]
        print(f"header: {header}")
        n_cols = len(header)

        data = [[] for n in header]
        for r in values[1:]:
            n_vals = len(r)
            if n_vals == 0: continue
            if n_vals < n_cols:
                logger.warning(f"fewer columns than expected ({n_cols})")
                logger.warning(f"  {r}")
            for i in range(n_vals):
                data[i].append(r[i])
            for i in range(n_vals, n_cols):
                data[i].append('')    

        xdict = {}
        for n, vals in zip(header, data): xdict[n] = vals
        return pd.DataFrame(xdict)


# --- a simple test
def main():


    gs = GoogleWorksheet(trace=True)
    id = gs.get_sheet_id_by_name("dev")
    values = gs.read_values(id, 'Worksheet!G3:L4')
    print(f"  {values}")

if __name__ == '__main__':
    main()