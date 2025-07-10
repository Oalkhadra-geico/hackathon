import pandas as pd
import reactpy
from reactpy import html, hooks

# Load the Excel file instead of CSV
df = pd.read_excel('../ResponseData.xlsx')

print(df.head())
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
    # State for filtered data
    filtered_data, set_filtered_data = hooks.use_state(df)

    def apply_filters():
        """Apply the selected filters to the dataframe"""
        filtered_df = df.copy()
        
        # Filter by states if any are selected
        if selected_states:
            filtered_df = filtered_df[filtered_df['State'].isin(selected_states)]
        
        # Filter by LOBs if any are selected
        if selected_lobs:
            filtered_df = filtered_df[filtered_df['LOB'].isin(selected_lobs)]
        
        set_filtered_data(filtered_df)

    def handle_input_change(event):
        set_user_input(event["target"]["value"])

    def handle_state_toggle(state):
        def toggle(event):
            if state in selected_states:
                new_states = selected_states - {state}
                set_selected_states(new_states)
            else:
                new_states = selected_states | {state}
                set_selected_states(new_states)
            # Apply filters whenever states change
            apply_filters()
        return toggle

    def handle_dropdown_toggle(event):
        set_show_dropdown(not show_dropdown)

    def handle_lob_toggle(lob):
        def toggle(event):
            if lob in selected_lobs:
                new_lobs = selected_lobs - {lob}
                set_selected_lobs(new_lobs)
            else:
                new_lobs = selected_lobs | {lob}
                set_selected_lobs(new_lobs)
            # Apply filters whenever LOBs change
            apply_filters()
        return toggle

    def handle_lob_dropdown_toggle(event):
        set_show_lob_dropdown(not show_lob_dropdown)

    # Apply filters on component mount and whenever filters change
    hooks.use_effect(apply_filters, [selected_states, selected_lobs])

    return html.div(
        {"style": {"maxWidth": "1200px", "margin": "0 auto", "padding": "20px"}},
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
                f"Filter by State ({len(selected_states)} selected)",
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
                f"Filter by LOB ({len(selected_lobs)} selected)",
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
            {"style": {"marginTop": "20px", "marginBottom": "20px"}},
            html.p(f"Selected States: {', '.join(selected_states) or 'None'}"),
            html.p(f"Selected LOBs: {', '.join(selected_lobs) or 'None'}"),
            html.p(f"First word you typed: {user_input.split()[0] if user_input else None}"),
        ),
        # Display Filtered Data Summary
        html.div(
            {"style": {"marginTop": "20px", "marginBottom": "20px"}},
            html.h3("Filtered Data Summary"),
            html.p(f"Total records: {len(filtered_data)}"),
            html.p(f"Unique States in filtered data: {len(filtered_data['State'].unique()) if len(filtered_data) > 0 else 0}"),
            html.p(f"Unique LOBs in filtered data: {len(filtered_data['LOB'].unique()) if len(filtered_data) > 0 else 0}"),
        ),
        # Display Sample of Filtered Data
        html.div(
            {"style": {"marginTop": "20px"}},
            html.h3("Sample of Filtered Data"),
            html.div(
                {
                    "style": {
                        "border": "1px solid #ccc",
                        "padding": "10px",
                        "backgroundColor": "#f9f9f9",
                        "maxHeight": "400px",
                        "overflowY": "auto",
                    }
                },
                html.pre(
                    {
                        "style": {
                            "whiteSpace": "pre-wrap",
                            "fontSize": "12px",
                            "margin": "0",
                        }
                    },
                    str(filtered_data.head(10).to_string()) if len(filtered_data) > 0 else "No data matches the current filters."
                ),
            ),
        ),
    )

reactpy.run(UserInputApp)
