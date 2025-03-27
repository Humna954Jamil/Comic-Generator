# Comic-Generator
I’m a big fan of mangas, comics, and webtoons, and I want to explore creating original comics tailored to fan preferences. Right now, I’m sharing the initial version of my story and character generation process.

# Approach

**A. User Input**

1. User selects genre, writing style, and story length.

2. Defines characters with names, traits, and backgrounds.

**B. Story Generation (Mistral-7B-Instruct)**

1. A structured prompt generates the story.

2. The story is formatted and displayed.

3. Users can download it as a text file.

**C. Character Image Generation (Stable Diffusion)**

1. AI generates artistic images based on character traits.

2. Images are displayed alongside the story.

3. Users can download them.

# How to Run the Streamlit App
Follow these steps to set up and run story generator Streamlit app:
1. Install Dependencies:

   **pip install -r requirements.txt**

2. Create a .env File:

   **HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_key_here**
3. Run the Streamlit App:

    **streamlit run main.py**

4. Interact with the App

   * Open the link displayed in the terminal (usually http://localhost:8501).

   * Customize the story settings (genre, characters, writing style, etc.).

   * Click "Generate Story" to create a unique AI-generated story.

   * View and download the generated story and images.






