import streamlit as st
from lida import Manager, TextGenerationConfig, llm
import os
import base64
from PIL import Image
from io import BytesIO
import pandas as pd
import time


def base64_to_image(base64_string):
    byte_data = base64.b64decode(base64_string)
    return Image.open(BytesIO(byte_data))


def load_data(file):
    if file.name.endswith(".csv"):
        data = pd.read_csv(file)
    elif file.name.endswith(".xls") or file.name.endswith(".xlsx"):
        data = pd.read_excel(file)
    elif file.name.endswith(".json"):
        data = pd.read_json(file)
    else:
        st.error(
            "Unsupported File Type! Please upload any .csv (or) .xls (or) .xlsx (or) .json files !"
        )
        return None
    return data


st.title("Visualize your Data using this application!")

with st.sidebar:
    st.subheader("Upload Your Data Here!")
    uploaded_file = st.file_uploader(
        "Upload your CSV, Excel or JSON file", type=["csv", "xlsx", "json"]
    )

if uploaded_file is not None:
    data = load_data(uploaded_file)
    if data is not None:
        st.write("Preview:", data.head())

        query = st.text_area(
            "Query your Data : ",
            height=150,
        )

        if st.button("Generate Charts!"):
            if len(query) > 0:
                st.info("Your Query : " + query)
                lida = Manager(
                    text_gen=llm(
                        provider="palm",
                        palm_key_file=os.environ["PALM_SERVICE_ACCOUNT_KEY_FILE"],
                        project_id=os.environ["PALM_PROJECT_ID"],
                        project_location=os.environ["PALM_PROJECT_LOCATION"],
                        api_key=None,
                    )
                )

                textgen_config = TextGenerationConfig(
                    model="text-bison@002", n=1, temperature=0.4, use_cache=True
                )

                summary = lida.summarize(
                    data, summary_method="default", textgen_config=textgen_config
                )

                library = "seaborn"

                textgen_config = TextGenerationConfig(
                    n=1, temperature=0.5, use_cache=True
                )

                charts = lida.visualize(
                    summary=summary,
                    goal=query,
                    textgen_config=textgen_config,
                    library=library,
                )

                image_base64_string = charts[0].raster

                img = base64_to_image(image_base64_string)

                st.image(img)
