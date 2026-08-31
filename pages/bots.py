import customtkinter as ctk

from tkinter import filedialog
from tkinter import messagebox

from pathlib import Path
import json
import zipfile


class BotLibraryPage(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        app
    ):

        super().__init__(
            parent,
            corner_radius=0
        )

        self.app = app

        self.selected = None

        self.build_ui()

        self.refresh()


    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        ctk.CTkLabel(
            header,
            text="Bot Library",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            header,
            text="Reload",
            width=90,
            command=self.reload
        ).pack(
            side="right",
            padx=5
        )

        ctk.CTkButton(
            header,
            text="Import Bot",
            width=110,
            command=self.import_bot
        ).pack(
            side="right",
            padx=5
        )


        # -------------------------------------------------
        # BODY
        # -------------------------------------------------

        body = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        body.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=5
        )


        # -------------------------------------------------
        # LEFT
        # -------------------------------------------------

        self.bot_list = ctk.CTkScrollableFrame(
            body,
            width=300
        )

        self.bot_list.pack(
            side="left",
            fill="both",
            padx=(0, 12)
        )


        # -------------------------------------------------
        # RIGHT
        # -------------------------------------------------

        self.detail = ctk.CTkFrame(
            body,
            corner_radius=12
        )

        self.detail.pack(
            side="left",
            fill="both",
            expand=True
        )


        self.title_label = ctk.CTkLabel(
            self.detail,
            text="Select a bot",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        self.title_label.pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )


        self.info_label = ctk.CTkLabel(
            self.detail,
            text="",
            text_color="gray"
        )

        self.info_label.pack(
            anchor="w",
            padx=25
        )


        self.description_label = ctk.CTkLabel(
            self.detail,
            text="",
            anchor="w",
            justify="left",
            wraplength=700
        )

        self.description_label.pack(
            fill="x",
            padx=25,
            pady=15
        )


        # -------------------------------------------------
        # CONTROLS
        # -------------------------------------------------

        controls = ctk.CTkFrame(
            self.detail,
            fg_color="transparent"
        )

        controls.pack(
            fill="x",
            padx=25,
            pady=5
        )


        self.run_button = ctk.CTkButton(
            controls,
            text="Start",
            width=100,
            command=self.toggle_running
        )

        self.run_button.pack(
            side="left",
            padx=(0, 5)
        )


        self.reload_button = ctk.CTkButton(
            controls,
            text="Reload Bot",
            width=100,
            command=self.reload_selected
        )

        self.reload_button.pack(
            side="left",
            padx=5
        )


        self.unload_button = ctk.CTkButton(
            controls,
            text="Unload",
            width=100,
            command=self.unload_selected
        )

        self.unload_button.pack(
            side="left",
            padx=5
        )


        # -------------------------------------------------
        # CODE
        # -------------------------------------------------

        ctk.CTkLabel(
            self.detail,
            text="Bot Code",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 5)
        )


        self.editor = ctk.CTkTextbox(
            self.detail,
            font=("Consolas", 13)
        )

        self.editor.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=5
        )


        ctk.CTkButton(
            self.detail,
            text="Save Code",
            command=self.save_code
        ).pack(
            anchor="e",
            padx=25,
            pady=(5, 20)
        )


    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        for widget in self.bot_list.winfo_children():

            widget.destroy()


        manager = self.app.bot_manager

        if manager is None:

            return


        try:

            bots = manager.list_bots()

        except Exception as error:

            print(
                "[Bots UI] Failed to list bots:",
                error
            )

            return


        for bot in bots:

            self.create_card(
                bot
            )


        if self.selected:

            if manager.get_bot(
                self.selected
            ):

                self.select_bot(
                    self.selected
                )


    # =====================================================
    # CARD
    # =====================================================

    def create_card(
        self,
        bot
    ):

        frame = ctk.CTkFrame(
            self.bot_list,
            corner_radius=10
        )

        frame.pack(
            fill="x",
            pady=5
        )


        name = ctk.CTkLabel(
            frame,
            text=bot["name"],
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        name.pack(
            anchor="w",
            padx=12,
            pady=(10, 2)
        )


        manager = self.app.bot_manager

        try:

            running = manager.is_running(
                bot["id"]
            )

        except Exception:

            running = False


        if running:

            status = "● RUNNING"

            status_color = "#4ade80"

        else:

            status = "● STOPPED"

            status_color = "#f87171"


        label = ctk.CTkLabel(
            frame,
            text=status,
            text_color=status_color
        )

        label.pack(
            anchor="w",
            padx=12,
            pady=(0, 10)
        )


        for widget in (
            frame,
            name,
            label
        ):

            widget.bind(
                "<Button-1>",
                lambda event,
                bot_id=bot["id"]:
                    self.select_bot(bot_id)
            )


    # =====================================================
    # SELECT
    # =====================================================

    def select_bot(
        self,
        bot_id
    ):

        manager = self.app.bot_manager

        bot = manager.get_bot(
            bot_id
        )

        if not bot:

            return


        self.selected = bot["id"]


        manifest = bot["manifest"]


        self.title_label.configure(
            text=manifest.name
        )


        self.info_label.configure(
            text=(
                f"ID: {manifest.id}    "
                f"v{manifest.version}    "
                f"API {manifest.api_version}    "
                f"{manifest.runtime}"
            )
        )


        self.description_label.configure(
            text=(
                getattr(
                    manifest,
                    "description",
                    ""
                )
                or "No description."
            )
        )


        # -------------------------------------------------
        # CODE
        # -------------------------------------------------

        self.editor.delete(
            "1.0",
            "end"
        )


        try:

            entrypoint = (
                bot["path"]
                / manifest.entrypoint
            )

            if entrypoint.exists():

                code = entrypoint.read_text(
                    encoding="utf-8"
                )

                self.editor.insert(
                    "1.0",
                    code
                )

        except Exception as error:

            print(
                "[Bots UI] "
                f"Cannot read code: {error}"
            )


        self.update_controls()


    # =====================================================
    # CONTROLS
    # =====================================================

    def update_controls(self):

        if not self.selected:

            return


        manager = self.app.bot_manager

        bot = manager.get_bot(
            self.selected
        )

        if not bot:

            return


        try:

            running = manager.is_running(
                self.selected
            )

        except Exception:

            running = False


        if running:

            self.run_button.configure(
                text="Stop"
            )

        else:

            self.run_button.configure(
                text="Start"
            )


    # =====================================================
    # START / STOP
    # =====================================================

    def toggle_running(self):

        if not self.selected:

            return


        manager = self.app.bot_manager


        try:

            if manager.is_running(
                self.selected
            ):

                success = manager.stop_bot(
                    self.selected
                )

            else:

                success = manager.start_bot(
                    self.selected
                )


        except Exception as error:

            messagebox.showerror(
                "Bot Error",
                str(error)
            )

            return


        if not success:

            messagebox.showerror(
                "Bot",
                "Could not start or stop bot."
            )

            return


        self.refresh()

        self.select_bot(
            self.selected
        )


    # =====================================================
    # UNLOAD
    # =====================================================

    def unload_selected(self):

        if not self.selected:

            return


        manager = self.app.bot_manager


        try:

            success = manager.unload_bot(
                self.selected
            )

        except Exception as error:

            messagebox.showerror(
                "Bot Error",
                str(error)
            )

            return


        if success:

            self.refresh()

            self.select_bot(
                self.selected
            )


    # =====================================================
    # RELOAD
    # =====================================================

    def reload(self):

        manager = self.app.bot_manager

        if manager is None:

            return


        try:

            manager.reload()

        except Exception as error:

            messagebox.showerror(
                "Reload Error",
                str(error)
            )

            return


        self.refresh()


    # =====================================================
    # RELOAD SELECTED
    # =====================================================

    def reload_selected(self):

        if not self.selected:

            return


        manager = self.app.bot_manager


        try:

            success = manager.reload_bot(
                self.selected
            )

        except Exception as error:

            messagebox.showerror(
                "Bot Error",
                str(error)
            )

            return


        if not success:

            messagebox.showwarning(
                "Bot",
                "Bot no longer exists."
            )

            self.selected = None

            self.clear_detail()

            self.refresh()

            return


        self.refresh()

        self.select_bot(
            self.selected
        )


    # =====================================================
    # SAVE CODE
    # =====================================================

    def save_code(self):

        if not self.selected:

            messagebox.showwarning(
                "Bot",
                "Select a bot first."
            )

            return


        manager = self.app.bot_manager

        bot = manager.get_bot(
            self.selected
        )

        if not bot:

            return


        manifest = bot["manifest"]


        code = self.editor.get(
            "1.0",
            "end-1c"
        )


        try:

            entrypoint = (
                bot["path"]
                / manifest.entrypoint
            )

            entrypoint.write_text(
                code,
                encoding="utf-8"
            )


            # Reload instance so new code is used.

            manager.unload_bot(
                self.selected
            )


            messagebox.showinfo(
                "Bot",
                "Code saved."
            )


        except Exception as error:

            messagebox.showerror(
                "Bot",
                f"Could not save code:\n{error}"
            )


    # =====================================================
    # IMPORT
    # =====================================================

    def import_bot(self):

        path = filedialog.askopenfilename(
            title="Import Crytopz Bot",
            filetypes=[
                (
                    "Crytopz Bot",
                    "*.zip"
                )
            ]
        )


        if not path:

            return


        source = Path(
            path
        )


        try:

            with zipfile.ZipFile(
                source,
                "r"
            ) as archive:

                names = archive.namelist()


                # -------------------------------------------------
                # Find manifest
                # -------------------------------------------------

                manifest_name = None

                for name in names:

                    if name.endswith(
                        "manifest.json"
                    ):

                        manifest_name = name

                        break


                if manifest_name is None:

                    raise ValueError(
                        "manifest.json not found."
                    )


                manifest = json.loads(
                    archive.read(
                        manifest_name
                    ).decode(
                        "utf-8"
                    )
                )


                required = [
                    "id",
                    "name",
                    "version",
                    "api_version",
                    "runtime",
                    "entrypoint"
                ]


                for field in required:

                    if field not in manifest:

                        raise ValueError(
                            f"Missing manifest field: "
                            f"{field}"
                        )


                bot_id = manifest["id"]


                # -------------------------------------------------
                # Destination
                # -------------------------------------------------

                destination = (
                    self.app.bot_manager.bots_dir
                    / bot_id
                )


                if destination.exists():

                    answer = messagebox.askyesno(
                        "Bot already exists",
                        f'"{bot_id}" already exists.\n'
                        "Replace it?"
                    )

                    if not answer:

                        return


                destination.mkdir(
                    parents=True,
                    exist_ok=True
                )


                # -------------------------------------------------
                # Extract safely
                # -------------------------------------------------

                for member in archive.infolist():

                    member_path = (
                        destination
                        / member.filename
                    ).resolve()


                    if not str(
                        member_path
                    ).startswith(
                        str(
                            destination.resolve()
                        )
                    ):

                        raise ValueError(
                            "Unsafe ZIP path."
                        )


                    archive.extract(
                        member,
                        destination
                    )


            # -------------------------------------------------
            # Reload registry
            # -------------------------------------------------

            self.app.bot_manager.reload()

            self.selected = bot_id

            self.refresh()

            self.select_bot(
                bot_id
            )


            messagebox.showinfo(
                "Import",
                f'Imported "{manifest["name"]}".'
            )


        except Exception as error:

            messagebox.showerror(
                "Import failed",
                str(error)
            )


    # =====================================================
    # CLEAR
    # =====================================================

    def clear_detail(self):

        self.title_label.configure(
            text="Select a bot"
        )

        self.info_label.configure(
            text=""
        )

        self.description_label.configure(
            text=""
        )

        self.editor.delete(
            "1.0",
            "end"
        )


# =========================================================
# COMPATIBILITY
# =========================================================

BotPage = BotLibraryPage