import pandas as pd
import pickle
import streamlit as st


df = pd.read_csv("netflix_titles.csv")
cosine_sim = pickle.load(open("similar.pkl", "rb"))

def get_recommendations(title):
    indx = df[df['title'].str.lower() == title.lower()].index

    if len(indx) == 0:
        return []
    indx = indx[0]
    
    sim_scores = list(enumerate(cosine_sim[indx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    show_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[show_indices].tolist()


st.title("Netflix Show Recommendation System")

show_list = df['title'].dropna().unique().tolist()
selected_show = st.selectbox("Choose a TV show", sorted(show_list))


if st.button("Recommend"):
    recommendations = get_recommendations(selected_show)
    if recommendations:
        st.success("Recommended shows:")
        for show in recommendations:
            st.write("•", show)
    else:
        st.warning("No similar shows found.")