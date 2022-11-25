import streamlit as st
import pandas as pd 
from db_fxns import * 
import datetime
import streamlit.components.v1 as stc

def main():
    st.title("Hospital Database made by Bexultan Tokan for CSCI-341")
    menu = ["Create","Read","Update","Delete", "Queries"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Create":
        table_name = "DiseaseType"
        st.subheader("Add Item")
        table_name = st.selectbox("Table Name",["DiseaseType","Country","Disease","Discover","Users","PublicServant","Doctor","Specialize","Record"])
        if table_name == 'DiseaseType':
            id = st.text_input("ID")
            description = st.text_input("Description")
            if st.button("Add DiseaseType"):
                if id == '' or description == '':
                    st.warning("Please input all fields")
                elif id.isdigit() == False:
                    st.warning("ID must be a number")   
                elif not read_data(table_name).empty and str(id) in str(read_data(table_name)['id'].values):
                    st.warning("ID already exists")
                else:
                    add_data(table_name,[id, description])
                    st.success("Added ::{} ::To DiseaseType".format(description))
        elif table_name == 'Country':
            name = st.text_input("Name")
            population = st.text_input("Population")
            if st.button("Add Country"):
                if name == '' or population == '':
                    st.warning("Please input all fields")
                elif population.isdigit() == False:
                    st.warning("Population must be a number")
                elif not read_data(table_name).empty and name in read_data(table_name)['cname'].values:
                    st.warning("Country already exists")
                else:
                    add_data(table_name,[name, population])
                    st.success("Added ::{} ::To Country".format(name))
        elif table_name == 'Disease':
            if read_data('DiseaseType').empty:
                st.warning("Please add DiseaseType first")
            else:
                id = str(st.selectbox("ID",read_data('DiseaseType')['id'].values))
                disease_code = st.text_input("Disease Code")
                pathogen = st.text_input("Pathogen")
                description = st.text_input("Description")
                if st.button("Add Disease"):
                    if disease_code == '' or pathogen == '' or description == '':
                        st.warning("Please input all fields")
                    elif not read_data(table_name).empty and disease_code in read_data(table_name)['disease_code'].values:
                        st.warning("Disease Code already exists")
                    else:
                        add_data(table_name,[disease_code, pathogen, description, id])
                        st.success("Added ::{} ::To Disease".format(disease_code))
        elif table_name == 'Discover':
            if len(read_data('Country')) == 0 or len(read_data('Disease')) == 0:
                st.warning("Please add Country and Disease first")
            else:
                country_name = st.selectbox("Country Name",read_data('Country')['cname'].values)
                disease_code = st.selectbox("Disease Code",read_data('Disease')['disease_code'].values)
                date = st.date_input("Date", min_value=pd.to_datetime('1688-01-01'), max_value=pd.to_datetime(datetime.date.today()))
                if st.button("Add Discover"):
                    if not read_data(table_name).empty and disease_code in read_data(table_name)['disease_code'].values:
                        st.warning("Disease already was discovered")
                    else:
                        add_data(table_name,[country_name, disease_code, str(date)])
                        st.success("Added ::{} ::To Discover".format(country_name))
        elif table_name == 'Users':
            if read_data('Country').empty:
                st.warning("Please add Country first")
            else:
                email = st.text_input("Email")
                name = st.text_input("Name")
                surname = st.text_input("Surname")
                salary = st.text_input("Salary")
                phone = st.text_input("Phone")
                country = st.selectbox("Country", read_data('Country')['cname'].values)
                if st.button("Add Users"):
                    if email == '' or name == '' or surname == '' or salary == '' or phone == '' or country == '':
                        st.warning("Please input all fields")
                    elif salary.isdigit() == False:
                        st.warning("Salary must be a number")
                    elif not read_data(table_name).empty and email in read_data(table_name)['email'].values:
                        st.warning("Email already exists")
                    elif phone.isdigit() == False:
                        st.warning("Phone must be a number")
                    else:
                        add_data(table_name,[email, name, surname, salary, phone, country])
                        st.success("Added ::{} ::To Users".format(email))
        elif table_name == 'PublicServant':
            if read_data('Users').empty:
                st.warning("Please add Users first")
            email = st.selectbox("Email", read_data('Users')['email'].values)
            department = st.text_input("Department")
            if st.button("Add PublicServant"):
                if department == '':
                    st.warning("Please input all fields")
                elif not read_data(table_name).empty and email in read_data(table_name)['email'].values:
                    st.warning("Public Servant with this email already exists")
                else:
                    add_data(table_name,[email, department])
                    st.success("Added :: {} ::To PublicServant".format(email))
        elif table_name == 'Doctor':
            if read_data('Users').empty:
                st.warning("Please add Users first")
            email = st.selectbox("Email", read_data('Users')['email'].values)
            degree = st.text_input("Degree")
            if st.button("Add Doctor"):
                if degree == '':
                    st.warning("Please input all fields")
                elif not read_data(table_name).empty and email in read_data(table_name)['email'].values:
                    st.warning("Doctor with this email already exists")
                else:
                    add_data(table_name,[email, degree])
                    st.success("Added ::{} ::To Doctor".format(email))
        elif table_name == 'Specialize':
            if read_data('Doctor').empty or read_data('DiseaseType').empty:
                st.warning("Please add Doctor and DiseaseType first")
            email = str(st.selectbox("Email", read_data('Doctor')['email'].values))
            id = str(st.selectbox("ID", read_data('DiseaseType')['id'].values))
            if st.button("Add Specialize"):
                add_data(table_name,[id, email])
                st.success("Added :: {} ::To Specialize".format(email))
        elif table_name == 'Record':
            if read_data('Users').empty or read_data('Country').empty or read_data('Disease').empty:
                st.warning("Please add Users, Country and Disease first")
            email = st.selectbox("Email", read_data('Users')['email'].values)
            country = st.selectbox("Country", read_data('Country')['cname'].values)
            disease_code = st.selectbox("Disease Code", read_data('Disease')['disease_code'].values)
            total_deaths = st.text_input("Total Deaths")
            total_patients = st.text_input("Total Patients")
            if st.button("Add Record"):
                if total_deaths == '' or total_patients == '':
                    st.warning("Please input all fields")
                elif not total_deaths.isnumeric():
                    st.warning("Total Deaths must be a number")
                elif not total_patients.isnumeric():
                    st.warning("Total Patients must be a number")
                else:
                    add_data(table_name,[email, country, disease_code, total_deaths, total_patients])
                    st.success("Added ::{} ::To Record".format(email))
    elif choice == "Read":
        st.subheader("View Table")
        table_name = st.selectbox("Table Name",["DiseaseType","Country","Disease","Discover","Users","PublicServant","Doctor","Specialize","Record"])
        result = read_data(table_name)
        if result.empty:
            st.warning("No data available")
        else:
            st.write(result)
    elif choice == "Update":
        st.subheader("Update Table")
        table_name = st.selectbox("Table Name", ["DiseaseType","Country","Disease","Discover","Users","PublicServant","Doctor","Specialize","Record"])
        data = read_data(table_name)
        if len(data) == 0:
            st.warning("No data to update")
        else:
            st.write(data)
            row = st.text_input("Enter which row to update")
            if row == '':
                st.warning("Please input a row number")
            elif not row.isnumeric() or int(row) > len(data) or int(row) < 0:
                st.warning("Please input a valid row number")
            else:
                row = int(row)
                st.write('Unchangeable key ' + data.columns[0] + ': ', data.iloc[row,0])
                for i in range(1, len(data.columns)):
                    data.iloc[row,i] = st.text_input(data.columns[i],data.iloc[row,i])
                if st.button("Update"):
                    if len(data) == 0:
                        st.warning("Table is empty")
                    else:
                        update_data(table_name, row, data)
                        st.success("Updated Row {}".format(row))   
                        data = read_data(table_name)
                        st.header("Changed Table")
                        if len(data) == 0:
                            st.warning("Table is empty")
                        else:
                            st.write(data) 

    elif choice == "Delete":
        st.subheader("Delete Row")
        table_name = st.selectbox("Table Name", ["DiseaseType","Country","Disease","Discover","Users","PublicServant","Doctor","Specialize","Record"])
        st.header("Initial Table")
        data = read_data(table_name)
        if data.empty:
            print("Table is empty")
            st.warning("Table is empty")
        else:
            st.write(data)
            row = st.text_input("Enter which row to delete")
            if row == '':
                st.warning("Please input a row number")
            elif not row.isnumeric() or int(row) > len(data) or int(row) < 0:
                st.warning("Please input a valid row number")
            else:
                row = int(row)
                if st.button("Delete"):
                    delete_data(table_name, row, data)
                    st.success("Deleted Row {}".format(row))    
                    data = read_data(table_name)
                    st.header("Changed Table")
                    if data.empty:
                        st.warning("Table is empty")
                    else:
                        st.write(data)
    elif choice == "Queries":
        st.subheader("Queries")
        query = st.selectbox("Query", ["1","2","3","4","5","6","7","8","9","10","11"])
        if query == "1":
            st.write("List the disease code and the description of diseases that are caused by “bacteria” (pathogen) and were discovered before 1990.")
            if st.button("Execute"):
                result = query1()
                if result.empty:
                    st.warning("No data available")
                else:
                    st.write(result)
        elif query == "2":
            st.write("List the name, surname and degree of doctors who are not specialized in “infectious diseases”.")
            if st.button("Execute"):
                result = query2()
                if result.empty:
                    st.warning("No data available")
                else:
                    st.write(result)
        elif query == "3":
            st.write("List the name, surname and degree of doctors who are specialized in more than 2 disease types.")
            if st.button("Execute"):
                result = query3()
                if result.empty:
                    st.warning("No data available")
                else:
                    st.write(result)
        elif query == "4":
            st.write("For each country list the cname and average salary of doctors who are specialized in “virology”.")
            if st.button("Execute"):
                result = query4()
                if result.empty:
                    st.warning("No data available")
                else:
                    st.write(result)
        elif query == "5":
            st.write("List the departments of public servants who report “covid-19” cases in more than one country and the number of such public servants who work in these departments. (i.e “Dept1 3” means that in the “Dept1” department there are 3 such employees.)")
            if st.button("Execute"):
                result = query5()
                if result.empty:
                    st.warning("No data available")
                else:
                    st.write(result)
        elif query == "6":
            st.write("Double the salary of public servants who have recorded covid-19 patients more than 3 times.")
            if st.button("Execute"):
                result = query6()
                if result.empty:
                    st.warning("No data available")
                else:
                    st.write(result)
        elif query == "7":
            st.write("Delete the users whose name contain the substring “bek” or “gul” (e.g. Alibek, Gulsim)")
            if st.button("Execute"):
                result = query7()
                if result.empty:
                    st.warning("No data available")
                else:
                    st.write(result)
        elif query == "8":
            st.write("Create an index namely “idx pathogen” on the “pathogen” field.")
            if st.button("Execute"):
                result = query8()
                if result.empty:
                    st.warning("No data available")
                else:
                    st.write(result)
        elif query == "9":
            st.write("List the email, name, and department of public servants who have created records where the number of patients is between 100000 and 999999")
            if st.button("Execute"):
                result = query9()
                if result.empty:
                    st.warning("No data available")
                else:
                    st.write(result)
        elif query == "10":
            st.write("List the top 5 counties with the highest number of total patients recorded.")
            if st.button("Execute"):
                result = query10()
                if result.empty:
                    st.warning("No data available")
                else:
                    st.write(result)
        elif query == "11":
            st.write("Group the diseases by disease type and the total number of patients treated.")
            if st.button("Execute"):
                result = query11()
                if result.empty:
                    st.warning("No data available")
                else:
                    st.write(result)
     

if __name__ == '__main__':
	main()
