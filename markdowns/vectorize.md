# Vectorize your documents

This project uses [chroma db](https://docs.trychroma.com/) for storing
document embeddings/vectors.

At this time I've noticed good results with PDF _text_ and reqular text documents. The instructions will be updated when I play with other document types.

- The project comes with a free PDF book [dracula.pdf](https://www.planetebook.com/free-ebooks/dracula.pdf) in `./documents` directory. I noticed that the extracted texts from the PDF version of dracula gives much better results than the free dracula.txt and time [Project Gutenberg](https://www.gutenberg.org/). If you want, copy some PDF files to `./documents` directory and vectorize them. If new documents are found, they will be appended to the vector database.

```
copy file.pdf ./documents
```

- Vectorize

```
python3 ./ingest/ingest.py or ./ingest.sh
```

The vector database will be created in `./db` directory as configured in `config.py`.