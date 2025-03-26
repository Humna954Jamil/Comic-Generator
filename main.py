import streamlit as st
import requests
import json
from PIL import Image
import io
import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/"
HUGGINGFACE_HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# Generate Story Function
def generate_story(genre, characters, writing_style, story_length):
    model_name = "mistralai/Mistral-7B-Instruct-v0.2"
    length_descriptions = {
        "Short Story": "2 paragraphs",
        "Episode-Based": "a few short episodes",
        "Long Novel": "2 pages long"
    }

    character_details = "\n".join([
        f"- Name: {char['name']}\n  - Traits: {char['traits']}\n  - Background: {char['background']}"
        for char in characters
    ])

    template = f"""
    Write a {length_descriptions[story_length]} story in the {genre} genre with a {writing_style} tone.
    The story should focus on the following characters:
    {character_details}
    Ensure the story is engaging, well-structured, and includes a character arc.
    """

    prompt = PromptTemplate(input_variables=[], template=template)
    llm = HuggingFaceHub(repo_id=model_name, huggingfacehub_api_token=HUGGINGFACE_API_KEY)
    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        response = chain.invoke({})
        story_text = response.get("text", "").strip() if isinstance(response, dict) else str(response).strip()
        formatted_story = "\n\n".join(story_text.split(". "))
        title = story_text.split(".")[0] if "." in story_text else "Untitled Story"
        return title, formatted_story
    except Exception as e:
        return "Error", f"🚨 Story generation failed: {str(e)}"

# Generate Image Function
def generate_image(prompt):
    model_name = "runwayml/stable-diffusion-v1-5"
    formatted_prompt = f"A high-quality image of {prompt} in an artistic style."
    api_url = f"{HUGGINGFACE_API_URL}{model_name}"

    response = requests.post(api_url, headers=HUGGINGFACE_HEADERS, json={"inputs": formatted_prompt})

    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    return None

# Streamlit UI
def main():
    st.title("✨ AI Story Generator ✨")
    st.sidebar.header("📜 Story Settings")

    # Sidebar Inputs
    genre = st.sidebar.selectbox("📖 Choose a Genre", ["Fantasy", "Sci-Fi", "Mystery", "Horror", "Romance", "Adventure"])
    writing_style = st.sidebar.selectbox("✍️ Choose Writing Style", ["Formal", "Humorous", "Dark", "Casual"])
    story_length = st.sidebar.radio("📏 Select Story Length", ["Short Story", "Episode-Based", "Long Novel"])

    num_characters = st.sidebar.slider("👥 Number of Characters", 1, 2, 1)
    characters = []
    for i in range(num_characters):
        name = st.sidebar.text_input(f"🧑‍🎨 Character {i+1} Name", f"Character {i+1}")
        traits = st.sidebar.text_area(f"💡 Character {i+1} Traits", "Brave, witty, curious")
        background = st.sidebar.text_area(f"📜 Character {i+1} Background", "A young adventurer seeking the truth about an ancient prophecy.")
        characters.append({"name": name, "traits": traits, "background": background})

    # Story Generation Button
    story = None
    if st.sidebar.button("🎭 Generate Story"):
        with st.spinner("🔮 Crafting your story..."):
            title, story = generate_story(genre, characters, writing_style, story_length)

    # Display Story
    if story:
        st.subheader(f"📖 {title}")
        st.markdown(f"""
        <div style='padding: 15px; background-color: #f9f9f9; border-radius: 10px; text-align: justify; font-size: 16px;'>
        {story.replace("\n", "<br>")}
        </div>
        """, unsafe_allow_html=True)

        # Download Button
        st.download_button("📥 Download Story", story, file_name="generated_story.txt")

        # Character Images
        for char in characters:
            st.subheader(f"🖼 Image for {char['name']}")
            image_prompt = f"A {genre.lower()} character with traits: {char['traits']}, in an artistic fantasy style."
            with st.spinner(f"🎨 Creating an image for {char['name']}..."):
                image = generate_image(image_prompt)
                if image:
                    st.image(image, caption=f"{char['name']} - {genre} Character", use_container_width=True)
                    image_bytes = io.BytesIO()
                    image.save(image_bytes, format='PNG')
                    st.download_button(f"📥 Download {char['name']}'s Image", image_bytes.getvalue(), file_name=f"{char['name']}.png", mime="image/png")
                else:
                    st.error(f"🚨 Failed to generate image for {char['name']}. Try again later.")

if __name__ == "__main__":
    main()
