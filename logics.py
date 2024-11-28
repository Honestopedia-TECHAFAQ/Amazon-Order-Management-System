import csv
import os

def process_txt_to_actegruse(txt_file_path):
    try:
        with open(txt_file_path, 'r') as file:
            content = file.read().strip()
            actegruse_content = f"ACTEGRUSE TEXT DATA:\n{content}\n"
            return actegruse_content
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return None

def process_csv_to_actegruse(csv_file_path):
    try:
        actegruse_content = "ACTEGRUSE CSV DATA:\n"
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                actegruse_content += ",".join(row) + "\n"
        return actegruse_content
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def save_to_file(content, output_file_path):
    try:
        with open(output_file_path, 'w') as file:
            file.write(content)
        print(f"File saved successfully to {output_file_path}")
    except Exception as e:
        print(f"Error saving the file: {e}")

def file_exists(file_path):
    return os.path.exists(file_path)

def validate_file_extension(file_path, valid_extensions):
    file_extension = os.path.splitext(file_path)[1].lower()
    return file_extension in valid_extensions

def create_backup(file_path):
    backup_path = file_path + ".bak"
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        with open(backup_path, 'w') as backup_file:
            backup_file.write(content)
        print(f"Backup created at {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {e}")

def convert_txt_to_json(txt_content):
    try:
        json_content = {"content": txt_content.strip()}
        return str(json_content)
    except Exception as e:
        print(f"Error converting TXT to JSON: {e}")
        return None

def convert_csv_to_json(csv_content):
    try:
        rows = csv_content.strip().split("\n")
        headers = rows[0].split(",")
        json_data = []
        for row in rows[1:]:
            values = row.split(",")
            json_data.append(dict(zip(headers, values)))
        return str(json_data)
    except Exception as e:
        print(f"Error converting CSV to JSON: {e}")
        return None

def compress_content(content):
    try:
        compressed = content.replace("\n", " ").strip()
        return compressed
    except Exception as e:
        print(f"Error compressing content: {e}")
        return None

def main():
    txt_file_path = "example.txt"
    csv_file_path = "example.csv"
    
    if not file_exists(txt_file_path):
        print(f"Error: The TXT file {txt_file_path} does not exist.")
        return

    if not file_exists(csv_file_path):
        print(f"Error: The CSV file {csv_file_path} does not exist.")
        return
    
    if not validate_file_extension(txt_file_path, ['.txt']):
        print(f"Error: Invalid file extension for {txt_file_path}.")
        return

    if not validate_file_extension(csv_file_path, ['.csv']):
        print(f"Error: Invalid file extension for {csv_file_path}.")
        return
    
    create_backup(txt_file_path)
    create_backup(csv_file_path)
    
    txt_content = process_txt_to_actegruse(txt_file_path)
    if txt_content:
        save_to_file(txt_content, "output_actegruse.txt")
    
    csv_content = process_csv_to_actegruse(csv_file_path)
    if csv_content:
        save_to_file(csv_content, "output_actegruse.csv")
    
    compressed_txt = compress_content(txt_content)
    if compressed_txt:
        save_to_file(compressed_txt, "compressed_output.txt")
    
    txt_json = convert_txt_to_json(txt_content)
    if txt_json:
        save_to_file(txt_json, "txt_as_json.txt")
    
    csv_json = convert_csv_to_json(csv_content)
    if csv_json:
        save_to_file(csv_json, "csv_as_json.csv")

if __name__ == "__main__":
    main()
