import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description

class CSV:
  CSV_FILE = 'finance_data.csv'
  COLUMNS = ['date', 'amount', 'category', 'description']
  FORMAT = '%d-%m-%Y'

  @classmethod
  def initialize_csv(cls):
    try:
      pd.read_csv(cls.CSV_FILE)
    except FileNotFoundError:
      df = pd.DataFrame(columns= cls.COLUMNS )
      df.to_csv(cls.CSV_FILE, index=False )

  @classmethod
  def add_entry(cls, date, amount, category, description):
    # Using disctionary to write into the correct columns when we use csv writer. 
    new_entry = {
      'date': date,
      'amount': amount,
      'category': category,
      'description': description
    }
    # 'a' appending to the end of the file
    with open(cls.CSV_FILE, 'a', newline='') as csvfile:
      # Taking the dictionary and write that in csv file
      writer = csv.DictWriter(csvfile, fieldnames= cls.COLUMNS)
      writer.writerow(new_entry)
    print('Entry added successfuly!')


  @classmethod
  def get_transactions(cls, start_date, end_date):
    df = pd.read_csv(cls.CSV_FILE)
    # Converte dates inside date column into datetime object to use them to filter by different transactions
    df['date'] = pd.to_datetime(df['date'], format = CSV.FORMAT)
    # Date that was given is in a form of str, we want to convert it to the right format
    start_date = datetime.strptime(start_date, CSV.FORMAT)
    end_date = datetime.strptime(end_date, CSV.FORMAT)
    # We can compare dates, which we couldn't do if date was sting
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_df = df.loc[mask]

    if filtered_df.empty:
      print("No transactions found in given data range!")
    else:
      print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
      print(filtered_df.to_string(index = False, formatters = {'date': lambda x : x.strftime(CSV.FORMAT)}))

      total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
      total_expense = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()
      print('\nSummary:')
      print(f"Total Income: ${total_income:.2f}")
      print(f"Total Expense: ${total_expense:.2f}")
      print(f"Total Savings: ${(total_income - total_expense):.2f}")

    return filtered_df


# f that will call f in the order that we want in order to colect our data
def add():
  CSV.initialize_csv()
  date = get_date("Enter the date of transaction", allow_default=True)
  amount = get_amount()
  category = get_category()
  description = get_description()
  CSV.add_entry(date, amount, category, description)

CSV.get_transactions("06-07-2024", "07-08-2024")
