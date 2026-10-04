import math
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "change-me"

# ---------------------------------------------------------------
# EDIT YOUR PERSONAL DATA HERE - every page reads from this dict.
# ---------------------------------------------------------------
ME = {
    "name": "Mary Grace A. Santos",
    "nick": "Grace",
    "role": "BSCpE student at Polytechnic University of the Philippines",
    "location": "Binangonan, Rizal",
    "email": "marygracesantos83@gmail.com",
    "phone": "09638833432",
    "github": "https://github.com/mgracesantos",
    "facebook": "https://www.facebook.com/gracesantos.97/",
    "linkedin": "",
    "about": [
        "I'm Grace, a Computer Engineering student who believes that success is built "
        "one small, steady step at a time, and that a good life is built the same way.",
        "I enjoy learning how software and hardware work together, from writing Python and "
        "Flask web apps to understanding networks and computer hardware. "
        "I'm working toward a career where I can keep learning and build things that matter.",
    ],
    "skills": ["Python Programming", "HTML & CSS", "Computer Networking",
               "Web Development", "Computer Hardware"],
    "education": [
        {"school": "Polytechnic University of the Philippines",
         "program": "Bachelor of Science in Computer Engineering (BSCpE)",
         "years": "Year level: 2-3"},
    ],
    "interests": [],
}


@app.context_processor
def inject_me():
    return {"me": ME}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------- Programming works ----------------
@app.route("/works", methods=["GET", "POST"])
def works():
    result = None
    original = ""
    if request.method == "POST":
        original = request.form.get("inputString", "")
        result = original.upper()
    return render_template("touppercase.html", result=result, original=original)


@app.route("/works/area/circle", methods=["GET", "POST"])
def acircle():
    result, error, radius = None, None, ""
    if request.method == "POST":
        radius = request.form.get("radius", "").strip()
        try:
            r = float(radius)
            if r < 0:
                raise ValueError
            result = round(math.pi * r * r, 4)
        except ValueError:
            error = "Enter a radius that is a number of 0 or more."
    return render_template("circle.html", result=result, error=error, radius=radius)


@app.route("/works/area/triangle", methods=["GET", "POST"])
def atriangle():
    result, error, base, height = None, None, "", ""
    if request.method == "POST":
        base = request.form.get("base", "").strip()
        height = request.form.get("height", "").strip()
        try:
            b, h = float(base), float(height)
            if b < 0 or h < 0:
                raise ValueError
            result = round(0.5 * b * h, 4)
        except ValueError:
            error = "Enter a base and a height that are numbers of 0 or more."
    return render_template("triangle.html", result=result, error=error, base=base, height=height)


# ---------------- Linked list ----------------
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert_head(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node
        self.size += 1

    def insert_tail(self, value):
        node = Node(value)
        if not self.head:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node
        self.size += 1

    def insert_at(self, index, value):
        if index <= 0 or not self.head:
            return self.insert_head(value)
        if index >= self.size:
            return self.insert_tail(value)
        cur = self.head
        for _ in range(index - 1):
            cur = cur.next
        node = Node(value)
        node.next = cur.next
        cur.next = node
        self.size += 1

    def delete(self, value):
        prev, cur = None, self.head
        while cur:
            if cur.value == value:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                self.size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def search(self, value):
        cur, i = self.head, 0
        while cur:
            if cur.value == value:
                return i
            cur, i = cur.next, i + 1
        return -1

    def reverse(self):
        prev, cur = None, self.head
        while cur:
            cur.next, prev, cur = prev, cur, cur.next
        self.head = prev

    def clear(self):
        self.head, self.size = None, 0

    def to_list(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out


linked = LinkedList()
for v in ("Python", "Flask", "Jinja"):
    linked.insert_tail(v)


@app.route("/works/linkedlist", methods=["GET", "POST"])
def linkedlist():
    found = None
    if request.method == "POST":
        action = request.form.get("action")
        value = request.form.get("value", "").strip()
        index = request.form.get("index", "").strip()
        needs_value = action in ("head", "tail", "at", "delete", "search")
        if needs_value and not value:
            flash("Type a value first.", "error")
        elif action == "head":
            linked.insert_head(value); flash(f"Added '{value}' at the head.", "ok")
        elif action == "tail":
            linked.insert_tail(value); flash(f"Added '{value}' at the tail.", "ok")
        elif action == "at":
            if index.lstrip("-").isdigit():
                linked.insert_at(int(index), value); flash(f"Inserted '{value}' at position {index}.", "ok")
            else:
                flash("Position must be a whole number.", "error")
        elif action == "delete":
            if linked.delete(value):
                flash(f"Deleted the first '{value}'.", "ok")
            else:
                flash(f"'{value}' is not in the list.", "error")
        elif action == "search":
            pos = linked.search(value)
            if pos >= 0:
                found = pos; flash(f"'{value}' found at position {pos}.", "ok")
            else:
                flash(f"'{value}' is not in the list.", "error")
        elif action == "reverse":
            linked.reverse(); flash("List reversed.", "ok")
        elif action == "clear":
            linked.clear(); flash("List cleared.", "ok")
        if found is None:
            return redirect(url_for("linkedlist"))
    return render_template("linkedlist.html", items=linked.to_list(), size=linked.size, found=found)


if __name__ == "__main__":
    app.run(debug=True)
