import pandas as pd
import numpy as np
from datetime import datetime
from dataclasses import dataclass, field
from io import BytesIO
from fpdf import FPDF
import base64
import plotly.graph_objects as go
import metrics

@dataclass
class ReportState:
    page_type: str  # "equity", "strategy", "portfolio"
    tickers: list
    benchmark: str = "SPY"
    start_date: str = ""
    end_date: str = ""
    settings: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)
    tables: dict = field(default_factory=dict)
    figures: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@dataclass
class ReportArtifact:
    html: str
    pdf: bytes
    csv: str
    filename_base: str

def generate_exec_summary(state: ReportState) -> list:
    """Deterministic rule-based summary generation."""
    summary = []
    m = state.metrics
    
    if state.page_type == "equity":
        ticker = state.tickers[0] if state.tickers else "Asset"
        ret = m.get('ann_ret', 0)
        vol = m.get('vol', 0)
        sharpe = m.get('sharpe', 0)
        drawdown = abs(m.get('max_dd', 0))
        
        summary.append(f"{ticker} generated an annualized return of {ret*100:.2f}%.")
        
        if sharpe > 1:
            summary.append(f"Risk-adjusted performance is strong (Sharpe: {sharpe:.2f}).")
        elif sharpe > 0.5:
            summary.append(f"Risk-adjusted performance is moderate (Sharpe: {sharpe:.2f}).")
        else:
            summary.append(f"Performance adjusted for risk is weak (Sharpe: {sharpe:.2f}).")
            
        if drawdown > 0.25:
            summary.append(f"Significant peak-to-trough risk detected ({drawdown*100:.1f}% drawdown).")
        
    elif state.page_type == "strategy":
        st_ret = m.get('strat_ret', 0)
        bh_ret = m.get('bh_ret', 0)
        st_dd = abs(m.get('strat_dd', 0))
        
        if st_ret > bh_ret:
            summary.append(f"The strategy outperformed Buy & Hold by {(st_ret-bh_ret)*100:.2f}% annualized.")
        else:
            summary.append(f"Passive Buy & Hold outperformed the strategy by {(bh_ret-st_ret)*100:.2f}% annualized.")
            
        if st_dd < abs(m.get('bh_dd', 0)):
            summary.append(f"The model successfully reduced downside volatility relative to the asset.")
            
    elif state.page_type == "portfolio":
        ret = m.get('return', 0)
        vol = m.get('volatility', 0)
        sharpe = m.get('sharpe', 0)
        
        summary.append(f"Consolidated portfolio targets {ret*100:.2f}% expected annual return.")
        summary.append(f"Portfolio volatility is modeled at {vol*100:.2f}%.")
        
        if sharpe > 1.2:
            summary.append("This allocation offers highly efficient risk/reward trade-offs.")

    return summary

