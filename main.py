import streamlit as st
from openai import OpenAI

api_key = st.secrets["OPENAI-SECRET"]
client = OpenAI(api_key=api_key)

# def financial_evaluation():
#     pass

def create_story(income, state, slider_values, comment):
    prompt = f"""The user has a monthly income of RM{income} and is from {state}. The ratio of money to spend on each category is as follows:
    - Entertainment: {slider_values[0]}%
    - Food: {slider_values[1]}%
    - Travel: {slider_values[2]}%
    - Shopping: {slider_values[3]}%
    - Health: {slider_values[4]}%
    - Other: {slider_values[5]}%

    Additional comments: {comment}

    Generate a budget table for Monday to Sunday, considering the region's overall food cost."""

    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are the best budget planner for beginners. You will take users' prompts and generate a table for budget planning. the x-axis will be Food, Travel, Shopping, Health, and Others. Make the bar graph for each category. The y-axis will be the price based on percentage of the user's income., the visuale will be a bar graph. The table will be in the format of a budget table."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
        temperature=0.8
    )

    story = completion.choices[0].message.content
    return story

gif_html = """
<div style="text-align: center;">
    <img src="https://media.giphy.com/media/l0Ex6kAKAoFRsFh6M/giphy.gif" alt="Yvng Swag GIF">
</div>
"""

st.markdown(gif_html, unsafe_allow_html=True)


st.subheader('Finance Planner with OpenAI API', divider='rainbow')
st.write('This Finance Planner would help you to plan your financial budget.')

# 초기값 설정
income = st.number_input("Enter your monthly income (RM):", min_value=0)
target = st.slider("Select your target saving (%)", 0, 100, 50, step=5)

state = st.selectbox("Select a state", ("Johor", "Kedah", "Kelantan", "Malacca", "Negeri Sembilan", "Pahang", "Penang", "Perak", "Perlis", "Selangor", "Sarawak", "Sabah", "Terengganu"))

# 슬라이더 초기값 설정
initial_values = [10, 10, 10, 10, 10, 10]
sliders = ['Entertainment', 'Food', 'Travel', 'Shopping', 'Health', 'Other']
slider_values = []

st.markdown("<h3 style='text-align: center; font-weight: bold;'>Ratio of money to spend on each category.</h3>", unsafe_allow_html=True)

for i, slider in enumerate(sliders):
    value = st.slider(slider, 0, 100, initial_values[i], step = 5, key=i)
    slider_values.append(value)

total_sum = sum(slider_values)

if total_sum > 100:
    st.error(f"Total value exceeds 100! Current total: {total_sum}")
else:
    st.success(f"Current total: {total_sum}")

comment = st.text_input("Give me if you want to let me know about some personal finance preferences. Example: I want to spend very less only on Tuesday.")
submitted = st.button("Submit")

if submitted:
    result = create_story(income*(100-target)/100/4, state, slider_values, comment)
    st.write(result)

st.markdown("Enjoy! :sunflower:")

