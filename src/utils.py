import copy
from typing import List, Dict, Any

import streamlit as st
import matplotlib.pyplot as plt

from languages_content import LANGUAGES


def get_text(key: str) -> str:
    return LANGUAGES[st.session_state.language][key]


def hash_function(value: int , size: int) -> int:
    return value % size


def find_index(ht: List[int], element: int, D: int) -> int:
    start_index = hash_function(element, D)
    index = start_index
    while ht[index] != element:
        if ht[index] is None:
            return None
        index = (index + 1) % D
        if index == start_index:
            return None
    return index


def plot_hash_table(
    ht: List[int],
    highlight: int = None,
    moving_idx: int = None,
    title: str = "Hash Table",
    i: int = None,
    j: int = None,
    r: int = None
) -> plt.Figure:
    """Plot the hash table as a horizontal bar chart.

    Args:

    ht (List[int]): The hash table to plot.
    highlight (int): Index to highlight.
    moving_idx (int): Index of the element being moved.
    title (str): Title of the plot.
    i (int): Current index i.
    j (int): Current index j.
    r (int): Hash value r.

    Returns:

    fig: The matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.set_xlim(-0.5, len(ht) - 0.5)
    ax.set_ylim(-0.5, 1.5)
    ax.axis("off")
    ax.get_yaxis().set_visible(False)

    for idx, v in enumerate(ht):
        color = "lightblue" if idx == highlight else "lightgray"
        if idx == moving_idx:
            color = "lightcoral"
        rect = plt.Rectangle((idx-0.4, 0), 0.8, 1, color=color, ec="black")
        ax.add_patch(rect)
        if v is not None:
            ax.text(idx, 0.5, str(v), color="black", ha="center", va="center", fontweight="bold")
        ax.text(idx, -0.2, str(idx), color="black", ha="center", va="center", fontsize=8)

    info_text = f"i = {i if i is not None else 'N/A'}, j = {j if j is not None else 'N/A'}, r = {r if r is not None else 'N/A'}"
    ax.text(
        0.5,
        1.3,
        info_text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=10,
        bbox=dict(
            facecolor="white",
            edgecolor="black",
            boxstyle="round,pad=0.5"
        )
    )

    ax.set_title(title)
    return fig


def step_through(ht: List[int], D: int, i: int) -> List[Dict[str, Any]]:
    """
    Step through the process of removing an element from the hash table.

    Args:

    ht (List[int]): The hash table.
    D (int): The size of the hash table.
    i (int): The index of the element to remove.

    Returns:

    steps (List[Dict[str, Any]]): A list of steps in the process.
    """
    steps = []
    j = i
    removed_value = ht[j]
    ht[j] = None
    steps.append({
        "ht": copy.deepcopy(ht),
        "highlight": i,
        "moving_idx": None,
        "title": get_text("removing").format(removed_value, i),
        "description": get_text("empty_slot").format(j, j),
        'i': i,
        'j': j,
        'r': None
    })
    j = (j + 1) % D

    while ht[j] is not None and j != i:
        r = hash_function(ht[j], D)
        steps.append({
            "ht": copy.deepcopy(ht),
            "highlight": None,
            "moving_idx": j,
            "title": get_text("checking_move").format(j),
            "description": get_text("while_loop").format(j, j, i, j),
            'i': i,
            'j': j,
            'r': r
        })
        condition = not (((i < r <= j) or (j < i < r) or (r <= j < i)))
        if condition:
            steps.append({
                "ht": copy.deepcopy(ht),
                "highlight": None,
                "moving_idx": j,
                "title": get_text("no_move_needed").format(j),
                "description": get_text("no_move_needed").format(j),
                'i': i,
                'j': j,
                'r': r
            })
            break
        j = (j + 1) % D

    if j != i and ht[j] is not None:
        ht[i] = ht[j]
        ht[j] = None
        steps.append({
            "ht": copy.deepcopy(ht),
            "highlight": i,
            "moving_idx": j,
            "title": get_text("moving_element").format(j, i),
            "description": get_text("moved_element").format(ht[i], j, i),
            'i': i,
            'j': j,
            'r': r
        })
        steps.extend(step_through(ht, D, j))

    return steps


def display_current_step() -> None:
    """
    Display the current step in the process.
    """
    if st.session_state.steps:
        current_step = st.session_state.steps[st.session_state.current_step]
        fig = plot_hash_table(
            current_step["ht"],
            highlight=current_step["highlight"],
            moving_idx=current_step["moving_idx"],
            title=current_step["title"],
            i=current_step['i'],
            j=current_step['j'],
            r=current_step['r']
        )
        st.pyplot(fig)
        st.write(current_step["description"])
        if len(st.session_state.steps) > 1:
            st.progress(st.session_state.current_step / (len(st.session_state.steps) - 1))
    else:
        fig = plot_hash_table(st.session_state.ht)
        st.pyplot(fig)
