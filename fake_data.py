from faker import Faker
import pandas as pd
from itertools import cycle
from sqlalchemy import create_engine
import random


quarters = [(year, quarter) for year in range(2010, 2025) for quarter in range(1, 5)]
random.shuffle(quarters)  # Shuffle the quarters to randomize the order

# Create a Faker instance
fake = Faker()

engine = create_engine('mssql+pyodbc://DESKTOP-UMHE8LJ\SQLEXPRESS/ARMISDatabase2024?driver=SQL+Server+Native+Client+11.0')

# Query the database to get the unique values of the column
df = pd.read_sql_query("SELECT DISTINCT username FROM stg2.ColaboradoresMerged", con=engine)


# Define a function to generate a single row of data
def generate_row():
    random_value = random.choice(df['username'].tolist())
    year, quarter = random.choice(quarters)
    absolute_quarter = (year - 2010) * 4 + quarter
    multiplier = 1 + 0.05 * (absolute_quarter - 1)
    fiscal_month = ((quarter - 1) * 3) + random.choice(range(1, 4))

    cod_mov = fake.random_element(elements=('R01', 'R11', 'R13', 'R30', 'R31', 'D90', 'R08', 'R34', 'R36', 'R02', 'R42', 'R19', 'R22', 'R37', 'R33', 'D01', 'D20', 'D21','R27'))
    valor_generators = {
        'R01': lambda: int(fake.random_int(min=800, max=1000) * multiplier),
        'R13': lambda: int(fake.random_int(min=10, max=15) * multiplier),
        'D01': lambda: int(fake.random_int(min=5, max=95) * multiplier),
        'D02': lambda: int(fake.random_int(min=5, max=95) * multiplier),
        'D05': lambda: int(fake.random_int(min=10, max=30) * multiplier),
        'R30': lambda: int(fake.random_int(min=50, max=100) * multiplier),
        'R31': lambda: int(fake.random_int(min=50, max=200) * multiplier),
        'R11': lambda: int(fake.random_int(min=20, max=80) * multiplier),
        'D90': lambda: int(fake.random_int(min=15, max=55) * multiplier),
        'R08': lambda: int(fake.random_int(min=10, max=20) * multiplier),
        'R34': lambda: int(fake.random_int(min=200, max=300) * multiplier),
        'R36': lambda: int(fake.random_int(min=13, max=19) * multiplier),
        'R02': lambda: int(fake.random_int(min=5, max=20) * multiplier),
        'R42': lambda: int(fake.random_int(min=100, max=150) * multiplier),
        'R19': lambda: int(fake.random_int(min=10, max=30) * multiplier),
        'R22': lambda: int(fake.random_int(min=40, max=55) * multiplier),
        'R37': lambda: int(fake.random_int(min=60, max=85) * multiplier),
        'R33': lambda: int(fake.random_int(min=10, max=33) * multiplier),
        'D20': lambda: int(fake.random_int(min=100, max=600) * multiplier),
        'D21': lambda: int(fake.random_int(min=40, max=59) * multiplier),
        'R27': lambda: int(fake.random_int(min=100, max=600) * multiplier),
    }

    valor = valor_generators[cod_mov]()
    return [
        cod_mov,
        random_value,
        valor,
        quarter,
        fiscal_month,
        fake.random_int(min=1, max=3),
        valor * 0.1, #Segurança social é 10% do valor
        year  
    ]

# Generate multiple rows of data
data = [generate_row() for _ in range(100000)]

# Convert the list of rows into a pandas DataFrame
df = pd.DataFrame(data, columns=['CodMov', 'Funcionario', 'Valor','Quarter', 'MesFiscal', 'TipoTabela', 'ValorSegSocialEntPatronal', 'Ano'])

df.to_sql('MovimentosFuncionarios', con=engine, if_exists='replace', index=False, schema='primavera')# Print the DataFrame
print(df)