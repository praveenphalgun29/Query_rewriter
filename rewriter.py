import json

def load_user_data():
    """Loads the user persona data from the JSON file."""
    try:
        with open('data/data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: data.json not found. Make sure the file is in the 'data' directory.")
        return None
    except json.JSONDecodeError:
        print("Error: Could not decode data.json. Please check for syntax errors.")
        return None

def rewrite_query(user_id, query):
    
    all_users_data = load_user_data()
    if not all_users_data:
        return query # Return original query if data loading fails

    # Find the specific user by user_id
    user_data = next((user for user in all_users_data if user['user_id'] == user_id), None)

    if not user_data:
        return query # Return original query if user not found

    context = user_data.get('context', {})
    rewritten_query = query # Start with the original query

    # --- Rule-Based Personalization Logic ---

    # Rule 1: For the Health-Conscious Cook (User 3)
    if user_id == 3:
        dietary_needs = " ".join(context.get('dietary_needs', []))
        if any(keyword in query for keyword in ["recipe", "ideas", "food", "salad", "dinner"]):
            rewritten_query = f"{dietary_needs} {rewritten_query}"
        if "organic" in context.get('preferences', []) and "buy" in query:
             rewritten_query = f"where to buy organic {query.replace('buy ', '')}"

    # Rule 2: For the Budget Traveler (User 2)
    elif user_id == 2:
        if context.get('budget') == 'low':
            if any(keyword in query for keyword in ["hotels", "flights", "things to do", "museums"]):
                rewritten_query = f"cheap {rewritten_query}"
        if "how to get around" in query and context.get('budget') == 'low':
            rewritten_query = f"{query} on a budget"


    # Rule 3: For the Tech Enthusiast (User 1)
    elif user_id == 1:
        if context.get('expertise') == 'high' and any(keyword in query for keyword in ["laptop", "phone", "keyboard"]):
            rewritten_query = f"{rewritten_query} for high-performance gaming"


    if 'location' in context and any(keyword in query for keyword in ["near me", "nearby", "bakeries", "stores"]):
         rewritten_query = f"{rewritten_query.replace('near me', '').replace('nearby', '')} in {context['location']}"


    return rewritten_query.strip() # Return the final, cleaned-up query

if __name__ == "__main__":
    print("--- Testing Query Rewriter ---")

    # Test Case 1: Tech Enthusiast
    query1 = "best laptop"
    rewritten1 = rewrite_query(1, query1)
    print(f"User 1 (Original):  '{query1}'")
    print(f"User 1 (Rewritten): '{rewritten1}'\n")

    # Test Case 2: Budget Traveler
    query2 = "hotels in Paris"
    rewritten2 = rewrite_query(2, query2)
    print(f"User 2 (Original):  '{query2}'")
    print(f"User 2 (Rewritten): '{rewritten2}'\n")

    # Test Case 3: Health-Conscious Home Cook
    query3 = "salad recipe"
    rewritten3 = rewrite_query(3, query3)
    print(f"User 3 (Original):  '{query3}'")
    print(f"User 3 (Rewritten): '{rewritten3}'\n")
    
    # Test Case 4: Location-based query
    query4 = "bakeries near me"
    rewritten4 = rewrite_query(3, query4)
    print(f"User 3 (Original):  '{query4}'")
    print(f"User 3 (Rewritten): '{rewritten4}'")