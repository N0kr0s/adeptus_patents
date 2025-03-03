from data_processing import process_excel_and_save

excel_file_path = '../data/gp-search-20250301-010925.xlsx'
csv_file_path = '../data/patents.csv'

process_excel_and_save(excel_file_path, csv_file_path)