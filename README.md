# PDF to Flashcards

This project allows users to upload PDF study materials and converts them into question-answer flashcards using AWS services.

## Architecture

- **S3**: Stores uploaded PDFs.
- **Lambda**: Processes PDFs and generates flashcards.
- **API Gateway**: Exposes endpoints for uploading PDFs and fetching flashcards.
- **DynamoDB**: Stores the generated flashcards.
