from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
import os


# Load environment variables
load_dotenv() 
client = OpenAI()

st.markdown(
    "<h2 style='text-align: center; color: #FF69B4;'>🍨 Frozen Delights </h2>",
    unsafe_allow_html=True
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
        You are OrderBot, an automated service to collect orders for an ice-cream parlour.
        Greet the customer, collect their order, confirm dine-in or delivery, summarize, 
        ask if they want to add anything else, then collect address (if delivery), and payment.
        The menu includes: 
        Ice Cream Flavours (per scoop): 
            vanilla 3.50, 
            chocolate 3.50, 
            strawberry 3.50, 
            butterscotch 4.00, 
            mint chocolate chip 4.00, 
            cookies & cream 4.50 
        Serving Styles: 
            cup free, 
            cone 1.00, 
            waffle cone 2.00 
        Toppings: 
            sprinkles 0.75, 
            chocolate chips 1.00, 
            hot fudge 1.50, 
            caramel 1.50, 
            nuts 1.00, 
            whipped cream 1.00, 
            cherry 0.50 
        Milkshakes: 
            vanilla 5.50, 
            chocolate 5.50, 
            strawberry 5.50, 
            oreo 6.00 
        Drinks: 
            coke 2.00, 
            sprite 2.00, 
            bottled water 2.50
        """}
    ]
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])
if user_input := st.chat_input("What would you like to order?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Send conversation to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    bot_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)
