import os
import subprocess

# Modifiable variables (Update these as needed)
DEFAULT_DIRECTORY_PATH = "/Users/hembo/Desktop/Ruta trascibuse asjad/export_job_14399447/1878792/Tallinna_Magistraat_0000Ae2/alto"  # Path to the directory containing XML files
DEFAULT_XSL_FILE_PATH = "/Users/hembo/Desktop/Ruta trascibuse asjad/export_job_14399447/1878792/Tallinna_Magistraat_0000Ae2/annotationListNoArt.xsl"  # Path to the XSL file
MANIFEST_URI = "https://db.dl.tlu.ee/iiif/manifest/magistraat/20"  # Manifest URI template
XRATIO = "1"  # Default xRatio parameter for xsltproc
YRATIO = "1"  # Default yRatio parameter for xsltproc

def process_directory(directory, xsl_file):
    """
    Process all XML files in the specified directory using xsltproc with the given XSL file.

    Args:
        directory (str): The path to the directory containing XML files.
        xsl_file (str): The XSL file to be used by xsltproc.
    """
    # Check if the provided directory path is valid
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    # Sort the files in alphabetical order
    files = sorted([f for f in os.listdir(directory) if f.endswith(".xml")])

    # Iterate over all files in alphabetical order
    for index, filename in enumerate(files, start=1):
        input_xml = os.path.join(directory, filename)  # Full path to the input XML file

        # Construct the required URIs and output file path
        anno_uri = f"https://db.dl.tlu.ee/iiif/{os.path.splitext(filename)[0]}.json"
        canvas_uri = f"https://db.dl.tlu.ee/iiif/canvas/{index}"  # Use sequence index instead of file_id
        output_json = os.path.join(directory, f"{os.path.splitext(filename)[0]}.json")

        # Prepare the xsltproc command
        command = [
            "xsltproc",
            "--stringparam", "annoURI", anno_uri,
            "--stringparam", "manifestURI", MANIFEST_URI,
            "--stringparam", "xRatio", XRATIO,
            "--stringparam", "yRatio", YRATIO,
            "--stringparam", "canvasURI", canvas_uri,
            xsl_file,
            input_xml
        ]

        print(f"Processing {filename} with sequence index {index}...")

        # Execute the xsltproc command and write the output to a JSON file
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            with open(output_json, "w") as output_file:
                output_file.write(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error processing {filename}: {e.stderr}")
        except Exception as general_error:
            print(f"An unexpected error occurred while processing {filename}: {general_error}")

if __name__ == "__main__":
    # Prompt the user for input paths
    try:
        # Default values can be modified here or overridden by user input
        directory_path = input(f"Enter the directory path containing XML files (default: {DEFAULT_DIRECTORY_PATH}): ").strip() or DEFAULT_DIRECTORY_PATH
        xsl_file_path = input(f"Enter the path to the XSL file (default: {DEFAULT_XSL_FILE_PATH}): ").strip() or DEFAULT_XSL_FILE_PATH

        # Ensure spaces in directory and file paths are handled properly
        directory_path = os.path.abspath(directory_path)
        xsl_file_path = os.path.abspath(xsl_file_path)

        # Call the process_directory function with user-provided paths
        process_directory(directory_path, xsl_file_path)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
