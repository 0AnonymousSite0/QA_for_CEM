import os
import pandas as pd
import qianfan
chat_comp = qianfan.ChatCompletion(ak="YOUR_API_KEY", sk="YOUR_SECRET_KEY")
os.environ['QIANFAN_AK'] = "YOUR_API_KEY"
os.environ['QIANFAN_SK'] = "YOUR_SECRET_KEY"
import nltk

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
  if "四个" in Question:
    score = score_of_single_choice(answers_from_model, answers)
  if "五个" in Question:
    score = score_of_multi_choice(answers_from_model, answers)
  return score


is_chinese = True
if is_chinese:
    #WEB_URL = "https://zhuanlan.zhihu.com/p/85289282"
    CUSTOM_PROMPT_TEMPLATE = """
        使用下面的语料来回答本模板最末尾的问题。如果你不知道问题的答案，直接回答 "我不知道"，禁止随意编造答案。
        为了保证答案尽可能简洁，你的回答仅限于ABCDE五个字母。
        以下是一对问题和答案的样例：
            请问：单项选择题，请从A、B、C、D四个选项中选出唯一正确的答案填入括号中，回答请仅限于ABCD,不要解释。1、  下列法律文件中，属于我国法的形式的是（  ）。        A 宗教法        B 判例        C 国际条约        D 人民法院的判决书   
            答案是A。

        以下是语料：

        {context}

        请问：{question}
    """
    QUESTION1 = "单项选择题，请从A、B、C、D四个选项中选出唯一正确的答案填入括号中，回答请仅限于ABCD,不要解释。1、  下列法律文件中，属于我国法的形式的是（  ）。        A 宗教法        B 判例        C 国际条约        D 人民法院的判决书         "

else:
    WEB_URL = "https://lilianweng.github.io/posts/2023-06-23-agent/"
    CUSTOM_PROMPT_TEMPLATE = """
        Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        Use three sentences maximum and keep the answer as concise as possible. 
        Always say "thanks for asking!" at the end of the answer. 
        {context}
        Question: {question}
        Helpful Answer:
    """
    QUESTION1 = "How do agents use Task decomposition?"
    QUESTION2 = "What are the various ways to implemet memory to support it?"
from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import QianfanEmbeddingsEndpoint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

if not os.path.exists('VectorStore_KNOWLEDGE_BASE'):
  nltk.download("punkt")
  text_loader_kwargs={'autodetect_encoding': True}
  loader = DirectoryLoader(r'YOUR_KNOWLEDGE_BASE_PATH',glob="**/*.docx", show_progress=True)
  data = loader.load()
  print("data_loaded")
  text_splitter = RecursiveCharacterTextSplitter(chunk_size = 250, chunk_overlap = 50, separators=["\n\n", "\n", " ", "", "。", "，"])
  all_splits = text_splitter.split_documents(data)

  vectorstore = Chroma.from_documents(documents=all_splits, embedding=QianfanEmbeddingsEndpoint(),
                                        persist_directory="VectorStore_KNOWLEDGE_BASE")
  vectorstore.persist()
else:
    vectorstore = Chroma(persist_directory='VectorStore_KNOWLEDGE_BASE', embedding_function=QianfanEmbeddingsEndpoint())
    print(vectorstore)

print("vectorstore_stored")
print("prompt问题："+QUESTION1)
docs = vectorstore.similarity_search_with_relevance_scores(QUESTION1)
[(document.page_content, score) for document, score in docs]

from langchain.chains import RetrievalQA
from langchain.chat_models import QianfanChatEndpoint
from langchain.prompts import PromptTemplate

QA_CHAIN_PROMPT = PromptTemplate.from_template(CUSTOM_PROMPT_TEMPLATE)
llm_ERNIE_Bot_turbo40 = QianfanChatEndpoint(streaming=True, model="ERNIE-Bot-4",temperature=0.5,top_p=0,penalty_score=1)
llm_ERNIE_Bot_turbo = QianfanChatEndpoint(streaming=True, model="ERNIE-Bot-turbo",temperature=0.5,top_p=0,penalty_score=1)

retriever = vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={'score_threshold': 0.1})

from langchain.chains import RetrievalQA

qa_chain_llm_ERNIE_Bot_turbo40 = RetrievalQA.from_chain_type(llm_ERNIE_Bot_turbo40, retriever=retriever, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}, return_source_documents=True)
qa_chain_llm_ERNIE_Bot_turbo = RetrievalQA.from_chain_type(llm_ERNIE_Bot_turbo, retriever=retriever, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}, return_source_documents=True)


years=["First_Level_RCQE_2011"]
for year in years:
  print("Code of the examination",year)
  Questions=read_excel_column(year+".xlsx", "Sheet1", "Question")
  Answers=read_excel_column(year+".xlsx", "Sheet1", "Answer")
  df = pd.DataFrame(columns=["Question","Correct_Answer",'Answer1', "Score1","Answer2","Score2"])
  for i in range(len(Questions)):
    result_llm_ERNIE_Bot_turbo40 = qa_chain_llm_ERNIE_Bot_turbo40({"query": Questions[i]})
    result_llm_ERNIE_Bot_turbo = qa_chain_llm_ERNIE_Bot_turbo({"query": Questions[i]})
    df2 = pd.DataFrame([{"Question":Questions[i],"Correct_Answer":Answers[i],
                         "Answer1":result_llm_ERNIE_Bot_turbo40['result'],"Score1":final_score(Questions[i],result_llm_ERNIE_Bot_turbo40['result'],Answers[i]),
                         "Answer2":result_llm_ERNIE_Bot_turbo['result'],"Score2":final_score(Questions[i],result_llm_ERNIE_Bot_turbo['result'],Answers[i])}])


    print("No of Question",i+1,"\n","Right_Answer:",Answers[i],
          "\n"+"Answer_from_CEM_knowledge-incorporated_ERNIE_Bot_turbo40:",str(result_llm_ERNIE_Bot_turbo40['result']).strip().replace("\n",""),
          "\n"+"Answer_from_CEM_knowledge-incorporated_ERNIE_Bot_turbo:",str(result_llm_ERNIE_Bot_turbo['result']).strip().replace("\n",""))
    df = pd.concat([df, df2], axis=0)
  save_df_to_excel(df, "Answer_from_CEM_knowledge-incorporated_ERNIE_Bot 4.0_ERNIE-Bot-turbo"+year+".xlsx", "sheet1")