import streamlit as st
import time

# Function to refresh the page
def refresh_page():
    # Get the current time
    current_time = time.time()

    # Store the last refresh time in session state
    last_refresh_time = st.session_state.get('last_refresh_time', current_time)

    # Check if 1 minute has passed since the last refresh
    if current_time - last_refresh_time >= 60:
        # Update last refresh time
        st.session_state.last_refresh_time = current_time
        
        # Refresh the page
        st.experimental_rerun()

# Main function to run the Streamlit app
def main():
    st.title("Auto-refreshing Streamlit App")
    st.write("This app will automatically refresh every minute.")
    
    # Function call to refresh the page
    refresh_page()

    # Simulate some activity that changes over time
    for i in range(10):
        st.write(f"Updating... {i}")
        time.sleep(1)

if __name__ == "__main__":
    main()
