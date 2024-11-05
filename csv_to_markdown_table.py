import csv
import sys
import os

def csv_to_markdown(csv_file_path):
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            rows = list(csv_reader)
            
            markdown = '| ' + ' | '.join(headers) + ' |\n'
            markdown += '| ' + ' | '.join(['---' for _ in headers]) + ' |\n'
            
            for row in rows:
                escaped_row = row.copy()
                summary_index = headers.index('summary')
                escaped_row[summary_index] = f'<details><summary>Click to expand</summary>{row[summary_index]}</details>'
                escaped_row = [cell.replace('|', '\\|') for cell in escaped_row]
                markdown += '| ' + ' | '.join(escaped_row) + ' |\n'
            
            return markdown

    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error occurred: {str(e)}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python csv_to_markdown_table.py <csv_file_path>")
        return
    
    csv_file_path = sys.argv[1]
    markdown_table = csv_to_markdown(csv_file_path)
    #print(markdown_table)
    
    if len(sys.argv) == 3:
        markdown_file = sys.argv[2]
        if not markdown_file.endswith('.md'):
            markdown_file += '.md'
    else:
        markdown_file = os.path.splitext(os.path.basename(csv_file_path))[0] + '.md'
    
    markdown_table = csv_to_markdown(csv_file_path)
    
    if markdown_table == "File not found" or markdown_table == "Error occurred:":
        print("Failed to convert CSV to Markdown. Error:", markdown_table)
        return
    
    try:
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_table)
        print(f"Successfully saved to {markdown_file}")
    except Exception as e:
        print(f"Error saving file: {str(e)}")
    

if __name__ == "__main__":
    main()