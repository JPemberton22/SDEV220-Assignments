"""
Final_Project_With_GUI.py

A Dangerous Goods checking system with: Four classes, Collections, GUI interface (tkinter), and Input validation for label, inspection,
and pictogram number

A box is considered Dangerous Goods if any of the following is true: Label is IDG, ADG, or ICE, Inspection sticker is YES, A hazard 
pictogram number is provided
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox


# Class 1
class Box:
    # Simple data container for a shipment box
    def __init__(self, label: str, inspection: bool, pictograms: list[str]):
        self.label = label
        self.inspection = inspection
        self.pictograms = pictograms  

    def __repr__(self) -> str:
        return f"Box(label={self.label!r}, inspection={self.inspection!r}, pictograms={self.pictograms!r})"


# Class 2
class LabelChecker:
    VALID_LABELS = ["IDG", "ADG", "ICE", "NONE"]

    def normalize(self, label: str) -> str:
        return (label or "").strip().upper()

    def is_valid(self, label: str) -> bool:
        return self.normalize(label) in self.VALID_LABELS

    def validate_or_raise(self, label: str) -> str:
        label_norm = self.normalize(label)
        if label_norm not in self.VALID_LABELS:
            raise ValueError(
                "Unaccepted input for label.\n\n"
                "Instructions:\n"
                "Choose one label from: IDG, ADG, ICE, NONE."
            )
        return label_norm

    def is_dg_label(self, label: str) -> bool:
        label_norm = self.normalize(label)
        return label_norm in ("IDG", "ADG", "ICE")


# Class 3
class InspectionChecker:
    # Validates yes/no inspection input (GUI uses radio buttons, but we still validate)

    def validate_or_raise(self, inspection_value: str) -> bool:
        val = (inspection_value or "").strip().lower()
        if val not in ("yes", "no"):
            raise ValueError(
                "Unaccepted input for inspection sticker.\n\n"
                "Instructions:\n"
                "Select YES or NO for the inspection sticker."
            )
        return val == "yes"


# Class 4
class PictogramChecker:
    PICTOGRAMS = {
        "2.2": "Non-flammable non-toxic gas",
        "6.1": "Toxic",
        "6.2": "Infectious substance",
        "7.1": "RADIOACTIVE I White",
        "7.2": "RADIOACTIVE II Yellow",
        "7.3": "RADIOACTIVE III Yellow",
        "7.4": "Criticality Safety Index",
        "9.1": "Class 9",
        "9.2": "Lithium Batteries or Sodium Ion Batteries",
        "1.4": "Explosive",
        "2.1": "Flammable gas",
        "3.1": "Flammable liquid",
        "4.1": "Flammable solid",
        "4.2": "Spontaneously combustible",
        "4.3": "Dangerous when wet",
        "5.1": "Oxidizer",
        "5.2": "Organic Peroxide",
        "8.1": "CORROSIVE",
    }

    def normalize(self, number: str) -> str:
        return (number or "").strip()

    def is_valid(self, number: str) -> bool:
        return self.normalize(number) in self.PICTOGRAMS

    def get_name(self, number: str) -> str:
        return self.PICTOGRAMS.get(self.normalize(number), "Unknown pictogram")

    def validate_or_raise(self, has_pictogram: str, pictogram_number: str) -> list[str]:
        
        has_val = (has_pictogram or "").strip().lower()
        if has_val not in ("yes", "no"):
            raise ValueError(
                "Unaccepted input for pictogram presence.\n\n"
                "Instructions:\n"
                "Select YES or NO for whether a hazard pictogram is on the box."
            )

        if has_val == "no":
            return []

        number_norm = self.normalize(pictogram_number)
        if number_norm not in self.PICTOGRAMS:
            allowed = ", ".join(self.PICTOGRAMS.keys())
            raise ValueError(
                "Unaccepted input for pictogram number.\n\n"
                "Instructions:\n"
                "If you selected YES, enter ONE of the approved pictogram numbers:\n"
                f"{allowed}"
            )
        return [number_norm]


# System
class DangerousGoodsSystem:
    def __init__(self):
        self.label_checker = LabelChecker()
        self.inspection_checker = InspectionChecker()
        self.pictogram_checker = PictogramChecker()

    def evaluate(self, label: str, inspection_value: str, has_pictogram: str, pictogram_number: str) -> dict:
       
        label_norm = self.label_checker.validate_or_raise(label)
        inspection_bool = self.inspection_checker.validate_or_raise(inspection_value)
        pictograms = self.pictogram_checker.validate_or_raise(has_pictogram, pictogram_number)

        box = Box(label=label_norm, inspection=inspection_bool, pictograms=pictograms)

        reasons = []
        if self.label_checker.is_dg_label(label_norm):
            reasons.append(f"DG label present: {label_norm}")
        if inspection_bool:
            reasons.append("Inspection sticker: YES")
        if pictograms:
            num = pictograms[0]
            reasons.append(f"Hazard pictogram: {num} - {self.pictogram_checker.get_name(num)}")

        dangerous = len(reasons) > 0

        if pictograms:
            num = pictograms[0]
            pict_display = f"{num} - {self.pictogram_checker.get_name(num)}"
        else:
            pict_display = "None"

        return {
            "box": box,
            "dangerous_goods": dangerous,
            "dg_reasons": reasons,
            "pictogram_display": pict_display,
        }


# GUI
class DangerousGoodsGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Dangerous Goods Checker")
        self.geometry("760x540")
        self.resizable(False, False)

        self.system = DangerousGoodsSystem()

        # Variables
        self.label_var = tk.StringVar(value="NONE")
        self.inspection_var = tk.StringVar(value="no")  
        self.has_pictogram_var = tk.StringVar(value="no")  
        self.pictogram_number_var = tk.StringVar(value="")

        # UI
        self._build_ui()
        self._toggle_pictogram_entry()

    def _build_ui(self):
        pad = {"padx": 12, "pady": 8}

        header = ttk.Label(self, text="Dangerous Goods Check-In", font=("Segoe UI", 16, "bold"))
        header.pack(pady=12)

        container = ttk.Frame(self)
        container.pack(fill="x", **pad)

        # Label selection
        lf_label = ttk.Labelframe(container, text="Packaging Label", padding=12)
        lf_label.pack(fill="x", **pad)

        ttk.Label(lf_label, text="Select the label on the box:").grid(row=0, column=0, sticky="w")
        label_combo = ttk.Combobox(
            lf_label,
            textvariable=self.label_var,
            values=self.system.label_checker.VALID_LABELS,
            state="readonly",
            width=18,
        )
        label_combo.grid(row=0, column=1, sticky="w", padx=10)
        ttk.Label(lf_label, text="(Valid: IDG, ADG, ICE, NONE)").grid(row=0, column=2, sticky="w")

        # Inspection
        lf_insp = ttk.Labelframe(container, text="Inspection Sticker", padding=12)
        lf_insp.pack(fill="x", **pad)

        ttk.Label(lf_insp, text="Is there an inspection sticker?").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(lf_insp, text="Yes", variable=self.inspection_var, value="yes").grid(row=0, column=1, sticky="w", padx=10)
        ttk.Radiobutton(lf_insp, text="No", variable=self.inspection_var, value="no").grid(row=0, column=2, sticky="w")

        # Pictogram
        lf_pic = ttk.Labelframe(container, text="Hazard Pictogram", padding=12)
        lf_pic.pack(fill="x", **pad)

        ttk.Label(lf_pic, text="Is there a hazard pictogram on the box?").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(
            lf_pic, text="Yes", variable=self.has_pictogram_var, value="yes", command=self._toggle_pictogram_entry
        ).grid(row=0, column=1, sticky="w", padx=10)
        ttk.Radiobutton(
            lf_pic, text="No", variable=self.has_pictogram_var, value="no", command=self._toggle_pictogram_entry
        ).grid(row=0, column=2, sticky="w")

        ttk.Label(lf_pic, text="If YES, enter pictogram number:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.pict_entry = ttk.Entry(lf_pic, textvariable=self.pictogram_number_var, width=24)
        self.pict_entry.grid(row=1, column=1, sticky="w", pady=(10, 0), padx=10)

        show_list_btn = ttk.Button(lf_pic, text="Show Valid Numbers", command=self._show_valid_pictograms)
        show_list_btn.grid(row=1, column=2, sticky="w", pady=(10, 0))

        # Buttons
        btn_row = ttk.Frame(self)
        btn_row.pack(fill="x", **pad)

        ttk.Button(btn_row, text="Check Box", command=self._on_check).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Reset", command=self._on_reset).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Exit", command=self.destroy).pack(side="right", padx=6)

        # Output
        lf_out = ttk.Labelframe(self, text="Result", padding=12)
        lf_out.pack(fill="both", expand=True, padx=12, pady=12)

        self.output = tk.Text(lf_out, height=12, wrap="word")
        self.output.pack(fill="both", expand=True)

        self._write_output(
            "Ready.\n\n"
            "Instructions:\n"
            "1) Choose a packaging label.\n"
            "2) Select YES/NO for inspection sticker.\n"
            "3) Select YES/NO for pictogram presence.\n"
            "   - If YES, enter a valid pictogram number.\n"
            "4) Click 'Check Box'.\n"
        )

    def _toggle_pictogram_entry(self):
        if self.has_pictogram_var.get().strip().lower() == "yes":
            self.pict_entry.configure(state="normal")
            self.pict_entry.focus_set()
        else:
            self.pictogram_number_var.set("")
            self.pict_entry.configure(state="disabled")

    def _show_valid_pictograms(self):
        items = "\n".join([f"{k} - {v}" for k, v in self.system.pictogram_checker.PICTOGRAMS.items()])
        messagebox.showinfo("Valid Hazard Pictogram Numbers", items)

    def _write_output(self, text: str, clear: bool = True):
        self.output.configure(state="normal")
        if clear:
            self.output.delete("1.0", "end")
        self.output.insert("end", text)
        self.output.configure(state="disabled")

    def _on_reset(self):
        self.label_var.set("NONE")
        self.inspection_var.set("no")
        self.has_pictogram_var.set("no")
        self.pictogram_number_var.set("")
        self._toggle_pictogram_entry()
        self._write_output("Reset complete. Enter new box details and click 'Check Box'.\n")

    def _on_check(self):
        try:
            result = self.system.evaluate(
                label=self.label_var.get(),
                inspection_value=self.inspection_var.get(),
                has_pictogram=self.has_pictogram_var.get(),
                pictogram_number=self.pictogram_number_var.get(),
            )
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            self._write_output(
                f"{e}\n\n"
                "Repeat Instructions:\n"
                "- Label must be one of: IDG, ADG, ICE, NONE\n"
                "- Inspection sticker must be YES or NO\n"
                "- Pictogram presence must be YES or NO\n"
                "- If pictogram is YES, pictogram number must be one of:\n"
                f"  {', '.join(self.system.pictogram_checker.PICTOGRAMS.keys())}\n"
            )
            return

        box = result["box"]
        dg = result["dangerous_goods"]
        reasons = result["dg_reasons"]
        pict_disp = result["pictogram_display"]

        out_lines = []
        out_lines.append("Box Details:")
        out_lines.append(f"- Label: {box.label}")
        out_lines.append(f"- Inspection sticker: {'YES' if box.inspection else 'NO'}")
        out_lines.append(f"- Hazard pictogram: {pict_disp}")
        out_lines.append("")
        out_lines.append("Hazardous Pictograms Found: " + (", ".join(box.pictograms) if box.pictograms else "None"))
        out_lines.append("")
        if dg:
            out_lines.append("Result: This box IS Dangerous Goods.")
            out_lines.append("Reasons:")
            for r in reasons:
                out_lines.append(f"  - {r}")
        else:
            out_lines.append("Result: This box is NOT Dangerous Goods.")
            out_lines.append("Reasons: None")

        self._write_output("\n".join(out_lines))


def main():
    app = DangerousGoodsGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
