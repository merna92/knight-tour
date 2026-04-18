# ♞ Knight's Tour Problem
### Artificial Intelligence Project — Warnsdorff's Heuristic Algorithm

---

## 👩‍💻 Student
| Name | 
|------|
| Mirna Mohamed El-Atafi |

---

## 📌 Project Description
The **Knight's Tour** is a classic Artificial Intelligence problem where a chess knight must visit every square on an N×N chessboard **exactly once**, following the standard L-shaped movement rules.

This project implements an intelligent AI agent that solves the Knight's Tour problem efficiently using **Warnsdorff's Heuristic Algorithm**.

---

## 🧠 Algorithm Used — Warnsdorff's Rule
At every step, the knight moves to the square that has the **fewest onward moves** available.

**Why this works:**
- Always go to the most "trapped" neighbor first
- Avoids getting stuck later in the tour
- Solves 8×8 board instantly without backtracking

```
Step 1: Get all valid moves from current position
Step 2: For each neighbor, count how many moves it has
Step 3: Move to the neighbor with the MINIMUM count
Step 4: Repeat until all 64 squares are visited
```

---

## 🧩 PEAS
| Component | Description |
|-----------|-------------|
| **Performance** | Visit all N×N squares exactly once with no repetition |
| **Environment** | N×N chessboard (default 8×8) |
| **Actuators** | Move the knight to one of up to 8 L-shaped positions |
| **Sensors** | Current position, visited squares, onward move counts |

---

## 🔄 ODESA
| Property | Type | Reason |
|----------|------|--------|
| Observable | Fully Observable | Agent sees the entire board at all times |
| Deterministic | Deterministic | Same move always leads to same result |
| Episodic | Sequential | Each move depends on all previous moves |
| Static | Static | Board doesn't change while agent thinks |
| Actions | Discrete / Single Agent | One AI agent, max 8 moves per step |

---

## 🤖 Agent Type
**Goal-Based Agent**
- Clear goal: visit all 64 squares exactly once
- Uses Warnsdorff's heuristic to decide the best next move
- Plans ahead rather than reacting randomly

---

## 🖥️ Project Structure
```
knight-tour/
│
├── knight_tour_ui.py        # Main UI file (tkinter)
├── README.md                # This file
└── proposal/
    └── Knight_Tour_Proposal.pdf
```

---

## ▶️ How to Run
**Requirements:** Python 3.x (tkinter is built-in)

```bash
python knight_tour_ui.py
```

**Steps:**
1. Click any square to place the knight
2. Press **Start** to watch the AI solve the tour
3. Use the speed slider to control animation speed
4. Press **Reset** to start over

---

## 📚 External Resources
- [Knight's Tour — Wikipedia](https://en.wikipedia.org/wiki/Knight%27s_tour)
- [Warnsdorff's Rule](https://en.wikipedia.org/wiki/Knight%27s_tour#Warnsdorff's_rule)
- Python `tkinter` library (built-in)
- `arabic_reshaper` library
- `python-bidi` library
- `reportlab` library

---

## 🏫 Faculty
Faculty of Computers and Information — Artificial Intelligence Course
