# Task2emitrr
# Medical Sentiment and Intent Classification System

## Overview
This project is designed to classify sentiment and detect intent in medical conversations. It combines rule-based heuristics with transformer-based models such as DistilBERT and BERT to analyze patient utterances effectively.

## Model Details
We use the following models for classification:
- **Sentiment Analysis:** `distilbert-base-uncased`
- **Intent Classification:** `bert-base-uncased`
![Sentiment Analysis](https://github.com/Shrey152002/Task2emitrr/blob/main/Screenshot%20(11).png)
Initially, we attempted fine-tuning on the **Reddit Mental Health Dataset**, but due to certain challenges, this approach was not applied in the final implementation.
## Output
![Sentiment Analysis](https://github.com/Shrey152002/Task2emitrr/blob/main/Screenshot%20(12).png)
![Sentiment Analysis](https://github.com/Shrey152002/Task2emitrr/blob/main/Screenshot%20(13).png)
![Sentiment Analysis](https://github.com/Shrey152002/Task2emitrr/blob/main/Screenshot%20(14).png)
![Sentiment Analysis](https://github.com/Shrey152002/Task2emitrr/blob/main/Screenshot%20(15).png)
![Sentiment Analysis](https://github.com/Shrey152002/Task2emitrr/blob/main/Screenshot%20(16).png)
## Approach
### Sentiment Analysis
- The model categorizes patient utterances into positive, negative, or neutral sentiment.
- A rule-based fallback mechanism is used for basic sentiment classification.

### Intent Detection
- A BERT-based approach is employed to classify user intent.
- Rule-based heuristics help refine intent classification when needed.

## Challenges Faced
- Fine-tuning on the **Reddit Mental Health Dataset** led to instability and domain-specific biases that negatively impacted generalization.
- Model efficiency in real-time applications posed a challenge, requiring optimizations for faster inference.

## Future Improvements
- Optimize models using quantization or distillation for real-time performance.
- Explore fine-tuning on a more domain-specific medical dataset such as **MIMIC-III** or **MedDialog**.
- Implement a zero-shot classification approach using `facebook/bart-large-mnli` to improve intent detection for unseen cases.

## Installation & Usage
1. Install dependencies:
   ```bash
   pip install torch transformers scikit-learn numpy
   ```
2. Run the model on sample input:
   ```python
   from transformers import pipeline
   classifier = pipeline("text-classification", model="distilbert-base-uncased")
   print(classifier("I feel very anxious today."))
   ```
3. Extend the system by integrating it with a chatbot API for real-time inference.


# Reddit Mental Health Classification

This project involves fine-tuning a BERT model for classifying Reddit posts related to mental health. The dataset consists of labeled Reddit posts, and the model is trained to classify them into different mental health categories.

## Table of Contents
- [Introduction](#introduction)
- [Dataset](#dataset)
- [Preprocessing](#preprocessing)
- [Model Training](#model-training)
- [Evaluation](#evaluation)
- [Visualization](#visualization)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Future Improvements](#future-improvements)

## Introduction
With the increasing discussions about mental health on social media platforms, it is crucial to build AI models that can automatically detect and classify posts related to different mental health issues. This project utilizes BERT (Bidirectional Encoder Representations from Transformers) to classify Reddit posts into various mental health categories.

## Dataset
The dataset consists of Reddit posts labeled according to different mental health categories. Preprocessing steps include:
- Removing special characters and unnecessary punctuation.
- Tokenizing text using a BERT tokenizer.
- Splitting data into training and testing sets.

## Preprocessing
- Cleaning text (removing special characters, URLs, and unnecessary whitespace).
- Tokenizing and encoding the text using the `BertTokenizer`.
- Padding sequences to a fixed length.
- Splitting the dataset into training and testing sets.

## Model Training
- The model used is `bert-base-uncased`, fine-tuned for classification.
- Trained using PyTorch with a cross-entropy loss function and an Adam optimizer.
- Training includes early stopping and learning rate scheduling.
- Training progress is monitored using validation loss and accuracy.

## Evaluation
- Model performance is evaluated using accuracy, precision, recall, and F1-score.
- Confusion matrix is plotted for further analysis.

## Visualization
- Training and validation loss curves.
- Confusion matrix to analyze misclassifications.
- Word clouds and other exploratory data analysis techniques.

## Installation
To set up the project, install the required dependencies:

```bash
pip install torch transformers datasets scikit-learn matplotlib seaborn
```

## Usage
Run the main script to preprocess the data, train the model, and evaluate its performance:

```bash
python train_model.py
```

To visualize the results:
```bash
python visualize_results.py
```

## Results
- The model achieved high accuracy on the test set.
- Common misclassifications were analyzed using confusion matrices.
- Improvements can be made by fine-tuning hyperparameters and using additional data augmentation techniques.
- But could ne apply on the dataset given by emitrr.
![Finetuning Result Analysis](https://github.com/Shrey152002/Task2emitrr/blob/main/Screenshot%20(10).png)
![Finetuning Result Analysis](https://github.com/Shrey152002/Task2emitrr/blob/main/Screenshot%20(9).png)
![Finetuning Result Analysis](https://github.com/Shrey152002/Task2emitrr/blob/main/Screenshot%20(8).png)
![Finetuning Result Analysis](https://github.com/Shrey152002/Task2emitrr/blob/main/Screenshot%20(7).png)
![Finetuning Result Analysis](https://github.com/Shrey152002/Task2emitrr/blob/main/Screenshot%20(6).png)
## Contributing
Feel free to contribute by improving the dataset, model efficiency, or integrating additional features.

## License
This project is open-source and available under the MIT License.

