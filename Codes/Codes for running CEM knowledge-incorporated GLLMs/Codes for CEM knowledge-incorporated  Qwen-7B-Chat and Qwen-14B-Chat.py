from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings, HuggingFaceEmbeddings
import numpy as np
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(model_name=r'/root/autodl-tmp/RAG_langchain/Dmeta-embedding',
                                   encode_kwargs={'normalize_embeddings': True})

loader = DirectoryLoader(r"/root/autodl-tmp/RAG_langchain/CEM_knowledge",
                         show_progress=True, use_multithreading=True)
loaded_docs = loader.load()
print("len(loaded_docs)", len(loaded_docs))
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50, )
docs = text_splitter.split_documents(loaded_docs)

db = FAISS.from_documents(docs, embeddings)
db.save_local("faiss_index_CEM")

db2 = FAISS.load_local("faiss_index_CEM", embeddings)

excel_file2 = r'/root/autodl-tmp/RAG_langchain/Dataset_for_RAG_performance_test/First_Level_RCQE_2011.xlsx'
df_test = pd.read_excel(excel_file2)

queries = df_test["Question"].tolist()
query_code = df_test["No."].tolist()
queries_prompt = df_test["Prompt"].tolist()
data = []
augmented_prompts = []
for index, query in enumerate(queries):
    source_knowledge = ""
    searched_docs = db.similarity_search_with_score(query, k=3)
    rank = 0
    n = 0
    for doc, score in searched_docs:
        n = n + 1
        page_content = doc.page_content
        source = doc.metadata
        source_knowledge = source_knowledge + "No." + str(n) + "source knowledge:" + "\n".join([doc.page_content])
        print(doc, score)
        print(source_knowledge)

    augmented_prompt = "Please answer the question in Chinese based on the source knowledge below, and the answer should be concise. Source knowledge :  {" + "\n" + source_knowledge + "}" + "\n" + "Question: {" + \
                       queries_prompt[index] + query + "}"

    augmented_prompts.append(augmented_prompt)

df_test['augmented_prompt'] = augmented_prompts
df_test.to_excel("augmented_prompt" + " " + "First_Level_RCQE_2011.xlsx", index=False)



from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import os
import pandas as pd
import re
import csv
from bs4 import BeautifulSoup
import uuid
import openpyxl

tokenizer = AutoTokenizer.from_pretrained("/root/autodl-tmp/Qwen-7B-Chat/", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("/root/autodl-tmp/Qwen-7B-Chat/", device_map="auto",
                                             trust_remote_code=True, top_p=0,
                                             temperature=0.5).eval()

# Replace Qwen-14B-Chat model
#tokenizer = AutoTokenizer.from_pretrained("/root/autodl-tmp/Qwen-14B-Chat/", trust_remote_code=True)
#model = AutoModelForCausalLM.from_pretrained("/root/autodl-tmp/Qwen-14B-Chat/", device_map="auto",
#                                             trust_remote_code=True, top_p=0,
#                                             temperature=0.5).eval()

def score_of_single_choice(answers_from_model, correct_answer):
    score = 0
    number_of_answers = 0
    if correct_answer in str(answers_from_model):
        score = 1
    if "A" in correct_answer:
        number_of_answers = number_of_answers + 1
    if "B" in correct_answer:
        number_of_answers = number_of_answers + 1
    if "C" in correct_answer:
        number_of_answers = number_of_answers + 1
    if "D" in correct_answer:
        number_of_answers = number_of_answers + 1
    if number_of_answers > 1:
        score = 0
    return score

def save_df_to_excel(df, file_path, sheet_name):
    writer = pd.ExcelWriter(file_path)
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.close()

def split_correct_answers(string):
    answer = []
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

years = ["augmented_prompt First_Level_RCQE_2011"]
messages = []
for year in years:
    print("Code of the examination", year)
    Questions = read_excel_column(year + ".xlsx", "Sheet1", "augmented_prompt")
    Answers = read_excel_column(year + ".xlsx", "Sheet1", "Answer")
    df = pd.DataFrame(
        columns=["Question", "Correct_Answer", 'Answer1', "Score1"])
    for i in range(len(Questions)):
        message = Questions[i]

        def final_score(Question, answers_from_model, answers):
            if "四个" in Question:
                score = score_of_single_choice(answers_from_model, answers)
            if "五个" in Question:
                score = score_of_multi_choice(answers_from_model, answers)
            return score

        history = []
        answers_from_model, history = model.chat(tokenizer, Questions[i], history=[])
        answer1 = answers_from_model

        df2 = pd.DataFrame([
            {"Question": Questions[i], "Correct_Answer": Answers[i], "Answer1": answer1,
             "Score1": final_score(Questions[i], answer1, Answers[i])}])

        print("No Question", i + 1, "\n", "Right_Answer:", Answers[i], "\nAnswer_from_CEM_knowledge-incorporated_Qwen_7B_Chat:",
              answer1.strip().replace("\n", ""))
        df = pd.concat([df, df2], axis=0)
    save_df_to_excel(df, "All_answers_from_CEM_knowledge-incorporated_Qwen_7B_Chat1" + year + ".xlsx", "sheet1")