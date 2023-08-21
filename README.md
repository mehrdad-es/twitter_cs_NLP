# Twitter Customer Service NLP
Product users often talk about their experience on twitter (perhaps more than any other platform). However, comprehending the large number of tweets and sifting through irrelevant product mentions (posts which are not product feedback) is very difficult to be done with a rule-based approach. Hence, NLP was used to simplify understanding product feedback on Twitter.

In this repository you will find the steps to recreate the models that based on the vector embedding (i.e. openai vector embedding) of a tweet text classify whether it is product feedback or not. To play with saved models visit the ./models folder. 

* Make sure to change "bucket template" folder name to just "bucket" before testing.
* To start open the numbered notebooks in order in ./notebooks
* To view the python source code visit ./src
---
## Project Steps
1. Scrape Twitter
2. ETL
3. Feature Engineering->(with chatgpt and openai embeddings)
4. Data Quality Monitoring
5. ML model development
---
## TODO
1. Model performance monitoring
2. Docker containerization
3. Clustering Experimentation
