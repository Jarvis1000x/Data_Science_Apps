import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image


image = Image.open("image.jpg")
st.image(image, use_column_width=True)
st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA
***
""")

sequence_input = ">DNA Query \nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

sequence = st.text_area("Sequence Input", sequence_input, height=250)
sequence = sequence.splitlines()
sequence = sequence[1:]
sequence = ''.join(sequence)

st.write("""
***
""")

st.header("INPUT (DNA Query)")
sequence

st.header("OUTPUT (DNA Nucleotide Count)")

st.subheader("1. Print Dictionary")
def DNA_nucleotide_count(seq):
    d = dict([
        ("A", seq.count("A")),
        ("T", seq.count("G")),
        ("G", seq.count("G")),
        ("C", seq.count("C"))
    ])
    return d

X = DNA_nucleotide_count(sequence)
X_label = list(X)
X_values = list(X.values())
X

st.subheader("2. Print Text")
st.write("There are " + str(X["A"]) + " adenine (A)")
st.write("There are " + str(X["T"]) + " thymine (T)")
st.write("There are " + str(X["G"]) + " guanine (G)")
st.write("There are " + str(X["C"]) + " cytosine (C)")

st.subheader("3. Displaying Dataframe")
df = pd.DataFrame.from_dict(X, orient="index")
df = df.rename({0: "count"}, axis="columns")
df.reset_index(inplace=True)
df = df.rename(columns = {"index":"nucleotide"})
st.write(df)

st.subheader('4. Display Bar chart')
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)
p = p.properties(
    width=alt.Step(80)
)
st.write(p)





