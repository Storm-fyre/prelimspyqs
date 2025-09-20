import json
import os

def reindex_polity_questions():
    """
    Reads a JSON file containing polity questions, re-indexes them with a 
    global sequential ID, and saves the result to a new file.

    The new ID schema is: POL-YEAR-GLOBAL_SEQUENTIAL_NUMBER
    """
    print("--- Polity JSON ID Re-generator ---")

    # 1. Get input and output filenames from the user
    input_filename = input("Enter the name of the input JSON file (e.g., polity.json): ")
    output_filename = input("Enter the name for the new output JSON file (e.g., polity_updated.json): ")

    # Check if the input file exists in the current directory
    if not os.path.exists(input_filename):
        print(f"\nError: The file '{input_filename}' was not found in this directory.")
        print("Please make sure the file is in the same folder as the script and try again.")
        return

    try:
        # 2. Read and load the JSON data
        with open(input_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"\nSuccessfully loaded '{input_filename}'. Processing...")

    except json.JSONDecodeError:
        print(f"\nError: The file '{input_filename}' is not a valid JSON file.")
        return
    except Exception as e:
        print(f"\nAn unexpected error occurred while reading the file: {e}")
        return

    # 3. Initialize the global counter for the ID
    global_id_counter = 1

    # Get the years and sort them in descending order to process from newest to oldest
    # This ensures a consistent order every time the script is run.
    years_sorted = sorted(data.get('years', {}).keys(), reverse=True)

    if not years_sorted:
        print("Warning: The JSON file does not contain a 'years' key or it is empty.")
    
    # 4. Iterate through the data, update IDs, and increment the counter
    for year in years_sorted:
        questions_list = data['years'][year]
        for question in questions_list:
            # Generate the new ID using the specified schema
            # Using f-string formatting to add leading zeros (e.g., 001, 002, ... 100)
            new_id = f"ENVI-{year}-{global_id_counter:03}"
            
            # Update the 'id' field in the question dictionary
            question['id'] = new_id
            
            # Increment the global counter for the next question
            global_id_counter += 1

    # 5. Write the updated data to the new output file
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            # Use indent=2 for nice, readable formatting in the output file
            json.dump(data, f, indent=2)
        
        print(f"\nProcessing complete!")
        print(f"A total of {global_id_counter - 1} questions have been re-indexed.")
        print(f"The updated file has been saved as '{output_filename}'.")

    except Exception as e:
        print(f"\nAn error occurred while writing to the output file: {e}")


if __name__ == "__main__":
    reindex_polity_questions()