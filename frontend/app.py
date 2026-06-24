import streamlit as st
import requests
import pandas as pd
import json
import os

API_BASE = os.getenv("API_BASE", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="AIForge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: #4361ee;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
    }
    .main-header p {
        color: #a0a0b0;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    .metric-card {
        background: #1e1e2e;
        border: 1px solid #2d2d4e;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .status-completed { color: #4caf50; font-weight: bold; }
    .status-running   { color: #ff9800; font-weight: bold; }
    .status-failed    { color: #f44336; font-weight: bold; }
    .stButton > button {
        background: linear-gradient(135deg, #4361ee, #3a0ca3);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3a0ca3, #4361ee);
    }
</style>
""", unsafe_allow_html=True)


# --- Helpers ---
def api_get(endpoint):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", timeout=300)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


def api_post(endpoint, data):
    try:
        r = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=300)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


def check_api():
    try:
        r = requests.get(f"{API_BASE}/health", timeout=5)
        return r.status_code == 200
    except:
        return False


# --- Sidebar ---
st.sidebar.markdown("## ⚡ AIForge")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "🧪 Run Experiment",
        "📊 Results & Metrics",
        "📝 Prompt Manager",
        "📁 Dataset Manager",
        "📄 Reports",
    ]
)

api_ok = check_api()
if api_ok:
    st.sidebar.success("🟢 API Connected")
else:
    st.sidebar.error("🔴 API Offline — start backend first")

st.sidebar.markdown("---")
st.sidebar.markdown("**AIForge v1.0.0**")
st.sidebar.markdown("AI Evaluation Platform")


# ─────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────
if page == "🏠 Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>⚡ AIForge</h1>
        <p>Production AI Evaluation & Agent Testing Platform</p>
    </div>
    """, unsafe_allow_html=True)

    if not api_ok:
        st.error("Backend is offline. Run: `uvicorn backend.api.main:app --reload --port 8000`")
        st.stop()

    col1, col2, col3, col4 = st.columns(4)

    exps = api_get("/experiments")
    total_exps = len(exps["experiments"]) if exps else 0
    completed = len([e for e in exps["experiments"] if e["status"] == "completed"]) if exps else 0
    failed = len([e for e in exps["experiments"] if e["status"] == "failed"]) if exps else 0

    models_data = api_get("/models")
    total_models = len(models_data["models"]) if models_data else 0

    with col1:
        st.metric("Total Experiments", total_exps)
    with col2:
        st.metric("Completed", completed)
    with col3:
        st.metric("Failed", failed)
    with col4:
        st.metric("Available Models", total_models)

    st.markdown("---")
    st.subheader("Recent Experiments")

    if exps and exps["experiments"]:
        df = pd.DataFrame(exps["experiments"])
        df = df[["id", "name", "dataset_name", "status", "created_at"]].head(10)
        df.columns = ["ID", "Name", "Dataset", "Status", "Created At"]
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No experiments yet. Go to **Run Experiment** to start.")

    st.markdown("---")
    st.subheader("Available Models")
    if models_data:
        cols = st.columns(len(models_data["models"]))
        for i, model in enumerate(models_data["models"]):
            with cols[i]:
                st.success(f"✅ {model}")


# ─────────────────────────────────────────
# PAGE: RUN EXPERIMENT
# ─────────────────────────────────────────
elif page == "🧪 Run Experiment":
    st.title("🧪 Run Experiment")

    if not api_ok:
        st.error("Backend is offline.")
        st.stop()

    with st.form("experiment_form"):
        st.subheader("Experiment Configuration")

        exp_name = st.text_input("Experiment Name", placeholder="e.g. RAG Evaluation Round 1")

        datasets = api_get("/datasets")
        dataset_files = datasets["datasets"] if datasets else []
        if not dataset_files:
            st.warning("No datasets found. Upload one in Dataset Manager.")
            dataset_choice = None
        else:
            dataset_choice = st.selectbox("Select Dataset", dataset_files)

        models_data = api_get("/models")
        all_models = models_data["models"] if models_data else []
        selected_models = st.multiselect(
            "Select Models to Compare",
            all_models,
            default=all_models[:2] if len(all_models) >= 2 else all_models
        )

        prompts_data = api_get("/prompts")
        prompt_list = prompts_data["prompts"] if prompts_data else []
        prompt_versions = [p["version"] for p in prompt_list]
        prompt_labels = [f"{p['version']} — {p['name']}" for p in prompt_list]
        prompt_choice = st.selectbox("Select Prompt Version", prompt_labels) if prompt_labels else None

        submitted = st.form_submit_button("🚀 Run Experiment", use_container_width=True)

    if submitted:
        if not exp_name:
            st.error("Please enter experiment name.")
        elif not dataset_choice:
            st.error("Please upload a dataset first.")
        elif not selected_models:
            st.error("Please select at least one model.")
        else:
            prompt_version = prompt_versions[prompt_labels.index(prompt_choice)] if prompt_choice else "v1"
            dataset_path = f"datasets/{dataset_choice}"

            with st.spinner(f"Running experiment on {len(selected_models)} model(s)... This may take a few minutes."):
                result = api_post("/experiments/run", {
                    "name": exp_name,
                    "dataset_path": dataset_path,
                    "selected_models": selected_models,
                    "prompt_version": prompt_version,
                })

            if result:
                st.success(f"✅ Experiment completed! ID: **{result['experiment_id']}**")
                st.balloons()
                st.info("Go to **Results & Metrics** to view the results.")


# ─────────────────────────────────────────
# PAGE: RESULTS & METRICS
# ─────────────────────────────────────────
elif page == "📊 Results & Metrics":
    st.title("📊 Results & Metrics")

    if not api_ok:
        st.error("Backend is offline.")
        st.stop()

    exps = api_get("/experiments")
    if not exps or not exps["experiments"]:
        st.info("No experiments yet.")
        st.stop()

    exp_options = {f"#{e['id']} — {e['name']}": e["id"] for e in exps["experiments"]}
    selected_exp = st.selectbox("Select Experiment", list(exp_options.keys()))
    exp_id = exp_options[selected_exp]

    metrics = api_get(f"/experiments/{exp_id}/metrics")
    best = api_get(f"/experiments/{exp_id}/best-model")

    if best and best.get("best_model"):
        b = best["best_model"]
        st.success(f"🏆 Best Model: **{b['model_name']}** | Similarity: {b['avg_similarity_score']:.4f} | Judge: {b['avg_llm_judge_score']:.2f}/10")

    if metrics and metrics.get("metrics"):
        st.subheader("Model Comparison")
        df = pd.DataFrame(metrics["metrics"])
        df = df[[
            "model_name", "avg_similarity_score", "avg_llm_judge_score",
            "avg_latency_seconds", "total_cost_usd", "success_rate", "hallucination_rate"
        ]]
        df.columns = ["Model", "Similarity", "Judge Score", "Latency(s)", "Cost($)", "Success Rate", "Hallucination Rate"]
        st.dataframe(df, use_container_width=True)

        st.subheader("Visual Comparison")
        chart_metric = st.selectbox("Chart Metric", ["Similarity", "Judge Score", "Latency(s)", "Cost($)"])
        st.bar_chart(df.set_index("Model")[chart_metric])

    st.subheader("Detailed Results")
    results = api_get(f"/experiments/{exp_id}/results")
    if results and results.get("results"):
        df_results = pd.DataFrame(results["results"])
        models_in_exp = df_results["model_name"].unique().tolist()
        model_filter = st.selectbox("Filter by Model", ["All"] + models_in_exp)
        if model_filter != "All":
            df_results = df_results[df_results["model_name"] == model_filter]
        st.dataframe(df_results[[
            "model_name", "question", "generated_answer",
            "similarity_score", "llm_judge_score", "latency_seconds", "is_hallucination"
        ]], use_container_width=True)


# ─────────────────────────────────────────
# PAGE: PROMPT MANAGER
# ─────────────────────────────────────────
elif page == "📝 Prompt Manager":
    st.title("📝 Prompt Manager")

    if not api_ok:
        st.error("Backend is offline.")
        st.stop()

    prompts = api_get("/prompts")
    if prompts and prompts["prompts"]:
        st.subheader("Existing Prompt Versions")
        for p in prompts["prompts"]:
            with st.expander(f"{p['version']} — {p['name']}"):
                full = api_get("/prompts")
                st.write(p.get("description", ""))

    st.markdown("---")
    st.subheader("Create New Prompt Version")

    with st.form("prompt_form"):
        version = st.text_input("Version (e.g. v4)", placeholder="v4")
        name = st.text_input("Name", placeholder="Expert Assistant")
        description = st.text_input("Description", placeholder="Short description")
        content = st.text_area("Prompt Content", height=150, placeholder="You are an expert AI assistant...")
        submitted = st.form_submit_button("💾 Save Prompt")

    if submitted:
        if not version or not name or not content:
            st.error("Version, Name, and Content are required.")
        else:
            result = api_post("/prompts", {
                "version": version,
                "name": name,
                "content": content,
                "description": description,
            })
            if result:
                st.success(f"✅ Prompt '{version}' saved.")
                st.rerun()


# ─────────────────────────────────────────
# PAGE: DATASET MANAGER
# ─────────────────────────────────────────
elif page == "📁 Dataset Manager":
    st.title("📁 Dataset Manager")

    if not api_ok:
        st.error("Backend is offline.")
        st.stop()

    st.subheader("Upload Dataset (CSV)")
    st.markdown("CSV must have columns: `question` and `expected_answer`")

    uploaded = st.file_uploader("Choose CSV file", type=["csv"])
    if uploaded:
        try:
            df_preview = pd.read_csv(uploaded)
            if "question" not in df_preview.columns or "expected_answer" not in df_preview.columns:
                st.error("CSV must have 'question' and 'expected_answer' columns.")
            else:
                st.success(f"✅ Valid CSV — {len(df_preview)} rows detected.")
                st.dataframe(df_preview.head(5), use_container_width=True)

                uploaded.seek(0)
                if st.button("⬆️ Upload to Server"):
                    files = {"file": (uploaded.name, uploaded, "text/csv")}
                    r = requests.post(f"{API_BASE}/datasets/upload", files=files, timeout=30)
                    if r.status_code == 200:
                        st.success(f"✅ Dataset '{uploaded.name}' uploaded.")
                        st.rerun()
                    else:
                        st.error(f"Upload failed: {r.text}")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    st.markdown("---")
    st.subheader("Available Datasets")
    datasets = api_get("/datasets")
    if datasets and datasets["datasets"]:
        for d in datasets["datasets"]:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"📄 {d}")
            with col2:
                if st.button("Preview", key=d):
                    try:
                        df_p = pd.read_csv(f"datasets/{d}")
                        st.dataframe(df_p.head(5), use_container_width=True)
                    except:
                        st.error("Could not load file.")
    else:
        st.info("No datasets uploaded yet.")

    st.markdown("---")
    st.subheader("Sample CSV Format")
    sample = pd.DataFrame({
        "question": ["What is RAG?", "What is MCP?"],
        "expected_answer": ["Retrieval Augmented Generation", "Model Context Protocol"]
    })
    st.dataframe(sample, use_container_width=True)
    csv = sample.to_csv(index=False)
    st.download_button("⬇️ Download Sample CSV", csv, "sample.csv", "text/csv")


# ─────────────────────────────────────────
# PAGE: REPORTS
# ─────────────────────────────────────────
elif page == "📄 Reports":
    st.title("📄 PDF Reports")

    if not api_ok:
        st.error("Backend is offline.")
        st.stop()

    exps = api_get("/experiments")
    completed_exps = [e for e in exps["experiments"] if e["status"] == "completed"] if exps else []

    if not completed_exps:
        st.info("No completed experiments yet. Run an experiment first.")
        st.stop()

    exp_options = {f"#{e['id']} — {e['name']}": e["id"] for e in completed_exps}
    selected = st.selectbox("Select Experiment", list(exp_options.keys()))
    exp_id = exp_options[selected]

    if st.button("📄 Generate & Download PDF Report", use_container_width=True):
        with st.spinner("Generating PDF report..."):
            r = requests.get(f"{API_BASE}/experiments/{exp_id}/report", timeout=60)
            if r.status_code == 200:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=r.content,
                    file_name=f"AIForge_Report_Experiment_{exp_id}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.success("✅ Report ready for download.")
            else:
                st.error(f"Report generation failed: {r.text}")