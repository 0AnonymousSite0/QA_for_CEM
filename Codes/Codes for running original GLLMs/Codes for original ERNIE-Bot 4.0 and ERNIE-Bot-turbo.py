import requests
import json
import qianfan
import pandas as pd
import os
chat_comp = qianfan.ChatCompletion(ak="YOUR_API_KEY", sk="YOUR_SECRET_KEY")
os.environ['QIANFAN_AK'] = "YOUR_API_KEY"
os.environ['QIANFAN_SK'] = "YOUR_SECRET_KEY"
import pandas as pd

def score_of_single_choice(answers_from_model, correct_answer):
  score = 0
  number_of_answers=0
  if correct_answer in str(answers_from_model):
    score = 1
  if "A" in correct_answer:
    number_of_answers=number_of_answers+1
  if "B" in correct_answer:
    number_of_answers=number_of_answers+1
  if "C" in correct_answer:
    number_of_answers=number_of_answers+1
  if "D" in correct_answer:
    number_of_answers=number_of_answers+1
  if number_of_answers>1:
    score=0
  return score

def save_df_to_excel(df, file_path, sheet_name):
  writer = pd.ExcelWriter(file_path)
  df.to_excel(writer, sheet_name=sheet_name, index=False)
  writer.close()
def split_correct_answers(string):
  answer = []
  print("string:", string)
  for character in string:
    answer.append(character)
  return answer

def score_of_multi_choice(answers_from_model, correct_answers):
  score = 0
  correct_ones = 0
  missed_ones = 0
  wrong_ones = 0
  individual_correct_answers = split_correct_answers(correct_answers)
  for individual_answer in individual_correct_answers:
    if individual_answer in str(answers_from_model):
      correct_ones = correct_ones + 1
    if individual_answer not in str(answers_from_model):
      missed_ones = missed_ones + 1
  wrong_answers = set(["A", "B", "C", "D", "E"]).difference(correct_answers)
  for individual_wrong_answer in wrong_answers:
    if individual_wrong_answer in str(answers_from_model):
      wrong_ones = wrong_ones + 1

  if wrong_ones == 0:
    if missed_ones == 0:
      score = 2
    else:
      score = min(correct_ones * 0.5, 2)
  return score

def read_excel_column(file_path, sheet_name, column_name):
  df = pd.read_excel(file_path, sheet_name=sheet_name)
  column_data = df[column_name].tolist()
  return column_data

def final_score(Question, answers_from_model, answers):
  score=0
  if "四个" in Question:
    score = score_of_single_choice(answers_from_model, answers)

  if "五个" in Question:
    score = score_of_multi_choice(answers_from_model, answers)

  return score

years=["First_Level_RCQE_2011"]
messages = []
for year in years:
  print("Year",year)
  Questions=read_excel_column(year+".xlsx", "Sheet1", "Question")
  Answers=read_excel_column(year+".xlsx", "Sheet1", "Answer")
  df = pd.DataFrame(columns=["Question","Correct_Answer","Answer1", "Score1","Answer2", "Score2"])
  n = 0
  messages = []
  for i in range(len(Questions)):
    n=n+1
    message=Questions[i]

    result_llm_ERNIE_Bot_turbo40=chat_comp.do(model="ERNIE-Bot-4", messages=[{
    "role": "user",
    "content": message
    }])

    result_llm_ERNIE_Bot_turbo=chat_comp.do(model="ERNIE-Bot-turbo", messages=[{
    "role": "user",
    "content": message
    }])

    df2 = pd.DataFrame([{"Question": Questions[i], "Correct_Answer": Answers[i],
                         "Answer1": result_llm_ERNIE_Bot_turbo40['result'],"Score1": final_score(Questions[i], result_llm_ERNIE_Bot_turbo40['result'], Answers[i]),
                         "Answer2": result_llm_ERNIE_Bot_turbo['result'],"Score2": final_score(Questions[i], result_llm_ERNIE_Bot_turbo['result'], Answers[i])}])

    print("No of Question", i + 1, "\n", "Right_Answer:", Answers[i],
          "\n" + "Answer_from_original_ERNIE_Bot_turbo40:",
          str(result_llm_ERNIE_Bot_turbo40['result']).strip().replace("\n", ""),
          "\n" + "Answer_from_original_ERNIE_Bot_turbo:",
          str(result_llm_ERNIE_Bot_turbo['result']).strip().replace("\n", ""))
    df = pd.concat([df, df2], axis=0)
  save_df_to_excel(df, "Answer_from_original_ERNIE-Bot 4.0_ERNIE-Bot_turbo" + year + ".xlsx", "sheet1")