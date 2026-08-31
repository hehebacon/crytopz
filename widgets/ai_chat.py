import customtkinter as ctk


class AIChat(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("crytopz AI")
        self.geometry("400x540")

        self.configure(
            fg_color="#111318"
        )

        self.build()


    def build(self):

        # Header

        header = ctk.CTkFrame(
            self,
            height=55,
            corner_radius=14
        )

        header.pack(
            fill="x",
            padx=8,
            pady=8
        )

        header.pack_propagate(False)


        title = ctk.CTkLabel(
            header,
            text="✦  crytopz AI",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.pack(
            side="left",
            padx=15
        )


        online = ctk.CTkLabel(
            header,
            text="● Demo",
            text_color="#4ade80",
            font=ctk.CTkFont(size=11)
        )

        online.pack(
            side="left"
        )


        close = ctk.CTkButton(
            header,
            text="×",
            width=32,
            height=32,
            fg_color="transparent",
            hover_color="#27272A",
            command=self.withdraw
        )

        close.pack(
            side="right",
            padx=8
        )


        # Chat

        self.chat = ctk.CTkTextbox(
            self,
            corner_radius=12,
            border_width=0,
            wrap="word"
        )

        self.chat.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

        self.chat.insert(
            "end",
            "crytopz AI\n\n"
            "Xin chào 👋\n"
            "Đây là AI demo của crytopz.\n\n"
        )

        self.chat.configure(
            state="disabled"
        )


        # Input

        bottom = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        bottom.pack(
            fill="x",
            padx=8,
            pady=8
        )


        self.entry = ctk.CTkEntry(
            bottom,
            height=42,
            corner_radius=12,
            placeholder_text="Ask crytopz AI..."
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 6)
        )


        ctk.CTkButton(
            bottom,
            text="➤",
            width=48,
            height=42,
            corner_radius=12,
            command=self.send
        ).pack(
            side="right"
        )


    def send(self):

        text = self.entry.get().strip()

        if not text:
            return


        self.entry.delete(
            0,
            "end"
        )


        self.chat.configure(
            state="normal"
        )

        self.chat.insert(
            "end",
            f"You\n{text}\n\n"
            "crytopz AI\n"
            "AI backend chưa được kết nối.\n\n"
        )

        self.chat.configure(
            state="disabled"
        )

        self.chat.see("end")