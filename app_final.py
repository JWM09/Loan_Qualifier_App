# -*- coding: utf-8 -*-
# Purpose of application is to match applicants with available loans
#based on the criteria they input

# the following libraries are required for the operation of this program
import sys
import fire
import questionary
import csv
from pathlib import Path

# to support modularity we have created funtions to better build out the logic of the applicatoin
from qualifier.utils.fileio import load_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value



# Here we load the master list of all loans currently available to all clients
def load_bank_data():
  
    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)

# Here we ask the client to enter their information that will be used to filter to loans that meet their criteria 
def get_applicant_info():

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value

# This function identifies the various loans available based on the criteria entered above
def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    
    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered

# Once available loans have been identified, the program asks the user if they want to save the list of available loans
def save_qualifying_loans(qualifying_loans):
  
    data_save = questionary.confirm("would you like to save your qualified loans?").ask()

    if data_save:
        csvpath = questionary.text("Where do you want to save your loan (file path)? ").ask()
        csvpath = Path(csvpath)
    else:
        sys.exit(f"Thank you for researching loans.")
    return save_csv(csvpath, qualifying_loans)

# This function builds on the above, and creates the new csv file
def save_csv(csvpath, data, header=None):
    with open(csvpath, 'w', newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",") 
        #csvwriter.writerow(header)
        
        csvwriter.writerow(data)

# This is where I am not understanding the structure of the program 
def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)


if __name__ == "__main__":
    fire.Fire(run)


