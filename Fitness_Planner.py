import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import pathlib

load_dotenv()
API_KEY = os.getenv("openai_api_key")
client = OpenAI(api_key=API_KEY)

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("assets/styles.css")
load_css(css_path)

def get_workout_plan(fitness_goal, muscle, cardio, calories, time, rest_days, age, weight, height, calories2, day):
    prompt = f"""
    Create a 7 day schedule in the form of a plain text table 
    the schedule should be based on:
    - Fitness goal: {fitness_goal}
    - To find out the muscle they want to grow: {muscle}
    - To find their preferred cardio machine: {cardio}
    - Amount of calories they burn each day: {calories}
    - Amount of calories they would like to burn: {calories2}
    - Amount of time they want to work out each day: {time}
    - Amount of rest days per week: {rest_days}
    - Age: {age}
    - Weight: {weight}
    - Height: {height}
    - The specific days they can work out: {day}

    Requirements: 
    1. Organize everything neatly as a plain text chart with rows and columns
    2. Include minimum 3 exerices per muscle group
    3. Do not use any html tags
    4. Output must look like a clean table that can be copied directly into a text file
    """
    response = client.chat.completions.create(
        model = "gpt-4.1",
        messages = [
            {"role": "system", "content": "You are a fitness expert"},
            {"role": "user", "content": prompt }
        ]
    )

    return response.choices[0].message.content


def main():
    st.title("AI Fitness Planner")
    st.write("Let's help you achieve your fitness goal")

    menu = ["Basic Info", "Fitness Goals", "Get Workout Schedule"]
    choice = st.sidebar.radio("Fitness_planner", menu)

    if "user_inputs" not in st.session_state:
        st.session_state.user_inputs = {}

    if choice == "Basic Info":
        st.header(" Basic Info")
        age = st.text_input(
            "* What is your age?",
            value=st.session_state.user_inputs.get("age", "")
        )

        weight = st.text_input(
            "* What is your weight?",
            value=st.session_state.user_inputs.get("weight", "")
        )

        height = st.text_input(
            "* What is your height?",
            value=st.session_state.user_inputs.get("height", "")
        )

        calories = st.text_input(
            "* How many calories do you approximately burn",
            value=st.session_state.user_inputs.get("calories", "")
        )

        

        if st.button("Save Info", key="orange"):
            st.session_state.user_inputs.update({
                "age": age,
                "weight": weight,
                "height": height,
                "calories": calories
            })

    elif choice == "Fitness Goals":
        fitness_goal = st.selectbox(
            "* What is your fitness goal?",
            ["Lose Wight", "Gain Weight"],
        index=["Lose Wight", "Gain Weight"].index(st.session_state.user_inputs.get("fitness_goal", "Lose Wight")))
        muscle_type = ["Triceps", "Biceps", "Forearms", "Shoulders", "Lats", "Traps", "Chest", "Abs", "Obliques", "Quads", "Calfs", "Fullbody"]
        muscle = st.multiselect(
            "* Choose all the muscles you mainly want to grow",
            muscle_type,
            default=st.session_state.user_inputs.get("muscle", ["Biceps", "Shoulders"])
        )        
        cardio_type = ["Treadmill", "Elliptical", "Stair Master", "Curve Treadmill", "Stationary bikes"]
        cardio = st.multiselect(
            "* Choose all the cardio machines you want to use",
            cardio_type,
            default=st.session_state.user_inputs.get("cardio", ["Treadmill", "Elliptical"])
        )        
        time = st.text_input(
            "* How long can you work out?",
            value=st.session_state.user_inputs.get("time", "")
        )        
        rest_days = st.text_input(
            "* How many rest days would you like per week?",
            value=st.session_state.user_inputs.get("rest_days", ""))

        calories2 = st.text_input(
            "* How many calories would you like to burn",
            value=st.session_state.user_inputs.get("calories2", ""))
        

        days1 = ["Monday", "Tuesday", "Wednesday" ,"Thursday", "Friday", "Saturday", "Sunday"]
        day = st.multiselect(
            "* Choose all the days you can work out",
            days1,
            default=st.session_state.user_inputs.get("day", ["Monday", "Friday", "Wednesday"])
        )
        if st.button("Save Fitness Goals", key="orange"):
            st.session_state.user_inputs.update({
                "fitness_goal": fitness_goal,
                "muscle": muscle,
                "cardio": cardio,
                "calories2": calories2,
                "time": time,
                "rest_days": rest_days,
                "day":day
            })


    elif choice == "Get Workout Schedule":
        required_keys = ["fitness_goal", "muscle", "cardio", "calories", "time", "rest_days", "age", "weight", "height", "calories2", "day"]
        if not all(key in st.session_state.user_inputs and st.session_state.user_inputs[key] for key in required_keys):
            st.warning(" Please complete both 'Basic Info' and 'Fitness Goals' before generating a plan.")
            return

        if st.button("Generate My Workout Plan", key="orange2"):
            with st.spinner("Generating your personalized workout plan..."):
                try:
                    plan = get_workout_plan(*[st.session_state.user_inputs[key] for key in required_keys])
                    st.markdown(plan)
                except Exception as e:
                    st.error("An error occurred while generating the plan. Please try again.")
                    st.exception(e)


if __name__=="__main__":
    main()

