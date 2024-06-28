import streamlit as st
import pandas as pd

# Read the Excel sheet
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Initialize session state to keep track of current index and annotations
    if 'index' not in st.session_state:
        st.session_state.index = 0
    if 'annotations' not in st.session_state:
        st.session_state.annotations = []

    # Function to save annotations to a CSV file
    def save_annotations():
        annotations_df = pd.DataFrame(st.session_state.annotations, columns=['id', 'source1', 'source2', 'source3', 'question', 'answer', 'annotation'])
        annotations_df.to_csv('annotations.csv', index=False)
        st.success("Annotations saved to annotations.csv")

    # Display current entry
    if st.session_state.index < len(df):
        row = df.iloc[st.session_state.index]
        st.write(f"ID: {row['id']}")
        st.write(f"Source 1: {row['source_1']}")
        st.write(f"Source 2: {row['semoa_info']}")
        st.write(f"Source 3: {row['source_2']}")
        st.write(f"Question: {row['question']}")
        st.write(f"Answer: {row['answer']}")

        # Annotation options
        annotation = st.radio("Is the question and answer proper?", ('Yes', 'No', 'Not Sure'))

        if st.button('Next'):
            # Save current annotation
            st.session_state.annotations.append([row['id'], row['source_1'], row['semoa_info'], row['source_2'], row['question'], row['answer'], annotation])
            st.session_state.index += 1

            # Automatically save annotations after each entry
            save_annotations()

            # If there are more entries, display the next one
            if st.session_state.index < len(df):
                st.experimental_rerun()
            else:
                st.write("No more data to annotate.")
    else:
        st.write("No more data to annotate.")

