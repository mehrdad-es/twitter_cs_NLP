# test-twitter-customer_service-NLP

* setup python script to access twitter API to get customer service conversations

---
Project Steps
0. Dependencies, AWS CDK and Prerequisites
1. ETL
    1. Extract with Selenium
    2. Push to AWS S3
    3. Perform transform
    4. Setup Crawler and push to Glue Database
    5. Setup Setup function
    6. (Optional) Setup Eventbridge Notification with SNS
2. Feature Engineering and Feature Store
3. Data Quality Monitoring (anomalies, drift, etc.)
4. ML model development
5. Productionalizing the model
6. Select deployment type (batch, near real-time, real-time) and deploy
7. Monitoring Model Performance
8. Model Registry
9. (Optional) custom dashboard for performance monitoring
10. Capturing false positives and negatives and sending them to ETL
