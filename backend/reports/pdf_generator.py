import os
import logging
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

logger = logging.getLogger(__name__)


class PDFReportGenerator:

    def __init__(self):
        os.makedirs("reports", exist_ok=True)

    def generate(self, experiment: dict, metrics: list, best_model: dict, results: list) -> str:
        try:
            filename = f"reports/AIForge_Report_Experiment_{experiment['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
            styles = getSampleStyleSheet()
            story = []

            # --- Title ---
            title_style = ParagraphStyle("Title", parent=styles["Title"], fontSize=22, textColor=colors.HexColor("#1a1a2e"), spaceAfter=6, alignment=TA_CENTER)
            sub_style = ParagraphStyle("Sub", parent=styles["Normal"], fontSize=11, textColor=colors.HexColor("#4a4a4a"), spaceAfter=4, alignment=TA_CENTER)
            body_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, textColor=colors.HexColor("#2d2d2d"), spaceAfter=4)
            heading_style = ParagraphStyle("Heading", parent=styles["Heading2"], fontSize=13, textColor=colors.HexColor("#1a1a2e"), spaceBefore=12, spaceAfter=6)

            story.append(Paragraph("AIForge Evaluation Report", title_style))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}", sub_style))
            story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#4361ee")))
            story.append(Spacer(1, 12))

            # --- Experiment Info ---
            story.append(Paragraph("Experiment Overview", heading_style))
            exp_data = [
                ["Experiment ID", str(experiment.get("id", ""))],
                ["Name", experiment.get("name", "")],
                ["Dataset", experiment.get("dataset_name", "")],
                ["Prompt Version", experiment.get("prompt_version", "")],
                ["Status", experiment.get("status", "")],
                ["Models Tested", ", ".join(experiment.get("models_used", []))],
                ["Created At", str(experiment.get("created_at", ""))],
            ]
            exp_table = Table(exp_data, colWidths=[2*inch, 4*inch])
            exp_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef2ff")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1a1a2e")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#c0c0c0")),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f8f9ff")]),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(exp_table)
            story.append(Spacer(1, 12))

            # --- Best Model ---
            if best_model:
                story.append(Paragraph("Best Performing Model", heading_style))
                best_data = [
                    ["Model", best_model.get("model_name", "")],
                    ["Avg Similarity Score", f"{best_model.get('avg_similarity_score', 0):.4f}"],
                    ["Avg LLM Judge Score", f"{best_model.get('avg_llm_judge_score', 0):.2f} / 10"],
                    ["Avg Latency", f"{best_model.get('avg_latency_seconds', 0):.3f} sec"],
                    ["Total Cost", f"${best_model.get('total_cost_usd', 0):.6f}"],
                    ["Success Rate", f"{best_model.get('success_rate', 0)*100:.1f}%"],
                    ["Hallucination Rate", f"{best_model.get('hallucination_rate', 0)*100:.1f}%"],
                ]
                best_table = Table(best_data, colWidths=[2*inch, 4*inch])
                best_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#d4edda")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1a1a2e")),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#c0c0c0")),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f0fff4")]),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]))
                story.append(best_table)
                story.append(Spacer(1, 12))

            # --- Model Comparison ---
            if metrics:
                story.append(Paragraph("Model Comparison", heading_style))
                headers = ["Model", "Similarity", "Judge Score", "Latency", "Cost USD", "Hallucination%"]
                rows = [headers]
                for m in metrics:
                    rows.append([
                        m.get("model_name", "").replace("llama-", "llama-\n").replace("gemma", "gemma"),
                        f"{m.get('avg_similarity_score', 0):.4f}",
                        f"{m.get('avg_llm_judge_score', 0):.2f}",
                        f"{m.get('avg_latency_seconds', 0):.3f}s",
                        f"${m.get('total_cost_usd', 0):.6f}",
                        f"{m.get('hallucination_rate', 0)*100:.1f}%",
                    ])
                col_widths = [2.2*inch, 0.9*inch, 0.9*inch, 0.8*inch, 0.9*inch, 1.0*inch]
                metrics_table = Table(rows, colWidths=col_widths)
                metrics_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4361ee")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#c0c0c0")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9ff")]),
                    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                    ("PADDING", (0, 0), (-1, -1), 5),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]))
                story.append(metrics_table)
                story.append(Spacer(1, 12))

            # --- Sample Results ---
            if results:
                story.append(Paragraph("Sample Results (First 5)", heading_style))
                for i, r in enumerate(results[:5]):
                    story.append(Paragraph(f"Q{i+1}: {r.get('question', '')}", body_style))
                    story.append(Paragraph(f"<b>Model:</b> {r.get('model_name', '')}", body_style))
                    story.append(Paragraph(f"<b>Generated:</b> {r.get('generated_answer', '')[:600]}", body_style))
                    story.append(Paragraph(
                        f"<b>Similarity:</b> {r.get('similarity_score', 0):.4f} | "
                        f"<b>Judge:</b> {r.get('llm_judge_score', 0):.2f}/10 | "
                        f"<b>Hallucination:</b> {'Yes' if r.get('is_hallucination') else 'No'}",
                        body_style
                    ))
                    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e0e0e0")))
                    story.append(Spacer(1, 4))

            # --- Footer ---
            story.append(Spacer(1, 20))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#4361ee")))
            story.append(Paragraph("Generated by AIForge — AI Evaluation Platform", sub_style))

            doc.build(story)
            logger.info(f"PDF report generated: {filename}")
            return filename

        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            raise