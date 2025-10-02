
import streamlit as st
from openai import OpenAI
import time
import os

# Load environment variables
load_dotenv() 
# client = OpenAI()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- SESSION STATE FLAGS ---
if "first_order" not in st.session_state:
    st.session_state.first_order = True
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
        You are OrderBot, an automated service to collect orders for an ice-cream parlour.
        Greet the customer, collect their order, confirm dine-in or delivery, summarize, 
        ask if they want to add anything else, then collect address (if delivery), and payment.
        The menu includes: 
        Ice Cream Flavours (per scoop): 
    vanilla ₹250, 
    chocolate ₹250, 
    strawberry ₹250, 
    butterscotch ₹300, 
    mint chocolate chip ₹300, 
    cookies & cream ₹350 
Serving Styles: 
    cup free, 
    cone ₹50, 
    waffle cone ₹100 
Toppings: 
    sprinkles ₹20, 
    chocolate chips ₹50, 
    hot fudge ₹75, 
    caramel ₹75, 
    nuts ₹50, 
    whipped cream ₹50, 
    cherry ₹25 
Milkshakes: 
    vanilla ₹400, 
    chocolate ₹400, 
    strawberry ₹400, 
    oreo ₹450 
Drinks: 
    coke ₹120, 
    sprite ₹120, 
    bottled water ₹150

        """}
    ]

# --- TITLE ---
st.markdown(
    "<h2 style='text-align: center; color: #FF69B4;'>🍨 Frozen Delights </h2>",
    unsafe_allow_html=True
)

# --- ICE CREAM ANIMATION ---
with st.container():
    ice_cream_stages = [
        "🍦",
        "🍦✨",
        "🍦✨🍫",
        "🍦✨🍫🍓",
        "🍦✨🍫🍓🥜",
        "🍦✨🍫🍓🥜🍒",
        "🍦 🍯🧈",
        "🍦 🍪🍦",
        "📋 What would you like to order 😋"
    ]
    placeholder = st.empty()

    # Show animation only on first visit
    if st.session_state.first_order:
        for stage in ice_cream_stages:
            placeholder.markdown(
                f"<h1 style='text-align:center; font-size:35px;'>{stage}</h1>",
                unsafe_allow_html=True
            )
            time.sleep(0.5)

# --- DISPLAY PREVIOUS CHAT MESSAGES ---
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

# --- CHAT INPUT ---
if user_input := st.chat_input("What would you like to order?"):
    # After first input, animation will not show again
    st.session_state.first_order = False

    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Show tasty emoji confirmation
    st.success(f"📝 Noted your order 😊 : **{user_input}**")

    # Send conversation to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    # Bot reply
    bot_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)

