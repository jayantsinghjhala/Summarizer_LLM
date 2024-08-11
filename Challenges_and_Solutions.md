
# Approach, Challenges, and Solutions

## **Overview**

This document outlines the approach taken to develop the application, the challenges encountered during the development process, and the solutions implemented to overcome these challenges.

## **Challenges and Solutions**

### **1. Issue with Torch Library**
   - **Problem:**
     - Encountered an `OSError WinError 126` error when attempting to import the Torch library, related to loading `fbgemm.dll` or its dependencies.
   - **Solution:**
     - Resolved the issue by downloading and pasting the `libomp140.x86_64.dll` file into the `Windows/System32` directory.
     - Reinstalled Torch with a downgraded version of NumPy for compatibility.
     - [Download DLL file](https://www.dllme.com/dll/files/libomp140_x86_64/00637fe34a6043031c9ae4c6cf0a891d/download).

### **2. Linking React App with Flask Backend**
   - **Problem:**
     - Encountered a CORS policy issue when trying to connect the React frontend with the Flask backend. The error message indicated that the request was blocked due to the absence of the `Access-Control-Allow-Origin` header.
   - **Solution:**
     - Integrated CORS configuration directly into the `route.py` file containing the API functions.
     - Initially attempted to manually add the required headers using `after_request`, but found that the built-in CORS configuration approach was more efficient.

### **3. Handling Large Files for Summarization and Process Stopping**
   - **Problem:**
     - Managing the processing of large files was challenging, especially when needing to halt the process partway through.
   - **Solution:**
     - Implemented text chunking with threading to handle large files more efficiently.
     - Added a "Stop Processing" button to allow users to halt the summarization process. The visibility and functionality of this button are managed based on the file size and the current process status.

### **4. Adding Stop Processing Button**
   - **Problem:**
     - Difficulty in adding the "Stop Processing" button specifically for large files that require splitting and processing, while not affecting the handling of smaller files.
   - **Solution:**
     - Implemented conditional rendering for the "Stop Processing" button based on file size and processing status.
     - Managed the button's text and state dynamically based on the process status and the size of the file being processed.

## **Conclusion**

By addressing the challenges outlined above, the application now handles large files more efficiently, integrates smoothly with the backend, and provides a better user experience with the ability to halt processes as needed.
