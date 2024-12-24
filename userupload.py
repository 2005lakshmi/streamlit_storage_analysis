import streamlit as st
import os
import shutil

# Directory to store uploaded files
UPLOAD_DIR = 'uploads'

# Check if the directory exists, if not create it
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Helper function to get the size of files in the upload directory
def get_storage_usage():
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(UPLOAD_DIR):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

# Convert bytes to human-readable format
def bytes_to_human_readable(byte_size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if byte_size < 1024.0:
            return f"{byte_size:.2f} {unit}"
        byte_size /= 1024.0
    return f"{byte_size:.2f} TB"

# Get disk usage of the current environment
def get_disk_usage():
    total, used, free = shutil.disk_usage("/")
    return total, used, free

# Streamlit UI
st.title(":green[T]emp :blue[S]hare")
st.subheader(":blue[Upload File]")

# File uploader
uploaded_file = st.file_uploader("Upload file", type=["txt", "csv", "pdf", "jpg", "png"])

if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    # Save the uploaded file to the directory
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File {uploaded_file.name} uploaded successfully!")

# Display uploaded files when "Display Files" button is clicked
if st.button("Display Uploaded Files"):
    # List uploaded files and sort them by name or modification time
    uploaded_files = sorted(os.listdir(UPLOAD_DIR))  # Sorting by filename

    if uploaded_files:
        st.subheader("Uploaded Files:")
        for file in uploaded_files:
            file_path = os.path.join(UPLOAD_DIR, file)

            # File download button
            with open(file_path, "rb") as f:
                file_data = f.read()
            st.download_button(
                label=f"Download {file}",
                data=file_data,
                file_name=file,
                mime="application/octet-stream"
            )

            # Delete button
            if st.button(f"Delete {file}"):
                os.remove(file_path)
                st.success(f"File {file} deleted successfully!")
    else:
        st.write("No files uploaded yet.")

# Get disk usage info
total_capacity, used_capacity, free_capacity = get_disk_usage()

# Convert to GB for easier reading
total_capacity = total_capacity / (1024 ** 3)
used_capacity = used_capacity / (1024 ** 3)
free_capacity = free_capacity / (1024 ** 3)

# Display storage usage as a text
st.subheader("Disk Usage Information")

st.write(f"Total storage: {total_capacity:.2f} GB")
st.write(f"Used storage: {used_capacity:.2f} GB")
st.write(f"Free storage: {free_capacity:.2f} GB")

# Show the storage chart using a bar chart
storage_data = {
    "Used Storage": used_capacity,
    "Free Storage": free_capacity
}

# Display a simple bar chart with the data
st.bar_chart(storage_data)
