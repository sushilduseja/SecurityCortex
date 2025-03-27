import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np

class Visualizations:
    """
    A utility class for creating visualizations used in the AI Governance Dashboard.
    Provides helper methods for creating common charts and graphs.
    """
    
    @staticmethod
    def create_compliance_gauge(
        value: float,
        threshold: float,
        title: str = "Compliance Score",
        is_lower_better: bool = False
    ) -> go.Figure:
        """
        Create a gauge chart for compliance metrics.
        
        Args:
            value: The current value
            threshold: The threshold value
            title: The title of the gauge
            is_lower_better: Whether a lower value is better (e.g., for drift metrics)
            
        Returns:
            A Plotly figure object
        """
        if is_lower_better:
            # For metrics where lower is better (e.g., drift)
            gauge_color = "green" if value <= threshold else "red"
            steps = [
                {'range': [0, threshold], 'color': "lightgreen"},
                {'range': [threshold, 1], 'color': "lightgray"}
            ]
        else:
            # For metrics where higher is better (e.g., compliance %)
            gauge_color = "green" if value >= threshold else "red"
            steps = [
                {'range': [0, threshold], 'color': "lightgray"},
                {'range': [threshold, 1], 'color': "lightgreen"}
            ]
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            gauge={
                'axis': {'range': [0, 1]},
                'bar': {'color': gauge_color},
                'steps': steps,
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': threshold
                }
            }
        ))
        
        return fig
    
    @staticmethod
    def create_risk_distribution_chart(risk_scores: List[float], labels: Optional[List[str]] = None) -> go.Figure:
        """
        Create a histogram showing the distribution of risk scores.
        
        Args:
            risk_scores: List of risk scores
            labels: Optional list of labels corresponding to the risk scores
            
        Returns:
            A Plotly figure object
        """
        # Create a dataframe for the risk scores
        if labels:
            df = pd.DataFrame({
                'Risk Score': risk_scores,
                'Model': labels
            })
        else:
            df = pd.DataFrame({
                'Risk Score': risk_scores
            })
        
        # Create the histogram
        fig = px.histogram(
            df, 
            x='Risk Score',
            nbins=10,
            color_discrete_sequence=['#17a2b8'],
            title='Distribution of Risk Scores',
            labels={'Risk Score': 'Risk Score (0-100)'}
        )
        
        # Add a vertical line for the average risk score
        avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        fig.add_vline(
            x=avg_risk, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Avg: {avg_risk:.1f}",
            annotation_position="top"
        )
        
        # Update layout
        fig.update_layout(
            xaxis_range=[0, 100],
            bargap=0.1
        )
        
        return fig
    
    @staticmethod
    def create_compliance_status_pie(status_counts: Dict[str, int]) -> go.Figure:
        """
        Create a pie chart showing the distribution of compliance statuses.
        
        Args:
            status_counts: Dictionary mapping status names to counts
            
        Returns:
            A Plotly figure object
        """
        # Create lists for labels and values
        labels = list(status_counts.keys())
        values = list(status_counts.values())
        
        # Define colors for different statuses
        colors = {
            'Critical': '#d9534f',
            'Warning': '#f0ad4e',
            'Normal': '#5bc0de',
            'Good': '#5cb85c'
        }
        
        # Get colors based on labels
        color_list = [colors.get(label, '#777777') for label in labels]
        
        # Create the pie chart
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.4,
            marker_colors=color_list
        )])
        
        # Update layout
        fig.update_layout(
            title_text="Compliance Status Distribution",
            annotations=[dict(text=f"Total: {sum(values)}", x=0.5, y=0.5, font_size=15, showarrow=False)]
        )
        
        return fig
    
    @staticmethod
    def create_policy_category_bar(categories: Dict[str, int]) -> go.Figure:
        """
        Create a bar chart showing the number of policies by category.
        
        Args:
            categories: Dictionary mapping category names to counts
            
        Returns:
            A Plotly figure object
        """
        # Sort categories by count in descending order
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        
        # Create lists for labels and values
        labels = [item[0] for item in sorted_categories]
        values = [item[1] for item in sorted_categories]
        
        # Create the bar chart
        fig = go.Figure(data=[go.Bar(
            x=labels,
            y=values,
            marker_color='#007bff'
        )])
        
        # Update layout
        fig.update_layout(
            title_text="Policies by Category",
            xaxis_title="Category",
            yaxis_title="Number of Policies"
        )
        
        return fig
    
    @staticmethod
    def create_compliance_trend_line(dates: List[str], values: List[float]) -> go.Figure:
        """
        Create a line chart showing compliance trends over time.
        
        Args:
            dates: List of date strings
            values: List of compliance values corresponding to the dates
            
        Returns:
            A Plotly figure object
        """
        # Create a dataframe for the compliance values
        df = pd.DataFrame({
            'Date': dates,
            'Compliance Rate': values
        })
        
        # Create the line chart
        fig = px.line(
            df, 
            x='Date', 
            y='Compliance Rate',
            title='Compliance Rate Over Time',
            labels={'Compliance Rate': 'Compliance Rate (%)'}
        )
        
        # Add a threshold line at 80%
        fig.add_hline(
            y=80, 
            line_dash="dash", 
            line_color="green",
            annotation_text="Target (80%)",
            annotation_position="top right"
        )
        
        # Update layout
        fig.update_layout(
            yaxis_range=[0, 100],
            xaxis_title="Date",
            yaxis_title="Compliance Rate (%)"
        )
        
        return fig
    
    @staticmethod
    def create_risk_heatmap(models: List[str], risk_categories: List[str], risk_scores: List[List[float]]) -> go.Figure:
        """
        Create a heatmap showing risk scores across different models and categories.
        
        Args:
            models: List of model names
            risk_categories: List of risk category names
            risk_scores: 2D list of risk scores (models x categories)
            
        Returns:
            A Plotly figure object
        """
        # Create the heatmap
        fig = go.Figure(data=go.Heatmap(
            z=risk_scores,
            x=risk_categories,
            y=models,
            colorscale='Reds',
            colorbar=dict(title='Risk Score')
        ))
        
        # Update layout
        fig.update_layout(
            title='Risk Scores by Model and Category',
            xaxis_title='Risk Category',
            yaxis_title='Model'
        )
        
        return fig
    
    @staticmethod
    def create_governance_maturity_radar(
        categories: List[str],
        scores: List[float],
        benchmark: Optional[List[float]] = None
    ) -> go.Figure:
        """
        Create a radar chart showing governance maturity across different categories.
        
        Args:
            categories: List of governance category names
            scores: List of maturity scores for each category (0-100)
            benchmark: Optional list of benchmark scores for comparison
            
        Returns:
            A Plotly figure object
        """
        # Create the radar chart
        fig = go.Figure()
        
        # Add the organization's scores
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Organization'
        ))
        
        # Add benchmark scores if provided
        if benchmark:
            fig.add_trace(go.Scatterpolar(
                r=benchmark,
                theta=categories,
                fill='toself',
                name='Industry Benchmark'
            ))
        
        # Update layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title='Governance Maturity Assessment',
            showlegend=True
        )
        
        return fig

# Example usage
if __name__ == "__main__":
    # Example compliance gauge
    gauge_fig = Visualizations.create_compliance_gauge(
        value=0.85,
        threshold=0.8,
        title="Data Privacy Compliance"
    )
    
    # Example risk distribution chart
    risk_scores = [65, 42, 78, 53, 91, 35, 67, 82, 45, 60]
    risk_dist_fig = Visualizations.create_risk_distribution_chart(risk_scores)
    
    # Example compliance status pie chart
    status_counts = {
        'Critical': 2,
        'Warning': 5,
        'Normal': 12,
        'Good': 8
    }
    status_pie_fig = Visualizations.create_compliance_status_pie(status_counts)
