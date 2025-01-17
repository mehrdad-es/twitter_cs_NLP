# Product Feedback NLP on Twitter
## Intro
Product users often talk about their experience on twitter (perhaps more than any other platform). However, comprehending the large number of tweets and sifting through irrelevant product mentions (posts which are not product feedback like spam, secondary-sales, irrelevant reference to the product) is very difficult to be done with a rule-based approach. Hence, NLP (i.e. word2vec embeddings) was used to simplify understanding product feedback on Twitter through semi-supervised learning.
## Getting started
In ./notebooks you will find the steps to recreate the models that based on the vector embedding (i.e. openai vector embedding) of a tweet text classify whether it is product feedback or not. To play with saved models visit the ./model_registry folder or run the Dockerfile. 
* Make sure to change "data bucket template" folder name to just "bucket" before testing.
* To view the python source code visit ./src
## Project Steps
1. Get Tweets
2. ETL
3. Feature Store (feature engineering)
4. Data Quality Monitoring
5. ML model development
6. ML model deployment
## Next Steps
- [ ] Model performance monitoring
- [x] Docker containerization
- [x] Clustering Experimentation
