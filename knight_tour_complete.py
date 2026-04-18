import tkinter as tk
from tkinter import font as tkfont

# ══════════════════════════════════════
#  SETTINGS
# ══════════════════════════════════════
N        = 8
CELL     = 70
BOARD_PX = N * CELL
DELAY    = 300

C_LIGHT   = "#F0D9B5"
C_DARK    = "#B58863"
C_VISITED = "#A8D8A8"
C_KNIGHT  = "#E94560"
C_BG      = "#1A1A2E"
C_PANEL   = "#16213E"
C_BTN     = "#0F3460"
C_BTN_H   = "#E94560"
C_WHITE   = "#FFFFFF"
C_GOLD    = "#F0A500"
C_NUMBER  = "#2C3E50"

# ══════════════════════════════════════
#  WARNSDORFF'S ALGORITHM
# ══════════════════════════════════════

# حركات الحصان الـ 8 على شكل L
MOVES = [
    (-2, -1), (-2, +1),
    (-1, -2), (-1, +2),
    (+1, -2), (+1, +2),
    (+2, -1), (+2, +1),
]

def is_valid(board, r, c):
    """
    بتتحقق إن الحركة صح:
    1. المربع جوه الرقعة
    2. المربع لسه مش متزارتش (-1)
    """
    return (
        0 <= r < N and
        0 <= c < N and
        board[r][c] == -1
    )

def count_moves(board, r, c):
    """
    قلب خوارزمية Warnsdorff:
    بتعد كام حركة ممكنة من المربع ده
    عشان نختار الأضيق
    """
    return sum(1 for dr, dc in MOVES if is_valid(board, r + dr, c + dc))

def solve_knight(start_r, start_c):
    """
    بتحل مشكلة رحلة الحصان باستخدام Warnsdorff:
    - بتبدأ من نقطة البداية
    - في كل خطوة بتروح للمربع اللي عنده أقل حركات
    - بترجع الـ path كامل أو None لو مفيش حل
    """
    # إنشاء الرقعة — -1 معناها لسه مش متزارتش
    board = [[-1] * N for _ in range(N)]
    path  = []

    r, c = start_r, start_c
    board[r][c] = 0
    path.append((r, c))

    for step in range(1, N * N):
        # الحركات الممكنة من الموقع الحالي
        neighbors = [
            (r + dr, c + dc)
            for dr, dc in MOVES
            if is_valid(board, r + dr, c + dc)
        ]

        # لو مفيش حركات — مفيش حل
        if not neighbors:
            return None, []

        # Warnsdorff: اختار المربع اللي عنده أقل حركات
        r, c = min(neighbors, key=lambda pos: count_moves(board, *pos))

        board[r][c] = step
        path.append((r, c))

    return board, path

