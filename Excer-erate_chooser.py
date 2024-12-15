import csv
import pandas as pd

def trim_dictionary(input_dict, target_size):
    removed_items = {}
    while len(input_dict) > target_size:
        key, value = input_dict.popitem()
        removed_items[key] = value
    return input_dict, removed_items

def applicantaccepter(target_size):
    #Read CSV file and created a dataframe
    df = pd.read_csv(r'Excel-erate Application.csv')

    acceptedPatrons = {}

    while len(acceptedPatrons) < target_size:
        for i in range(len(df)):
            # TODO: Check for applicants who did not agree to terms, and do not have access to required tech
            # Check for age, commitment, duplicates and for an email
            if (df.iloc[i, 3] == 'Yes' and df.iloc[i, 5] == 'Yes' and df.iloc[i, 2] not in acceptedPatrons
                    and not pd.isnull(df.iloc[i, 1])):

                # Check if there are less than 20 people applied
                if len(df) <= target_size:
                    acceptedPatrons.update({df.iloc[i, 2] : df.iloc[i, 1]})

                # Check for income level
                elif df.iloc[i, 13] == 'Less than $20,000' and len(acceptedPatrons) <= target_size:
                    acceptedPatrons.update({df.iloc[i, 2] : df.iloc[i, 1]})

                # Check for lower education groups
                elif ((df.iloc[i, 11] == 'No High School' or df.iloc[i, 11] == 'Some High School' or
                      df.iloc[i, 11] == 'High School/GED' or df.iloc[i, 11] == 'Some College but no degree') and
                      len(acceptedPatrons) <= target_size):
                    acceptedPatrons.update({df.iloc[i, 2] : df.iloc[i, 1]})

                # Check for underrepresented gender and identities
                elif ((df.iloc[i, 11] == 'Female' or df.iloc[i, 11] == 'Non-binary/third gender' or
                       df.iloc[i, 11] == 'Cisgender' or df.iloc[i, 11] == 'Agender' or
                       df.iloc[i, 11] == 'Genderqueer' or df.iloc[i, 9] == 'Asian' or
                       df.iloc[i, 9] == 'Black, non-Hispanic' or df.iloc[i, 9] == 'Hispanic/Latino' or
                       df.iloc[i, 9] == 'Native Hawaiian/Pacific Islander' or df.iloc[i, 9] == 'Native American')
                       and len(acceptedPatrons) <= target_size):
                    acceptedPatrons.update({df.iloc[i, 2]: df.iloc[i, 1]})

                if len(acceptedPatrons) < target_size:
                    acceptedPatrons.update({df.iloc[i, 2] : df.iloc[i, 1]})

    if target_size < len(acceptedPatrons):
        acceptedPatrons, waitlistedPatrons = trim_dictionary(acceptedPatrons, target_size)
    else:
        waitlistedPatrons = {}

    return acceptedPatrons, waitlistedPatrons

def main():
    # TODO: have the input checked for any letters or symbols, and removed
    target_size = int(input("Enter the maximum size of the class: ").strip())
    if target_size < 1:
        while target_size < 1:
            target_size = int(input("Please enter a number greater than 0: "))
    acceptedPatrons, waitlistedPatrons = applicantaccepter(target_size)
    with open('acceptedPatrons.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Email', 'Waitlisted Name', 'Waitlisted Email'])
        for name, email in acceptedPatrons.items():
            for waitlistedName, waitlistedEmail in waitlistedPatrons.items():
                writer.writerow([name, email, waitlistedName, waitlistedEmail])


if __name__ == '__main__':
    main()