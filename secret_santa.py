import random # For random number generating
# These imports are for sending email:
from email.message import EmailMessage
import ssl
import smtplib

# Lower value for reciprocal_probability means that it is less likely
def name_assignment(names, reciprocal_probability=0.2): 
    shuffled_names = names.copy()
    random.shuffle(shuffled_names)

    def assign_names(index):  # Nested recursive function
        if index == len(shuffled_names): # Base case
            return True
        
        person = shuffled_names[index]
        if person[5]:  # Check if the person has a preference
            for i in range(len(shuffled_names)):
                if person[5] == shuffled_names[i][0]: # If there is a preference, this finds the name of the preferred assignment
                    assignment = shuffled_names[i]
                    if (
                        person[1] != assignment[1]  # Family number should not match
                        and not assignment[3]  # Assignment should not be assigned
                    ):
                        shuffled_names[index][2] = i
                        shuffled_names[i][3] = True
                        if assign_names(index + 1): # Recursive step
                            return True
                        shuffled_names[index][2] = 999  # Backtrack
                        shuffled_names[i][3] = False
                    return False

        for k in range(len(shuffled_names)):
            assignment = shuffled_names[k]

            if (
                person[1] != assignment[1]  # Family number should not match
                and not assignment[3]  # Person cannot already be assigned
                # and shuffled_names[k][2] != index  # Avoid reciprocal assignments
                and (k != index or random.random() <= reciprocal_probability)  # Allows for chance of reciprocal assignments
            ):
                shuffled_names[index][2] = k  # Assignment is made
                shuffled_names[k][3] = True   # Notes that the person has now been assigned to someone

                if assign_names(index + 1): # Recursive step
                    return True
                
                shuffled_names[index][2] = 999  # Backtrack in case of the previous if statement returning False
                shuffled_names[k][3] = False

        return False
    if assign_names(0): # Calls recursive function (wants the function to return true)
        return shuffled_names # Returns the assignments


def print_assignments(assigned):
    for i in range(len(assigned)):
        assignment = assigned[i][2]
        print(assigned[i][0], "is assigned", assigned[assignment][0])


def send_email_person(person, assignments): # Sends an assignment email to one person at a time.
    sender = "email_name@mail.com" 
    password = "password here"
    reciever = person[4]
    subject = f"Find out who your person for the Gift Exchange is, {person[0]}!"

    your_person = assignments[person[2]][0]

    body = f"Your person is {your_person}! Make it known if this seems like an error!"

    em = EmailMessage()
    em['From'] = sender
    em['To'] = reciever
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, reciever, em.as_string())


def send_email_master(adult_assignments, kid_assignments, email):
    sender = "email_name@mail.com"
    password = "password here"
    reciever = email

    subject = f"Here is the full list of assignments!"

    adultss = ""
    for i in range(len(adult_assignments)):
        assignment = adult_assignments[i][2]
        adultss += f"\n{adult_assignments[i][0]} is assigned {adult_assignments[assignment][0]}"

    kidss = ""
    for i in range(len(kid_assignments)):
        assignment = kid_assignments[i][2]
        kidss += f"\n{kid_assignments[i][0]} is assigned {kid_assignments[assignment][0]}"

    all = f"{adultss} \n {kidss}"
    body = all

    em = EmailMessage()
    em['From'] = sender
    em['To'] = reciever
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, reciever, em.as_string())


# array item format: [name, family number, assignment number placeholder, assigned(T/F), email, assignment preference]
adults = [["Bart", 1, 999, False, "email_name@mail.com", "Bradan"], ["Evelyn", 1, 999, False, "email_name@mail.com", ""], 
        ["Trevor", 2, 999, False, "email_name@mail.com", ""], ["Charlotte", 2, 999, False, "email_name@mail.com", ""],
        ["Josh", 3, 999, False, "email_name@mail.com", ""], ["Emily (Josh's Wife)", 3, 999, False, "email_name@mail.com", ""], 
        ["Bradan", 4, 999, False, "email_name@mail.com", ""], ["Haley", 4, 999, False, "email_name@mail.com", ""],
        ["Jakob", 5, 999, False, "email_name@mail.com", ""], ["Emily (Bart's Daughter)", 1, 999, False, "email_name@mail.com", ""]]

kids = [["Hannah", 1, 999, False, "email_name@mail.com", ""], ["Alice", 1, 999, False, "email_name@mail.com", ""], 
        ["Owen", 1, 999, False, "email_name@mail.com", ""], ["Oliver", 1, 999, False, "email_name@mail.com", ""],
        ["James", 2, 999, False, "email_name@mail.com", ""], ["Sam", 2, 999, False, "email_name@mail.com", ""], 
        ["Sophie", 2, 999, False, "email_name@mail.com", ""], ["Emma", 2, 999, False, "email_name@mail.com", ""],
        ["Charly", 3, 999, False, "email_name@mail.com", ""]]

assigned_adults = name_assignment(adults)
assigned_kids = name_assignment(kids)

if assigned_adults:
    print("Successful assignments:")
    print_assignments(assigned_adults)
    print()
    print_assignments(assigned_kids)

    # Code for sending the emails:
    # for i in range(len(assigned_adults)):
    #     send_email_person(assigned_adults[i], assigned_adults)

    # for i in range(len(assigned_kids)):
    #     send_email_person(assigned_kids[i], assigned_kids)

    # send_email_master(assigned_adults, assigned_kids, "hdowdle23@gmail.com")
else:
    print("No valid assignments found.")