# ══════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════
class KnightTourApp:
    def __init__(self, root):
        self.root      = root
        self.root.title("Knight's Tour — AI Project | Mirna Mohamed El-Atafi")
        self.root.configure(bg=C_BG)
        self.root.resizable(False, False)

        self.board     = [[-1] * N for _ in range(N)]
        self.path      = []
        self.step_idx  = 0
        self.running   = False
        self.start_r   = 0
        self.start_c   = 0
        self.selecting = True

        self._build_ui()
        self._draw_board()
        self._set_status("انقر على أي مربع لتحديد نقطة البداية", C_GOLD)

    # ─── BUILD UI ───────────────────────────────
    def _build_ui(self):
        title_f = tkfont.Font(family="Arial", size=16, weight="bold")
        lbl_f   = tkfont.Font(family="Arial", size=11)
        btn_f   = tkfont.Font(family="Arial", size=11, weight="bold")

        # شريط العنوان
        top = tk.Frame(self.root, bg=C_PANEL, pady=10)
        top.pack(fill="x")
        tk.Label(top, text="♞  Knight's Tour", font=title_f,
                 bg=C_PANEL, fg=C_WHITE).pack()
        tk.Label(top, text="Warnsdorff's Heuristic Algorithm",
                 font=lbl_f, bg=C_PANEL, fg="#AAAAAA").pack()

        # المنطقة الرئيسية
        main = tk.Frame(self.root, bg=C_BG)
        main.pack(padx=20, pady=10)

        # رقعة الشطرنج
        self.canvas = tk.Canvas(main, width=BOARD_PX, height=BOARD_PX,
                                bg=C_BG, highlightthickness=2,
                                highlightbackground=C_BTN)
        self.canvas.pack(side="left", padx=(0, 20))
        self.canvas.bind("<Button-1>", self._on_click)

        # البانيل الجانبي
        panel = tk.Frame(main, bg=C_PANEL, padx=16, pady=16, width=210)
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)

        tk.Label(panel, text="المعلومات",
                 font=tkfont.Font(family="Arial", size=12, weight="bold"),
                 bg=C_PANEL, fg=C_GOLD).pack(anchor="w", pady=(0, 12))

        def info_row(label, default):
            f = tk.Frame(panel, bg=C_PANEL)
            f.pack(fill="x", pady=3)
            tk.Label(f, text=label, font=lbl_f, bg=C_PANEL,
                     fg="#AAAAAA").pack(side="left")
            v = tk.StringVar(value=default)
            tk.Label(f, textvariable=v,
                     font=tkfont.Font(family="Arial", size=11, weight="bold"),
                     bg=C_PANEL, fg=C_WHITE).pack(side="right")
            return v

        self.v_step  = info_row("الخطوة:", "0 / 64")
        self.v_start = info_row("البداية:", "—")
        self.v_state = info_row("الحالة:", "اختيار")

        tk.Frame(panel, bg="#333355", height=1).pack(fill="x", pady=12)

        # الدليل
        tk.Label(panel, text="الدليل",
                 font=tkfont.Font(family="Arial", size=12, weight="bold"),
                 bg=C_PANEL, fg=C_GOLD).pack(anchor="w", pady=(0, 8))

        def legend(color, text):
            f = tk.Frame(panel, bg=C_PANEL)
            f.pack(fill="x", pady=2)
            tk.Label(f, bg=color, width=2, height=1).pack(side="left", padx=(0, 8))
            tk.Label(f, text=text, font=lbl_f, bg=C_PANEL, fg=C_WHITE).pack(side="left")

        legend(C_KNIGHT,  "موقع الحصان الحالي")
        legend(C_VISITED, "مربع تم زيارته")
        legend(C_LIGHT,   "مربع فاتح")
        legend(C_DARK,    "مربع داكن")

        tk.Frame(panel, bg="#333355", height=1).pack(fill="x", pady=12)

        # سرعة الحركة
        tk.Label(panel, text="سرعة الحركة", font=lbl_f,
                 bg=C_PANEL, fg="#AAAAAA").pack(anchor="w")
        self.speed = tk.IntVar(value=DELAY)
        tk.Scale(panel, from_=50, to=800, orient="horizontal",
                 variable=self.speed, bg=C_PANEL, fg=C_WHITE,
                 troughcolor=C_BTN, highlightthickness=0,
                 showvalue=False).pack(fill="x", pady=(4, 12))

        # الأزرار
        def btn(text, cmd):
            b = tk.Button(panel, text=text, command=cmd, font=btn_f,
                          bg=C_BTN, fg=C_WHITE, relief="flat",
                          activebackground=C_BTN_H, activeforeground=C_WHITE,
                          cursor="hand2", pady=8)
            b.pack(fill="x", pady=4)
            b.bind("<Enter>", lambda e: b.config(bg=C_BTN_H))
            b.bind("<Leave>", lambda e: b.config(bg=C_BTN))
            return b

        self.btn_solve = btn("▶  ابدأ الحل", self._start_solve)
        self.btn_pause = btn("⏸  إيقاف مؤقت", self._pause)
        self.btn_reset = btn("↺  إعادة تعيين", self._reset)

        # شريط الحالة
        tk.Frame(panel, bg="#333355", height=1).pack(fill="x", pady=8)
        self.status_var = tk.StringVar()
        self.status_lbl = tk.Label(panel, textvariable=self.status_var,
                                   font=lbl_f, bg=C_PANEL, fg=C_GOLD,
                                   wraplength=185, justify="right")
        self.status_lbl.pack(fill="x")

    # ─── DRAW BOARD ────────────────────────────
    def _draw_board(self):
        self.canvas.delete("all")
        self.rects = {}

        for r in range(N):
            for c in range(N):
                x1, y1 = c * CELL, r * CELL
                x2, y2 = x1 + CELL, y1 + CELL
                color = C_LIGHT if (r + c) % 2 == 0 else C_DARK
                rid = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline=""
                )
                self.rects[(r, c)] = {"id": rid, "base": color}

        # تسميات الأعمدة والصفوف
        for c in range(N):
            self.canvas.create_text(c * CELL + CELL // 2, BOARD_PX - 8,
                                    text="abcdefgh"[c],
                                    fill="#888888", font=("Arial", 8))
        for r in range(N):
            self.canvas.create_text(6, r * CELL + CELL // 2,
                                    text=str(N - r),
                                    fill="#888888", font=("Arial", 8))

    def _color_cell(self, r, c, color, number=None):
        self.canvas.itemconfig(self.rects[(r, c)]["id"], fill=color)
        if number is not None:
            x1, y1 = c * CELL, r * CELL
            self.canvas.create_text(
                x1 + CELL // 2, y1 + CELL // 2,
                text=str(number), fill=C_NUMBER,
                font=("Arial", 13, "bold"),
                tags=f"num_{r}_{c}"
            )

    def _draw_knight(self, r, c):
        self.canvas.delete("knight_icon")
        x = c * CELL + CELL // 2
        y = r * CELL + CELL // 2
        self.canvas.create_text(x, y, text="♞", fill=C_WHITE,
                                font=("Arial", 28), tags="knight_icon")

    # ─── EVENTS ────────────────────────────────
    def _on_click(self, event):
        if not self.selecting:
            return
        c = event.x // CELL
        r = event.y // CELL
        if 0 <= r < N and 0 <= c < N:
            self.start_r, self.start_c = r, c
            self.v_start.set(f"{'abcdefgh'[c]}{N - r}")
            self._draw_board()
            self._color_cell(r, c, C_KNIGHT)
            self._draw_knight(r, c)
            self._set_status(
                f"البداية: {'abcdefgh'[c]}{N - r}\nاضغط 'ابدأ الحل'", C_GOLD
            )

    def _start_solve(self):
        if self.running:
            return
        self.selecting = False

        # تشغيل الخوارزمية
        board, path = solve_knight(self.start_r, self.start_c)

        if not path:
            self._set_status("❌ لا يوجد حل من هذه النقطة!", "#FF6B6B")
            return

        self.path     = path
        self.step_idx = 0
        self.running  = True
        self.v_state.set("يعمل")
        self._set_status("الحصان يحل اللغز...", "#88FF88")
        self._animate()

    def _animate(self):
        if not self.running:
            return
        if self.step_idx >= len(self.path):
            self.running = False
            self.v_state.set("مكتمل ✓")
            self._set_status(f"✅ تم! زيارة {N*N} مربع بنجاح", "#88FF88")
            return

        r, c = self.path[self.step_idx]

        # لون المربع السابق كمزار
        if self.step_idx > 0:
            pr, pc = self.path[self.step_idx - 1]
            self._color_cell(pr, pc, C_VISITED, self.step_idx)

        # لون المربع الحالي كحصان
        self._color_cell(r, c, C_KNIGHT)
        self._draw_knight(r, c)

        self.v_step.set(f"{self.step_idx + 1} / {N * N}")
        self.step_idx += 1

        self.root.after(max(50, self.speed.get()), self._animate)

    def _pause(self):
        if self.running:
            self.running = False
            self.v_state.set("متوقف")
            self._set_status("⏸ متوقف\nاضغط 'ابدأ الحل' للاستمرار", C_GOLD)
        else:
            if self.path and self.step_idx < len(self.path):
                self.running = True
                self.v_state.set("يعمل")
                self._set_status("الحصان يحل اللغز...", "#88FF88")
                self._animate()

    def _reset(self):
        self.running   = False
        self.selecting = True
        self.path      = []
        self.step_idx  = 0
        self.v_step.set("0 / 64")
        self.v_start.set("—")
        self.v_state.set("اختيار")
        self._draw_board()
        self._set_status("انقر على أي مربع لتحديد نقطة البداية", C_GOLD)

    def _set_status(self, msg, color=C_WHITE):
        self.status_var.set(msg)
        self.status_lbl.config(fg=color)

# ══════════════════════════════════════
#  RUN
# ══════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    KnightTourApp(root)
    root.mainloop()
