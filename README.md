# Personalized Query Rewriter

## Dataset Description
The system uses a synthetic dataset (`data/data.json`) built around three distinct user personas, as creating synthetic data was a suggested option. The dataset contains a manageable number of queries to demonstrate personalization. The personas are:
* **The Tech Enthusiast:** A user interested in high-end, specific gadgets.
* **The Budget Traveler:** A user focused on affordable travel options.
* **The Health-Conscious Home Cook:** A user with specific dietary needs like vegetarian and gluten-free.

Each user has a `context` object and a list of `queries`, where each query has an `original_query` and a `ground_truth_rewrite` for evaluation purposes.

## Setup and Execution
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/praveenphalgun29/Query_rewriter
    cd Query_rewriter
    ```
2.  **Install dependencies:**
    ```bash
    pip install torch bert-score
    ```
3.  **Run the rewriter (demo):**
    To see a few examples of the rewriter in action, run:
    ```bash
    python rewriter.py
    ```
4.  **Run the full evaluation:**
    To evaluate the rewriter against the entire dataset, run:
    ```bash
    python evaluation.py
    ```

## Evaluation Methodology
The system was evaluated using both an automatic and a qualitative metric, as required by the assignment.

### Automatic Evaluation: BERTScore
**Justification:** BERTScore was chosen as the automatic metric. It measures the semantic similarity between the generated rewrite and the ground-truth rewrite. Unlike metrics like ROUGE or BLEU, it can understand that different words can have similar meanings (e.g., "cheap" vs. "affordable"), making it more suitable for this task.
**Results:**
BERTScore Results:
Average Precision: 0.9297
Average Recall: 0.8974
Average F1 Score: 0.9131

The high F1 score of **0.913** demonstrates that the rewritten queries are semantically very close to the ideal ground truth.

### Qualitative Evaluation: Heuristics
**Justification:** A heuristic-based approach was used for the qualitative evaluation. This provides a consistent and repeatable measure of quality. A "successful" rewrite was defined by two criteria: whether the query was made more specific and whether it incorporated elements from the user's context.
**Results:**
Heuristic Results:
Total Queries Evaluated: 15
Success Rate (Made More Specific): 80.00%
Success Rate (Was Personalized): 33.33%

The results show that the rewriter makes queries more specific 80% of the time. The lower "Personalized" score highlights a limitation of the simple heuristic, which only checks for exact keyword matches from the user's context and misses more nuanced personalizations. This is a key area for future improvement.




