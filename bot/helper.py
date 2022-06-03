from datetime import datetime, timedelta
from models import ScrappingStatus, Session
import csv


def diff_more_than_3_hours(date_1, date_2, hours_difference=3):
    if (date_1 - timedelta(hours=hours_difference)) >= date_2:
        return True
    return False

def checkScrappingStatus():
    with Session as session:
        scrapping_status=session.query(ScrappingStatus).first() 
        return scrapping_status.finished_scrapping, diff_more_than_3_hours(datetime.now(), scrapping_status.last_scrapped)

def updateScrappingStatus():
    with Session as session:
        scrapping_status=session.query(ScrappingStatus).first() 
        scrapping_status.last_scrapped = datetime.now()
        scrapping_status.finished_scrapping = True
        session.commit()

def saveDataToCSV(model, filename):
    with open(f'{filename}.csv', 'w') as outfile:
        with Session as session:
            outcsv = csv.writer(outfile)
            records = session.query(model).all()
            outcsv.writerow([column.name for column in model.__mapper__.columns])
            [outcsv.writerow([getattr(curr, column.name) for column in model.__mapper__.columns]) for curr in records]
            