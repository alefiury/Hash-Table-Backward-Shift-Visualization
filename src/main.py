import copy
import asyncio

import streamlit as st

from languages_content import LANGUAGES
from utils import (
    get_text,
    find_index,
    step_through,
    display_current_step,
    auto_step
)


def main():
    st.set_page_config(layout="wide")

    if "language" not in st.session_state:
        st.session_state.language = "English"

    st.sidebar.selectbox("Select Language", options=list(LANGUAGES.keys()), key="language")

    st.title(get_text("title"))

    if "ht" not in st.session_state:
        st.session_state.ht = []
        st.session_state.size = 10
        st.session_state.steps = []
        st.session_state.current_step = 0
        st.session_state.paused = True

    col1, col2 = st.columns([1, 2])

    with col1:
        size_input = st.number_input(
            get_text("size_input"),
            min_value=1,
            max_value=20,
            value=st.session_state.size
        )

        if st.button(get_text("initialize_button")):
            st.session_state.ht = [219, 821, 981, 388, 594, 192, 636, 144, 170, 399]
            st.session_state.size = size_input
            st.session_state.steps = []
            st.session_state.current_step = 0
            st.session_state.paused = True
            st.experimental_rerun()

        elements = st.text_input(
            get_text("elements_input"),
            value=",".join(str(x) if x is not None else 'None' for x in st.session_state.ht)
        )
        try:
            st.session_state.ht = [None if x.strip() == 'None' else int(x.strip()) for x in elements.split(',')]
        except ValueError:
            st.error("Invalid input. Please enter integers or 'None'.")

        element_to_remove = st.number_input(get_text('remove_input'), value=821)

        if st.button(get_text("start_removal")):
            index_to_remove = find_index(st.session_state.ht, element_to_remove, st.session_state.size)
            if index_to_remove is None:
                st.error(get_text("element_not_found"))
            else:
                st.session_state.steps = step_through(copy.deepcopy(st.session_state.ht), st.session_state.size, index_to_remove)
                st.session_state.current_step = 0
                st.session_state.paused = True
                st.experimental_rerun()

    with col2:
        st.subheader(get_text("visualization_title"))

        if st.session_state.steps:
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                if st.button(get_text("previous_step")) and st.session_state.current_step > 0:
                    st.session_state.current_step -= 1
                    st.session_state.paused = True
            with col2:
                if st.button(get_text("next_step")) and st.session_state.current_step < len(st.session_state.steps) - 1:
                    st.session_state.current_step += 1
                    st.session_state.paused = True
            with col3:
                if st.button(get_text("reset_to_start")):
                    st.session_state.current_step = 0
                    st.session_state.paused = True
            with col4:
                if st.button(get_text("jump_to_end")):
                    st.session_state.current_step = len(st.session_state.steps) - 1
                    st.session_state.paused = True
            with col5:
                if st.session_state.paused:
                    if st.button(get_text("auto_play")):
                        st.session_state.paused = False
                else:
                    if st.button(get_text("pause")):
                        st.session_state.paused = True

            delay = st.slider(get_text("delay_slider"), 0.1, 5.0, 1.0, 0.1)

            if not st.session_state.paused:
                asyncio.run(auto_step(st.session_state.steps, delay))

        display_current_step()

        if st.session_state.steps and st.button(get_text("apply_changes")):
            st.session_state.ht = st.session_state.steps[-1]["ht"]
            st.session_state.steps = []
            st.session_state.current_step = 0
            st.success(get_text("changes_applied"))
            st.experimental_rerun()


if __name__ == "__main__":
    main()