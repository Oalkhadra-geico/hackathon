import pandas as pd
import reactpy
from reactpy import html, hooks
import requests
import json
import numpy as np

# Load the Excel file
try:
    df = pd.read_excel('../ResponseData.xlsx', sheet_name='GEICO')
    print(f"Successfully loaded Excel file with {len(df)} rows")
except Exception as e:
    print(f"Error loading Excel file: {e}")
    # Create empty dataframe as fallback
    df = pd.DataFrame()

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

def clean_data_for_json(data):
    """
    Clean data to make it JSON serializable by replacing NaN values with None.
    
    Args:
        data: pandas DataFrame or list of dictionaries
        
    Returns:
        list: Cleaned data with NaN values replaced by None
    """
    if isinstance(data, pd.DataFrame):
        # Convert DataFrame to records and clean NaN values
        records = data.to_dict('records')
    else:
        records = data
    
    cleaned_records = []
    for record in records:
        cleaned_record = {}
        for key, value in record.items():
            if pd.isna(value) or (isinstance(value, float) and np.isnan(value)):
                cleaned_record[key] = None
            else:
                cleaned_record[key] = value
        cleaned_records.append(cleaned_record)
    
    return cleaned_records

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
    
    # State for selected Topics
    selected_topics, set_selected_topics = hooks.use_state(set(("MTF", "Rate Capping", "Tariffs")))
    # State for Topic dropdown visibility
    show_topics_dropdown, set_show_topics_dropdown = hooks.use_state(False)

    # State for selected Carriers
    selected_carriers, set_selected_carriers = hooks.use_state(set())
    # State for Carrier dropdown visibility
    show_carriers_dropdown, set_show_carriers_dropdown = hooks.use_state(False)

    # State for filtered data
    filtered_data, set_filtered_data = hooks.use_state(df)
    # State for LLM response
    llm_response, set_llm_response = hooks.use_state("")
    # State for loading
    is_loading, set_is_loading = hooks.use_state(False)

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
            
        # Filter by Topics if any are selected
        if selected_topics:
            filtered_df = filtered_df[filtered_df['Topic'].isin(selected_topics)]
        
        # Filter by Carrier if any are selected
        if selected_carriers:
            filtered_df = filtered_df[filtered_df['Carrier'].isin(selected_carriers)]

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

    def handle_topics_toggle(topic):
        def toggle(event):
            if topic in selected_topics:
                new_topic = selected_topics - {topic}
                set_selected_topics(new_topic)
            else:
                new_topics = selected_topics | {topic}
                set_selected_topics(new_topics)
            # Apply filters whenever Response Types change
            apply_filters()
        return toggle

    def handle_topics_dropdown_toggle(event):
        set_show_topics_dropdown(not show_topics_dropdown)

    def handle_carriers_toggle(carrier):
        def toggle(event):
            if carrier in selected_carriers:
                new_carrier = selected_carriers - {carrier}
                set_selected_carriers(new_carrier)
            else:
                new_carriers = selected_carriers | {carrier}
                set_selected_carriers(new_carriers)
            # Apply filters whenever Response Types change
            apply_filters()
        return toggle

    def handle_carriers_dropdown_toggle(event):
        set_show_carriers_dropdown(not show_carriers_dropdown)

    def submit_query_to_backend(event):
        """Send the query and filtered data to the backend"""
        if not user_input.strip():
            set_llm_response("❌ Please enter a query first.")
            return
        
        if len(filtered_data) == 0:
            set_llm_response("❌ No data available with current filters. Please adjust your filters.")
            return
        
        set_is_loading(True)
        set_llm_response("🔄 Processing your query...")
        
        try:
            # Prepare the data for backend
            backend_data = {
                "query": user_input.strip(),
                "filtered_data": clean_data_for_json(filtered_data),
                "filter_summary": {
                    "total_records": len(filtered_data),
                    "states": list(selected_states),
                    "lobs": list(selected_lobs),
                    "filing_types": list(selected_filing_types),
                    "response_types": list(selected_response_types),
                    "topics": list(selected_topics),
                    "carriers": list(selected_carriers)
                }
            }
            
            # Send to backend
            response = requests.post(
                "http://localhost:5000/query",
                json=backend_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                set_llm_response(result.get("response", "No response from backend"))
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get("error", f"Backend returned status {response.status_code}")
                except:
                    error_message = f"Backend returned status {response.status_code}"
                set_llm_response(f"❌ Error: {error_message}")
                
        except requests.exceptions.ConnectionError:
            set_llm_response("❌ Error: Cannot connect to backend. Please ensure the backend server is running.")
        except requests.exceptions.Timeout:
            set_llm_response("❌ Error: Request timed out. Please try again.")
        except json.JSONDecodeError as e:
            set_llm_response(f"❌ Error: Invalid JSON response from backend: {str(e)}")
        except Exception as e:
            set_llm_response(f"❌ Error: {str(e)}")
        finally:
            set_is_loading(False)

    # Apply filters on component mount and whenever filters change
    hooks.use_effect(apply_filters, [selected_states, selected_lobs, selected_filing_types, selected_response_types, selected_topics, selected_carriers])

    return html.div(
        {
            "style": {
                "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                "backgroundColor": "#a185a8",
                "minHeight": "100vh",
                "padding": "0",
                "margin": "0"
            }
        },
        # Header Section
        html.div(
            {
                "style": {
                    "backgroundColor": "#cf9ed1",
                    "color": "white",
                    "padding": "2rem 0",
                    "marginBottom": "2rem",
                    "boxShadow": "0 4px 20px rgba(0, 0, 0, 0.15)",
                    "position": "relative",
                    "overflow": "hidden"
                }
            },
            # Background decoration
            html.div(
                {
                    "style": {
                        "position": "absolute",
                        "top": "-50%",
                        "right": "-10%",
                        "width": "200px",
                        "height": "200px",
                        "background": "rgba(255, 255, 255, 0.1)",
                        "borderRadius": "50%",
                        "transform": "rotate(45deg)"
                    }
                }
            ),
            html.div(
                {
                    "style": {
                        "maxWidth": "1200px",
                        "margin": "0 auto",
                        "padding": "0 20px",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                        "position": "relative",
                        "zIndex": "1"
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
                            "src": "https://graphicdesignergeeks.com/wp-content/uploads/2024/05/Geicos-Gecko-Branding-with-Mascots-1-1080x628.jpg",
                            "alt": "GEICO Logo",
                            "style": {
                                "height": "120px",
                                "marginRight": "1rem",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.2)"
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
                                "color": "#000000",
                                "fontSize": "3rem",
                                "fontWeight": "700",
                                "margin": "0",
                                "letterSpacing": "0.05em",
                                "textShadow": "0 2px 4px rgba(0, 0, 0, 0.3)"
                            }
                        },
                        "🔍 DORA"
                    ),
                    html.p(
                        {
                            "style": {
                                "color": "#000000",
                                "fontSize": "1.3rem",
                                "margin": "0.5rem 0 0 0",
                                "opacity": "0.95",
                                "fontWeight": "200"
                            }
                        },
                        "📊 DOI Objection Research Assistant"
                    )
                ),
                # Spacer for logo balance
                html.div(
                    {
                        "style": {
                            "width": "50px",
                            "marginLeft": "10rem"
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
                        "background": "#c5c5d3",
                        "borderRadius": "12px",
                        "padding": "2rem",
                        "marginBottom": "2rem",
                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)"
                    }
                },
                html.h2(
                    {
                        "style": {
                            "fontSize": "1.8rem",
                            "fontWeight": "700",
                            "color": "#1a202c",
                            "margin": "0 0 1.5rem 0",
                            "borderBottom": "3px solid #667eea",
                            "paddingBottom": "0.5rem",
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "0.5rem"
                        }
                    },
                    "🎛️ Filters"
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
                                    "fontWeight": "600",
                                    "color": "#3e2d48",
                                    "marginBottom": "0.5rem"
                                }
                            },
                            "📍 State"
                        ),
                        html.button(
                            {
                                "onClick": handle_dropdown_toggle,
                                "style": {
                                    "width": "100%",
                                    "padding": "14px 16px",
                                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "10px",
                                    "cursor": "pointer",
                                    "fontSize": "1rem",
                                    "fontWeight": "600",
                                    "transition": "all 0.3s ease",
                                    "boxShadow": "0 4px 12px rgba(102, 126, 234, 0.4)",
                                    "transform": "translateY(0)",
                                    "hover": {
                                        "transform": "translateY(-2px)",
                                        "boxShadow": "0 6px 16px rgba(102, 126, 234, 0.5)"
                                    }
                                }
                            },
                            f"📍 States ({len(selected_states)} selected) {'▼' if not show_dropdown else '▲'}",
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
                                    "fontWeight": "600",
                                    "color": "#2d3748",
                                    "marginBottom": "0.5rem"
                                }
                            },
                            "🏢 Line of Business"
                        ),
                        html.button(
                            {
                                "onClick": handle_lob_dropdown_toggle,
                                "style": {
                                    "width": "100%",
                                    "padding": "14px 16px",
                                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "10px",
                                    "cursor": "pointer",
                                    "fontSize": "1rem",
                                    "fontWeight": "600",
                                    "transition": "all 0.3s ease",
                                    "boxShadow": "0 4px 12px rgba(240, 147, 251, 0.4)",
                                    "transform": "translateY(0)",
                                    "hover": {
                                        "transform": "translateY(-2px)",
                                        "boxShadow": "0 6px 16px rgba(240, 147, 251, 0.5)"
                                    }
                                }
                            },
                            f"🏢 LOB ({len(selected_lobs)} selected) {'▼' if not show_lob_dropdown else '▲'}",
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
                                    "fontWeight": "600",
                                    "color": "#2d3748",
                                    "marginBottom": "0.5rem"
                                }
                            },
                            "📄 Filing Type"
                        ),
                        html.button(
                            {
                                "onClick": handle_filing_type_dropdown_toggle,
                                "style": {
                                    "width": "100%",
                                    "padding": "14px 16px",
                                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "10px",
                                    "cursor": "pointer",
                                    "fontSize": "1rem",
                                    "fontWeight": "600",
                                    "transition": "all 0.3s ease",
                                    "boxShadow": "0 4px 12px rgba(79, 172, 254, 0.4)",
                                    "transform": "translateY(0)",
                                    "hover": {
                                        "transform": "translateY(-2px)",
                                        "boxShadow": "0 6px 16px rgba(79, 172, 254, 0.5)"
                                    }
                                }
                            },
                            f"📄 Filing Type ({len(selected_filing_types)} selected) {'▼' if not show_filing_type_dropdown else '▲'}",
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
                    # Topic Filter
                    html.div(
                        {},
                        html.label(
                            {
                                "style": {
                                    "display": "block",
                                    "fontSize": "0.9rem",
                                    "fontWeight": "600",
                                    "color": "#2d3748",
                                    "marginBottom": "0.5rem"
                                }
                            },
                            "📝 Topic"
                        ),
                        html.button(
                            {
                                "onClick": handle_topics_dropdown_toggle,
                                "style": {
                                    "width": "100%",
                                    "padding": "14px 16px",
                                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "10px",
                                    "cursor": "pointer",
                                    "fontSize": "1rem",
                                    "fontWeight": "600",
                                    "transition": "all 0.3s ease",
                                    "boxShadow": "0 4px 12px rgba(168, 237, 234, 0.4)",
                                    "transform": "translateY(0)",
                                    "hover": {
                                        "transform": "translateY(-2px)",
                                        "boxShadow": "0 6px 16px rgba(168, 237, 234, 0.5)"
                                    }
                                }
                            },
                            f"📝 Topic ({len(selected_topics)} selected) {'▼' if not show_topics_dropdown else '▲'}",
                        ),
                        # Topic Dropdown
                        html.div(
                            {
                                "style": {
                                    "display": "block" if show_topics_dropdown else "none",
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
                                            "backgroundColor": "#374151" if topic in selected_topics else "transparent",
                                            "color": "white" if topic in selected_topics else "#2d3748",
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
                                                "checked": topic in selected_topics,
                                                "onChange": handle_topics_toggle(topic),
                                                "style": {
                                                    "marginRight": "8px",
                                                    "cursor": "pointer"
                                                }
                                            }
                                        ),
                                        topic,
                                    ),
                                )
                                for topic in TOPIC_OPTIONS
                            ],
                        ),
                    ),
                    # Carrier Filter
                    html.div(
                        {},
                        html.label(
                            {
                                "style": {
                                    "display": "block",
                                    "fontSize": "0.9rem",
                                    "fontWeight": "600",
                                    "color": "#2d3748",
                                    "marginBottom": "0.5rem"
                                }
                            },
                            "📦 Carrier"
                        ),
                        html.button(
                            {
                                "onClick": handle_carriers_dropdown_toggle,
                                "style": {
                                    "width": "100%",
                                    "padding": "14px 16px",
                                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "10px",
                                    "cursor": "pointer",
                                    "fontSize": "1rem",
                                    "fontWeight": "600",
                                    "transition": "all 0.3s ease",
                                    "boxShadow": "0 4px 12px rgba(255, 236, 210, 0.4)",
                                    "transform": "translateY(0)",
                                    "hover": {
                                        "transform": "translateY(-2px)",
                                        "boxShadow": "0 6px 16px rgba(255, 236, 210, 0.5)"
                                    }
                                }
                            },
                            f"📦 Carrier ({len(selected_carriers)} selected) {'▼' if not show_carriers_dropdown else '▲'}",
                        ),
                        # Carrier Dropdown
                        html.div(
                            {
                                "style": {
                                    "display": "block" if show_carriers_dropdown else "none",
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
                                            "backgroundColor": "#374151" if carrier in selected_carriers else "transparent",
                                            "color": "white" if carrier in selected_carriers else "#2d3748",
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
                                                "checked": carrier in selected_carriers,
                                                "onChange": handle_carriers_toggle(carrier),
                                                "style": {
                                                    "marginRight": "8px",
                                                    "cursor": "pointer"
                                                }
                                            }
                                        ),
                                        carrier,
                                    ),
                                )
                                for carrier in CARRIER_OPTIONS
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
                                    "fontWeight": "600",
                                    "color": "#2d3748",
                                    "marginBottom": "0.5rem"
                                }
                            },
                            "💬 Response Type"
                        ),
                        html.button(
                            {
                                "onClick": handle_response_type_dropdown_toggle,
                                "style": {
                                    "width": "100%",
                                    "padding": "14px 16px",
                                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "10px",
                                    "cursor": "pointer",
                                    "fontSize": "1rem",
                                    "fontWeight": "600",
                                    "transition": "all 0.3s ease",
                                    "boxShadow": "0 4px 12px rgba(102, 126, 234, 0.4)",
                                    "transform": "translateY(0)",
                                    "hover": {
                                        "transform": "translateY(-2px)",
                                        "boxShadow": "0 6px 16px rgba(102, 126, 234, 0.5)"
                                    }
                                }
                            },
                            f"💬 Response Type ({len(selected_response_types)} selected) {'▼' if not show_response_type_dropdown else '▲'}",
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
            # Status Section
            html.div(
                {
                    "style": {
                        "background": "#c5c5d3",
                        "borderRadius": "12px",
                        "padding": "2rem",
                        "marginBottom": "2rem",
                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)"
                    }
                },
                html.h2(
                    {
                        "style": {
                            "fontSize": "1.8rem",
                            "fontWeight": "700",
                            "color": "#1a202c",
                            "margin": "0 0 1.5rem 0",
                            "borderBottom": "3px solid #667eea",
                            "paddingBottom": "0.5rem",
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "0.5rem"
                        }
                    },
                    "📊 Current Selection"
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
                                "background": "#0048e2",
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
                                    "fontSize": "1.2rem",
                                    "fontWeight": "700"
                                }
                            },
                            "📍 Selected States"
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
                                "background": "#00c3ff",
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
                                    "fontSize": "1.2rem",
                                    "fontWeight": "700"
                                }
                            },
                            "🏢 Selected LOBs"
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
                                "background": "#00FF62",
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
                                    "fontSize": "1.2rem",
                                    "fontWeight": "700"
                                }
                            },
                            "📄 Selected Filing Types"
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
                    # Selected Topics Card
                    html.div(
                        {
                            "style": {
                                "background": "#BBFF00",
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
                                    "fontSize": "1.2rem",
                                    "fontWeight": "700"
                                }
                            },
                            "📝 Selected Topics"
                        ),
                        html.p(
                            {
                                "style": {
                                    "margin": "0",
                                    "fontSize": "0.9rem",
                                    "opacity": "0.9"
                                }
                            },
                            ', '.join(sorted(selected_topics)) if selected_topics else 'No topics selected'
                        ),
                    ),
                    # Selected Carriers Card
                    html.div(
                        {
                            "style": {
                                "background": "#FF0037",
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
                                    "fontSize": "1.2rem",
                                    "fontWeight": "700"
                                }
                            },
                            "📦 Selected Carriers"
                        ),
                        html.p(
                            {
                                "style": {
                                    "margin": "0",
                                    "fontSize": "0.9rem",
                                    "opacity": "0.9"
                                }
                            },
                            ', '.join(sorted(selected_carriers)) if selected_carriers else 'No carriers selected'
                        ),
                    ),
                    # Selected Response Types Card
                    html.div(
                        {
                            "style": {
                                "background": "#ff5100",
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
                                    "fontSize": "1.2rem",
                                    "fontWeight": "700"
                                }
                            },
                            "💬 Selected Response Types"
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
                    )
                ),
            ),
            # Data Summary Section
            html.div(
                {
                    "style": {
                        "background": "#c5c5d3",
                        "borderRadius": "12px",
                        "padding": "2rem",
                        "marginBottom": "2rem",
                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)"
                    }
                },
                html.h2(
                    {
                        "style": {
                            "fontSize": "1.8rem",
                            "fontWeight": "700",
                            "color": "#1a202c",
                            "margin": "0 0 1.5rem 0",
                            "borderBottom": "3px solid #667eea",
                            "paddingBottom": "0.5rem",
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "0.5rem"
                        }
                    },
                    "📈 Data Analytics"
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
                    # Unique States
                    html.div(
                        {
                            "style": {
                                "background": "#0048e2",
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
                                    "fontSize": "1rem",
                                    "opacity": "0.95",
                                    "fontWeight": "600"
                                }
                            },
                            "🗺️ Unique States"
                        ),
                    ),
                    # Unique LOBs
                    html.div(
                        {
                            "style": {
                                "background": "#00c3ff",
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
                                    "fontSize": "1rem",
                                    "opacity": "0.95",
                                    "fontWeight": "600"
                                }
                            },
                            "🏢 Unique LOBs"
                        ),
                    ),
                    # Unique Filing Types
                    html.div(
                        {
                            "style": {
                                "background": "#00FF62",
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
                                    "fontSize": "1rem",
                                    "opacity": "0.95",
                                    "fontWeight": "600"
                                }
                            },
                            "📄 Unique Filing Types"
                        ),
                    ),
                    # Unique Filing Types
                    html.div(
                        {
                            "style": {
                                "background": "#BBFF00",
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
                                    "fontSize": "1rem",
                                    "opacity": "0.95",
                                    "fontWeight": "600"
                                }
                            },
                            "📝 Unique Topics"
                        ),
                    ),
                    # Unique Filing Types
                    html.div(
                        {
                            "style": {
                                "background": "#FF0037",
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
                                    "fontSize": "1rem",
                                    "opacity": "0.95",
                                    "fontWeight": "600"
                                }
                            },
                            "📦 Unique Carriers"
                        ),
                    ),
                    # Unique Response Types
                    html.div(
                        {
                            "style": {
                                "background": "#ff5100",
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
                                    "fontSize": "1rem",
                                    "opacity": "0.95",
                                    "fontWeight": "600"
                                }
                            },
                            "💬 Unique Response Types"
                        ),
                    ),
                    # Total Records
                    html.div(
                        {
                            "style": {
                                "background": "#4b0000",
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
                                    "fontSize": "1rem",
                                    "opacity": "0.95",
                                    "fontWeight": "600"
                                }
                            },
                            "📊 Total Records"
                        ),
                    ),
                ),
            ),
            # Input Section
            html.div(
                {
                    "style": {
                        "background": "#c5c5d3",
                        "borderRadius": "12px",
                        "padding": "2rem",
                        "marginBottom": "2rem",
                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)"
                    }
                },
                html.h2(
                    {
                        "style": {
                            "fontSize": "1.8rem",
                            "fontWeight": "700",
                            "color": "#1a202c",
                            "margin": "0 0 1.5rem 0",
                            "borderBottom": "3px solid #667eea",
                            "paddingBottom": "0.5rem",
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "0.5rem"
                        }
                    },
                    "✍️ Query Input"
                ),
                html.textarea(
                    {
                        "value": user_input,
                        "onChange": handle_input_change,
                        "placeholder": "💡 Enter your query or analysis request here...",
                        "style": {
                            "width": "100%",
                            "height": "140px",
                            "padding": "20px",
                            "fontSize": "1.1rem",
                            "border": "3px solid #e2e8f0",
                            "borderRadius": "12px",
                            "resize": "vertical",
                            "fontFamily": "inherit",
                            "transition": "all 0.3s ease",
                            "boxSizing": "border-box",
                            "background": "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
                            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.05)",
                            "focus": {
                                "borderColor": "#667eea",
                                "boxShadow": "0 6px 20px rgba(102, 126, 234, 0.2)",
                                "outline": "none"
                            }
                        }
                    }
                ),
                # Submit Button
                html.div(
                    {
                        "style": {
                            "marginTop": "1rem",
                            "textAlign": "right"
                        }
                    },
                    html.button(
                        {
                            "onClick": submit_query_to_backend,
                            "disabled": is_loading,
                            "style": {
                                "padding": "12px 24px",
                                "fontSize": "1.1rem",
                                "fontWeight": "600",
                                "color": "white",
                                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" if not is_loading else "linear-gradient(135deg, #a0aec0 0%, #718096 100%)",
                                "border": "none",
                                "borderRadius": "10px",
                                "cursor": "pointer" if not is_loading else "not-allowed",
                                "transition": "all 0.3s ease",
                                "boxShadow": "0 4px 12px rgba(102, 126, 234, 0.4)" if not is_loading else "0 2px 4px rgba(0, 0, 0, 0.1)",
                                "transform": "translateY(0)",
                                "hover": {
                                    "transform": "translateY(-2px)",
                                    "boxShadow": "0 6px 20px rgba(102, 126, 234, 0.6)"
                                } if not is_loading else {}
                            }
                        },
                        "🔄 Processing..." if is_loading else "🚀 Submit Query"
                    )
                ),
            ),
            # Sample Data Section
            html.div(
                {
                    "style": {
                        "background": "#c5c5d3",
                        "borderRadius": "12px",
                        "padding": "2rem",
                        "marginBottom": "2rem",
                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.05)"
                    }
                },
                html.h2(
                    {
                        "style": {
                            "fontSize": "1.8rem",
                            "fontWeight": "700",
                            "color": "#1a202c",
                            "margin": "0 0 1.5rem 0",
                            "borderBottom": "3px solid #667eea",
                            "paddingBottom": "0.5rem",
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "0.5rem"
                        }
                    },
                    "📋 Model Output"
                ),
                                    html.div(
                        {
                            "style": {
                                "border": "2px solid #e2e8f0",
                                "borderRadius": "12px",
                                "padding": "2rem",
                                "background": "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
                                "maxHeight": "500px",
                                "overflowY": "auto",
                                "overflowX": "auto",
                                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.05)"
                            }
                        },
                                            html.pre(
                            {
                                "style": {
                                    "whiteSpace": "pre-wrap",
                                    "fontSize": "0.9rem",
                                    "margin": "0",
                                    "fontFamily": "'Courier New', monospace",
                                    "color": "#1a202c",
                                    "lineHeight": "1.6",
                                    "fontWeight": "500"
                                }
                            },
                            llm_response if llm_response else ("❌ No data matches the current filters. Please adjust your filter selection." if len(filtered_data) == 0 else "💡 Enter a query above and click 'Submit Query' to get AI-powered insights from your filtered data.")
                        ),
                ),
            ),
        ),
    )

reactpy.run(UserInputApp)
