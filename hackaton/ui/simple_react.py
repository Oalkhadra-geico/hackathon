import reactpy
from reactpy import html, hooks

# List of US state abbreviations (including DC)
STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", 
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", 
    "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", 
    "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", 
    "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

# List of LOB (Line of Business) options
LOB_OPTIONS = [
    "AIP", "Auto", "Boat", "Commercial", "Cycle", "PURE", "RV", "Umbrella"
]

@reactpy.component
def UserInputApp():
    # State for user input
    user_input, set_user_input = hooks.use_state("")
    # State for selected states
    selected_states, set_selected_states = hooks.use_state(set())
    # State for dropdown visibility
    show_dropdown, set_show_dropdown = hooks.use_state(False)
    # State for selected LOBs
    selected_lobs, set_selected_lobs = hooks.use_state(set())
    # State for LOB dropdown visibility
    show_lob_dropdown, set_show_lob_dropdown = hooks.use_state(False)

    def handle_input_change(event):
        set_user_input(event["target"]["value"])

    def handle_state_toggle(state):
        def toggle(event):
            if state in selected_states:
                set_selected_states(selected_states - {state})
            else:
                set_selected_states(selected_states | {state})
        return toggle

    def handle_dropdown_toggle(event):
        set_show_dropdown(not show_dropdown)

    def handle_lob_toggle(lob):
        def toggle(event):
            if lob in selected_lobs:
                set_selected_lobs(selected_lobs - {lob})
            else:
                set_selected_lobs(selected_lobs | {lob})
        return toggle

    def handle_lob_dropdown_toggle(event):
        set_show_lob_dropdown(not show_lob_dropdown)

    return html.div(
        {"style": {"maxWidth": "600px", "margin": "0 auto", "padding": "20px"}},
        html.h1("DORA"),
        # State Filter Dropdown
        html.div(
            {"style": {"marginBottom": "20px"}},
            html.button(
                {
                    "onClick": handle_dropdown_toggle,
                    "style": {
                        "padding": "10px",
                        "backgroundColor": "#f0f0f0",
                        "border": "1px solid #ccc",
                        "cursor": "pointer",
                    },
                },
                "Filter by State",
            ),
            # Dropdown List
            html.div(
                {
                    "style": {
                        "display": "block" if show_dropdown else "none",
                        "border": "1px solid #ccc",
                        "backgroundColor": "#fff",
                        "padding": "10px",
                        "marginTop": "10px",
                        "maxHeight": "200px",
                        "overflowY": "auto",
                    },
                },
                [
                    html.div(
                        {"style": {"marginBottom": "5px"}},
                        html.label(
                            {"style": {"display": "flex", "alignItems": "center"}},
                            html.input(
                                {
                                    "type": "checkbox",
                                    "checked": state in selected_states,
                                    "onChange": handle_state_toggle(state),
                                    "style": {"marginRight": "10px"},
                                }
                            ),
                            state,
                        ),
                    )
                    for state in STATES
                ],
            ),
        ),
        # LOB Filter Dropdown
        html.div(
            {"style": {"marginBottom": "20px"}},
            html.button(
                {
                    "onClick": handle_lob_dropdown_toggle,
                    "style": {
                        "padding": "10px",
                        "backgroundColor": "#f0f0f0",
                        "border": "1px solid #ccc",
                        "cursor": "pointer",
                    },
                },
                "Filter by LOB",
            ),
            # LOB Dropdown List
            html.div(
                {
                    "style": {
                        "display": "block" if show_lob_dropdown else "none",
                        "border": "1px solid #ccc",
                        "backgroundColor": "#fff",
                        "padding": "10px",
                        "marginTop": "10px",
                        "maxHeight": "200px",
                        "overflowY": "auto",
                    },
                },
                [
                    html.div(
                        {"style": {"marginBottom": "5px"}},
                        html.label(
                            {"style": {"display": "flex", "alignItems": "center"}},
                            html.input(
                                {
                                    "type": "checkbox",
                                    "checked": lob in selected_lobs,
                                    "onChange": handle_lob_toggle(lob),
                                    "style": {"marginRight": "10px"},
                                }
                            ),
                            lob,
                        ),
                    )
                    for lob in LOB_OPTIONS
                ],
            ),
        ),
        # Text Input Box
        html.textarea(
            {
                "value": user_input,
                "onChange": handle_input_change,
                "placeholder": "Type your message here...",
                "style": {
                    "width": "100%",
                    "height": "150px",
                    "padding": "10px",
                    "fontSize": "16px",
                    "border": "1px solid #ccc",
                    "borderRadius": "5px",
                },
            }
        ),
        # Display Selected States, LOBs, and User Input
        html.div(
            {"style": {"marginTop": "20px"}},
            html.p(f"Selected States: {', '.join(selected_states) or 'None'}"),
            html.p(f"Selected LOBs: {', '.join(selected_lobs) or 'None'}"),
            html.p(f"First word you typed: {user_input.split()[0] if user_input else None}"),
        ),
    )

reactpy.run(UserInputApp)