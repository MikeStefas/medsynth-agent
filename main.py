from langchain_core.messages import HumanMessage
from src.graph import graph

if __name__ == "__main__":
    initial_state = {
        "messages": [
            HumanMessage(content="Can you search for recent research on metformin and cardiovascular outcomes in type 2 diabetes?")
        ],
        "dataset_path": "data/raw/pima_diabetes_dataset.csv"
    }
    graph.invoke(initial_state)