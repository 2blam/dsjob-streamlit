# DS Job UI 
The dashboard was run by using Streamlit Docker. I used MongoDB as the backend for reporting.

Instruction:
1. Clone streamlit-docker repo - https://github.com/MrTomerLevi/streamlit-docker
2. Copy the ```docker/requirements.txt``` and ```Dockerfile``` to streamlit-docker directory - which instruct the docker to install the related libraries, e.g. Pymongo, Plotly
3. Build the custom image command: ```docker build -t tomerlevi/streamlit-docker .```. If everything works fine, then a new image named ```tomerlevi/streamlit-docker:latest``` was created. (use command: ```docker images``` to verify)
4. Create a hidden directory ```.streamlit``` in the project folder
5. Go to ```.streamlit``` and create a file named ```secret.toml``` and provide the related mongo db connection information, for example:

```
[mongo]
host = "localhost"
port = 27017
username =""
password =""
```

6. Go back to your project home directory and run the streamlit by command: ```docker run -it --net=host  -v ~/dsjob-streamlit/:/app tomerlevi/streamlit-docker:latest app.py```

Note: in this repo, I did not provide the database. I just want to share how to use the streamlit-docker and how to use streamlit to gather the data from MongoDB
