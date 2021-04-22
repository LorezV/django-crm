import pandas

xl = pandas.read_excel('./base.xlsx', sheet_name='Общ')
xl = xl.head().to_dict()
for col in xl:
    print(xl[col])