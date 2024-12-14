from flask import Flask, render_template, request, jsonify
heroku logs --tail
app = Flask(__name__)

# アプリのデータ（状態）
total = 0
click_counts = {"お守り": 0, "おまもり": 0, "松山": 0, "アマテラス": 0, "破魔矢": 0, "おみくじ": 0}
name_values = {"お守り": 500, "おまもり": 800, "松山": 800, "アマテラス": 1000, "破魔矢": 1500, "おみくじ": 100}
actions = []  # 操作履歴（買い物と支払い）

@app.route("/")
def index():
    return render_template(
        "index.html", 
        total=total, 
        click_counts=click_counts, 
        name_values=name_values
    )

@app.route("/add", methods=["POST"])
def add():
    global total
    name = request.json["name"]
    total += name_values[name]
    click_counts[name] += 1
    actions.append({"type": "add", "name": name})
    return jsonify({"total": total, "click_counts": click_counts})

@app.route("/subtract", methods=["POST"])
def subtract():
    global total
    value = request.json["value"]
    total -= value
    actions.append({"type": "subtract", "value": value})
    return jsonify({"total": total})

@app.route("/undo", methods=["POST"])
def undo():
    global total, click_counts, actions
    if not actions:
        return jsonify({"total": total, "click_counts": click_counts, "message": "戻る操作はありません。"})
    
    last_action = actions.pop()
    if last_action["type"] == "add":
        name = last_action["name"]
        total -= name_values[name]
        click_counts[name] -= 1
    elif last_action["type"] == "subtract":
        total += last_action["value"]

    return jsonify({"total": total, "click_counts": click_counts})

@app.route("/reset", methods=["POST"])
def reset():
    global total, click_counts
    total = 0
    click_counts = {key: 0 for key in click_counts}
    actions.clear()
    return jsonify({"total": total, "click_counts": click_counts})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
