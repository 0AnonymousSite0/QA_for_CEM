# Integrating domain-specific knowledge and fine-tuned general-purpose large language models for question-answering in construction engineering management

## !!! As the paper is under review, all materials in this repository currently are not allowed to be re-used by anyone until this announcement is deleted.

# 0. Videos of running original GLLMs, CEM knowledge-incorporated GLLMs, CEM knowledge-incorporated fine-tuned GLLMs, and CEM-QA prototype
![GIF for running video of original GLLMs.gif](https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Images%20for%20readme/GIF%20for%20running%20video%20of%20original%20GLLMs.gif)

↑↑↑Multiple original GLLMs simultaneously answering the CEM-related questions

![GIF for running video of CEM knowledge-incorporated GLLMs](https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Images%20for%20readme/GIF%20for%20running%20video%20of%20CEM%20knowledge-incorporated%20GLLMs.gif)

↑↑↑Multiple CEM knowledge-incorporated GLLMs simultaneously answering the CEM-related questions

![GIF for running video of CEM knowledge-incorporated fine-tuned GLLMs](https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Images%20for%20readme/GIF%20for%20running%20video%20of%20CEM%20knowledge-incorporated%20fine-tuned%20GLLMs.gif)

↑↑↑Multiple CEM knowledge-incorporated fine-tuned GLLMs simultaneously answering the CEM-related questions

![GIF for running video of CEM-QA prototype](https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Images%20for%20readme/GIF%20for%20running%20video%20of%20CEM-QA%20prototype.gif)

↑↑↑CEM-QA prototype answering the CEM-related question


# 1. General introduction of this repository

1.1 This repository aims at providing the codes and data regarding the paper entitled “……” for the public, and it is developed by University of XXX in UK and XXX University in China.

1.2 We greatly appreciate the selfless spirits of these voluntary contributors of a series of open python libraries, including langchain, llamaindex, openai, chatglm, numpy, and so on. Our work stands on the shoulders of these giants.

1.3 As for anything regarding the copyright, please refer to the MIT License or contact the authors.

# 2. Summary of supplemental materials in this repository

The table below shows all supplemental materials. All sheets in Tables S1, S2, S3, and S4 are arranged in the order shown in this table.

![Inventory of supplemental materials](https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Images%20for%20readme/Inventory%20of%20supplemental%20materials.png)

