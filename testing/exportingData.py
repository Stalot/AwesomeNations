from awesomeNations import AwesomeNations
from awesomeNations.customMethods import join_keys
from typing import Iterator
import csv
import pandas as pd

def ReadCsv(filepath: str) -> Iterator:
    with open(str(filepath), 'r', encoding='utf-8') as csvfile:
        read_data = csv.DictReader(csvfile)
        for line in read_data:
            yield line

def WriteCsv(filepath: str  = None, fieldnames: list = None, content: list = None) -> None:
    with open(str(filepath), 'w', newline='', encoding='utf-8') as csvfile:
        csv_fieldnames = fieldnames if fieldnames != None else [key for key in content[0]]
        writer = csv.writer(csvfile)
        writer.writerow(csv_fieldnames)
        for row in content:
            row_values = [row[key] for key in row]
            writer.writerow(row_values)

def main():
    awn = AwesomeNations("AwesomeNations/0.1.0 (by:Orlys; usedBy:Orlys)")
    nation_name = "orlys"
    shards_data = awn.Nation(nation_name).get_public_shards('census', scale="all")
    shards_data = shards_data['nation']['census']['scale']
    
    csv_filepath = "junk/census.csv"
    excel_filepath = f"junk/{nation_name} census.xlsx".lower()
    
    WriteCsv(csv_filepath, ["id", "score", "w rank", "r rank"], shards_data)
    pd.read_csv(csv_filepath, delimiter=",").to_excel(excel_filepath,
                                                           index=False,
                                                           freeze_panes=(1, 0),
                                                           sheet_name=f"Nation census statistics",
                                                           )
    
    for row in ReadCsv("junk/census.csv"):
        print(row)
        input("Next row...")

main()