import streamlit as st 
from lida import Manager, TextGenerationConfig , llm  
import openai
from PIL import Image
from io import BytesIO
import base64
import pandas as pd
from json_to_csv import ldjson_to_csv, json_to_csv

#......Intial approach ...... 
# def load_data(file):
#     if file.name.endswith(".csv"):
#         data = pd.read_csv(file)
#     elif file.name.endswith(".xls") or file.name.endswith(".xlsx"):
#         data = pd.read_excel(file)
#     elif file.name.endswith(".json"):
#         data = pd.read_json(file)
#     else:
#         st.error(
#             "Unsupported File Type! Please upload any .csv (or) .xls (or) .xlsx (or) .json files !"
#         )
#         return None
#     return data


# st.title("Visualize your Data using this application!")

# with st.sidebar:
#     st.subheader("Upload Your Data Here!")
#     uploaded_file = st.file_uploader(
#         "Upload your CSV, Excel or JSON file", type=["csv", "xlsx", "json"]
#     )

# if uploaded_file is not None:
#     data = load_data(uploaded_file)
#     if data is not None:
#         st.write("Preview:", data.head())

#         query = st.text_area(
#             "Query your Data : ",
#             height=150,
#         )

#         if st.button("Generate Charts!"):
#             if len(query) > 0:
#                 st.info("Your Query : " + query)

#                 # Load FLAN-T5 model
#                 # model_name = "google/flan-t5-small"  # or "flan-t5-base" for better accuracy
#                 model_name = "uukuguy/speechless-llama2-hermes-orca-platypus-13b"
#                 # tokenizer = AutoTokenizer.from_pretrained(model_name)
#                 # # model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
#                 # model = AutoModelForSeq2SeqLM.from_pretrained(
#                 #     model_name,
#                 #     torch_dtype=dtype,  # Change to torch.bfloat16 if supported
#                 #     device_map="auto",
#                 # )

#                 # # Generate text using FLAN-T5
#                 # input_text = f"{query}: {data.to_string()}"
#                 # inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)
#                 # inputs = {key: value.to(dtype) for key, value in inputs.items()} 
#                 # inputs["input_ids"] = inputs["input_ids"].to(torch.long)  # Ensure input_ids are integers
#                 # outputs = model.generate(**inputs, max_length=200)
#                 # summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
#                 # lida = Manager()
#                 lida = Manager(
#                     text_gen=llm(
#                         provider="hf",
#                         model=model_name,
#                         device_map={"": "cpu"}
#                     )
#                 )

#                 textgen_config = TextGenerationConfig(
#                     model=model_name, n=1, temperature=0.4, use_cache=True
#                 )   

#                 summary = lida.summarize(
#                     data, summary_method="default", textgen_config=textgen_config
#                 )

#                 library = "seaborn"

#                 textgen_config = TextGenerationConfig(
#                     n=1, temperature=0.5, use_cache=True
#                 )

#                 charts = lida.visualize(
#                     summary=summary,
#                     goal=query,
#                     textgen_config=textgen_config,
#                     library=library,
#                 )

#                 image_base64_string = charts[0].raster

#                 img = base64_to_image(image_base64_string)

#                 st.image(img)


openai.api_key =  st.secrets["OPENAI_API_KEY"]

def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)
    
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))

#....Implemention of LIDA arcitechture begins here....

lida = Manager(text_gen = llm("openai"))
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-0125", use_cache=True)

menu = st.sidebar.selectbox("Choose an Option", ["Summarize", "Question based Graph"])

if menu == "Question based Graph":
    st.subheader("Query your Data to Generate Graph")
    file_uploader = st.file_uploader("Upload your CSV or JSON or LDJSON", type=["csv","json","ldjson"])
    print(file_uploader)
    if file_uploader is not None:
        file_ext = file_uploader.name.split(".").pop()
        path_to_save = f"datafile.{file_ext}"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        if file_ext == "ldjson":
            ldjson_to_csv(path_to_save)
        elif file_ext == "json":
            json_to_csv(path_to_save)
        text_area = st.text_area("Query your Data to Generate Graph", height=200)
        if st.button("Generate Graph"):
            if len(text_area) > 0:
                st.info("Your Query: " + text_area)
                lida = Manager(text_gen = llm("openai")) 
                textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
                summary = lida.summarize("datafile.csv", summary_method="default", textgen_config=textgen_config)
                user_query = text_area
                charts = lida.visualize(summary=summary, goal=user_query, textgen_config=textgen_config)  
                charts[0]
                image_base64 = charts[0].raster
                img = base64_to_image(image_base64)
                st.image(img)

elif menu == "Summarize":
    st.subheader("Summarization of your Data")
    file_uploader = st.file_uploader("Upload your CSV or JSON or LDJSON", type=["csv","json","ldjson"])
    if file_uploader is not None:
        file_ext = file_uploader.name.split(".").pop()
        path_to_save = f"datafile.{file_ext}"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        if file_ext == "ldjson":
            ldjson_to_csv(path_to_save)
        elif file_ext == "json":
            json_to_csv(path_to_save)
        summary = lida.summarize("datafile.csv", summary_method="default", textgen_config=textgen_config)
        st.write(summary)
        # goals = lida.goals(summary, n=2, textgen_config=textgen_config)
        # for goal in goals:
        #     st.write(goal)
        #     break
        # i = 0
        # library = "seaborn"
        # textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
        # charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)
        # img_base64_string = charts[0].raster
        # img = base64_to_image(img_base64_string)
        # st.image(img)
        


        

