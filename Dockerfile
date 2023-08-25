FROM python:3.9

ADD src/model_deployment/inference.py .
ADD model_registry/2023/jul/model_export_iphone6/label_spread_rbf_with_ChatGPT.sav .
RUN pip install openai
RUN pip install scikit-learn

CMD ["python","./inference.py"]

# You have to add your bearer_token env variable during runtime of docker
# using -e bearer_token
# because the python function asks for user input a -i is necessary
# docker run command will look like this:
# docker run -e bearer_token -i {docker_build_name}

