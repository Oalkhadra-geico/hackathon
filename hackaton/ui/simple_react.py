import pandas as pd
import reactpy
from reactpy import html, hooks

# Load the CSV file
df = pd.read_csv('../ResponseData.csv')

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
    "AIP", "Boat", "Commercial", "Cycle", "Home Owners", "Personal Auto", "RV", "Umbrella"
]

# List of Filing Type options
FILING_TYPE_OPTIONS = [
    "Form", "Rate", "Rate/Rule", "Rule", "Symbols", "Underwriting"
]

# List of Response Type options
RESPONSE_TYPE_OPTIONS = [
    "DOI Objection", "Annual Credit Questionnaire", "Market Conduct", "Standard Filing Inquiry"
]

# List of Topic options
TOPIC_OPTIONS = [
    "Actuarial Justification", "Additional Support/Exhibits", "Amendment", "Compliance", "Confirm Item",
    "Credit", "Discounts", "Fee", "Filing Requirements", "Histogram", "Incomplete/Missing Items", 
    "Models", "MTF", "Policy Holder Notification", "Rate Capping", "Rating Criteria/Factors", "Regulation/Statute",
     "Submission Errors", "Tariffs", "Territory", "Tiers", "Underwriting"
]

# List of Carrier options
CARRIER_OPTIONS = [
    "AmFam", "GEICO", "Kemper", "Other", "Progressive"
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
    # State for selected Filing Types
    selected_filing_types, set_selected_filing_types = hooks.use_state(set())
    # State for Filing Type dropdown visibility
    show_filing_type_dropdown, set_show_filing_type_dropdown = hooks.use_state(False)
    # State for selected Response Types
    selected_response_types, set_selected_response_types = hooks.use_state(set())
    # State for Response Type dropdown visibility
    show_response_type_dropdown, set_show_response_type_dropdown = hooks.use_state(False)
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
        
        # Filter by Filing Types if any are selected
        if selected_filing_types:
            filtered_df = filtered_df[filtered_df['Filing_Type'].isin(selected_filing_types)]
        
        # Filter by Response Types if any are selected
        if selected_response_types:
            filtered_df = filtered_df[filtered_df['RespType'].isin(selected_response_types)]
        
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

    def handle_filing_type_toggle(filing_type):
        def toggle(event):
            if filing_type in selected_filing_types:
                new_filing_types = selected_filing_types - {filing_type}
                set_selected_filing_types(new_filing_types)
            else:
                new_filing_types = selected_filing_types | {filing_type}
                set_selected_filing_types(new_filing_types)
            # Apply filters whenever Filing Types change
            apply_filters()
        return toggle

    def handle_filing_type_dropdown_toggle(event):
        set_show_filing_type_dropdown(not show_filing_type_dropdown)

    def handle_response_type_toggle(response_type):
        def toggle(event):
            if response_type in selected_response_types:
                new_response_types = selected_response_types - {response_type}
                set_selected_response_types(new_response_types)
            else:
                new_response_types = selected_response_types | {response_type}
                set_selected_response_types(new_response_types)
            # Apply filters whenever Response Types change
            apply_filters()
        return toggle

    def handle_response_type_dropdown_toggle(event):
        set_show_response_type_dropdown(not show_response_type_dropdown)

    # Apply filters on component mount and whenever filters change
    hooks.use_effect(apply_filters, [selected_states, selected_lobs, selected_filing_types, selected_response_types])

    return html.div(
        {
            "style": {
                "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                "backgroundColor": "#f8fafc",
                "minHeight": "100vh",
                "padding": "0",
                "margin": "0"
            }
        },
        # Header Section
        html.div(
            {
                "style": {
                    "background": "#2563eb",
                    "color": "white",
                    "padding": "1.5rem 0",
                    "marginBottom": "2rem",
                    "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)"
                }
            },
            html.div(
                {
                    "style": {
                        "maxWidth": "1200px",
                        "margin": "0 auto",
                        "padding": "0 20px",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between"
                    }
                },
                # Logo Section
                html.div(
                    {
                        "style": {
                            "display": "flex",
                            "alignItems": "center"
                        }
                    },
                    html.img(
                        {
                            "src": "https://blog.logomyway.com/wp-content/uploads/2022/11/geico-logo.jpg",
                            "alt": "GEICO Logo",
                            "style": {
                                "height": "40px",
                                "marginRight": "2rem"
                            }
                        }
                    )
                ),
                # Title Section
                html.div(
                    {
                        "style": {
                            "flex": "1",
                            "textAlign": "center"
                        }
                    },
                    html.h1(
                        {
                            "style": {
                                "fontSize": "2.5rem",
                                "fontWeight": "600",
                                "margin": "0",
                                "letterSpacing": "0.05em"
                            }
                        },
                        "DORA"
                    ),
                    html.p(
                        {
                            "style": {
                                "fontSize": "1rem",
                                "margin": "0.5rem 0 0 0",
                                "opacity": "0.9"
                            }
                        },
                        "DORA: DOI Objection Research Assistant"
                    )
                ),
                # Spacer for logo balance
                html.div(
                    {
                        "style": {
                            "width": "40px",
                            "marginLeft": "2rem"
                        }
                    }
                )
            )
        ),
        # Main Content Container
        html.div(
            {
                "style": {
                    "maxWidth": "1200px",
                    "margin": "0 auto",
                    "padding": "0 20px"
                }
            },
            # Filters Section
            html.div(
                {
                    "style": {
                        "background": "white",
                        "borderRadius": "12px",
                        "padding": "2rem",
                        "marginBottom": "2rem",
                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)",
                        "border": "1px solid #e2e8f0"
                    }
                },
                html.h2(
                    {
                        "style": {
                            "fontSize": "1.5rem",
                            "fontWeight": "600",
                            "color": "#2d3748",
                            "margin": "0 0 1.5rem 0",
                            "borderBottom": "2px solid #2563eb",
                            "paddingBottom": "0.5rem"
                        }
                    },
                    "Filters"
                ),
                # Filter Grid
                html.div(
                    {
                        "style": {
                            "display": "grid",
                            "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                            "gap": "1.5rem"
                        }
                    },
                    # State Filter
                    html.div(
                        {},
                        html.label(
                            {
                                "style": {
                                    "display": "block",
                                    "fontSize": "0.9rem",
                                    "fontWeight": "500",
                                    "color": "#4a5568",
                                    "marginBottom": "0.5rem"
                                }
                            },
                            "Filter by State"
                        ),
                        html.button(
                            {
                                "onClick": handle_dropdown_toggle,
                                "style": {
                                    "width": "100%",
                                    "padding": "12px 16px",
                                    "backgroundColor": "#2563eb",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "cursor": "pointer",
                                    "fontSize": "1rem",
                                    "fontWeight": "500",
                                    "transition": "all 0.2s ease",
                                    "boxShadow": "0 2px 4px rgba(37, 99, 235, 0.3)"
                                }
                            },
                            f"States ({len(selected_states)} selected) {'▼' if not show_dropdown else '▲'}",
                        ),
                        # State Dropdown
                        html.div(
                            {
                                "style": {
                                    "display": "block" if show_dropdown else "none",
                                    "border": "1px solid #e2e8f0",
                                    "backgroundColor": "#fff",
                                    "borderRadius": "8px",
                                    "padding": "1rem",
                                    "marginTop": "0.5rem",
                                    "maxHeight": "200px",
                                    "overflowY": "auto",
                                    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
                                }
                            },
                            [
                                html.div(
                                    {
                                        "style": {
                                            "marginBottom": "8px",
                                            "padding": "4px 8px",
                                            "borderRadius": "4px",
                                            "backgroundColor": "#2563eb" if state in selected_states else "transparent",
                                            "color": "white" if state in selected_states else "#2d3748",
                                            "transition": "all 0.2s ease"
                                        }
                                    },
                                    html.label(
                                        {
                                            "style": {
                                                "display": "flex",
                                                "alignItems": "center",
                                                "cursor": "pointer",
                                                "fontSize": "0.9rem"
                                            }
                                        },
                                        html.input(
                                            {
                                                "type": "checkbox",
                                                "checked": state in selected_states,
                                                "onChange": handle_state_toggle(state),
                                                "style": {
                                                    "marginRight": "8px",
                                                    "cursor": "pointer"
                                                }
                                            }
                                        ),
                                        state,
                                    ),
                                )
                                for state in STATES
                            ],
                        ),
                    ),
                    # LOB Filter
                    html.div(
                        {},
                        html.label(
                            {
                                "style": {
                                    "display": "block",
                                    "fontSize": "0.9rem",
                                    "fontWeight": "500",
                                    "color": "#4a5568",
                                    "marginBottom": "0.5rem"
                                }
                            },
                            "Filter by Line of Business"
                        ),
                        html.button(
                            {
                                "onClick": handle_lob_dropdown_toggle,
                                "style": {
                                    "width": "100%",
                                    "padding": "12px 16px",
                                    "backgroundColor": "#6b7280",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "cursor": "pointer",
                                    "fontSize": "1rem",
                                    "fontWeight": "500",
                                    "transition": "all 0.2s ease",
                                    "boxShadow": "0 2px 4px rgba(107, 114, 128, 0.3)"
                                }
                            },
                            f"LOB ({len(selected_lobs)} selected) {'▼' if not show_lob_dropdown else '▲'}",
                        ),
                        # LOB Dropdown
                        html.div(
                            {
                                "style": {
                                    "display": "block" if show_lob_dropdown else "none",
                                    "border": "1px solid #e2e8f0",
                                    "backgroundColor": "#fff",
                                    "borderRadius": "8px",
                                    "padding": "1rem",
                                    "marginTop": "0.5rem",
                                    "maxHeight": "200px",
                                    "overflowY": "auto",
                                    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
                                }
                            },
                            [
                                html.div(
                                    {
                                        "style": {
                                            "marginBottom": "8px",
                                            "padding": "4px 8px",
                                            "borderRadius": "4px",
                                            "backgroundColor": "#6b7280" if lob in selected_lobs else "transparent",
                                            "color": "white" if lob in selected_lobs else "#2d3748",
                                            "transition": "all 0.2s ease"
                                        }
                                    },
                                    html.label(
                                        {
                                            "style": {
                                                "display": "flex",
                                                "alignItems": "center",
                                                "cursor": "pointer",
                                                "fontSize": "0.9rem"
                                            }
                                        },
                                        html.input(
                                            {
                                                "type": "checkbox",
                                                "checked": lob in selected_lobs,
                                                "onChange": handle_lob_toggle(lob),
                                                "style": {
                                                    "marginRight": "8px",
                                                    "cursor": "pointer"
                                                }
                                            }
                                        ),
                                        lob,
                                    ),
                                )
                                for lob in LOB_OPTIONS
                            ],
                        ),
                    ),
                    # Filing Type Filter
                    html.div(
                        {},
                        html.label(
                            {
                                "style": {
                                    "display": "block",
                                    "fontSize": "0.9rem",
                                    "fontWeight": "500",
                                    "color": "#4a5568",
                                    "marginBottom": "0.5rem"
                                }
                            },
                            "Filter by Filing Type"
                        ),
                        html.button(
                            {
                                "onClick": handle_filing_type_dropdown_toggle,
                                "style": {
                                    "width": "100%",
                                    "padding": "12px 16px",
                                    "backgroundColor": "#374151",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "cursor": "pointer",
                                    "fontSize": "1rem",
                                    "fontWeight": "500",
                                    "transition": "all 0.2s ease",
                                    "boxShadow": "0 2px 4px rgba(55, 65, 81, 0.3)"
                                }
                            },
                            f"Filing Type ({len(selected_filing_types)} selected) {'▼' if not show_filing_type_dropdown else '▲'}",
                        ),
                        # Filing Type Dropdown
                        html.div(
                            {
                                "style": {
                                    "display": "block" if show_filing_type_dropdown else "none",
                                    "border": "1px solid #e2e8f0",
                                    "backgroundColor": "#fff",
                                    "borderRadius": "8px",
                                    "padding": "1rem",
                                    "marginTop": "0.5rem",
                                    "maxHeight": "200px",
                                    "overflowY": "auto",
                                    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
                                }
                            },
                            [
                                html.div(
                                    {
                                        "style": {
                                            "marginBottom": "8px",
                                            "padding": "4px 8px",
                                            "borderRadius": "4px",
                                            "backgroundColor": "#374151" if filing_type in selected_filing_types else "transparent",
                                            "color": "white" if filing_type in selected_filing_types else "#2d3748",
                                            "transition": "all 0.2s ease"
                                        }
                                    },
                                    html.label(
                                        {
                                            "style": {
                                                "display": "flex",
                                                "alignItems": "center",
                                                "cursor": "pointer",
                                                "fontSize": "0.9rem"
                                            }
                                        },
                                        html.input(
                                            {
                                                "type": "checkbox",
                                                "checked": filing_type in selected_filing_types,
                                                "onChange": handle_filing_type_toggle(filing_type),
                                                "style": {
                                                    "marginRight": "8px",
                                                    "cursor": "pointer"
                                                }
                                            }
                                        ),
                                        filing_type,
                                    ),
                                )
                                for filing_type in FILING_TYPE_OPTIONS
                            ],
                        ),
                    ),
                    # Response Type Filter
                    html.div(
                        {},
                        html.label(
                            {
                                "style": {
                                    "display": "block",
                                    "fontSize": "0.9rem",
                                    "fontWeight": "500",
                                    "color": "#4a5568",
                                    "marginBottom": "0.5rem"
                                }
                            },
                            "Filter by Response Type"
                        ),
                        html.button(
                            {
                                "onClick": handle_response_type_dropdown_toggle,
                                "style": {
                                    "width": "100%",
                                    "padding": "12px 16px",
                                    "backgroundColor": "#4b5563",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "cursor": "pointer",
                                    "fontSize": "1rem",
                                    "fontWeight": "500",
                                    "transition": "all 0.2s ease",
                                    "boxShadow": "0 2px 4px rgba(75, 85, 99, 0.3)"
                                }
                            },
                            f"Response Type ({len(selected_response_types)} selected) {'▼' if not show_response_type_dropdown else '▲'}",
                        ),
                        # Response Type Dropdown
                        html.div(
                            {
                                "style": {
                                    "display": "block" if show_response_type_dropdown else "none",
                                    "border": "1px solid #e2e8f0",
                                    "backgroundColor": "#fff",
                                    "borderRadius": "8px",
                                    "padding": "1rem",
                                    "marginTop": "0.5rem",
                                    "maxHeight": "200px",
                                    "overflowY": "auto",
                                    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
                                }
                            },
                            [
                                html.div(
                                    {
                                        "style": {
                                            "marginBottom": "8px",
                                            "padding": "4px 8px",
                                            "borderRadius": "4px",
                                            "backgroundColor": "#4b5563" if response_type in selected_response_types else "transparent",
                                            "color": "white" if response_type in selected_response_types else "#2d3748",
                                            "transition": "all 0.2s ease"
                                        }
                                    },
                                    html.label(
                                        {
                                            "style": {
                                                "display": "flex",
                                                "alignItems": "center",
                                                "cursor": "pointer",
                                                "fontSize": "0.9rem"
                                            }
                                        },
                                        html.input(
                                            {
                                                "type": "checkbox",
                                                "checked": response_type in selected_response_types,
                                                "onChange": handle_response_type_toggle(response_type),
                                                "style": {
                                                    "marginRight": "8px",
                                                    "cursor": "pointer"
                                                }
                                            }
                                        ),
                                        response_type,
                                    ),
                                )
                                for response_type in RESPONSE_TYPE_OPTIONS
                            ],
                        ),
                    ),
                ),
            ),
            # Input Section
            html.div(
                {
                    "style": {
                        "background": "white",
                        "borderRadius": "12px",
                        "padding": "2rem",
                        "marginBottom": "2rem",
                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)",
                        "border": "1px solid #e2e8f0"
                    }
                },
                html.h2(
                    {
                        "style": {
                            "fontSize": "1.5rem",
                            "fontWeight": "600",
                            "color": "#2d3748",
                            "margin": "0 0 1.5rem 0",
                            "borderBottom": "2px solid #2563eb",
                            "paddingBottom": "0.5rem"
                        }
                    },
                    "Query Input"
                ),
                html.textarea(
                    {
                        "value": user_input,
                        "onChange": handle_input_change,
                        "placeholder": "Enter your query or analysis request here...",
                        "style": {
                            "width": "100%",
                            "height": "120px",
                            "padding": "16px",
                            "fontSize": "1rem",
                            "border": "2px solid #e2e8f0",
                            "borderRadius": "8px",
                            "resize": "vertical",
                            "fontFamily": "inherit",
                            "transition": "border-color 0.2s ease",
                            "boxSizing": "border-box"
                        }
                    }
                ),
            ),
            # Status Section
            html.div(
                {
                    "style": {
                        "background": "white",
                        "borderRadius": "12px",
                        "padding": "2rem",
                        "marginBottom": "2rem",
                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)",
                        "border": "1px solid #e2e8f0"
                    }
                },
                html.h2(
                    {
                        "style": {
                            "fontSize": "1.5rem",
                            "fontWeight": "600",
                            "color": "#2d3748",
                            "margin": "0 0 1.5rem 0",
                            "borderBottom": "2px solid #2563eb",
                            "paddingBottom": "0.5rem"
                        }
                    },
                    "Current Selection"
                ),
                html.div(
                    {
                        "style": {
                            "display": "grid",
                            "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                            "gap": "1rem"
                        }
                    },
                    # Selected States Card
                    html.div(
                        {
                            "style": {
                                "background": "#2563eb",
                                "color": "white",
                                "padding": "1.5rem",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 4px rgba(37, 99, 235, 0.3)"
                            }
                        },
                        html.h3(
                            {
                                "style": {
                                    "margin": "0 0 0.5rem 0",
                                    "fontSize": "1.1rem",
                                    "fontWeight": "600"
                                }
                            },
                            "Selected States"
                        ),
                        html.p(
                            {
                                "style": {
                                    "margin": "0",
                                    "fontSize": "0.9rem",
                                    "opacity": "0.9"
                                }
                            },
                            ', '.join(sorted(selected_states)) if selected_states else 'No states selected'
                        ),
                    ),
                    # Selected LOBs Card
                    html.div(
                        {
                            "style": {
                                "background": "#6b7280",
                                "color": "white",
                                "padding": "1.5rem",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 4px rgba(107, 114, 128, 0.3)"
                            }
                        },
                        html.h3(
                            {
                                "style": {
                                    "margin": "0 0 0.5rem 0",
                                    "fontSize": "1.1rem",
                                    "fontWeight": "600"
                                }
                            },
                            "Selected LOBs"
                        ),
                        html.p(
                            {
                                "style": {
                                    "margin": "0",
                                    "fontSize": "0.9rem",
                                    "opacity": "0.9"
                                }
                            },
                            ', '.join(sorted(selected_lobs)) if selected_lobs else 'No LOBs selected'
                        ),
                    ),
                    # Selected Filing Types Card
                    html.div(
                        {
                            "style": {
                                "background": "#374151",
                                "color": "white",
                                "padding": "1.5rem",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 4px rgba(55, 65, 81, 0.3)"
                            }
                        },
                        html.h3(
                            {
                                "style": {
                                    "margin": "0 0 0.5rem 0",
                                    "fontSize": "1.1rem",
                                    "fontWeight": "600"
                                }
                            },
                            "Selected Filing Types"
                        ),
                        html.p(
                            {
                                "style": {
                                    "margin": "0",
                                    "fontSize": "0.9rem",
                                    "opacity": "0.9"
                                }
                            },
                            ', '.join(sorted(selected_filing_types)) if selected_filing_types else 'No filing types selected'
                        ),
                    ),
                    # Selected Response Types Card
                    html.div(
                        {
                            "style": {
                                "background": "#4b5563",
                                "color": "white",
                                "padding": "1.5rem",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 4px rgba(75, 85, 99, 0.3)"
                            }
                        },
                        html.h3(
                            {
                                "style": {
                                    "margin": "0 0 0.5rem 0",
                                    "fontSize": "1.1rem",
                                    "fontWeight": "600"
                                }
                            },
                            "Selected Response Types"
                        ),
                        html.p(
                            {
                                "style": {
                                    "margin": "0",
                                    "fontSize": "0.9rem",
                                    "opacity": "0.9"
                                }
                            },
                            ', '.join(sorted(selected_response_types)) if selected_response_types else 'No response types selected'
                        ),
                    ),
                    # Query Status Card
                    html.div(
                        {
                            "style": {
                                "background": "#111827",
                                "color": "white",
                                "padding": "1.5rem",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 4px rgba(17, 24, 39, 0.3)"
                            }
                        },
                        html.h3(
                            {
                                "style": {
                                    "margin": "0 0 0.5rem 0",
                                    "fontSize": "1.1rem",
                                    "fontWeight": "600"
                                }
                            },
                            "Query Status"
                        ),
                        html.p(
                            {
                                "style": {
                                    "margin": "0",
                                    "fontSize": "0.9rem",
                                    "opacity": "0.9"
                                }
                            },
                            f"First word: {user_input.split()[0]}" if user_input else "No query entered"
                        ),
                    ),
                ),
            ),
            # Data Summary Section
            html.div(
                {
                    "style": {
                        "background": "white",
                        "borderRadius": "12px",
                        "padding": "2rem",
                        "marginBottom": "2rem",
                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)",
                        "border": "1px solid #e2e8f0"
                    }
                },
                html.h2(
                    {
                        "style": {
                            "fontSize": "1.5rem",
                            "fontWeight": "600",
                            "color": "#2d3748",
                            "margin": "0 0 1.5rem 0",
                            "borderBottom": "2px solid #2563eb",
                            "paddingBottom": "0.5rem"
                        }
                    },
                    "Data Analytics"
                ),
                html.div(
                    {
                        "style": {
                            "display": "grid",
                            "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
                            "gap": "1rem",
                            "marginBottom": "2rem"
                        }
                    },
                    # Total Records
                    html.div(
                        {
                            "style": {
                                "background": "#2563eb",
                                "color": "white",
                                "padding": "1.5rem",
                                "borderRadius": "8px",
                                "textAlign": "center",
                                "boxShadow": "0 2px 4px rgba(37, 99, 235, 0.3)"
                            }
                        },
                        html.h3(
                            {
                                "style": {
                                    "margin": "0 0 0.5rem 0",
                                    "fontSize": "2rem",
                                    "fontWeight": "700"
                                }
                            },
                            str(len(filtered_data))
                        ),
                        html.p(
                            {
                                "style": {
                                    "margin": "0",
                                    "fontSize": "0.9rem",
                                    "opacity": "0.9"
                                }
                            },
                            "Total Records"
                        ),
                    ),
                    # Unique States
                    html.div(
                        {
                            "style": {
                                "background": "#6b7280",
                                "color": "white",
                                "padding": "1.5rem",
                                "borderRadius": "8px",
                                "textAlign": "center",
                                "boxShadow": "0 2px 4px rgba(107, 114, 128, 0.3)"
                            }
                        },
                        html.h3(
                            {
                                "style": {
                                    "margin": "0 0 0.5rem 0",
                                    "fontSize": "2rem",
                                    "fontWeight": "700"
                                }
                            },
                            str(len(filtered_data['State'].unique()) if len(filtered_data) > 0 else 0)
                        ),
                        html.p(
                            {
                                "style": {
                                    "margin": "0",
                                    "fontSize": "0.9rem",
                                    "opacity": "0.9"
                                }
                            },
                            "Unique States"
                        ),
                    ),
                    # Unique LOBs
                    html.div(
                        {
                            "style": {
                                "background": "#374151",
                                "color": "white",
                                "padding": "1.5rem",
                                "borderRadius": "8px",
                                "textAlign": "center",
                                "boxShadow": "0 2px 4px rgba(55, 65, 81, 0.3)"
                            }
                        },
                        html.h3(
                            {
                                "style": {
                                    "margin": "0 0 0.5rem 0",
                                    "fontSize": "2rem",
                                    "fontWeight": "700"
                                }
                            },
                            str(len(filtered_data['LOB'].unique()) if len(filtered_data) > 0 else 0)
                        ),
                        html.p(
                            {
                                "style": {
                                    "margin": "0",
                                    "fontSize": "0.9rem",
                                    "opacity": "0.9"
                                }
                            },
                            "Unique LOBs"
                        ),
                    ),
                    # Unique Filing Types
                    html.div(
                        {
                            "style": {
                                "background": "#4b5563",
                                "color": "white",
                                "padding": "1.5rem",
                                "borderRadius": "8px",
                                "textAlign": "center",
                                "boxShadow": "0 2px 4px rgba(75, 85, 99, 0.3)"
                            }
                        },
                        html.h3(
                            {
                                "style": {
                                    "margin": "0 0 0.5rem 0",
                                    "fontSize": "2rem",
                                    "fontWeight": "700"
                                }
                            },
                            str(len(filtered_data['Filing_Type'].unique()) if len(filtered_data) > 0 else 0)
                        ),
                        html.p(
                            {
                                "style": {
                                    "margin": "0",
                                    "fontSize": "0.9rem",
                                    "opacity": "0.9"
                                }
                            },
                            "Unique Filing Types"
                        ),
                    ),
                    # Unique Response Types
                    html.div(
                        {
                            "style": {
                                "background": "#111827",
                                "color": "white",
                                "padding": "1.5rem",
                                "borderRadius": "8px",
                                "textAlign": "center",
                                "boxShadow": "0 2px 4px rgba(17, 24, 39, 0.3)"
                            }
                        },
                        html.h3(
                            {
                                "style": {
                                    "margin": "0 0 0.5rem 0",
                                    "fontSize": "2rem",
                                    "fontWeight": "700"
                                }
                            },
                            str(len(filtered_data['RespType'].unique()) if len(filtered_data) > 0 else 0)
                        ),
                        html.p(
                            {
                                "style": {
                                    "margin": "0",
                                    "fontSize": "0.9rem",
                                    "opacity": "0.9"
                                }
                            },
                            "Unique Response Types"
                        ),
                    ),
                ),
            ),
            # Sample Data Section
            html.div(
                {
                    "style": {
                        "background": "white",
                        "borderRadius": "12px",
                        "padding": "2rem",
                        "marginBottom": "2rem",
                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)",
                        "border": "1px solid #e2e8f0"
                    }
                },
                html.h2(
                    {
                        "style": {
                            "fontSize": "1.5rem",
                            "fontWeight": "600",
                            "color": "#2d3748",
                            "margin": "0 0 1.5rem 0",
                            "borderBottom": "2px solid #2563eb",
                            "paddingBottom": "0.5rem"
                        }
                    },
                    "Sample Data Preview"
                ),
                html.div(
                    {
                        "style": {
                            "border": "1px solid #e2e8f0",
                            "borderRadius": "8px",
                            "padding": "1.5rem",
                            "backgroundColor": "#f8fafc",
                            "maxHeight": "400px",
                            "overflowY": "auto",
                            "overflowX": "auto"
                        }
                    },
                    html.pre(
                        {
                            "style": {
                                "whiteSpace": "pre-wrap",
                                "fontSize": "0.85rem",
                                "margin": "0",
                                "fontFamily": "'Courier New', monospace",
                                "color": "#2d3748",
                                "lineHeight": "1.5"
                            }
                        },
                        str(filtered_data.head(10).to_string()) if len(filtered_data) > 0 else "No data matches the current filters. Please adjust your filter selection."
                    ),
                ),
            ),
        ),
    )

reactpy.run(UserInputApp)
