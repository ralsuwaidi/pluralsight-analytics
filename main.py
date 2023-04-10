from pandas._libs.tslibs import nat_strings
import streamlit as st
import pandas as pd
import json
from models.user import User, Skill
import utils
import plotly.express as px
import plotly.graph_objects as go


st.write(
    """
# Coders(hq) Assessment
Analytics of GiTex Coders(hq) assessment booth

## Overview

In the four days of gitext we had `338` people create an account but only `252` took a test. 
The total amount of tests taken is `377` (any person can take more than one test)
"""
)

# Get data
f = open("users.json")
data = json.load(f)
df = pd.json_normalize(data)

flattened_data = utils.flatten_json(data)
df = pd.json_normalize((flattened_data))

# lists for easy use
user_list = utils.json_to_user(data)
local_list = [user for user in user_list if user.is_local]
non_local_list = [user for user in user_list if not user.is_local]
male = [user for user in user_list if user.gender == "M"]
female = [user for user in user_list if user.gender == "F"]
local_male = [user for user in user_list if user.gender == "M" and user.is_local]
local_female = [user for user in user_list if user.gender == "F" and user.is_local]
lfj = [user for user in user_list if user.is_seeking_job]
llfj = [user for user in user_list if user.is_seeking_job and user.nationality=='AE']

# -----


## Nationality

st.write(
    """## Nationality
Most of the people who took the skill tests where indian (around 40%) while Emiratis
while emiratis compromised around 10% of the total.
"""
)
fig = px.bar(df, x="nationality")
st.plotly_chart(fig, use_container_width=True)

st.write("The number of emiratis who took the tests are around 10%")
labels = ["Emirati", "Other"]
values = [len(local_list), len(non_local_list)]
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
st.plotly_chart(fig, use_container_width=True)

st.write("### Nationality per skill assessed")
nationality = (
    df.groupby(["nationality"])["nationality"].count().reset_index(name="count")
)
nationality.loc[nationality["count"] < 7, "nationality"] = "Other"
fig = px.pie(nationality, values="count", names="nationality")
st.plotly_chart(fig, use_container_width=True)


## Gender

st.write(
    """## Gender
As expected, more males took the tests than females. Although the disparity is much
less with emiratis.
"""
)

st.write("### Total male / female ratio")
labels = ["Male", "Female"]
values = [len(male), len(female)]
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
st.plotly_chart(fig, use_container_width=True)

st.write("Emirati male / female ratio")
labels = ["Male", "Female"]
values = [len(local_male), len(local_female)]
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
st.plotly_chart(fig, use_container_width=True)

## Skills

st.write(
    """## Skills
Skills were distrebuted based on quintile levels **
* novice: 1
* proficient-emerging: 2
* proficient-average: 3
* proficient-above-average: 4
* expert: 5
** where 1 is the lowest and 5 is the highest score
"""
)
quintileLevel = (
    df.groupby(["quintileLevel"])["quintileLevel"].count().reset_index(name="count")
)
fig = px.pie(quintileLevel, values="count", names="quintileLevel")
st.plotly_chart(fig, use_container_width=True)

st.write("### Emirati skill distribution")
local = df.loc[df["nationality"] == "AE"]
local_skill = (
    local.groupby(["quintileLevel"])["quintileLevel"].count().reset_index(name="count")
)
fig = px.pie(local_skill, values="count", names="quintileLevel")
st.plotly_chart(fig, use_container_width=True)

st.write(
    """### Expert skill distribution
This is the distribution of anyone who got an expert 
assessment result. India and Pakistan has more experts than the rest combined
"""
)
experts = df.loc[df["quintileLevel"] == "expert"]
nationality = (
    experts.groupby(["nationality"])["nationality"].count().reset_index(name="count")
)
nationality.loc[nationality["count"] < 2, "nationality"] = "Other"
fig = px.pie(nationality, values="count", names="nationality")
st.plotly_chart(fig, use_container_width=True)

cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]
table = df.loc[df["nationality"] == "AE"].loc[
    :,
    df.columns.intersection(
        [
            "skillName",
            "quintileLevel",
            "is_seeking_job",
            "first_name",
            "last_name",
            "id",
            "academic_qualification",
        ]
    ),
]


fig = go.Figure(
    data=[
        go.Table(
            header=dict(values=list(table.columns), align="left"),
            cells=dict(
                values=[
                    table.first_name,
                    table.last_name,
                    table.is_seeking_job,
                    table.quintileLevel,
                    table.skillName,
                ],
                align="left",
            ),
        )
    ]
)
st.plotly_chart(fig, use_container_width=True)

table

st.write("### Total looking for jobs")
labels = ["Looking for jobs", "Not looking for jobs"]
values = [len(lfj), len(user_list)]
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
st.plotly_chart(fig, use_container_width=True)

st.write("### Local looking for jobs")
labels = ["Looking for jobs", "Not looking for jobs"]
values = [len(llfj), len(local_list)]
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
st.plotly_chart(fig, use_container_width=True)