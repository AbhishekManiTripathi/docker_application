# table_generator/app.py
import streamlit as st
import pandas as pd
import requests
import os # Import os module

st.set_page_config(layout="centered", page_title="Multiplication Table Generator")

st.title("🔢 Fancy Multiplication Table Generator")
st.markdown("""
Enter a number below to generate its multiplication table.
The table data is fetched from a FastAPI backend!
""")

# Read FastAPI URL from environment variable
# Defaults to localhost for local testing outside Docker Compose
FASTAPI_ENDPOINT = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")

# Input for the number
input_number = st.number_input("Enter a number:", min_value=1, value=1, step=1)

if st.button("Generate Table"):
    if input_number:
        try:
            # Use the dynamically determined FastAPI endpoint
            response = requests.post(f"{FASTAPI_ENDPOINT}/generate_table/", json={"number": input_number})
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            data = response.json()

            st.subheader(f"Multiplication Table for {data['number']}")

            # Prepare data for pandas DataFrame
            table_rows = []
            for item in data['table']:
                table_rows.append([
                    f"{data['number']} x {item['multiplier']}",
                    item['result']
                ])

            df = pd.DataFrame(table_rows, columns=["Expression", "Result"])

            # Display the table using st.dataframe for a fancy look
            st.dataframe(
                df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Expression": st.column_config.TextColumn(
                        "Expression",
                        help="Multiplication expression",
                        width="medium"
                    ),
                    "Result": st.column_config.NumberColumn(
                        "Result",
                        help="Calculated result",
                        format="%d",
                        width="small"
                    ),
                }
            )

            st.success("Table generated successfully!")

        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to the FastAPI backend at {FASTAPI_ENDPOINT}. Make sure it's running.")
            st.info("If running in Docker Compose, ensure the FastAPI service name is correctly used in the URL.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a number to generate the table.")

st.markdown("---")
st.caption("Powered by FastAPI and Streamlit")