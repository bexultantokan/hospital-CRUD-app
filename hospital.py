import streamlit as st
import pandas as pd 
from db_fxns import * 
import streamlit.components.v1 as stc

def main():
    menu = ["Create","Read","Update","Delete"]
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
                else:
                    add_data(table_name,[id, description])
                    st.success("Added ::{} ::To DiseaseType".format(description))
        elif table_name == 'Country':
            name = st.text_input("Name")
            population = st.text_input("Population")
            if st.button("Add Country"):
                if name == '' or population == '':
                    st.warning("Please input all fields")
                else:
                    add_data(table_name,[name, population])
                    st.success("Added ::{} ::To Country".format(name))
        elif table_name == 'Disease':
            disease_code = st.text_input("Disease Code")
            pathogen = st.text_input("Pathogen")
            description = st.text_input("Description")
            id = st.text_input("ID")
            if st.button("Add Disease"):
                if disease_code == '' or pathogen == '' or description == '' or id == '':
                    st.warning("Please input all fields")
                else:
                    add_data(table_name,[disease_code, pathogen, description, id])
                    st.success("Added ::{} ::To Disease".format(disease_code))
        elif table_name == 'Discover':
            country_name = st.text_input("Country Name")
            disease_code = st.text_input("Disease Code")
            date = st.text_input("Date")
            if st.button("Add Discover"):
                if country_name == '' or disease_code == '' or date == '':
                    st.warning("Please input all fields")
                else:
                    add_data(table_name,[country_name, disease_code, date])
                    st.success("Added ::{} ::To Discover".format(country_name))
        elif table_name == 'Users':
            email = st.text_input("Email")
            name = st.text_input("Name")
            surname = st.text_input("Surname")
            salary = st.text_input("Salary")
            phone = st.text_input("Phone")
            country = st.text_input("Country")
            if st.button("Add Users"):
                if email == '' or name == '' or surname == '' or salary == '' or phone == '' or country == '':
                    st.warning("Please input all fields")
                else:
                    add_data(table_name,[email, name, surname, salary, phone, country])
                    st.success("Added ::{} ::To Users".format(email))
        elif table_name == 'PublicServant':
            email = st.text_input("Email")
            department = st.text_input("Department")
            if st.button("Add PublicServant"):
                if email == '' or department == '':
                    st.warning("Please input all fields")
                else:
                    add_data(table_name,[email, department])
                    st.success("Added ::{} ::To PublicServant".format(email))
        elif table_name == 'Doctor':
            email = st.text_input("Email")
            degree = st.text_input("Degree")
            if st.button("Add Doctor"):
                if email == '' or degree == '':
                    st.warning("Please input all fields")
                else:
                    add_data(table_name,[email, degree])
                    st.success("Added ::{} ::To Doctor".format(email))
        elif table_name == 'Specialize':
            id = st.text_input("ID")
            email = st.text_input("Email")
            if st.button("Add Specialize"):
                if id == '' or email == '':
                    st.warning("Please input all fields")
                else:
                    add_data(table_name,[id, email])
                    st.success("Added ::{} ::To Specialize".format(email))
        elif table_name == 'Record':
            email = st.text_input("Email")
            country = st.text_input("Country")
            disease_code = st.text_input("Disease Code")
            total_deaths = st.text_input("Total Deaths")
            total_patients = st.text_input("Total Patients")
            if st.button("Add Record"):
                if email == '' or country == '' or disease_code == '' or total_deaths == '' or total_patients == '':
                    st.warning("Please input all fields")
                else:
                    add_data(table_name,[email, country, disease_code, total_deaths, total_patients])
                    st.success("Added ::{} ::To Record".format(email))
    elif choice == "Read":
        st.subheader("View Table")
        table_name = st.selectbox("Table Name",["DiseaseType","Country","Disease","Discover","Users","PublicServant","Doctor","Specialize","Record"])
        result = read_data(table_name)
        st.write(result)
    elif choice == "Update":
        st.subheader("Update Table")
        table_name = st.selectbox("Table Name", ["DiseaseType","Country","Disease","Discover","Users","PublicServant","Doctor","Specialize","Record"])
        data = read_data(table_name)
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
                update_data(table_name, row, data)
                st.success("Updated Row {}".format(row))    

    elif choice == "Delete":
        st.subheader("Delete Row")
        table_name = st.selectbox("Table Name", ["DiseaseType","Country","Disease","Discover","Users","PublicServant","Doctor","Specialize","Record"])
        data = read_data(table_name)
        st.write(data)
        row = st.text_input("Enter which row to delete")
        if row == '':
            st.warning("Please input a row number")
        elif not row.isnumeric() or int(row) > len(data) or int(row) < 0:
            st.warning("Please input a valid row number")
        else:
            row = int(row)
            # st.write('Unchangeable key ' + data.columns[0] + ': ', data.iloc[row,0])
            # for i in range(1, len(data.columns)):
            #     data.iloc[row,i] = st.text_input(data.columns[i],data.iloc[row,i])
            if st.button("Delete"):
                delete_data(table_name, row, data)
                st.success("Deleted Row {}".format(row))    



if __name__ == '__main__':
	main()
