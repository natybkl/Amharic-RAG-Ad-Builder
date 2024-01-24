# Amharic RAG Ad Builder
## Enabling Quality Embedding and Text Generation for Amharic Language

Welcome to the Amharic RAG Ad Builder repository! This project is initiated by AIQEM, an African startup specializing in AI and Blockchain solutions. The primary objective is to enhance the impact of technological innovations in the Ethiopian and African business landscape. The latest flagship project, Adbar, is an end-to-end AI-based Telegram Ad solution that optimally places ads to different Telegram channels through a network of bots and extensive data analysis.

## Business Need

As Telegram gains prominence as a messaging platform, AIQEM recognizes the necessity to adapt its advertising strategy to better align with this evolving ecosystem. The focus is on improving the effectiveness of promotional efforts by integrating powerful AI capabilities for Amharic text manipulation. Specifically, the project aims to create an Amharic RAG pipeline that generates creative text ad content for Telegram channels based on campaign information, including brand details and product information.

The success of this project ensures that advertisements are not only catchy but also highly relevant to the Telegram community. To achieve this, the technology must possess quality Amharic text embedding and text generation capabilities. The approach involves choosing a suitable open-source Large Language Model (LLM), such as Mistral, Llama 2, Falcon, or Stable AI 2, and further fine-tuning it to meet the business objectives.

## Project Overview

The project is organized into several tasks to achieve the business goals:

1. **Literature Review & Huggingface Ecosystem (Task 1):**
   - Understand key concepts and methods related to LLMs.
   - Explore the Huggingface ecosystem for inference and fine-tuning.
   - Review relevant literature and resources.

2. **Load an LLM and Use It for Inference (Task 2):**
   - Set up the work environment.
   - Choose an open-source LLM and load it.
   - Test the model's inference capabilities for various scenarios.

3. **Data Preprocessing and Preparation (Task 3):**
   - Parse and clean raw Telegram message data.
   - Extract and remove unnecessary features.
   - Prepare the data for fine-tuning.

4. **Fine-Tuning the LLM (Task 4):**
   - Understand the key components of LLM training and fine-tuning.
   - Choose a base model and fine-tune it for Amharic text.
   - Explore Huggingface documentation for inference and fine-tuning.

5. **Build a RAG Pipeline to Generate Telegram Amharic Ad Posts (Task 5):**
   - Implement RAG techniques for Amharic text generation.
   - Retrieve relevant information from English and Amharic texts.
   - Evaluate and deploy the RAG pipeline with a simple frontend.

## Repository Structure

- **assets:** Contains additional project assets.
- **demo:** Includes any demonstration files or resources.
- **modeling:** Holds scripts and code related to model training and fine-tuning.
- **notebooks:** Jupyter notebooks for exploratory data analysis and documentation.
- **scripts:** Contains utility scripts for various tasks.
- **utils:** Utility functions and helper modules.
- **backend:** FastAPI backend for serving the RAG model.
- **frontend:** React frontend for a user-friendly interface.

## How to Use

1. Clone the repository: `git clone https://github.com/group-3-collab-team/Amharic-RAG-Ad-Builder.git`
2. Navigate to the `backend` directory: `cd backend`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the FastAPI backend: `uvicorn main:app --reload`
5. Open a new terminal window, navigate to the `frontend` directory: `cd ../frontend`
6. Install frontend dependencies: `npm install`
7. Start the React frontend: `npm start`
8. Open your browser and go to `http://localhost:3000` to interact with the RAG Ad Builder.

## Contributors

- Abel Bekele (@AbelBekele)
- Birehan Anteneh (@birehan)
- Ekram Kedir (@ekram-kedir)
- Keriii (@Keriii)
- Mubarek Hussen (@MubarekHussen)
- Natnael Bekele (@natybkl)

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to contribute, provide feedback, or use the code as needed!