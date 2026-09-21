from langchain_core.messages import HumanMessage
from src.graph import graph

if __name__ == "__main__":
    initial_state = {
        "messages": [
            HumanMessage(content="High-risk diabetic patients with severe hyperglycemia, insulin resistance, and obesity.")
        ],
        "dataset_path": "data/raw/pima_diabetes_dataset.csv"
    }
    graph.invoke(initial_state)