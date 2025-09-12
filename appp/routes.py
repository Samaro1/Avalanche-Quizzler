from flask import Blueprint, request, jsonify, session, render_template
from .conductor import Conductor
from .logic import Logical
from .getnstoreq import Databaseq

routes = Blueprint("routes", __name__)

def get_instances():
    dab = Databaseq()
    lk = Logical()
    cd = Conductor()
    return dab, lk, cd


# ----------------------------
# UI ROUTES (HTML pages)
# ----------------------------

@routes.route("/index")
@routes.route("/")
def index():
    return render_template("index.html")


@routes.route("/quiz/<category>")
def quiz_page(category):
    #render the HTML UI for the quiz
    return render_template("quiz.html", category=category)


@routes.route("/results/<category>")
def results_page(category):
    if session.get("category") != category.lower():
        return render_template("index.html")

    questions = session.get("questions", [])
    score = session.get("score", 0)
    nft_eligible = score == len(questions)  # full marks required
    session["nft_eligible"] = nft_eligible

    return render_template(
        "result.html",
        category=category,
        score=score,
        total=len(questions),
        nft_eligible=nft_eligible
    )


@routes.route("/claim/<category>", methods=["GET", "POST"])
def claim(category):
    if request.method == "POST":
        wallet = request.form.get("wallet")

        # ✅ Process the claim here


        # Example: save claim to DB, call smart contract, etc.
        print(f"NFT claimed for category={category}, wallet={wallet}")

        # After successful claim, redirect to homepage
        return render_template("index.html")

    #show the claim form
    return render_template("claim.html", category=category)

# ----------------------------
# API ROUTES (JSON endpoints)
# ----------------------------

@routes.route("/api/start_quiz/<category>", methods=["GET"])
def api_start_quiz(category):
    dab, lk, cd = get_instances()
    try:
        categ_ques = dab.get_quiz_questions(category=category, n=3)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch questions: {str(e)}"}), 500

    questions = dab.strip_answers(question_batch=categ_ques) or []
    if not questions:
        return jsonify({"error": f"No questions available for category '{category}'"}), 404

    session["questions"] = questions
    session["index"] = 0
    session["score"] = 0
    session["category"] = category.lower()
    session["nft_eligible"] = False

    return jsonify({
        "message": f"Quiz started for {category}",
        "total_questions": len(questions),
        "first_question": questions[0],
        "category": category
    }), 200


@routes.route("/api/quiz/<category>/questions", methods=["GET"])

def api_quiz_questions(category):
    if session.get("category") != category.lower():
        return jsonify({"error": "Invalid quiz session"}), 400

    questions = session.get("questions")
    index = session.get("index", 0)

    if not questions or index >= len(questions):
        session["nft_eligible"] = session.get("score", 0) >= 2
        return jsonify({"finished": True}), 200

    question = questions[index]
    session["index"] = index + 1

    return jsonify({
        "question": question,
        "index": index,
        "remaining": len(questions) - index - 1
    }), 200


@routes.route("/api/submit_answer", methods=["POST"])
def api_submit_answer():
    dab, lk, cd = get_instances()
    data = request.get_json(silent=True) or {}
    question_id = data.get("question_id")
    user_answer = data.get("answer")
    category = data.get("category") or session.get("category")

    if not question_id or not user_answer or not category:
        return jsonify({"error": "Missing required fields: question_id, answer, category"}), 400

    try:
        question_id = int(question_id)
    except (ValueError, TypeError):
        return jsonify({"error": "question_id must be an integer"}), 400

    user_answer = str(user_answer).strip().upper()
    if user_answer not in ("A", "B", "C", "D"):
        return jsonify({"error": "answer must be one of A, B, C, D"}), 400

    result = lk.validate_answer(category=category, question_id=question_id, user_answer=user_answer)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400

    is_correct = bool(result.get("correct")) if isinstance(result, dict) else bool(result)

    if session.get("questions") is None:
        return jsonify({"error": "No active quiz session. Start quiz first."}), 400

    if is_correct:
        session["score"] = session.get("score", 0) + 1

    return jsonify({
        "correct": is_correct,
        "current_score": session.get("score", 0),
        "remaining": max(0, len(session.get("questions", [])) - session.get("index", 0)),
        "question": result if isinstance(result, dict) and "correct_answer" in result else None
    }), 200


@routes.route("/api/results/<category>", methods=["GET"])
def api_results(category):
    if session.get("category") != category.lower():
        return jsonify({"error": "Invalid category"}), 400

    questions = session.get("questions", [])
    score = session.get("score", 0)
    nft_eligible = session.get("nft_eligible", False)

    return jsonify({
        "score": score,
        "total": len(questions),
        "nft_eligible": nft_eligible
    }), 200

@routes.route("/api/claim/<category>", methods=["POST"])
def api_claim_nft(category):
    if session.get("category") != category.lower():
        return jsonify({"error": "Invalid category"}), 400

    if not session.get("nft_eligible", False):
        return jsonify({"error": "Not eligible for NFT reward"}), 403

    wallet_address = request.get_json(silent=True).get("wallet_address", "").strip()
    if not wallet_address:
        return jsonify({"error": "Wallet address required"}), 400

    # Placeholder: NFT minting logic here
    return jsonify({"success": True, "message": f"NFT claim recorded for {wallet_address}"}), 200
