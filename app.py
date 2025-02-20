import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def main():
    st.title("3D Bubble Plot of Constraints and Impacts")

    # --------------------------------------------------------------------------
    # 1) Load the CSV from /content/OpportunityCanvas.csv (Colab path)
    #    If you're using a local or different path, adjust accordingly.
    # --------------------------------------------------------------------------
 df = pd.read_csv("OpportunityCanvas.csv")
    except Exception as e:
        st.error(f"Error reading CSV from {csv_path}: {e}")
        return
    

    # --------------------------------------------------------------------------
    # 2) Display the full DataFrame
    # --------------------------------------------------------------------------
    st.subheader("Full Data Table")
    st.write(df)

    # --------------------------------------------------------------------------
    # 3) Define columns from your CSV
    #    Based on your CSV structure:
    #      Problem, Tech, Cost, Time, Regulations, Social Acceptance,
    #      Sum Constraints, IQ, QL, Total Impact, Notes
    # --------------------------------------------------------------------------
    problem_col = "Problem"
    tech_col = "Tech"
    cost_col = "Cost"
    time_col = "Time"
    regs_col = "Regulations"
    social_col = "Social Acceptance"
    sum_constraints_col = "Sum Constraints"
    iq_col = "IQ"        # We rename in tooltip to "Impact Quantity"
    ql_col = "QL"        # We rename in tooltip to "Impact Quality"
    total_impact_col = "Total Impact"
    notes_col = "Notes"

    # Choose which columns go on the 3D axes:
    constraint_cols = [cost_col, time_col, regs_col]

    # --------------------------------------------------------------------------
    # 4) Clip the constraint columns to [1..10], ensure integers
    # --------------------------------------------------------------------------
    for c in constraint_cols:
        df[c] = df[c].clip(1, 10).round().astype(int)

    # --------------------------------------------------------------------------
    # 5) Provide a slider to filter rows by Total Impact
    # --------------------------------------------------------------------------
    impact_min = int(df[total_impact_col].min())
    impact_max = int(df[total_impact_col].max())
    st.subheader("Filter by Total Impact")
    min_val, max_val = st.slider(
        "Select range",
        min_value=impact_min,
        max_value=impact_max,
        value=(impact_min, impact_max)
    )

    # Filter the DataFrame accordingly
    df_filtered = df[(df[total_impact_col] >= min_val) & (df[total_impact_col] <= max_val)]

    # --------------------------------------------------------------------------
    # 6) Bubble color = sum of constraints (already in CSV as "Sum Constraints")
    #    Bubble size = "Total Impact"
    # --------------------------------------------------------------------------
    df_filtered["BubbleSize"] = df_filtered[total_impact_col]

    # --------------------------------------------------------------------------
    # 7) Build custom hover text
    #    Show all columns in CSV order.
    #    Rename IQ->Impact Quantity, QL->Impact Quality.
    # --------------------------------------------------------------------------
    original_cols = list(df_filtered.columns)
    hover_texts = []
    for _, row in df_filtered.iterrows():
        lines = []
        for col in original_cols:
            val = row[col]
            if col == iq_col:
                lines.append(f"Impact Quantity: {val}")
            elif col == ql_col:
                lines.append(f"Impact Quality: {val}")
            else:
                lines.append(f"{col}: {val}")
        hover_texts.append("<br>".join(lines))

    # --------------------------------------------------------------------------
    # 8) Create 3D scatter plot with Plotly
    # --------------------------------------------------------------------------
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=df_filtered[cost_col],
                y=df_filtered[time_col],
                z=df_filtered[regs_col],
                mode="markers",
                text=hover_texts,
                hoverinfo="text",
                marker=dict(
                    size=df_filtered["BubbleSize"],
                    color=df_filtered[sum_constraints_col],
                    colorscale="Reds",
                    showscale=True,
                    opacity=0.8,
                    colorbar=dict(title="Sum of Constraints")  # <-- Color legend
                ),
            )
        ]
    )

    # --------------------------------------------------------------------------
    # 9) Configure 3D axes: range [1..10], integer ticks
    # --------------------------------------------------------------------------
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[1, 10], dtick=1, title=cost_col),
            yaxis=dict(range=[1, 10], dtick=1, title=time_col),
            zaxis=dict(range=[1, 10], dtick=1, title=regs_col),
        ),
        margin=dict(l=0, r=0, b=0, t=50),
        height=700,
        width=900,
        title={
            "text": "Opportunity Canvas - Findings 3D Plot (Bubble Size = Total Impact)",
            "x": 0.5,
            "xanchor": "center"
        }
    )

    # --------------------------------------------------------------------------
    # 10) Display figure
    # --------------------------------------------------------------------------
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
