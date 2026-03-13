# local module
from numpy import empty
from pandas import options
from pyarrow import null
from .options import curve_options, color_options, scale_options
from ..comboDashboard import combo_dashboard

import streamlit as st


def well_composite(well_data, depths):
    # Initialize session_state
    if "trajectory1" not in st.session_state:
        st.session_state.trajectory1 = {
            "data": [],
            "intervals": [],
            "scales": ["linear" for _ in range(3)],
            "labels": [],
            "positions": [],
            "colors": [],
        }
    if "trajectory2" not in st.session_state:
        st.session_state.trajectory2 = {
            "data": [],
            "intervals": [],
            "scales": [],
            "labels": [],
            "positions": [],
            "colors": [],
        }
    if "trajectory3" not in st.session_state:
        st.session_state.trajectory3 = {
            "data": [],
            "intervals": [],
            "scales": [],
            "labels": [],
            "positions": [],
            "colors": [],
        }
    if "trajectories_ready" not in st.session_state:
        st.session_state.trajectories_ready = False

    tracks = ["Track 1", "Track 2", "Track 3"]

    # initialize trajectories
    trajectories = [
        st.session_state.trajectory1,
        st.session_state.trajectory2,
        st.session_state.trajectory3,
    ]

    if "placeholder" not in st.session_state:
        st.session_state.placeholder = [0, 0]

    def store_values(idx, key, temporary_key):
        trajectories[idx][key] = st.session_state[temporary_key]

    def store_list(idx, temporary_key):
        st.session_state.placeholder[idx] = st.session_state[temporary_key]
        trajectories[idx]["scales"].append(st.session_state[temporary_key])

    with st.sidebar:
        for i in range(len(trajectories)):
            st.subheader(tracks[i])

            st.write(f"traject: {trajectories[i]['data']}")

            temporary_keys = [
                f"_curves_{i}",
                f"_labels_{i}",
                f"_positions_{i}",
                f"_colors_{i}",
            ]

            st.multiselect(
                label="curve",
                options=curve_options,
                default=trajectories[i]["data"],
                key=temporary_keys[0],
                on_change=store_values,
                args=(i, "data", temporary_keys[0]),
            )

            selected_curve = trajectories[i]["data"]

            st.write(f"updated traject: {selected_curve}")

            for j, selected_curve in enumerate(trajectories[i]["data"]):
                # initialize unique keys:
                min_key = f"min_key_{i}_{j}_{selected_curve}"
                max_key = f"max_key_{i}_{j}_{selected_curve}"
                scale_key = f"scale_key_{i}_{j}_{selected_curve}"

                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    st.number_input(
                        label=f"Min {selected_curve}",
                        # value=trajectories[i]["intervals"][j][0],
                        key=min_key,
                        on_change=store_list,
                        args=(0, min_key),
                    )
                min_interval = st.session_state.placeholder[0]
                with col2:
                    st.number_input(
                        label=f"Max {selected_curve}",
                        # value=trajectories[i]["intervals"][j][1],
                        key=max_key,
                        on_change=store_list,
                        args=(1, max_key),
                    )
                max_interval = st.session_state.placeholder[1]
                trajectories[i]["intervals"].append([min_interval, max_interval])

                with col3:
                    st.selectbox(
                        label="scales",
                        options=scale_options,
                        # index=scale_options.index(trajectories[i]["scales"][j]),
                        key=scale_key,
                        on_change=store_list,
                        args=(i, scale_key),
                    )

            st.multiselect(
                label="label",
                options=curve_options,
                default=trajectories[i]["labels"],
                key=temporary_keys[1],
                on_change=store_values,
                args=(i, "labels", temporary_keys[1]),
            )

            selected_positions = st.multiselect(
                label="Pos",
                options=[0, 40, 80],
                # default=trajectories[i]["positions"],
                key=f"positions_{i}_widgets",
            )
            trajectories[i]["positions"] = selected_positions

            selected_colors = st.multiselect(
                label="color",
                options=color_options,
                # default=trajectories[i]["colors"],
                key=f"colors_{i}_widgets",
            )
            trajectories[i]["colors"] = selected_colors

        # Add apply settings button
        if st.button("Apply Settings"):
            st.session_state.trajectories_ready = True

    tab1, tab2 = st.tabs(["Well Composites", "Custom Plot"])
    with tab1:
        if st.session_state.trajectories_ready:
            combo_dashboard(
                well_data,
                depths,
                st.session_state.trajectory1,
                st.session_state.trajectory2,
                st.session_state.trajectory3,
            )
        else:
            st.info("Configure Your Track First")
    with tab2:
        st.write("hehe")
