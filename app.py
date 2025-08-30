from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# In-memory orders for demo (reset when server restarts)
orders = []

@app.route("/")
def user_page():
    return render_template("user.html")

@app.route("/vendor")
def vendor_page():
    return render_template("vendor.html")

@app.route("/admin")
def admin_page():
    return render_template("admin.html")

# Serve static files normally (Flask does this automatically from /static)
# Socket handlers
@socketio.on("connect")
def on_connect():
    # Send current orders to newly connected client
    emit("all_orders", orders)

@socketio.on("place_order")
def handle_place_order(data):
    # Add server-side fields
    new_order = {
        "id": str(uuid4())[:8],
        "user": data.get("user", "Guest"),
        "vendor": data.get("vendor", "Vendor A"),
        "block": data.get("block", "Block A"),
        "item": data.get("item", "Food Item"),
        "status": "PLACED",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    orders.append(new_order)
    # broadcast new order (vendor + admin + user clients)
    emit("new_order", new_order, broadcast=True)
    # also return ack to the user who placed
    return {"result": "ok", "order": new_order}

@socketio.on("update_order")
def handle_update_order(data):
    oid = data.get("id")
    new_status = data.get("status")
    note = data.get("note", "")
    for o in orders:
        if o["id"] == oid:
            o["status"] = new_status
            o["last_update"] = {"status": new_status, "note": note, "ts": datetime.utcnow().isoformat() + "Z"}
            updated = o
            break
    else:
        updated = None

    if updated:
        emit("order_update", updated, broadcast=True)
        return {"result": "ok", "order": updated}
    else:
        return {"result": "error", "msg": "Order not found"}, 404

if __name__ == "__main__":
    print("Starting Flask-SocketIO server on http://localhost:5000")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
