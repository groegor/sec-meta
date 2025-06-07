from secmeta import Submissions

# Either use CIK
#df_cik = Submissions(cik="0001288776", form="10-K", name="John Doe", email="example@email.com").to_dataframe()

# Or Ticker Symbol to indentify a single company
#df_ticker = Submissions(ticker="GOOGL", form="10-K", name="John Doe", email="example@email.com").to_dataframe()


df_csv = Submissions(csv_path="input_companies.csv", form="10-k", year_from = 2015, year_to = 2025, name="Your Name", email="johndoe@example.com").to_dataframe()

# Result
print(list(df_csv))
print(df_csv.head(5))

df_csv.to_csv("output_companies.csv", sep=",")
