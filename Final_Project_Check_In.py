# Class 1
class Box:
    def __init__(self, label, inspection, pictograms):
        self.label = label
        self.inspection = inspection
        self.pictograms = pictograms


# Class 2
class LabelChecker:
    VALID_LABELS = ["IDG", "ADG", "ICE", "NONE"]

    def check_label(self, label):
        label = label.upper()
        if label in self.VALID_LABELS:
            return label
        return "NONE"


# Class 3
class PictogramChecker:
    HAZARD_PICTOGRAMS = ["DRY ICE", "FLAMMABLE", "TOXIC", "EXPLOSIVE"]

    def check_pictograms(self, pictogram_list):
        hazards_found = []
        for p in pictogram_list:
            if p.upper() in self.HAZARD_PICTOGRAMS:
                hazards_found.append(p.upper())
        return hazards_found


# Class 4: Main System
class DangerousGoodsSystem:
    def __init__(self):
        self.label_checker = LabelChecker()
        self.pictogram_checker = PictogramChecker()

    def evaluate_box(self, box):
        # Step 1: Check label
        label = self.label_checker.check_label(box.label)

        # Step 2: Check inspection sticker
        inspected = box.inspection.lower() == "yes"

        # Step 3: Check pictograms
        hazards = self.pictogram_checker.check_pictograms(box.pictograms)

        # Determine dangerous goods
        is_dg = label != "NONE" or inspected or len(hazards) > 0

        return {
            "label": label,
            "inspection": inspected,
            "hazard_pictograms": hazards,
            "dangerous_goods": is_dg
        }


# User input loop

def run_system():
    system = DangerousGoodsSystem()

    print("Dangerous Goods Classification System")

    label = input("Enter box label (IDG, ADG, ICE, NONE): ")
    inspection = input("Does it have an inspection sticker? (yes/no): ")

    pictograms = input("Enter pictograms separated by commas (DRY ICE, FLAMMABLE, TOXIC, EXPLOSIVE): ")
    pictogram_list = [p.strip() for p in pictograms.split(",")]

    box = Box(label, inspection, pictogram_list)
    result = system.evaluate_box(box)

    print("\nRESULT")
    print("Label:", result["label"])
    print("Inspection Sticker:", result["inspection"])
    print("Hazardous Pictograms Found:", result["hazard_pictograms"])
    
    if result["dangerous_goods"]:
        print("This box IS Dangerous Goods.")
    else:
        print("This box is NOT Dangerous Goods.")


run_system()
