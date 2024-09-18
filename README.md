# Chatterbox: RAG Chatbot with Streamlit

Welcome to **Chatterbox**, a Retrieval-Augmented Generation (RAG) Chatbot application! Chatterbox allows users to interact with documents through a conversational interface, powered by Streamlit. The app is designed to facilitate easy and efficient document retrieval and conversation, making it ideal for use cases such as customer support, educational tools, and research assistance.

## Features

- **Chat with Documents**: Engage in a conversation with your documents. Chatterbox uses advanced retrieval techniques to provide relevant responses based on the content of the documents.
- **Session Storage**: Enjoy extended conversations with session storage support. The app retains context across multiple interactions, allowing for a seamless chat experience.
- **User-Friendly Interface**: Built with Streamlit, Chatterbox offers a clean and intuitive user interface for easy navigation and interaction.
- **Document Upload**: Users can upload their own documents for personalized interaction.

## Requirements

To run this application, you will need:

- Python 3.8 or higher
- Streamlit
- Additional libraries (listed in `requirements.txt`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Quirky-AI-Labs/chatterbox.git
   cd chatterbox
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

4. Open your web browser and navigate to `http://localhost:8501` to access Chatterbox.

## Usage

1. **Upload Documents**: Start by uploading your documents using the provided interface. Supported formats include PDF, DOCX, and TXT.
2. **Start Chatting**: Once your documents are uploaded, initiate a conversation by typing your questions in the chat interface.
3. **Session Management**: Chatterbox automatically manages your session, allowing you to continue your conversation without losing context.

## Example Interaction

- **User**: What is the main topic of the document?
- **Chatterbox**: The main topic of the document is about the impact of climate change on marine life.

## Contributing

Contributions are welcome! If you'd like to contribute to Chatterbox, please fork the repository and submit a pull request with your changes.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

Happy chatting with your documents in **Chatterbox**! 🚀