All supplemental materials are provided in Github repository (https://github.com/0AnonymousSite0/QA_for_CEM). Besides the GitHub repository, the CEM-QA test dataset is also shared in the Hugging Face repository (https://huggingface.co/datasets/AnonymousSite/QA_test_dataset_for_CEM).

# 3. GLLM Leaderboard for CEM-QA

The test results of different GLLMs on the CEM-QA test dataset are shown below. Welcome global scholars to test their GLLM works on CEM-QA, please see the following specification of reusing the QA dataset.

| General-purpose large language models | Contributors | Average correctness ratio | SD1 | SD2 | SD3 | SD4 | SD5 | SD6 | SD7 | Ranking |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| Knowledge-incorporated ERNIE-Bot 4.0 | Baidu & The authors | 0.734 | 0.787 | 0.758 | 0.640 | 0.766 | 0.784 | 0.754 | 0.808 | 1 |
| Knowledge-incorporated fine-tuned Qwen-14B-Chat | Alibaba & The authors | 0.631 | 0.683 | 0.618 | 0.536 | 0.659 | 0.683 | 0.629 | 0.719 | 2 |
| Knowledge-incorporated GPT-4 | OpenAI & The authors | 0.620 | 0.672 | 0.611 | 0.431 | 0.694 | 0.695 | 0.694 | 0.678 | 3 |
| Original ERNIE-Bot 4.0 | Baidu | 0.608 | 0.661 | 0.632 | 0.507 | 0.656 | 0.648 | 0.632 | 0.622 | 4 |
| Knowledge-incorporated Qwen-14B-Chat | Alibaba & The authors | 0.583 | 0.641 | 0.565 | 0.465 | 0.621 | 0.641 | 0.578 | 0.669 | 5 |
| Original Qwen-14B-Chat | Alibaba | 0.522 | 0.583 | 0.512 | 0.393 | 0.565 | 0.548 | 0.521 | 0.594 | 6 |
| Knowledge-incorporated fine-tuned Baichuan2-7B-Chat | Baichuan AI & The authors | 0.517 | 0.568 | 0.701 | 0.224 | 0.682 | 0.682 | 0.682 | 0.682 | 7 |
| Knowledge-incorporated fine-tuned Qwen-7B-Chat | Alibaba & The authors | 0.517 | 0.574 | 0.538 | 0.410 | 0.567 | 0.575 | 0.514 | 0.597 | 8 |
| Knowledge-incorporated fine-tuned Baichuan2-13B-Chat | Baichuan AI & The authors | 0.497 | 0.547 | 0.491 | 0.413 | 0.566 | 0.552 | 0.494 | 0.553 | 9 |
| Original GPT-4 | OpenAI | 0.475 | 0.513 | 0.477 | 0.358 | 0.512 | 0.480 | 0.528 | 0.486 | 10 |
| Knowledge-incorporated Qwen-7B-Chat | Alibaba & The authors | 0.468 | 0.529 | 0.448 | 0.364 | 0.515 | 0.514 | 0.467 | 0.542 | 11 |
| Knowledge-incorporated fine-tuned GPT-3.5-turbo | OpenAI & The authors | 0.468 | 0.497 | 0.441 | 0.393 | 0.513 | 0.497 | 0.498 | 0.594 | 12 |
| Knowledge-incorporated Baichuan2-7B-Chat | Baichuan AI & The authors | 0.444 | 0.484 | 0.474 | 0.366 | 0.495 | 0.474 | 0.417 | 0.489 | 13 |
| Knowledge-incorporated Baichuan2-13B-Chat | Baichuan AI & The authors | 0.441 | 0.479 | 0.429 | 0.371 | 0.502 | 0.481 | 0.430 | 0.514 | 14 |
| Knowledge-incorporated fine-tuned ERNIE-Bot-turbo | Baidu & The authors | 0.427 | 0.487 | 0.401 | 0.374 | 0.479 | 0.487 | 0.436 | 0.583 | 15 |
| Knowledge-incorporated fine-tuned ChatGLM3-6B | Tsinghua & The authors | 0.425 | 0.482 | 0.406 | 0.353 | 0.471 | 0.487 | 0.422 | 0.472 | 16 |
| Original Qwen-7B-Chat | Alibaba | 0.410 | 0.461 | 0.370 | 0.316 | 0.475 | 0.445 | 0.423 | 0.411 | 17 |
| Knowledge-incorporated GPT-3.5-turbo | OpenAI & The authors | 0.407 | 0.458 | 0.395 | 0.356 | 0.438 | 0.456 | 0.422 | 0.447 | 18 |
| Knowledge-incorporated ChatGLM3-6B | Tsinghua & The authors | 0.399 | 0.462 | 0.395 | 0.314 | 0.454 | 0.452 | 0.394 | 0.406 | 19 |
| Original Baichuan2-13B-Chat | Baichuan AI | 0.393 | 0.443 | 0.408 | 0.323 | 0.447 | 0.443 | 0.378 | 0.456 | 20 |
| Knowledge-incorporated ERNIE-Bot-turbo | Baidu & The authors | 0.392 | 0.424 | 0.386 | 0.351 | 0.432 | 0.418 | 0.394 | 0.467 | 21 |
| Original Baichuan2-7B-Chat | Baichuan AI | 0.385 | 0.423 | 0.406 | 0.291 | 0.445 | 0.427 | 0.381 | 0.394 | 22 |
| Original ChatGLM3-6B | Tsinghua | 0.353| 0.411 | 0.351 | 0.298 | 0.394 | 0.403 | 0.343 | 0.339 | 23 |
| Original ERNIE-Bot-turbo | Baidu | 0.345 | 0.402 | 0.309 | 0.324 | 0.382 | 0.370 | 0.365 | 0.414 | 24 |
| Original GPT-3.5-turbo | OpenAI | 0.340 | 0.400 | 0.334 | 0.304 | 0.421 | 0.345 | 0.362 | 0.389 | 25 |

# 4. Reuse of the CEM-EKB with two optional versions

![Two optional versions of CEM-EKB](https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Images%20for%20readme/Two%20optional%20versions%20of%20CEM-EKB.png)

The CEM-EKB is available through this link (https://drive.google.com/drive/folders/1HL8hW_Co47fOPF_PnIogpBSo-REPQ1jc?usp=sharing).


# 5. Reuse of the CEM-QA test and training datasets

The CEM-QA test dataset containing 5,050 questions is manually annotated with four features, including the question source, single-answer multiple-choice question (SAMCQ) or multiple-answer multiple-choice question (MAMCQ), and calculation question or non-calculation question.


![CEM-QA test dataset in the Hugging Face repository](https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Images%20for%20readme/CEM-QA%20test%20dataset%20in%20the%20Hugging%20Face%20repository.png)
↑↑↑The CEM-QA test dataset in the Hugging Face repository


![CEM-QA training dataset in the Hugging Face repository](https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Images%20for%20readme/CEM-QA%20training%20dataset%20in%20the%20Hugging%20Face%20repository.png)
↑↑↑The CEM-QA training dataset in the Hugging Face repository

More information about the datasets can be found through these links (https://huggingface.co/datasets/AnonymousSite/QA_test_dataset_for_CEM)( https://huggingface.co/datasets/AnonymousSite/QA_training_dataset_for_CEM).

# 6. Reuse of the codes for running original GLLMs, CEM knowledge-incorporated GLLMs, CEM knowledge-incorporated fine-tuned GLLMs, and CEM-QA prototype
 
## 6.1 Environment set

All codes are developed on Python 3.10, and the IDE adopted is PyCharm (Professional version). The codes also support GPU computing for higher speed; the Navida CUDA we adopted is V10.0.130. The GIS platform is Arcgis Pro 2.3, and its license is necessary. 

aiohttp==3.9.0

aiolimiter==1.1.0

aiosignal==1.3.1

aiostream==0.5.2

annotated-types==0.6.0

anyio==3.7.1

Appium-Python-Client==3.1.0

async-timeout==4.0.3

attrs==23.1.0

backoff==2.2.1

bce-python-sdk==0.8.96

bcrypt==4.0.1

beautifulsoup4==4.12.2

......

Please refer to the supplementary materials for the complete requirement file.(https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Codes/Codes%20for%20running%20CEM%20knowledge-incorporated%20GLLMs/requirements.txt)

Before submitting these codes to Github, all of them have been tested to be well-performed (as shown in the images). Even so, we are not able to guarantee their operation in other computing environments due to the differences in the Python version, computer operating system, and adopted hardware.

## 6.2 Codes for testing the GLLMs

Closed-source GLLMs are API-only, and open-source GLLMs are deployed directly on the AutoDL Cloud server.


![Codes for running original GLLMs](https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Images%20for%20readme/Codes%20for%20running%20original%20GLLMs.png)
↑↑↑Codes for testing original GLLMs


![Codes for running CEM knowledge-incorporated GLLMs](https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Images%20for%20readme/Codes%20for%20running%20CEM%20knowledge-incorporated%20GLLMs.png)
↑↑↑Codes for testing CEM knowledge-incorporated GLLMs


![Codes for running CEM knowledge-incorporated fine-tuned GLLMs](https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Images%20for%20readme/Codes%20for%20running%20CEM%20knowledge-incorporated%20fine-tuned%20GLLMs.png)
↑↑↑Codes for testing CEM knowledge-incorporated fine-tuned GLLMs


![Codes for deploying and running CEM-QA prototype](https://github.com/0AnonymousSite0/QA_for_CEM/blob/main/Images%20for%20readme/Codes%20for%20deploying%20and%20running%20the%20CEM-QA%20%20prototype.png)
↑↑↑Codes for deploying and running CEM-QA prototype
