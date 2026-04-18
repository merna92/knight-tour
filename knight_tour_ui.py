import tkinter as tk
from tkinter import font as tkfont

# ══════════════════════════════════════
#  SETTINGS
# ══════════════════════════════════════
N        = 8
CELL     = 70
BOARD_PX = N * CELL

C_LIGHT  = "#F0D9B5"
C_DARK   = "#B58863"
C_BG     = "#1A1A2E"
C_PANEL  = "#16213E"
C_BTN    = "#0F3460"
C_BTN_H  = "#E94560"
C_WHITE  = "#FFFFFF"
C_GOLD   = "#F0A500"
C_KNIGHT = "#E94560"

# ══════════════════════════════════════
#  APP
# ══════════════════════════════════════
class KnightTourUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knight's Tour — UI | Mirna Mohamed El-Atafi")
        self.root.configure(bg=C_BG)
        self.root.resizable(False, False)
        self.knight_pos = None
        self._build_ui()
        self._draw_board()

    def _build_ui(self):
        title_f = tkfont.Font(family="Arial", size=16, weight="bold")
        lbl_f   = tkfont.Font(family="Arial", size=11)
        btn_f   = tkfont.Font(family="Arial", size=11, weight="bold")

        # title bar
        top = tk.Frame(self.root, bg=C_PANEL, pady=10)
        top.pack(fill="x")
        tk.Label(top, text="Knight's Tour", font=title_f,
                 bg=C_PANEL, fg=C_WHITE).pack()
        tk.Label(top, text="Warnsdorff's Heuristic Algorithm",
                 font=lbl_f, bg=C_PANEL, fg="#AAAAAA").pack()

        # main area
        main = tk.Frame(self.root, bg=C_BG)
        main.pack(padx=20, pady=10)

        # board
        self.canvas = tk.Canvas(main, width=BOARD_PX, height=BOARD_PX,
                                bg=C_BG, highlightthickness=2,
                                highlightbackground=C_BTN)
        self.canvas.pack(side="left", padx=(0, 20))
        self.canvas.bind("<Button-1>", self._on_click)

        # side panel
        panel = tk.Frame(main, bg=C_PANEL, padx=16, pady=16, width=200)
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

        self.v_pos   = info_row("الموقع:", "—")
        self.v_state = info_row("الحالة:", "انتظار")

        tk.Frame(panel, bg="#333355", height=1).pack(fill="x", pady=12)

        # legend
        tk.Label(panel, text="الدليل",
                 font=tkfont.Font(family="Arial", size=12, weight="bold"),
                 bg=C_PANEL, fg=C_GOLD).pack(anchor="w", pady=(0, 8))

        def legend(color, text):
            f = tk.Frame(panel, bg=C_PANEL)
            f.pack(fill="x", pady=2)
            tk.Label(f, bg=color, width=2, height=1).pack(side="left", padx=(0, 8))
            tk.Label(f, text=text, font=lbl_f, bg=C_PANEL, fg=C_WHITE).pack(side="left")

        legend(C_LIGHT,  "مربع فاتح")
        legend(C_DARK,   "مربع داكن")
        legend(C_KNIGHT, "موقع الحصان")

        tk.Frame(panel, bg="#333355", height=1).pack(fill="x", pady=12)

        # reset button
        b = tk.Button(panel, text="Reset", command=self._reset,
                      font=btn_f, bg=C_BTN, fg=C_WHITE, relief="flat",
                      activebackground=C_BTN_H, activeforeground=C_WHITE,
                      cursor="hand2", pady=8)
        b.pack(fill="x", pady=4)
        b.bind("<Enter>", lambda e: b.config(bg=C_BTN_H))
        b.bind("<Leave>", lambda e: b.config(bg=C_BTN))

        tk.Frame(panel, bg="#333355", height=1).pack(fill="x", pady=8)

        self.status_var = tk.StringVar(value="انقر على مربع لوضع الحصان")
        tk.Label(panel, textvariable=self.status_var, font=lbl_f,
                 bg=C_PANEL, fg=C_GOLD, wraplength=180,
                 justify="right").pack()

    def _draw_board(self):
        self.canvas.delete("all")
        self.rects = {}
        for r in range(N):
            for c in range(N):
                x1, y1 = c * CELL, r * CELL
                x2, y2 = x1 + CELL, y1 + CELL
                color = C_LIGHT if (r + c) % 2 == 0 else C_DARK
                rid = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                   fill=color, outline="")
                self.rects[(r, c)] = {"id": rid, "base": color}
        # labels
        for c in range(N):
            self.canvas.create_text(c*CELL + CELL//2, BOARD_PX - 8,
                                    text="abcdefgh"[c],
                                    fill="#888888", font=("Arial", 8))
        for r in range(N):
            self.canvas.create_text(6, r*CELL + CELL//2,
                                    text=str(N - r),
                                    fill="#888888", font=("Arial", 8))

    def _place_knight(self, r, c):
        if self.knight_pos:
            pr, pc = self.knight_pos
            self.canvas.itemconfig(self.rects[(pr,pc)]["id"],
                                   fill=self.rects[(pr,pc)]["base"])
        self.canvas.itemconfig(self.rects[(r,c)]["id"], fill=C_KNIGHT)
        self.canvas.delete("knight")
        x = c * CELL + CELL // 2
        y = r * CELL + CELL // 2
        self.canvas.create_text(x, y, text="♞", fill=C_WHITE,
                                font=("Arial", 28), tags="knight")
        self.knight_pos = (r, c)
        self.v_pos.set(f"{'abcdefgh'[c]}{N - r}")
        self.v_state.set("موضوع")
        self.status_var.set("تم وضع الحصان")

    def _on_click(self, event):
        c = event.x // CELL
        r = event.y // CELL
        if 0 <= r < N and 0 <= c < N:
            self._place_knight(r, c)

    def _reset(self):
        self.knight_pos = None
        self.v_pos.set("—")
        self.v_state.set("انتظار")
        self.status_var.set("انقر على مربع لوضع الحصان")
        self._draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    KnightTourUI(root)
    root.mainloop()