def build_html_report(state: ReportState) -> str:
    """Builds a premium HTML report for in-app preview and download."""
    summary_items = generate_exec_summary(state)
    summary_html = "".join([f"<li>{s}</li>" for s in summary_items])
    
    # Simple CSS for professional look
    style = """
    <style>
        .report-body { font-family: 'Inter', sans-serif; color: #1F2937; line-height: 1.5; max-width: 800px; margin: auto; padding: 40px; background: white; border: 1px solid #E5E7EB; border-radius: 8px; }
        .report-header { border-bottom: 2px solid #3B82F6; padding-bottom: 20px; margin-bottom: 30px; }
        .report-title { font-size: 24px; font-weight: 700; color: #111827; }
        .report-meta { font-size: 14px; color: #6B7280; margin-top: 5px; }
        .section-title { font-size: 18px; font-weight: 600; color: #111827; margin-top: 30px; margin-bottom: 15px; border-left: 4px solid #3B82F6; padding-left: 12px; }
        .metric-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 30px; }
        .metric-card { background: #F9FAFB; padding: 15px; border-radius: 6px; border: 1px solid #F3F4F6; }
        .metric-label { font-size: 12px; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; }
        .metric-value { font-size: 20px; font-weight: 700; color: #3B82F6; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th { text-align: left; background: #F9FAFB; padding: 10px; font-size: 13px; color: #374151; border-bottom: 1px solid #E5E7EB; }
        td { padding: 10px; border-bottom: 1px solid #F3F4F6; font-size: 14px; }
        .disclaimer { font-size: 11px; color: #9CA3AF; margin-top: 50px; text-align: center; font-style: italic; }
    </style>
    """
    
    # Generic table builder for weights or comparisons
    table_html = ""
    if 'weights' in state.tables:
        df_w = state.tables['weights']
        table_html = "<table><thead><tr><th>Asset</th><th>Weight</th></tr></thead><tbody>"
        for _, row in df_w.iterrows():
            table_html += f"<tr><td>{row['Asset']}</td><td>{row['Weight']*100:.2f}%</td></tr>"
        table_html += "</tbody></table>"
    elif 'comparison' in state.tables:
        df_c = state.tables['comparison']
        table_html = "<table><thead><tr><th>Metric</th><th>Strategy</th><th>Buy & Hold</th></tr></thead><tbody>"
        for _, row in df_c.iterrows():
            table_html += f"<tr><td>{row['Metric']}</td><td>{row['Strategy']}</td><td>{row['Buy & Hold']}</td></tr>"
        table_html += "</tbody></table>"

    html = f"""
    <div class="report-wrapper" style="background:#F3F4F6; padding: 40px 0;">
    <div class="report-body">
        {style}
        <div class="report-header">
            <div class="report-title">FinSight Research Report</div>
            <div class="report-meta">Type: {state.page_type.capitalize()} Intelligence | Generated: {state.timestamp}</div>
            <div class="report-meta">Range: {state.start_date} to {state.end_date}</div>
        </div>
        
        <div class="section-title">Executive Summary</div>
        <ul style="padding-left: 20px;">
            {summary_html}
        </ul>
        
        <div class="section-title">Key Performance Indicators</div>
        <div class="metric-grid">
            {" ".join([f'<div class="metric-card"><div class="metric-label">{k.replace("_", " ")}</div><div class="metric-value">{v}</div></div>' for k, v in state.metrics.items() if isinstance(v, str)])}
        </div>
        
        {f'<div class="section-title">Composition Details</div>{table_html}' if table_html else ''}
        
        <div class="disclaimer">
            This report is for educational and demonstrational purposes only. It does not constitute investment advice, 
            financial advice, trading advice, or any other sort of advice. All investments carry risk.
        </div>
    </div>
    </div>
    """
    return html

def build_pdf_report(state: ReportState) -> bytes:
    """Builds a professional PDF report using fpdf2."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 20)
    
    # Title
    pdf.cell(0, 15, "FinSight Research Report", ln=True, align='L')
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"Analysis Type: {state.page_type.capitalize()} Intelligence", ln=True)
    pdf.cell(0, 5, f"Date Range: {state.start_date} to {state.end_date}", ln=True)
    pdf.cell(0, 5, f"Generated: {state.timestamp}", ln=True)
    
    pdf.ln(10)
    pdf.set_draw_color(59, 130, 246)
    pdf.set_line_width(1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Executive Summary
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Executive Summary", ln=True)
    pdf.set_font("helvetica", "", 11)
    for s in generate_exec_summary(state):
        pdf.multi_cell(0, 7, f"- {s}")
    
    pdf.ln(10)
    
    # Metrics Table
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "Key Metrics", ln=True)
    pdf.set_font("helvetica", "B", 10)
    pdf.set_fill_color(249, 250, 251)
    
    col_width = 95
    pdf.cell(col_width, 10, "Metric", border=1, fill=True)
    pdf.cell(col_width, 10, "Value", border=1, fill=True, ln=True)
    
    pdf.set_font("helvetica", "", 10)
    for k, v in state.metrics.items():
        if isinstance(v, str):
            pdf.cell(col_width, 8, k.replace("_", " ").title(), border=1)
            pdf.cell(col_width, 8, str(v), border=1, ln=True)
            
    pdf.ln(10)

    # Disclaimer
    pdf.set_y(-40)
    pdf.set_font("helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.multi_cell(0, 4, "Disclaimer: This report is for educational purposes only. FinSight is not a financial advisor. Historical performance is not indicative of future results.", align='C')

    return pdf.output()

def create_report_artifact(state: ReportState) -> ReportArtifact:
    """Entry point to build all report formats."""
    html = build_html_report(state)
    pdf_bytes = build_pdf_report(state)
    
    # Simplified CSV from metrics
    csv_str = pd.DataFrame([state.metrics]).to_csv(index=False)
    
    filename = f"FinSight_{state.page_type}_{datetime.now().strftime('%Y%m%d')}"
    
    return ReportArtifact(
        html=html,
        pdf=pdf_bytes,
        csv=csv_str,
        filename_base=filename
    )
