from docx import Document
import re
import pandas as pd


input_file = 'YOUR_DOCUMENT_NAME.docx'
output_file = 'YOUR_DOCUMENT_NAME.xlsx'


doc = Document(input_file)
file_names_set = set()


for paragraph in doc.paragraphs:
    matches = re.findall(r'《(.*?)》', paragraph.text)
    file_names_set.update(matches)


file_names_list = sorted(file_names_set)


df = pd.DataFrame(file_names_list, columns=['File Names'])
df.to_excel(output_file, index=False)
print(f"The deduplicated file name has been stored in {output_file}.")