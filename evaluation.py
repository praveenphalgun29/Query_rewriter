import torch
from bert_score import score as bert_scorer
from rewriter import rewrite_query, load_user_data

def evaluate_automatically():
    
    print("--- Running Automatic Evaluation (BERTScore) ---")
    all_users_data = load_user_data()
    if not all_users_data:
        return

    candidates = [] # Our model's generated rewrites
    references = [] # The ground truth rewrites

    for user in all_users_data:
        user_id = user['user_id']
        for query_pair in user['queries']:
            original_query = query_pair['original_query']
            ground_truth = query_pair['ground_truth_rewrite']

            generated_rewrite = rewrite_query(user_id, original_query)

            candidates.append(generated_rewrite)
            references.append(ground_truth)

    # Calculate BERTScore
    P, R, F1 = bert_scorer(candidates, references, lang="en", verbose=False, idf=False)

    #The average F1 score, which is a good overall measure
    print(f"BERTScore Results:")
    print(f"Average Precision: {P.mean():.4f}")
    print(f"Average Recall: {R.mean():.4f}")
    print(f"Average F1 Score: {F1.mean():.4f}\n")


def evaluate_qualitatively():
    
    print("--- Running Qualitative Evaluation (Heuristics) ---")
    all_users_data = load_user_data()
    if not all_users_data:
        return

    total_queries = 0
    made_more_specific = 0
    was_personalized = 0

    for user in all_users_data:
        user_id = user['user_id']
        context_values = [str(v).lower() for v in user['context'].values()]

        for query_pair in user['queries']:
            total_queries += 1
            original_query = query_pair['original_query']
            generated_rewrite = rewrite_query(user_id, original_query)

            # Heuristic 1: Is the rewrite more specific (longer)?
            if len(generated_rewrite) > len(original_query):
                made_more_specific += 1

            # Heuristic 2: Does it contain a keyword from the user's context?
            is_personal = False
            for value in context_values:
                if any(part in generated_rewrite.lower() for part in value.split()):
                    is_personal = True
                    break
            if is_personal:
                was_personalized += 1

    print("Heuristic Results:")
    print(f"Total Queries Evaluated: {total_queries}")
    print(f"Success Rate (Made More Specific): {made_more_specific/total_queries:.2%}")
    print(f"Success Rate (Was Personalized): {was_personalized/total_queries:.2%}\n")


if __name__ == "__main__":
    evaluate_automatically()
    evaluate_qualitatively()